# Design System Documentation

## 1. TIPOGRAFIA

### Famílias de Fontes (Font Families)

#### Fonte Primária: General Sans
- **Fonte:** General Sans
- **Origem:** FontShare CDN
- **Fallbacks:** system-ui, -apple-system, sans-serif

**Pesos disponíveis:**
- 400 (Regular)
- 500 (Medium)
- 600 (SemiBold)
- 700 (Bold)

**Importação CSS:**
```css
@font-face {
  font-family: 'General Sans';
  src: url('//cdn.fontshare.com/...') format('woff2'),
       url('//cdn.fontshare.com/...') format('woff'),
       url('//cdn.fontshare.com/...') format('truetype');
  font-weight: 400;
  font-display: swap;
  font-style: normal;
}
```

---

### Escala Tipográfica

| Nível | Tamanho | Tamanho (px) | Line-Height | Font-Weight | Caso de Uso |
|-------|---------|--------------|-------------|-------------|-----------|
| **XS** (Caption) | 0.75rem | 12px | 1.5 | 400 | Captions, Help text, Badges |
| **SM** (Small) | 0.875rem | 14px | 1.5 | 400 | Small labels, Annotations |
| **Base** (Body) | 1rem | 16px | 1.6 | 400 | Texto corpo padrão |
| **LG** (Subheading) | 1.125rem | 18px | 1.5 | 500 | Subtítulos, Labels importantes |
| **XL** (Subheading Large) | 1.25rem | 20px | 1.5 | 600 | Subheadings, Card titles |
| **2XL** (Heading 3) | 1.5rem | 24px | 1.4 | 600 | H3 Headings |
| **3XL** (Heading 2) | 1.875rem | 30px | 1.3 | 700 | H2 Headings |
| **4XL** (Heading 1) | 2.25rem | 36px | 1.2 | 700 | H1 Headings, Hero titles |

#### Recomendações de Uso:
- **Headings:** font-weight 600-700, letter-spacing 0
- **Subheadings:** font-weight 500-600, letter-spacing -0.5px
- **Body text:** font-weight 400, line-height 1.6
- **Button text:** font-weight 600, tamanho ligeiramente reduzido em relação ao context

---

## 2. PALETA E REGRAS DE CORES

### 2.1 Cores Primárias (Blue)

