import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig, envField } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';
import node from '@astrojs/node';

const projectRoot = fileURLToPath(new URL('.', import.meta.url));

export default defineConfig({
  env: {
    schema: {
      INTERNAL_API_URL: envField.string({
        context: 'server',
        access: 'secret',
        optional: false,
      }),
      // Full public origin of the site, used for OG tags and hreflang.
      // Server-only + secret so it is read at runtime (overridable via compose
      // env), not inlined at build time.
      SITE_URL: envField.string({
        context: 'server',
        access: 'secret',
        optional: true,
        default: 'http://localhost:4321',
      }),
      // Display name in header, footer, and meta titles. Runtime-overridable.
      SITE_BRAND: envField.string({
        context: 'server',
        access: 'secret',
        optional: true,
        default: 'Your Name',
      }),
    },
  },
  integrations: [mdx(), tailwind()],
  srcDir: 'src',
  output: 'server',
  adapter: node({ mode: 'standalone' }),
  server: {
    host: '0.0.0.0',
    port: 4321
  },
  build: {
    format: 'directory'
  },
  vite: {
    resolve: {
      alias: {
        '@lib': resolve(projectRoot, 'src/lib'),
        '@config': resolve(projectRoot, 'src/config')
      }
    }
  },
  redirects: {
    '/': '/en/'
  }
});
