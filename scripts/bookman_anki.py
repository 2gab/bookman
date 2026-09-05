#!/usr/bin/env python3
"""Sync Bookman cartões to Anki via AnkiConnect.

One-way (Bookman -> Anki), idempotent: re-running sync on unchanged cartões
never creates duplicate notes. Bookman stays the source of truth; Anki is
just a rendering of it. Card identity is the cartão's own file path relative
to books/ — no ID needs to be written into the cartão files themselves.

Requires Anki open with the AnkiConnect add-on installed and listening on
its default port (127.0.0.1:8765). No third-party Python packages needed.
"""

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

ANKI_URL = "http://127.0.0.1:8765"
SYNC_INDEX_NAME = ".bookman-anki-sync.json"


def anki_request(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(ANKI_URL, data=payload)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise ConnectionError(
            f"AnkiConnect inalcançável ({e}). Anki está aberto, com o add-on AnkiConnect instalado?"
        )
    if result.get("error") is not None:
        raise RuntimeError(f"AnkiConnect recusou '{action}': {result['error']}")
    return result["result"]


def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "sem-valor"


def parse_cartao(path: Path):
    text = path.read_text(encoding="utf-8")

    def field(name):
        m = re.search(rf"\*\*{name}:\*\*\s*(.+)", text)
        return m.group(1).strip() if m else None

    def section(name):
        m = re.search(rf"^## {name}\s*\n\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
        return m.group(1).strip() if m else None

    titulo_m = re.search(r"^# Cartão — (.+)$", text, re.M)
    return {
        "titulo": titulo_m.group(1).strip() if titulo_m else path.stem,
        "dominio": field("Domínio"),
        "origem": field("Origem"),
        "pergunta": section("Pergunta"),
        "resposta": section("Resposta"),
    }


def content_hash(card):
    h = hashlib.sha256()
    h.update((card["pergunta"] or "").encode("utf-8"))
    h.update(b"\x00")
    h.update((card["resposta"] or "").encode("utf-8"))
    return h.hexdigest()[:16]


def find_cartoes(books_dir: Path):
    return sorted(books_dir.glob("*/cartoes/*.md"))


def card_id(books_dir: Path, path: Path):
    return str(path.relative_to(books_dir))


def load_index(books_dir: Path):
    p = books_dir / SYNC_INDEX_NAME
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def save_index(books_dir: Path, index):
    p = books_dir / SYNC_INDEX_NAME
    p.write_text(json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def classify(books_dir, index, paths):
    novo, mudou, igual, invalidos = [], [], [], []
    dominio_counts = {}
    for path in paths:
        card = parse_cartao(path)
        if not card["pergunta"] or not card["resposta"]:
            invalidos.append(path)
            continue
        dom_label = card["dominio"] or "(sem domínio)"
        dominio_counts[dom_label] = dominio_counts.get(dom_label, 0) + 1
        cid = card_id(books_dir, path)
        h = content_hash(card)
        entry = index.get(cid)
        if entry is None:
            novo.append(path)
        elif entry.get("contentHash") != h:
            mudou.append(path)
        else:
            igual.append(path)
    return novo, mudou, igual, invalidos, dominio_counts


def cmd_status(args):
    books_dir = Path(args.books_dir)
    if not books_dir.is_dir():
        sys.exit(f"Diretório não encontrado: {books_dir}")
    index = load_index(books_dir)
    paths = find_cartoes(books_dir)
    novo, mudou, igual, invalidos, dominio_counts = classify(books_dir, index, paths)

    print(f"Bookman → Anki  ({books_dir})\n")
    print(f"  {len(paths)} cartões encontrados\n")
    print(f"  = {len(igual)} sincronizados")
    print(f"  + {len(novo)} não enviados")
    print(f"  ~ {len(mudou)} modificados")
    if invalidos:
        print(f"  ! {len(invalidos)} sem Pergunta/Resposta legível (pulados)")

    if dominio_counts:
        print("\n  Domínios")
        for dom, n in sorted(dominio_counts.items()):
            print(f"    {dom:<20} {n}")

    try:
        anki_request("version")
        print("\n  Anki: conectado")
    except Exception as e:
        print(f"\n  Anki: não alcançável ({e})")

    if novo:
        print("\n  Novos:")
        for p in novo:
            print(f"    + {card_id(books_dir, p)}")
    if mudou:
        print("\n  Modificados:")
        for p in mudou:
            print(f"    ~ {card_id(books_dir, p)}")
    if invalidos:
        print("\n  Sem Pergunta/Resposta:")
        for p in invalidos:
            print(f"    ! {card_id(books_dir, p)}")


def ensure_deck(deck_name):
    decks = anki_request("deckNames")
    if deck_name not in decks:
        anki_request("createDeck", deck=deck_name)


def cmd_sync(args):
    books_dir = Path(args.books_dir)
    if not books_dir.is_dir():
        sys.exit(f"Diretório não encontrado: {books_dir}")

    try:
        anki_request("version")
    except Exception as e:
        sys.exit(f"Anki não alcançável: {e}\nAbra o Anki com o add-on AnkiConnect antes de sincronizar.")

    index = load_index(books_dir)
    paths = find_cartoes(books_dir)

    created = updated = skipped = errors = 0
    for path in paths:
        card = parse_cartao(path)
        cid = card_id(books_dir, path)
        if not card["pergunta"] or not card["resposta"]:
            print(f"  ! pulado (sem Pergunta/Resposta): {cid}")
            errors += 1
            continue

        h = content_hash(card)
        entry = index.get(cid)
        if entry is not None and entry.get("contentHash") == h:
            skipped += 1
            continue

        dominio = card["dominio"] or "(sem domínio)"
        deck_name = f"Bookman::{dominio}"
        tags = ["bookman"]
        if card["dominio"]:
            tags.append(f"dominio:{slugify(card['dominio'])}")
        fields = {"Front": card["pergunta"], "Back": card["resposta"]}

        try:
            ensure_deck(deck_name)
        except RuntimeError as e:
            print(f"  ! erro criando deck '{deck_name}': {e}")
            errors += 1
            continue

        if entry is None:
            note = {"deckName": deck_name, "modelName": "Basic", "fields": fields, "tags": tags}
            try:
                note_id = anki_request("addNote", note=note)
            except RuntimeError as e:
                print(f"  ! erro criando '{cid}': {e}")
                errors += 1
                continue
            index[cid] = {"noteId": note_id, "deckName": deck_name, "contentHash": h}
            created += 1
            print(f"  + criado: {cid}")
        else:
            try:
                anki_request("updateNoteFields", note={"id": entry["noteId"], "fields": fields})
            except RuntimeError as e:
                print(f"  ! erro atualizando '{cid}': {e}")
                errors += 1
                continue
            entry["contentHash"] = h
            entry["deckName"] = deck_name
            updated += 1
            print(f"  ~ atualizado: {cid}")

    save_index(books_dir, index)
    summary = f"{created} criados, {updated} atualizados, {skipped} sem mudança"
    if errors:
        summary += f", {errors} com erro"
    print(f"\n✓ Sync concluído — {summary}")


def main():
    parser = argparse.ArgumentParser(
        prog="bookman-anki",
        description="Sincroniza cartões do Bookman com Anki via AnkiConnect (one-way, idempotente).",
    )
    parser.add_argument("--books-dir", default="./books", help="Diretório books/ (default: ./books)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Mostra o que está sincronizado, novo ou modificado.").set_defaults(func=cmd_status)
    sub.add_parser("sync", help="Envia cartões novos/modificados para o Anki.").set_defaults(func=cmd_sync)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
