import { defineCollection, z } from 'astro:content';

// Blog post schema - Type-safe content for AI-generated posts
const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string().max(100),
    description: z.string().max(200),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    category: z.enum(['tech', 'entertainment', 'news']),
    tags: z.array(z.string()).max(5),
    author: z.string().default('FutureScopeHub AI'),
    readingTime: z.string().optional(),
    featured: z.boolean().default(false),
    sources: z.array(z.object({
      title: z.string(),
      url: z.string().url()
    })).optional(),
    tldr: z.string().max(300).optional(), // Quick summary for scanners
  })
});

export const collections = {
  blog: blogCollection
};
