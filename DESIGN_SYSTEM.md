# Community Control AI - Design System Documentation

## Overview

This design system provides a comprehensive, scalable, and reusable set of CSS variables, components, and utilities based on the visual identity of the Community Control AI platform. All pages use this consistent design language for a cohesive user experience.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Design Tokens](#design-tokens)
3. [Typography](#typography)
4. [Components](#components)
5. [Utility Classes](#utility-classes)
6. [Responsive Design](#responsive-design)
7. [Examples](#examples)

---

## Getting Started

### Integration

Include the design system CSS in your HTML:

```html
<link rel="stylesheet" href="/static/css/design-system.css">
```

### Font Dependencies

The design system requires these Google Fonts:

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Fustat:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## Design Tokens

### Color Palette

#### Primary Colors
```css
--color-bg-primary: #0d0d0d         /* Dark background */
--color-bg-secondary: #1e1e1e       /* Secondary dark */
--color-bg-tertiary: #2a0d29        /* Tertiary purple-dark */
```

#### Text Colors
```css
--color-text-primary: #ffb3fd       /* Primary pink */
--color-text-secondary: #ffbffd     /* Secondary pink */
--color-text-tertiary: #e8d4f0      /* Tertiary light purple */
--color-text-muted: rgba(232, 212, 240, 0.6)
--color-text-white: #ffffff
```

#### Accent Colors
```css
--color-accent-primary: #4d1849     /* Primary accent */
--color-accent-hover: #5d1e59       /* Hover state */
--color-accent-light: #e8a4d8       /* Light accent */
--color-accent-lighter: #f0b4e0     /* Lighter accent */
```

#### Border Colors
```css
--color-border-primary: rgba(255, 179, 253, 0.3)
--color-border-hover: rgba(255, 179, 253, 0.5)
--color-border-light: rgba(255, 255, 255, 0.15)
```

### Typography

#### Font Families
```css
--font-primary: 'Fustat', sans-serif      /* Body text */
--font-display: 'Instrument Serif', serif  /* Headings */
--font-mono: 'Roboto Mono', monospace     /* Code */
```

#### Font Sizes
```css
--text-xs: 0.75rem      /* 12px */
--text-sm: 0.875rem     /* 14px */
--text-base: 0.9375rem  /* 15px */
--text-md: 1rem         /* 16px */
--text-lg: 1.0625rem    /* 17px */
--text-xl: 1.125rem     /* 18px */
--text-2xl: 1.375rem    /* 22px */
--text-3xl: 1.5rem      /* 24px */
--text-4xl: 2rem        /* 32px */
--text-5xl: 2.25rem     /* 36px */
```

#### Font Weights
```css
--font-normal: 400
--font-medium: 500
--font-semibold: 600
--font-bold: 700
```

### Spacing Scale
```css
--space-1: 0.25rem   /* 4px */
--space-2: 0.5rem    /* 8px */
--space-3: 0.75rem   /* 12px */
--space-4: 1rem      /* 16px */
--space-5: 1.25rem   /* 20px */
--space-6: 1.5rem    /* 24px */
--space-8: 2rem      /* 32px */
--space-10: 2.5rem   /* 40px */
--space-12: 3rem     /* 48px */
--space-16: 4rem     /* 64px */
```

### Border Radius
```css
--radius-sm: 0.5rem    /* 8px */
--radius-md: 0.75rem   /* 12px */
--radius-lg: 0.875rem  /* 14px */
--radius-xl: 1rem      /* 16px */
--radius-2xl: 1.25rem  /* 20px */
--radius-3xl: 1.5rem   /* 24px */
--radius-full: 9999px
```

---

## Typography

### Headings

```html
<!-- Display Heading (36px) -->
<h1 class="heading-display">Display Heading</h1>

<!-- H1 (32px) -->
<h1 class="heading-1">Main Heading</h1>

<!-- H2 (24px) -->
<h2 class="heading-2">Section Heading</h2>

<!-- H3 (18px) -->
<h3 class="heading-3">Subsection Heading</h3>
```

### Text Utilities

```html
<!-- Font Families -->
<p class="font-primary">Body text</p>
<p class="font-display">Display text</p>
<code class="font-mono">Monospace code</code>

<!-- Font Sizes -->
<p class="text-sm">Small text</p>
<p class="text-base">Base text</p>
<p class="text-lg">Large text</p>

<!-- Font Weights -->
<p class="font-normal">Normal weight</p>
<p class="font-medium">Medium weight</p>
<p class="font-semibold">Semibold weight</p>

<!-- Text Colors -->
<p class="text-primary">Primary color</p>
<p class="text-secondary">Secondary color</p>
<p class="text-white">White text</p>
```

---

## Components

### Buttons

#### Primary Button
```html
<button class="btn btn-primary">Primary Button</button>
```

#### Secondary Button
```html
<button class="btn btn-secondary">Secondary Button</button>
```

#### Accent Button
```html
<button class="btn btn-accent">Accent Button</button>
```

#### Button Sizes
```html
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-md">Medium</button>
<button class="btn btn-primary btn-lg">Large</button>
```

#### Icon Button
```html
<button class="btn btn-primary btn-icon">
    <svg>...</svg>
</button>
```

### Cards

#### Basic Card
```html
<div class="card">
    <h3>Card Title</h3>
    <p>Card content goes here.</p>
</div>
```

#### Hoverable Card
```html
<div class="card card-hover">
    <h3>Interactive Card</h3>
    <p>This card has hover effects.</p>
</div>
```

#### Card Sizes
```html
<!-- Compact -->
<div class="card card-compact">Compact card</div>

<!-- Spacious -->
<div class="card card-spacious">Spacious card</div>
```

### Forms

#### Form Group
```html
<div class="form-group">
    <label class="form-label">Name</label>
    <input type="text" class="form-input" placeholder="Enter your name">
</div>
```

#### Select Dropdown
```html
<div class="form-group">
    <label class="form-label">Options</label>
    <select class="form-select">
        <option>Option 1</option>
        <option>Option 2</option>
    </select>
</div>
```

#### Textarea
```html
<div class="form-group">
    <label class="form-label">Message</label>
    <textarea class="form-textarea" rows="4"></textarea>
</div>
```

### Modals

```html
<div class="modal-overlay active">
    <div class="modal-content">
        <div class="modal-header">
            <h2 class="modal-title">Modal Title</h2>
            <button class="modal-close">×</button>
        </div>
        <div class="modal-body">
            <p>Modal content goes here.</p>
        </div>
    </div>
</div>
```

### Status Messages

```html
<!-- Success Alert -->
<div class="alert alert-success show">
    Operation completed successfully!
</div>

<!-- Error Alert -->
<div class="alert alert-error show">
    An error occurred. Please try again.
</div>
```

### Loading Spinner

```html
<!-- Default Spinner -->
<div class="spinner"></div>

<!-- Large Spinner -->
<div class="spinner spinner-lg"></div>
```

---

## Utility Classes

### Spacing

```html
<!-- Margin -->
<div class="mt-4">Margin top</div>
<div class="mb-6">Margin bottom</div>

<!-- Padding -->
<div class="p-4">Padding all sides</div>
```

### Flexbox

```html
<div class="flex items-center justify-between gap-4">
    <div>Item 1</div>
    <div>Item 2</div>
</div>
```

### Display

```html
<div class="flex">Flex container</div>
<div class="grid">Grid container</div>
<div class="hidden">Hidden element</div>
```

### Borders & Shadows

```html
<div class="rounded-lg shadow-md">
    Rounded card with shadow
</div>
```

### Transitions & Animations

```html
<!-- Smooth transition -->
<div class="transition">Animated element</div>

<!-- Fade in animation -->
<div class="animate-fade-in">Fading in</div>

<!-- Spinning animation -->
<div class="animate-spin">Spinner</div>
```

---

## Responsive Design

The design system includes responsive breakpoints:

- **Mobile**: `max-width: 480px`
- **Tablet**: `max-width: 768px`
- **Desktop**: Above 768px

### Responsive Utilities

```html
<!-- Touch-friendly button sizes on mobile -->
<button class="btn btn-primary">
    Button automatically 44px min-height on mobile
</button>
```

### Mobile Considerations

- All interactive elements have 44px minimum tap targets on mobile
- Font sizes automatically scale down on smaller screens
- Form inputs use 16px font size to prevent iOS zoom
- Modals are 95% width on mobile devices

---

## Examples

### Complete Button Example

```html
<button class="btn btn-primary btn-lg flex items-center gap-2">
    <svg width="20" height="20">...</svg>
    <span>Sign Up</span>
</button>
```

### Form with Validation

```html
<form>
    <div class="form-group">
        <label class="form-label">Email</label>
        <input type="email" class="form-input" placeholder="you@example.com">
    </div>

    <div class="alert alert-error show mb-4">
        Please enter a valid email address.
    </div>

    <button class="btn btn-primary" type="submit">
        Submit
    </button>
</form>
```

### Interactive Card Grid

```html
<div class="grid gap-6">
    <div class="card card-hover">
        <h3 class="heading-3 mb-3">Card 1</h3>
        <p class="text-tertiary">Description here</p>
        <button class="btn btn-secondary btn-sm mt-4">
            Learn More
        </button>
    </div>

    <div class="card card-hover">
        <h3 class="heading-3 mb-3">Card 2</h3>
        <p class="text-tertiary">Description here</p>
        <button class="btn btn-secondary btn-sm mt-4">
            Learn More
        </button>
    </div>
</div>
```

---

## Best Practices

### 1. Use CSS Variables

Always use CSS variables instead of hardcoded values:

```css
/* Good */
.my-component {
    color: var(--color-text-primary);
    padding: var(--space-4);
}

/* Avoid */
.my-component {
    color: #ffb3fd;
    padding: 16px;
}
```

### 2. Compose Classes

Build complex components by composing utility classes:

```html
<!-- Good -->
<button class="btn btn-primary flex items-center gap-2">

<!-- Avoid creating custom classes when utilities work -->
<button class="custom-flex-button-with-icon">
```

### 3. Maintain Consistency

- Use the spacing scale for all margins/padding
- Use defined border radius values
- Stick to the color palette
- Use typography scale for all text sizes

### 4. Responsive First

- Design for mobile first
- Use the provided responsive utilities
- Test on multiple device sizes

---

## Migration Guide

### Converting Existing Styles

**Before:**
```css
.my-button {
    background: #4d1849;
    color: #ffb3fd;
    padding: 12px 24px;
    border-radius: 14px;
    transition: all 0.3s ease;
}
```

**After:**
```css
.my-button {
    background: var(--color-accent-primary);
    color: var(--color-text-primary);
    padding: var(--space-3) var(--space-6);
    border-radius: var(--radius-lg);
    transition: all var(--transition-base);
}
```

Or better yet, use the component classes:
```html
<button class="btn btn-primary">My Button</button>
```

---

## Support

For questions or contributions to the design system:
- Review the main CSS file: `/static/css/design-system.css`
- Check existing component implementations in templates
- Follow the established patterns and conventions

---

**Version:** 1.0.0
**Last Updated:** November 2025
