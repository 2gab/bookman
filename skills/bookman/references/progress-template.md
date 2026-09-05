<!-- Template only. `{{...}}` marks a placeholder to replace with a real value — never copy the double-braces syntax itself into the actual progress.md. For a value that genuinely isn't known yet, write a plain marker like "(a classificar)" or "(a definir)" instead.

Three sections below hold data of genuinely different kinds — keep them separate rather than one flat header:
- Identidade: facts about the book itself (bibliographic, or "which copy the reader is using"). Set once, rarely revisited.
- Tese principal: a cache, not authored content — see below and SKILL.md's "State" section. Never hand-edit it.
- Estado da sessão atual: facts about the reader's ongoing engagement with it. Changes constantly.
Don't invent a fourth bucket for something that fits one of these three, or Metadados/Path — see SKILL.md's "Persist only what can't be reconstructed" principle. -->

# {{Título do livro}}

## Identidade

- **Autor:** {{nome}}
- **Tipo de livro:** (a classificar na passada inspecional — prático, teórico-história, teórico-ciência, teórico-filosofia, teórico-ciência-social, ou ficção; ver Regra 1, `how_to_read_books` Cap. 6)
- **Edição:** {{ex.: "Fifth Internet Edition", "Electronic Classics Series (ed. Jim Manis)" — o que a fonte concreta afirma sobre si, não inventado}}
- **Tradutor:** {{nome, se houver e o texto afirmar}}
- **Editora:** {{nome, se conhecida}}
- **Ano:** {{ano de publicação; se o texto só afirma o ano de uma tradução/edição específica, diga qual}}
- **Idioma:** {{idioma em que o leitor está lendo}}
- **ISBN:** {{se conhecido}}
- **Arquivo-fonte:** {{caminho do arquivo, ex. "Capital-Volume-I.pdf" na pasta de trabalho}} — qual exemplar/material o leitor está usando; salvo para não perguntar de novo em sessões futuras. Não é identidade bibliográfica estrita, mas fica aqui por ser um fato sobre o objeto, não sobre a sessão de leitura.

## Tese principal

<!-- Cache derivado das cartas — nunca editado à mão. Recalculado e sobrescrito por inteiro (nunca acrescentado) sempre que uma carta é rascunhada/aprovada, e sempre que "/bookman metadados" roda. Sourced só de Tema gerador + Trecho-chave das cartas existentes; uma carta rascunhada já basta, não precisa ser aprovada. -->

{{síntese do Bookman a partir das cartas existentes, ou "(ainda não há cartas registradas pra sintetizar uma tese)" se zero cartas existirem}}

## Passada inspecional (antes do Cap. 1)

- Do que trata o livro como um todo:
- Estrutura / partes principais:
- Palavras-chave / vocabulário técnico que já aparece no sumário ou prefácio:

## Progresso por capítulo

| Cap. | Título | Status | Carta |
|---|---|---|---|
| 1 | {{título do capítulo}} | {{não iniciado \| em diálogo \| carta rascunhada \| carta aprovada}} | {{link pro arquivo da carta, se existir}} |

## Estado da sessão atual

- Iniciado em: {{data}}
- Capítulo em andamento:
- Etapa do fluxo (`freire`, "The chapter session flow"): {{1 reading-of-the-world \| 2 provocação \| 3 problematização \| 4 co-escrita da carta \| 5 pergunta aberta}}
- Notas soltas da conversa em curso (o que já surgiu, ainda não formalizado na carta):

## Sessões

<!-- Append-only — nunca sobrescreva uma linha existente. Uma linha por evento relevante (não por mensagem), então esta tabela registra eventos, não reproduz a conversa. "Última sessão" se lê pela última linha, não é campo separado. -->

| Data | Evento | Observação |
|---|---|---|
| {{data}} | {{ex.: passada inspecional \| leitura Cap. N \| carta N criada \| carta N aprovada \| revisão}} | {{uma frase}} |
