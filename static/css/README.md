# Design System Quick Reference

## 🎨 Colors

| Variable | Value | Usage |
|----------|-------|-------|
| `--color-bg-primary` | #0d0d0d | Main background |
| `--color-text-primary` | #ffb3fd | Primary text |
| `--color-accent-primary` | #4d1849 | Buttons, accents |
| `--color-border-primary` | rgba(255, 179, 253, 0.3) | Borders |

## 📝 Typography

| Class | Size | Usage |
|-------|------|-------|
| `.text-xs` | 12px | Captions |
| `.text-sm` | 14px | Small text |
| `.text-base` | 15px | Body text |
| `.text-md` | 16px | Medium text |
| `.text-xl` | 18px | Large text |
| `.text-3xl` | 24px | Headings |
| `.text-5xl` | 36px | Display |

## 🔘 Buttons

```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-accent">Accent</button>

<!-- Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-lg">Large</button>
```

## 📦 Cards

```html
<div class="card">Basic card</div>
<div class="card card-hover">Hoverable</div>
<div class="card card-compact">Compact</div>
```

## 📏 Spacing

| Variable | Value |
|----------|-------|
| `--space-2` | 8px |
| `--space-3` | 12px |
| `--space-4` | 16px |
| `--space-5` | 20px |
| `--space-6` | 24px |

## 🎯 Common Patterns

### Flex Container
```html
<div class="flex items-center justify-between gap-4">
    <div>Left</div>
    <div>Right</div>
</div>
```

### Form Group
```html
<div class="form-group">
    <label class="form-label">Label</label>
    <input class="form-input" type="text">
</div>
```

### Status Alert
```html
<div class="alert alert-success show">Success message</div>
<div class="alert alert-error show">Error message</div>
```

## 📱 Responsive

- **Mobile**: < 480px
- **Tablet**: < 768px
- **Desktop**: > 768px

All interactive elements have 44px min-height on mobile for better touch targets.

## 🔗 Links

- Full Documentation: `/DESIGN_SYSTEM.md`
- CSS File: `/static/css/design-system.css`
