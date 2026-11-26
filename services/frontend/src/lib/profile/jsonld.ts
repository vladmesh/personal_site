import type { LlmSystemsCopy } from '@data/llm-systems';

/** schema.org Person + Service + Offer graph for the LLM systems page. */
export function llmSystemsJsonLd(opts: {
  copy: LlmSystemsCopy;
  lang: 'en' | 'ru';
  pageUrl: string;
  siteUrl: string;
  name: string;
  alternateNames: string[];
  email: string;
  sameAs: string[];
}): string {
  const personId = `${opts.siteUrl}/#person`;
  const graph = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Person',
        '@id': personId,
        name: opts.name,
        alternateName: opts.alternateNames,
        url: opts.siteUrl,
        email: `mailto:${opts.email}`,
        jobTitle: 'LLM systems engineer',
        homeLocation: { '@type': 'Place', name: 'Limassol, Cyprus' },
        sameAs: opts.sameAs
      },
      {
        '@type': 'Service',
        name: opts.copy.title,
        description: opts.copy.metaDescription,
        url: opts.pageUrl,
        inLanguage: opts.lang,
        areaServed: 'Worldwide',
        provider: { '@id': personId },
        offers: opts.copy.packages.map((pkg) => ({
          '@type': 'Offer',
          name: pkg.name,
          description: pkg.summary,
          url: `${opts.pageUrl}#${pkg.id}`,
          priceSpecification: {
            '@type': 'PriceSpecification',
            price: pkg.priceEur,
            priceCurrency: 'EUR',
            ...(pkg.price.startsWith('from') || pkg.price.startsWith('от') ? { minPrice: pkg.priceEur } : {})
          }
        }))
      }
    ]
  };
  // Escape "<" so the JSON cannot close the surrounding <script> tag.
  return JSON.stringify(graph).replace(/</g, '\\u003c');
}
