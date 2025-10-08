# Vlad Mesh — Personal Site

Static portfolio built with [Astro](https://astro.build/) + Tailwind + MDX. Russian and English versions live side by side under `/ru/*` and `/en/*` routes.

## Requirements

- Node.js 20+
- npm 9+

## Scripts

```bash
npm install       # install dependencies
npm run dev       # start local dev server
npm run build     # build static output to dist/
npm run preview   # preview production build
```

## Project structure

```
site/
├─ src/
│  ├─ pages/        # Astro pages (ru/en)
│  ├─ components/   # UI building blocks
│  ├─ content/      # MDX case studies (content collections)
│  ├─ data/         # Structured data (skills, testimonials)
│  ├─ layouts/      # Base layout + wrappers
│  ├─ middleware.ts # Accept-Language redirect to /ru or /en
│  └─ styles/       # Tailwind entrypoint
├─ public/          # Static assets (CVs, OG images)
├─ ops/             # Caddy config and deploy helper
├─ docker-compose.yml
├─ astro.config.mjs
├─ tailwind.config.mjs
└─ package.json
```

## Content workflow

- Case studies live in `src/content/{ru|en}/projects/*.mdx`.
- Update summary/stack inside MDX frontmatter; list view pulls the same data.
- Upload latest CVs to `public/cv/cv_ru.pdf` and `public/cv/cv_en.pdf`.
- OG images go into `public/og/` (one per page).

## Deployment

1. `npm run build`
2. Sync `dist/` to `/srv/site` on the VPS (use `ops/deploy.sh` or CI workflow).
3. Ensure Caddy is reloaded (`docker compose up -d`).

GitHub Actions workflow `.github/workflows/deploy.yml` automates the build + rsync + reload on pushes to `main`.
