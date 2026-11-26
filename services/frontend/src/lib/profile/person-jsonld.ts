/**
 * Minimal schema.org Person for the home pages. Uses the same `@id`
 * (`<site>/#person`) as the Person node on other pages, so search engines
 * merge them into one entity.
 */
export function personJsonLd(opts: {
  siteUrl: string;
  name: string;
  alternateNames: string[];
  sameAs: string[];
}): string {
  const person = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': `${opts.siteUrl}/#person`,
    name: opts.name,
    ...(opts.alternateNames.length > 0 ? { alternateName: opts.alternateNames } : {}),
    url: opts.siteUrl,
    ...(opts.sameAs.length > 0 ? { sameAs: opts.sameAs } : {})
  };
  // Escape "<" so the JSON cannot close the surrounding <script> tag.
  return JSON.stringify(person).replace(/</g, '\\u003c');
}
