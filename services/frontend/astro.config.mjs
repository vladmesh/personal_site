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
      PUBLIC_API_BASE_URL: envField.string({
        context: 'server',
        access: 'public',
        optional: false,
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
        '@lib': resolve(projectRoot, 'src/lib')
      }
    }
  },
  redirects: {
    '/': '/en/'
  }
});
