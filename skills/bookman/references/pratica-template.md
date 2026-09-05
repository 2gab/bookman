<!-- Template only. `{{...}}` marks a placeholder to replace with a real value — never copy the double-braces syntax itself into the actual pratica file. One file per chapter; a new "## {{referência}}" block is added for each new problem worked on in that chapter, never a new file. -->

# Prática — Capítulo {{n}}: {{título do capítulo}}

**Livro:** {{título do livro}}, {{autor}}

## {{referência exata do problema — ex. "§3, Exercício 22, pág. 14"}}

**Enunciado:**

> {{enunciado exato do problema, como aparece no livro — nunca reformulado ou simplificado}}

**Status:** {{em aberto | resolvido | solução mostrada}}

<!-- "solução mostrada" nunca equivale a "resolvido" — registra que o leitor viu a solução depois de tentativas, não que ele demonstrou saber resolver sozinho. Nenhuma leitura futura deste arquivo (revisão, mapa, ou qualquer feature) deve tratar as duas como a mesma coisa. -->

### Tentativas

<!-- Append-only — nunca sobrescreva uma tentativa anterior. Uma seção por tentativa, nunca uma tabela: uma prova ou cálculo de vários passos não cabe legível numa linha. -->

**{{data}} — Tentativa {{n}}**

**Resposta do leitor:**

{{a resposta ou tentativa de prova do leitor, na íntegra}}

**Veredito:** {{correto | parcialmente correto | incorreto | não verificável com certeza}}

**Feedback:**

{{o porquê do veredito, nunca só "certo"/"errado" sem explicação — se parcialmente correto, o que já funciona e onde exatamente quebra; se não verificável com certeza, diga isso explicitamente em vez de arriscar um veredito}}

<!-- Repita o bloco "## {{referência}}" inteiro para cada novo problema deste capítulo. -->
