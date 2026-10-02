/**
 * Renamed project slugs: old slug -> current slug. A request for an old project
 * URL in any locale gets a permanent redirect to the current one, so links shared
 * before a rename keep working. Add an entry whenever a slug changes in /admin.
 */
export const projectSlugRedirects: Readonly<Record<string, string>> = {
  secretary: 'ummanu',
};
