import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [mdx(), tailwind()],
  srcDir: 'src',
  output: 'static',
  build: {
    format: 'directory'
  },
  redirects: {
    '/': '/en/'
  }
});
