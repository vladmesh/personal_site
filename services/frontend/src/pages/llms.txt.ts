import type { APIRoute } from 'astro';
import { siteConfig } from '@config/site';
import { llmSystemsCopy } from '@data/llm-systems';
import { fetchContacts, selectContact } from '@lib/profile/contacts';

/** /llms.txt (https://llmstxt.org): a short plain-text summary for LLM crawlers. */
export const GET: APIRoute = async () => {
  const copy = llmSystemsCopy.en;
  const contacts = await fetchContacts('en');
  const email = selectContact(contacts, ['email']);
  const telegram = selectContact(contacts, ['telegram']);
  const github = selectContact(contacts, ['github']);
  const domain = siteConfig.domain;

  const lines = [
    `# ${siteConfig.brand}`,
    '',
    `> ${copy.intro[0]}`,
    '',
    copy.intro[1],
    '',
    '## Services',
    '',
    ...copy.packages.map(
      (pkg) => `- [${pkg.name}](${domain}/en/llm-systems/#${pkg.id}): ${pkg.summary} ${pkg.timeline}, ${pkg.price}.`
    ),
    `- Hourly: ${copy.hourly}`,
    '',
    '## Work',
    '',
    ...copy.cases.map((item) => (item.href ? `- [${item.title}](${item.href}): ${item.text}` : `- ${item.title}: ${item.text}`)),
    '',
    '## Contact',
    '',
    ...(email ? [`- Email: ${email.value}`] : []),
    ...(telegram ? [`- Telegram: ${telegram.href}`] : []),
    ...(github ? [`- GitHub: ${github.href}`] : []),
    `- Service page: ${domain}/en/llm-systems/ (Russian: ${domain}/ru/llm-systems/)`,
    `- Sitemap: ${domain}/sitemap.xml`,
    ''
  ];

  return new Response(lines.join('\n'), {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600'
    }
  });
};
