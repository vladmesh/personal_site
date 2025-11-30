import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';

const projectRoot = fileURLToPath(new URL('.', import.meta.url));

export default defineConfig({
  integrations: [mdx(), tailwind()],
  srcDir: 'src',
  output: 'static',
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
