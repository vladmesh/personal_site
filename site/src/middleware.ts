import type { MiddlewareHandler } from 'astro';

const supported = ['ru', 'en'] as const;

const detectLang = (headerValue: string | null) => {
  if (!headerValue) return 'en';
  const lower = headerValue.toLowerCase();
  if (lower.includes('ru')) return 'ru';
  return 'en';
};

export const onRequest: MiddlewareHandler = async ({ request, url, redirect }, next) => {
  if (url.pathname === '/' || url.pathname === '') {
    const lang = detectLang(request.headers.get('accept-language'));
    return redirect(`/${lang}/`, 302);
  }

  const [, maybeLocale] = url.pathname.split('/');
  if (maybeLocale && !supported.includes(maybeLocale as (typeof supported)[number])) {
    return redirect('/en/', 302);
  }

  return next();
};
