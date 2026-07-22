# 🎨 Design System: Dark Orange Analytics Dashboard

Um design system focado em interfaces analíticas em modo escuro com destaque vibrante em **Laranja / Amber**, ideal para dashboards executivos, de vendas ou gerenciamento financeiro/restaurante.

---

## 🖤 Paleta de Cores (Color Tokens)

### 1. Cores de Superfície & Fundo (Backgrounds & Surface)
Construção visual baseada em tons de marrom/cinza ultra escuros com alto contraste para leitura de dados.

| Token | Código HEX | Aplicação / Uso |
| :--- | :--- | :--- |
| `--bg-main` | `#121010` | Fundo principal da página/dashboard |
| `--bg-card` | `#1E1B1A` | Cards de informação, contêineres de gráficos e tabelas |
| `--bg-card-hover` | `#282422` | Estado hover de cards e componentes interativos |
| `--bg-input` | `#171514` | Campos de busca, filtros e select inputs |
| `--border-subtle` | `#2D2826` | Linhas divisórias, bordas de cards e separadores |

---

### 2. Cor Primária & Marca (Primary Brand Accent)
Laranja vibrante utilizado para elementos de destaque, botões primários, gráficos e indicadores ativos.

| Token | Código HEX | Exemplo na imagem |
| :--- | :--- | :--- |
| `--primary` | `#FF6B00` | Barras principais, gráficos de rosca (*Daily Target*), botões e ícones |
| `--primary-hover` | `#E05E00` | Estado hover de botões e seletores primários |
| `--primary-muted` | `#331B0A` | Fundo suave de botões secundários, badges e seletores (*Monthly*) |
| `--primary-border` | `#803800` | Bordas de botões em estilo outline (*More Details*) |

---

### 3. Cores de Status e Acentos Analíticos (Data Accents)
Utilizadas para barras secundárias em gráficos comparativos, métricas de crescimento e quedas.

| Categoria | Token | Código HEX | Uso Sugerido |
| :--- | :--- | :--- | :--- |
| **Growth / Success** | `--color-success` | `#2ECC71` | Indicadores de crescimento positivo (`+2,7%`) |
| **Danger / Loss** | `--color-danger` | `#FF4D4D` | Indicadores de queda ou alerta (`-0,5%`) |
| **Chart Bar 2 (Gray)**| `--chart-gray` | `#605E5C` | Métrica secundária nos gráficos de barras (*Expense*) |
| **Chart Bar 3 (Light)**| `--chart-light` | `#D9D9D9` | Métrica terciária nos gráficos de barras (*Others*) |

---

### 4. Tipografia & Neutros (Typography)

| Token | Código HEX | Uso |
| :--- | :--- | :--- |
| `--text-primary` | `#FFFFFF` | Títulos principais, grandes valores numéricos e números nos cards |
| `--text-secondary` | `#9E9A97` | Rótulos de campos, subtítulos, nomes de métricas |
| `--text-muted` | `#635E5B` | Legendas secundárias, eixos dos gráficos (Jan-Dec) e textos informativos |

---

## 📊 Regras de Aplicação nos Gráficos (Chart Styling)

### 1. Gráfico de Rosca / Progresso (Donut Chart)
* **Valor Atual / Progresso (70%):** `--primary` (`#FF6B00`)
* **Trilha Restante:** `--bg-card-hover` (`#282422`) ou tom escuro sutil.

### 2. Gráfico de Barras Comparativo (Multi-Bar Chart)
* **Série 1 (Income/Receita):** `--primary` (`#FF6B00`)
* **Série 2 (Expense/Despesas):** `--chart-gray` (`#605E5C`)
* **Série 3 (Outros):** `--chart-light` (`#D9D9D9`)

### 3. Sparklines / Minigráficos de Tendência
* **Linha do Gráfico:** `--primary` (`#FF6B00`)
* **Gradiente de Fundo:** Linear Gradient de `rgba(255, 107, 0, 0.25)` até `transparent`.

---

## 🛠 Exemplo de Implementação em CSS (Variables)

```css
:root {
  /* Surfaces */
  --bg-main: #121010;
  --bg-card: #1e1b1a;
  --bg-card-hover: #282422;
  --bg-input: #171514;
  --border-subtle: #2d2826;

  /* Primary Accent */
  --primary: #ff6b00;
  --primary-hover: #e05e00;
  --primary-muted: #331b0a;
  --primary-border: #803800;

  /* Data Accents */
  --color-success: #2ecc71;
  --color-danger: #ff4d4d;
  --chart-gray: #605e5c;
  --chart-light: #d9d9d9;

  /* Typography */
  --text-primary: #ffffff;
  --text-secondary: #9e9a97;
  --text-muted: #635e5b;
}

body {
  background-color: var(--bg-main);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.dashboard-card {
  background-color: var(--bg-card);
  border-radius: 12px;
  border: 1px solid var(--border-subtle);
  padding: 20px;
}

.button-outline {
  background-color: transparent;
  border: 1px solid var(--primary-border);
  color: var(--primary);
  border-radius: 6px;
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.button-outline:hover {
  background-color: var(--primary-muted);
  border-color: var(--primary);
}
```
