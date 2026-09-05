<!-- Template only. `{{...}}` marks a placeholder to replace with a real value — never copy the double-braces syntax itself into the actual entidades.md. Unlike carta/revisao, an entity's record is mutated in place as its Status changes (proposto → validado/rejeitado), not appended to — one section per entity, not one section per event. -->

# Entidades — {{Título do livro}}

## Pessoas

### {{Nome da pessoa}}

- **Papel:** {{ex.: Autor, figura citada, personagem}}
- **{{campo livre, ex.: Ocupação, Datas}}:** {{valor, só o que o texto de fato afirma}}
- **Fonte:** {{Cap. N, p. X}}
- **Status:** {{proposto | validado | rejeitado}}
- **Validado em:** {{data — só quando Status: validado}}

## Obras

### {{Título da obra citada}}

- **Autor:** {{se o texto afirmar}}
- **Fonte:** {{Cap. N, p. X}}
- **Status:** {{proposto | validado | rejeitado}}
- **Validado em:** {{data — só quando Status: validado}}

## Instituições

### {{Nome da instituição}}

- **{{campo livre}}:** {{valor}}
- **Fonte:** {{Cap. N, p. X}}
- **Status:** {{proposto | validado | rejeitado}}
- **Validado em:** {{data — só quando Status: validado}}
