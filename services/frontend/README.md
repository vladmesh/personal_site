# Vlad Mesh — Personal Site

Static portfolio built with [Astro](https://astro.build/) + Tailwind + MDX. Russian and English versions live side by side under `/ru/*` and `/en/*` routes.

## Requirements

- Node.js 20+
- npm 9+
- `.env` with `PUBLIC_API_BASE_URL` pointing to the backend (see below)

## Scripts

```bash
npm install       # install dependencies
npm run dev       # start local dev server
npm run build     # build static output to dist/
npm run preview   # preview production build
```

### Environment

Create `.env` in `services/frontend`:

```bash
cp .env.example .env
```

Set `PUBLIC_API_BASE_URL` to the backend base URL (shared for dev/prod inside the Docker network). Default: `http://backend:8000`. This is used to fetch contacts from `/api/v1/profile/contacts`.

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
├─ ops/             # Caddy config, deploy helpers and build image
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

## Deployment with manage.sh

For local or manual deployments there is a Docker Compose stack that renders the static site and serves it through Caddy. The helper script wraps the most common commands and loads environment variables from `.env` automatically.

```bash
./manage.sh build    # run npm ci && npm run build inside the builder container
./manage.sh start    # build the site and start Caddy
./manage.sh logs     # follow logs from all services
./manage.sh stop     # stop the stack
./manage.sh clean    # stop the stack and remove volumes (including dist)
```

Running `./manage.sh start` will first execute the `builder` service (producing `/app/dist` into the shared volume) and then bring the `proxy` service up in detached mode.

### `.env` variables

The script exports every variable from `.env` before invoking Docker Compose. Useful options include:

- `COMPOSE_PROJECT_NAME` — overrides the project name so volumes/networks are namespaced (defaults to the directory name).
- `DOCKER_CONTEXT` — set to a Docker context name to run commands against a remote host (falls back to the local Docker daemon).
- `DOCKER_HOST` — alternative way to target a remote Docker Engine; standard Docker variable that continues to work because it is sourced into the environment.

Create `.env` next to `manage.sh` and populate the variables relevant for your environment before running the script.
