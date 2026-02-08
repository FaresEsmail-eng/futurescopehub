import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = await getCollection('blog');
  
  const sortedPosts = posts.sort((a, b) => 
    new Date(b.data.pubDate).valueOf() - new Date(a.data.pubDate).valueOf()
  );
  
  return rss({
    title: 'FutureScopeHub',
    description: 'Your daily dose of tech, entertainment, and breaking news. Fresh perspectives powered by AI.',
    site: context.site!,
    items: sortedPosts.map(post => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/blog/${post.slug}/`,
      categories: [post.data.category, ...(post.data.tags || [])],
      author: post.data.author
    })),
    customData: `<language>en-us</language>`,
  });
}
