# נושאי מחקר לפיתוח צד-לקוח (Frontend)

## 1. ארכיטקטורה ותשתיות (Architecture & Frameworks)
* **Micro-Frontends:** גישות לאינטגרציה (Module Federation, Web Components, Iframes), ניהול מצב גלובלי בין מיקרו-אפליקציות ותקשורת בין DOMs שונים.
* **Server-Side Rendering (SSR) & Static Site Generation (SSG):** ניתוח והשוואה בין Next.js, Nuxt, ו-Remix. אסטרטגיות רנדור היברידי ו-Incremental Static Regeneration (ISR).
* **React Server Components (RSC):** השפעה על ביצועים, ניהול Data Fetching, שינוי פרדיגמת הפיתוח ב-React והשפעה על גודל הבאנדל (Bundle Size).
* **Frameworks מהדור החדש:** מחקר על Qwik, SolidJS, ו-Astro - התמקדות ב-Hydration, Resumability ו-Islands Architecture.

## 2. ביצועים (Performance)
* **Core Web Vitals:** מתודולוגיות לשיפור מדדי LCP, INP, ו-CLS. אופטימיזציית תמונות, פונטים וטעינת משאבים חוסמי-רינדור.
* **WebAssembly (WASM):** שילוב שפות כמו Rust/C++ בפרונטנד לביצוע פעולות כבדות דאטה (עיבוד תמונה, חישובים מתמטיים) ישירות בדפדפן.
* **Off-Main-Thread Architecture:** שימוש ב-Web Workers וספריות כמו Partytown להרצת סקריפטים צד-שלישי (Analytics, Ads) מחוץ לת'רד הראשי.
* **ניהול זכרון ו-Memory Leaks:** כלים ושיטות לאיתור ופתרון דליפות זיכרון באפליקציות Single Page (SPA).

## 3. ניהול מצב (State Management)
* **Signals:** מחקר על יישום Signals (ב-Preact, Solid, Angular v16+) ואיך מנגנון ה-Reactivity משתווה ל-Virtual DOM.
* **ספריות ניהול מצב מודרניות:** השוואה בין Zustand, Jotai, Redux Toolkit, ו-Recoil - מבחינת ביצועים, Boilerplate וקלות תחזוקה.
* **Server State vs Client State:** שימוש ב-React Query / SWR / Apollo לניהול מידע מהשרת (Caching, Invalidation) לעומת ניהול מצב UI לוקאלי.

## 4. כלים ותהליכי בנייה (Build Tools & Tooling)
* **Bundlers מדור חדש:** ביצועים והשוואה בין Vite (מבוסס Rollup/esbuild), Turbopack, ו-Rspack בזמני הפיתוח ובזמן הקימפול לפרודקשן.
* **Monorepo Management:** ניהול קודבייס מרובה פרויקטים וספריות בעזרת Turborepo, Nx, או Lerna. חלוקת קוד (Code Sharing) יעילה.

## 5. עיצוב וממשק משתמש (Styling & UI)
* **CSS Architecture:** עבודה עם Tailwind CSS בסביבות מורכבות, פתרונות CSS-in-JS (כמו Styled Components) אל מול סביבות Server Components (שם נדרש CSS חולץ/אפס זמן ריצה כמו Panda CSS).
* **Design Systems & Headless UI:** בנייה ותחזוקה של ספריות קומפוננטות אגנוסטיות ונגישות בעזרת Radix UI, אריזה ב-Storybook וניהול טוקנים (Design Tokens).
* **אנימציות מורכבות:** פיתוח מיקרו-אינטראקציות ואנימציות מבוססות דאטה עם Framer Motion, GSAP, ויישום View Transitions API בדפדפנים מודרניים.

## 6. בדיקות ואבטחת איכות (Testing & QA)
* **End-to-End (E2E):** השוואה בין Playwright ל-Cypress - יתרונות, חסרונות, תמיכה בדפדפנים ומהירות ריצה ב-CI.
* **Unit & Integration Tests:** מעבר מ-Jest ל-Vitest, שימוש ב-Testing Library בצורה יעילה לבדיקת התנהגות קומפוננטות (Behavioral Testing).

## 7. נגישות ובינלאומיות (a11y & i18n)
* **נגישות (Accessibility):** עמידה בתקני WCAG 2.1/2.2 AA. פיתוח מבוסס מקלדת, תמיכה בקוראי מסך (Screen Readers) ושימוש נכון ב-ARIA attributes. אוטומציה עם axe-core.
* **בינלאומיות (Internationalization):** ניהול שפות ותמיכה ב-RTL (ימין-לשמאל) בצורה נכונה וביצועית.

## 8. חדשנות ושילובי AI (Innovation & AI Integration)
* **AI on the Edge / Browser:** הרצת מודלי למידת מכונה (ML) ומודלי שפה (LLMs) ישירות בדפדפן באמצעות WebGL/WebGPU וספריות כמו WebLLM או ONNX Runtime Web.
* **Generative UI:** בניית ממשקים שנוצרים או משתנים בזמן אמת על בסיס קלט ממשתמש או החלטות אלגוריתמיות בשילוב שרת-לקוח.
