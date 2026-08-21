# 🎨 Design System 04 — Tidimar (marca oficial da empresa)

Aplicado no Sistema de Produtividade Operacional em 2026-08-20, substituindo o
antigo [dark-orange-design-system.md](dark-orange-design-system.md). Verde-teal
profundo + verde-lima como acento único, painel inteiro numa moldura
arredondada flutuando sobre um fundo mais escuro, marca d'água da logo sutil
atrás do conteúdo, títulos serifados + UI em sans.

---

## Paleta

| Papel | Hex | Uso |
|---|---|---|
| Verde-lima (acento) | `#8FC63E` | Títulos de destaque, valores de KPI, links ativos, botão primário, bordas em hover |
| Verde-lima escuro | `#5E8C28` | Ponta escura dos gradientes (botão, item de menu ativo) |
| Verde-lima claro | `#B4E06B` | Ponta clara dos mesmos gradientes |
| Fundo (dentro da moldura) | `#071815` | Fundo da área de conteúdo (`.tab-content.active` neste projeto) |
| Fundo da página (fora da moldura) | `#040F0D` | Fundo do `body` — **deliberadamente mais escuro** que o de dentro, ver "A moldura arredondada" |
| Superfície (card) | `#0C231F` | Cards, tabelas, filtros, modais |
| Superfície elevada | `#123530` | Hover, cabeçalho de tabela |
| Borda | `#1F4842` | Contornos, divisores |
| Texto primário | `#EAF3F0` | Texto principal |
| Texto secundário | `#7FA69E` | Labels, legendas, eixos de gráfico, texto apagado |
| Sombra | `rgba(0, 0, 0, 0.6)` | Sombra neutra (cards, modal) |
| Sombra do acento | `rgba(143, 198, 62, 0.28)` | Sombra colorida em hover/foco (glow do verde-lima) |

Cores semânticas (sucesso/erro) **não fazem parte do acento** — mantidas como
já existiam no projeto (`#2ECC71` verde-sucesso, `#FF4D4D` vermelho-erro), só
com o contraste corrigido (ver "Armadilhas" abaixo).

## Tipografia

- **Títulos/logo:** Playfair Display, peso 700 — serifado, só em `h1` do
  cabeçalho e `h2` de cada card (título de seção).
- **UI/corpo:** Inter, pesos 400–700 — todo o resto.
- Google Fonts: `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600;700&display=swap">`

## A moldura arredondada (o app inteiro, não só os cards)

O `.container` (elemento raiz dentro do `<body>`) vira a "moldura": arredondada,
flutuando sobre um fundo de página mais escuro.

```css
body {
  padding: 14px;
  background: #040F0D;    /* fundo da PAGINA - mais escuro que o de dentro */
}
.container {
  max-width: 1500px;
  margin: 0 auto;          /* centraliza em telas muito largas */
  min-height: calc(100vh - 28px);
  border-radius: 18px;
  border: 1px solid #1F4842;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(0,0,0,.6);
  background: #0C231F;
  padding: var(--space-lg); /* respiro entre a moldura e o conteudo interno */
}
```

**Armadilhas reais já pegas, documentadas pra não repetir:**

1. **Sem contraste, o arredondado some.** Se o fundo da página e o fundo de
   dentro da moldura forem a mesma cor, a borda arredondada não tem contraste
   pra aparecer — por isso o fundo da página (`#040F0D`) é deliberadamente
   mais escuro que o de dentro (`#071815`).
2. **Variáveis com mesmo alias para "claro" e "escuro" apagam o texto.**
   Neste projeto, `--success-light`/`--success-dark` (e o par de `--error-*`)
   apontavam pro **mesmo** token — `.message.success` e `.badge.active`
   ficavam com texto exatamente da cor do próprio fundo, invisível. Ao trocar
   de design system, confira se background e texto de mensagens/badges não
   colapsam na mesma variável.
3. **`prefers-color-scheme: dark` órfão.** Havia um `@media (prefers-color-scheme: dark)`
   sobrescrevendo `--background`/`--primary` pra um azul de outro template,
   nunca removido. Como o app é sempre escuro (sem toggle), isso podia trocar
   cores dependendo do SO do usuário sem ninguém perceber. Removido.
4. **Gráficos Chart.js não herdam CSS.** Cores de eixo/legenda/quadriculado
   precisam ser setadas via `Chart.defaults` e nas `options` de cada gráfico -
   `Chart.defaults.scale.grid.display = false` tira o quadriculado de fundo
   de todos de uma vez.

## Marca d'água da logo (sem mostrar borda/quadrado do recorte)

A logo original (`logo tidimar.png`, raiz do projeto) não tem fundo
transparente — é um retângulo sólido teal com o ícone (círculo + cruz) à
esquerda e o nome por extenso à direita. Usar o recorte direto como
`background-image` a baixa opacidade mostraria o **quadrado sólido do
recorte**, não o desenho do ícone. A correção é em 3 passos, feita uma vez,
gerando PNGs novos (script usado: ver histórico do projeto / peça pra
recriar):

