import { type Config } from 'tailwindcss';

export default {
  content: [
    './src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter var"', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['"Fira Code"', 'monospace']
      },
      colors: {
        brand: {
          DEFAULT: '#6366f1',
          dark: '#4338ca',
          light: '#a5b4fc'
        }
      }
    }
  },
  plugins: []
} satisfies Config;
