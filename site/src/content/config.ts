import { defineCollection, z } from 'astro:content';

const projectCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    role: z.string(),
    year: z.string(),
    summary: z.string(),
    stack: z.array(z.string()),
    links: z.array(
      z.object({
        href: z.string().url(),
        label: z.object({
          ru: z.string(),
          en: z.string()
        })
      })
    )
  })
});

export const collections = {
  'ru/projects': projectCollection,
  'en/projects': projectCollection
};