1. **Color-key:** remove o fundo sólido (amostra a cor num canto do recorte),
   deixando só o ícone com alpha real, com uma faixa de transição suave perto
   da borda do desenho.
2. **Degradê radial nos próprios pixels:** sem isso, a borda do ícone ainda
   aparece como um contorno duro quando usado em tamanho grande.
3. **Opacidade final:** multiplica o alpha final por um fator (~0.24 neste
   projeto — o valor "sutil" de referência do design system genérico, 0.10-0.11,
   ficou fraco demais pra aparecer atrás dos cards; ajustado depois de ver o
   resultado ao vivo).

Arquivos gerados: `frontend/img/logo-icone.png` (recorte opaco, pro selo
pequeno no cabeçalho) e `frontend/img/logo-marca-dagua.png` (transparente +
degradê + opacidade baixa, pro fundo).

Uso em CSS — **sem** pseudo-elemento, sem `mask-image`, sem `opacity` no
elemento, sem `z-index` (a opacidade e o degradê já estão nos pixels do
arquivo):

```css
.tab-content.active {
  background: #071815 url('img/logo-marca-dagua.png') no-repeat center center fixed;
  background-size: min(46vh, 440px) min(46vh, 440px);
  position: relative;
}
.tab-content.active > * { position: relative; z-index: 1; }
```

`background-attachment: fixed` ancora a marca d'água na janela (não no
conteúdo) — fica sempre no mesmo lugar visível, não importa quanto a página
role.

**Armadilha:** com a marca d'água centralizada, ela fica atrás dos cards que
estiverem no centro da tela — e como cards têm fundo **opaco**, ela some
completamente atrás deles. Neste projeto os cards de gráfico
(`.charts-grid .card`) foram deixados levemente translúcidos
(`background: rgba(12, 35, 31, 0.88)`) especificamente pra ela aparecer por
trás também nessa área, não só nos vãos entre os cards.

Pra um ícone pequeno e nítido ao lado do nome do app (não como marca d'água),
usa-se o recorte **original opaco** (`logo-icone.png`, sem o tratamento
acima) — um selo quadrado/arredondado com a cor de fundo da marca é padrão
normal de ícone de app, não precisa de transparência.

## Componentes

- **Cards:** `border-radius: 16px`, fundo `#0C231F`, borda `1px solid #1F4842`,
  sombra `0 2px 8px rgba(0,0,0,.6)`. Hover: `translateY(-3px)` + sombra do
  acento + borda vira a cor do acento.
- **Cards de KPI:** rótulo e valor **centralizados** (não à esquerda) — evita
  o número ficar desalinhado quando o rótulo é bem mais largo que o valor.
- **Botão primário:** gradiente `linear-gradient(90deg, #5E8C28, #8FC63E, #B4E06B)`,
  texto na cor do fundo (`#071815`, não branco — mais contraste sobre um
  gradiente claro).
- **Botão secundário (`.btn-secondary`):** outline `1px solid #1F4842`, fundo
  transparente, texto no texto-secundário — usado quando um botão não deve
  competir com a ação primária da tela (ex: "Cancelar Edição").
- **Tabelas:** todo `<table>` fica dentro de um wrapper (`.list-container`)
  com `border:1px solid #1F4842`, `border-radius:10px`, `box-shadow`,
  `max-height` + `overflow-y:auto`, cabeçalho `position:sticky` — aplicado em
  todas as tabelas da página de uma vez, via a classe já compartilhada.
- **Item de menu ativo (abas):** mesmo gradiente do botão primário, texto na
  cor do fundo, `font-weight:700`.
- **Gráficos (Chart.js):** série única por gráfico usa uma das 3 tonalidades
  do verde-lima (`#8FC63E` separação, `#5E8C28` conferência, `#B4E06B`
  resultado final); paleta categórica de 8-10 cores distintas (usada pra
  distinguir colaboradores numa lista/legenda) fica de fora do acento único,
  mantida colorida à parte. Datalabels com fundo `rgba(7,24,21,.85)` pra não
  se confundir com a grade; quadriculado de fundo desligado globalmente.

## Como aplicar num projeto novo

1. Troque as variáveis CSS de cor pelas da tabela acima — se o projeto já usa
   variáveis nomeadas parecidas, só troque o valor.
2. Gere o par de assets da logo (ícone opaco + marca d'água transparente)
   uma vez, salve como arquivos reais do projeto.
3. Aplique a moldura arredondada no container raiz do app, prestando atenção
   nas 4 armadilhas listadas acima.
4. Confira que toda tabela da página está dentro do mesmo wrapper com borda.
5. Se a marca d'água for centralizada atrás de cards opacos, deixe esses
   cards específicos levemente translúcidos, ou reposicione a marca d'água
   pra um vão sem cards por cima.