| Token | Cor | HEX | RGB | HSL | Uso |
|-------|-----|-----|-----|-----|-----|
| **Primary-50** | ![#f0f9ff](https://via.placeholder.com/20/f0f9ff/f0f9ff) | `#f0f9ff` | `rgb(240, 249, 255)` | `hsl(204, 100%, 97%)` | Backgrounds claros, Hover states |
| **Primary-500** | ![#3b82f6](https://via.placeholder.com/20/3b82f6/3b82f6) | `#3b82f6` | `rgb(59, 130, 246)` | `hsl(217, 98%, 60%)` | **Cor principal - CTAs, Links** |
| **Primary-900** | ![#1e3a8a](https://via.placeholder.com/20/1e3a8a/1e3a8a) | `#1e3a8a` | `rgb(30, 58, 138)` | `hsl(217, 79%, 33%)` | Texto on primary backgrounds |

### 2.2 Cores Secundárias (Gray)

| Token | Cor | HEX | RGB | HSL | Uso |
|-------|-----|-----|-----|-----|-----|
| **Neutral-50** | ![#f9fafb](https://via.placeholder.com/20/f9fafb/f9fafb) | `#f9fafb` | `rgb(249, 250, 251)` | `hsl(210, 40%, 98%)` | Background secundário |
| **Neutral-500** | ![#6b7280](https://via.placeholder.com/20/6b7280/6b7280) | `#6b7280` | `rgb(107, 114, 128)` | `hsl(217, 13%, 47%)` | Texto secundário, Dividers |
| **Neutral-900** | ![#111827](https://via.placeholder.com/20/111827/111827) | `#111827` | `rgb(17, 24, 39)` | `hsl(217, 39%, 11%)` | Background escuro, Texto dark |

### 2.3 Cores de Estado

#### Sucesso (Green)
```css
--success-color: #10b981;  /* Green-500 */
--success-light: #d1fae5;   /* Green-100 */
--success-dark: #065f46;    /* Green-900 */
```

#### Erro (Red)
```css
--error-color: #ef4444;     /* Red-500 - rgba(239, 68, 68) */
--error-light: #fee2e2;     /* Red-100 */
--error-dark: #7f1d1d;      /* Red-900 */
```

#### Alerta/Warning (Amber)
```css
--warning-color: #f59e0b;   /* Amber-500 */
--warning-light: #fef3c7;   /* Amber-100 */
--warning-dark: #78350f;    /* Amber-900 */
```

#### Informação (Blue - mesmo da primária)
```css
--info-color: #3b82f6;      /* Blue-500 */
--info-light: #eff6ff;      /* Blue-50 */
--info-dark: #1e40af;       /* Blue-800 */
```

### 2.4 Cores de Superfícies

#### Tema Claro (Light Mode)
```css
:root {
  --background-color: #ffffff;
  --surface-color: #f9fafb;
  --text-color: #1f2937;
  --text-secondary: #6b7280;
  --border-color: #e5e7eb;
  --primary-color: #3b82f6;
  --secondary-color: #6b7280;
}
```

#### Tema Escuro (Dark Mode)
```css
@media (prefers-color-scheme: dark) {
  :root {
    --background-color: #111827;
    --surface-color: #1f2937;
    --text-color: #f9fafb;
    --text-secondary: #9ca3af;
    --border-color: #374151;
    --primary-color: #3b82f6;
    --secondary-color: #9ca3af;
  }
}
```

### 2.5 Regras de Contraste WCAG AA

**Mínimos obrigatórios:**
- Texto normal (< 18px): **4.5:1**
- Texto grande (≥ 18px): **3:1**
- Componentes UI: **3:1**

**Combinações Aprovadas:**
- ✅ `#3b82f6` (Primary) sobre `#ffffff` (White): **4.6:1**
- ✅ `#1f2937` (Dark text) sobre `#ffffff` (White): **12.6:1**
- ✅ `#6b7280` (Gray) sobre `#ffffff` (White): **6.8:1**
- ✅ `#ffffff` sobre `#111827` (Dark bg): **14.1:1**
- ✅ `#3b82f6` sobre `#111827` (Dark bg): **5.2:1**

---

## 3. ESPAÇAMENTOS E GRID

### 3.1 Sistema de Espaçamento Base

**Base Unit: 4px** (Tailwind-based)

| Scale | Valor (px) | Valor (rem) | Uso |
|-------|-----------|------------|-----|
| **xs** | 4px | 0.25rem | Gaps pequenos entre elementos |
| **sm** | 8px | 0.5rem | Padding/margin em elementos pequenos |
| **md** | 12px | 0.75rem | Espaçamento padrão |
| **lg** | 16px | 1rem | Padding padrão em cards/inputs |
| **xl** | 24px | 1.5rem | Margin entre seções |
| **2xl** | 32px | 2rem | Margin vertical em seções |
| **3xl** | 48px | 3rem | Espaçamento grande entre blocos |
| **4xl** | 64px | 4rem | Section spacing |

### 3.2 Paddings Padrão

#### Buttons
```css
.btn-sm { padding: 0.5rem 1rem; }      /* 8px 16px */
.btn-md { padding: 0.75rem 1.5rem; }   /* 12px 24px */
.btn-lg { padding: 1rem 2rem; }        /* 16px 32px */
```

#### Cards
```css
.card-sm { padding: 1rem; }            /* 16px */
.card-md { padding: 1.5rem; }          /* 24px */
.card-lg { padding: 2rem; }            /* 32px */
```

#### Inputs/Form Fields
```css
.input { padding: 0.75rem 1rem; }      /* 12px 16px */
.input-lg { padding: 1rem 1.25rem; }   /* 16px 20px */
```

#### Containers
```css
.container-sm { padding: 1.5rem; }     /* 24px */
.container-md { padding: 2rem; }       /* 32px */
.container-lg { padding: 3rem; }       /* 48px */
```

### 3.3 Border Radius

| Token | Valor | Uso |
|-------|-------|-----|
| **rounded-sm** | 2px | Subtle borders, inputs |
| **rounded-md** | 4px | Buttons, small cards |
| **rounded-lg** | 8px | **Default - Cards, containers** |
| **rounded-xl** | 12px | Larger interactive elements |
| **rounded-2xl** | 16px | Prominent cards, modals |
| **rounded-full** | 50% | Circular elements, avatars, badges |

### 3.4 Box Shadows

```css
/* Subtle shadows */
--shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);

/* Medium shadows (Default) */
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 8px 25px rgba(0, 0, 0, 0.15);

/* Elevated shadows */
--shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.1);
--shadow-2xl: 0 25px 50px rgba(0, 0, 0, 0.15);

/* Inset shadows (para depressed effects) */
--shadow-inset: inset 0 2px 4px rgba(0, 0, 0, 0.06);
```

---

## 4. ANIMAÇÕES E TRANSIÇÕES

### 4.1 Curvas de Transição (Easing)

```css
/* Ease Families */
--ease-linear: cubic-bezier(0, 0, 1, 1);
--ease-in: cubic-bezier(0.42, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.58, 1);
--ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);

/* Custom eases */
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
--ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
```

### 4.2 Durations Padrão

| Duration | Valor | Uso |
|----------|-------|-----|
| **fast** | 150ms | Micro-interactions |
| **base** | 300ms | **Default - Hovers, state changes** |
| **slow** | 600ms | Page transitions, large animations |
| **slower** | 1000ms+ | Entrance animations, complex sequences |

### 4.3 Estados Interativos

#### Hover State
```css
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}
```

#### Active State
```css
.btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.1s ease;
}
```

#### Focus State (Keyboard Navigation)
```css
.btn:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1), 
              0 0 0 6px #3b82f6;
  transition: box-shadow 0.3s ease;
}
```

#### Disabled State
```css
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #e5e7eb;
  color: #9ca3af;
}
```

### 4.4 Animações Base

#### Loading Spinner
```css
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.spinner {
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #3b82f6;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}
```

#### Fade In/Out
```css
@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

@keyframes fadeOut {
  0% { opacity: 1; }
  100% { opacity: 0; }
}

.fade-in { animation: fadeIn 0.3s ease; }
.fade-out { animation: fadeOut 0.3s ease; }
```

#### Slide Up
```css
@keyframes slideUp {
  0% { transform: translateY(20px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

.slide-up { animation: slideUp 0.6s ease; }
```

#### Bounce
```css
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.bounce { animation: bounce 0.6s ease; }
```

#### Pulse (para skeletons/loading)
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.pulse { animation: pulse 2s ease-in-out infinite; }
```

### 4.5 Transitions Recomendadas

```css
/* Micro transitions */
transition: color 0.15s ease;
transition: background-color 0.15s ease;

/* Standard transitions */
transition: all 0.3s ease;
transition: transform 0.3s ease, box-shadow 0.3s ease;

/* Slow transitions */
transition: all 0.6s ease;

/* No motion (accessibility) */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 5. COMPONENTES BASE

### 5.1 Botões (Button Variants)

#### Button Primary (CTA)
```html
<button class="btn btn-primary">
  Click Me
</button>
```

```css
.btn-primary {
  background-color: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-primary:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-primary:focus {
  outline: none;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1), 
              0 0 0 6px #3b82f6;
}

.btn-primary:disabled {
  background-color: #d1d5db;
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
}
```

#### Button Secondary
```css
.btn-secondary {
  background-color: #f3f4f6;
  color: #1f2937;
  padding: 0.75rem 1.5rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background-color: #e5e7eb;
  border-color: #9ca3af;
}

.btn-secondary:dark {
  background-color: #374151;
  color: #f9fafb;
  border-color: #4b5563;
}
```

#### Button Outlined
```css
.btn-outlined {
  background-color: transparent;
  color: #3b82f6;
  padding: 0.75rem 1.5rem;
  border: 2px solid #3b82f6;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outlined:hover {
  background-color: rgba(59, 130, 246, 0.1);
}
```

#### Button Ghost
```css
.btn-ghost {
  background-color: transparent;
  color: #3b82f6;
  padding: 0.75rem 1.5rem;
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-ghost:hover {
  color: #2563eb;
  text-decoration: underline;
}
```

### 5.2 Input / Form Fields

#### Text Input
```html
<input 
  type="text" 
  class="input" 
  placeholder="Enter text..."
  aria-label="Input field"
/>
```

```css
.input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  background-color: white;
  color: #1f2937;
  transition: all 0.3s ease;
}

.input:hover {
  border-color: #9ca3af;
}

.input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input::placeholder {
  color: #9ca3af;
}

.input:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
  color: #9ca3af;
}

/* Error state */
.input.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

/* Success state */
.input.success {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
```

#### Form Group (com Label)
```html
<div class="form-group">
  <label for="email" class="label">Email Address</label>
  <input 
    type="email" 
    id="email" 
    class="input" 
    placeholder="you@example.com"
  />
  <span class="helper-text">We'll never share your email.</span>
</div>
```

```css
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.helper-text {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.error-text {
  font-size: 0.75rem;
  color: #ef4444;
  margin-top: 0.25rem;
}
```

### 5.3 Cards

#### Card Base
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Card Title</h3>
  </div>
  <div class="card-content">
    <p>Card content goes here...</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">Action</button>
  </div>
</div>
```

```css
.card {
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
  border-color: #d1d5db;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.card-content {
  padding: 1.5rem;
  color: #6b7280;
  line-height: 1.6;
}

.card-footer {
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 0.75rem;
}

/* Dark mode */
.dark .card {
  background-color: #1f2937;
  border-color: #374151;
  color: #f9fafb;
}

.dark .card-header {
  border-bottom-color: #374151;
}

.dark .card-title {
  color: #f9fafb;
}

.dark .card-footer {
  background-color: #111827;
  border-top-color: #374151;
}
```

### 5.4 Modal/Dialog

```html
<div class="modal-overlay" id="modal">
  <div class="modal">
    <div class="modal-header">
      <h2 class="modal-title">Modal Title</h2>
      <button class="modal-close" aria-label="Close">×</button>
    </div>
    <div class="modal-content">
      <p>Modal content here...</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-primary">Confirm</button>
    </div>
  </div>
</div>
```

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  animation: fadeIn 0.3s ease forwards;
}

.modal {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.6s ease;
}

.modal-header {
  padding: 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #6b7280;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: #1f2937;
}

.modal-content {
  padding: 2rem;
  color: #6b7280;
  line-height: 1.6;
}

.modal-footer {
  padding: 1rem 2rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
```

### 5.5 Alert / Toast

```html
<div class="alert alert-success" role="alert">
  <span class="alert-icon">✓</span>
  <span class="alert-message">Operation completed successfully!</span>
  <button class="alert-close" aria-label="Close alert">×</button>
</div>
```

```css
.alert {
  padding: 1rem 1.5rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  animation: slideUp 0.3s ease;
}

/* Success */
.alert-success {
  background-color: #d1fae5;
  border: 1px solid #10b981;
  color: #065f46;
}

/* Error */
.alert-error {
  background-color: #fee2e2;
  border: 1px solid #ef4444;
  color: #7f1d1d;
}

/* Warning */
.alert-warning {
  background-color: #fef3c7;
  border: 1px solid #f59e0b;
  color: #78350f;
}

/* Info */
.alert-info {
  background-color: #eff6ff;
  border: 1px solid #3b82f6;
  color: #1e40af;
}

.alert-icon {
  font-weight: 700;
  flex-shrink: 0;
}

.alert-message {
  flex-grow: 1;
  font-size: 0.95rem;
}

.alert-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: currentColor;
  opacity: 0.7;
  transition: opacity 0.3s ease;
  flex-shrink: 0;
}

.alert-close:hover {
  opacity: 1;
}
```

---

## 6. RESPONSIVIDADE

### 6.1 Breakpoints

```css
/* Mobile First Approach */
/* Default: Mobile (< 640px) */

@media (min-width: 640px) {
  /* Tablet: 640px to 1024px */
}

@media (min-width: 768px) {
  /* Large Tablet: 768px to 1024px */
}

@media (min-width: 1024px) {
  /* Desktop: >= 1024px */
}

@media (min-width: 1280px) {
  /* Large Desktop: >= 1280px */
}
```

### 6.2 Escala Responsiva

| Elemento | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| **H1** | 24px | 30px | 36px |
| **H2** | 20px | 24px | 30px |
| **Body** | 14px | 16px | 16px |
| **Padding** | 1rem | 1.5rem | 2rem |
| **Gap** | 12px | 16px | 24px |

---

## 7. ACESSIBILIDADE

### 7.1 Padrões WCAG AA

**Checklist:**
- ✅ Contrast ratio mínimo: **4.5:1** para texto normal
- ✅ Contrast ratio: **3:1** para texto grande (≥18px)
- ✅ Focus indicators visíveis para navegação por teclado
- ✅ Labels associados a inputs via `for` attribute
- ✅ ARIA attributes quando necessário
- ✅ Estrutura de heading hierárquica (H1 → H2 → H3)
- ✅ Alt text para imagens
- ✅ Suporte a `prefers-reduced-motion`

### 7.2 Exemplo de Focus State Acessível

```css
.interactive:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 7.3 Semantic HTML

```html
<!-- ✓ Bom -->
<button type="button" aria-label="Close menu">×</button>
<label for="email">Email</label>
<input id="email" type="email" />

<!-- ✗ Evitar -->
<div onclick="...">Click me</div>
<div>Email</div>
<div contenteditable></div>
```

---

## 8. VARIÁVEIS CSS (CSS Custom Properties)

```css
:root {
  /* Colors */
  --primary-50: #f0f9ff;
  --primary-500: #3b82f6;
  --primary-900: #1e3a8a;
  
  --neutral-50: #f9fafb;
  --neutral-500: #6b7280;
  --neutral-900: #111827;
  
  --success: #10b981;
  --error: #ef4444;
  --warning: #f59e0b;
  --info: #3b82f6;
  
  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  
  /* Typography */
  --font-family: 'General Sans', system-ui, sans-serif;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  /* Borders & Shadows */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 50%;
  
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 8px 25px rgba(0, 0, 0, 0.15);
  --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.1);
  
  /* Transitions */
  --duration-fast: 150ms;
  --duration-base: 300ms;
  --duration-slow: 600ms;
  --ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);
}
```

---

## 9. USAGE EXAMPLES

### Exemplo 1: Card com Botão
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Welcome</h3>
  </div>
  <div class="card-content">
    <p>This is a sample card component.</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">Get Started</button>
  </div>
</div>
```

### Exemplo 2: Form com Validação
```html
<div class="form-group">
  <label for="name">Full Name</label>
  <input 
    type="text" 
    id="name" 
    class="input" 
    required
  />
</div>

<div class="form-group">
  <label for="email">Email</label>
  <input 
    type="email" 
    id="email" 
    class="input error" 
  />
  <span class="error-text">Please enter a valid email</span>
</div>

<button class="btn btn-primary">Submit</button>
```

### Exemplo 3: Componente Responsivo
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="card">
    <div class="card-content">
      <h4 class="font-semibold text-lg mb-2">Feature 1</h4>
      <p class="text-gray-600">Description here</p>
    </div>
  </div>
  <!-- Repetir para mais cards -->
</div>
```

---

## 10. TOKENS SUMMARY

| Categoria | Token | Valor |
|-----------|-------|-------|
| **Primária** | Primary | #3b82f6 |
| **Fundo** | Background | #ffffff / #111827 |
| **Texto** | Text | #1f2937 / #f9fafb |
| **Espaço** | Base Unit | 4px |
| **Tipo** | Font Family | General Sans |
| **Raio** | Default | 8px |
| **Sombra** | Medium | 0 4px 6px rgba(0,0,0,0.1) |
| **Transição** | Default | 300ms ease |

---

## 11. IMPLEMENTATION CHECKLIST

- [ ] Importar fonte General Sans via CDN
- [ ] Definir variáveis CSS no `:root`
- [ ] Implementar componentes base (Button, Input, Card)
- [ ] Testar contraste de cores (WCAG AA)
- [ ] Validar focus states em todos os interativos
- [ ] Testar responsividade em breakpoints
- [ ] Implementar dark mode (`prefers-color-scheme`)
- [ ] Adicionar suporte a `prefers-reduced-motion`
- [ ] Documentar customizações específicas do projeto

---

**Versão:** 1.0  
**Última atualização:** 2026-07-21  
**Status:** Produção Pronto
