# cafe-rothschild — כללי פיתוח

## HTML

- כל קובץ HTML חייב לכלול `dir="rtl"` ו-`lang="he"` על תגית `<html>`.

```html
<html lang="he" dir="rtl">
```

## עיצוב

- השתמש **תמיד** ב-Tailwind CSS v4 דרך CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

- **Mobile-first** — עצב תחילה למסך קטן, הוסף breakpoints (`sm:`, `md:`, `lg:`) רק לפי הצורך.
- **אין CSS חיצוני** — כל עיצוב דרך מחלקות Tailwind בלבד. אין `<style>` ואין קבצי `.css`.