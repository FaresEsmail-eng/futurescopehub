"""
FutureScopeHub - Daily Digest Generator
========================================
This script is the core of the automated content pipeline.
It fetches news, synthesizes content using Gemini 3, and generates blog posts.

Requirements:
- google-genai (Vertex AI SDK)
- feedparser
- python-slugify
- Pillow (for image handling)

Environment Variables:
- GOOGLE_API_KEY: Your Gemini API key from Google AI Studio or Vertex AI
"""

import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import hashlib

# Third-party imports
try:
    import feedparser
    from slugify import slugify
    from google import genai
    from google.genai import types
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install google-genai feedparser python-slugify")
    exit(1)


# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Central configuration for the digest generator."""
    
    # API Configuration
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
    
    # Model Selection (2026 Gemini 3 family)
    MODEL_WRITER = "gemini-2.0-flash"  # Fast drafting - update to gemini-3-flash when available
    MODEL_EDITOR = "gemini-2.0-pro"    # Quality refinement - update to gemini-3-pro when available
    
    # Content Settings
    OUTPUT_DIR = Path("src/content/blog")
    IMAGE_DIR = Path("public/images/posts")
    
    # RSS Feeds to Monitor (Tech, Entertainment, News)
    RSS_FEEDS = {
        "tech": [
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/index.xml",
            "https://arstechnica.com/feed/",
            "https://feeds.wired.com/wired/index",
        ],
        "entertainment": [
            "https://variety.com/feed/",
            "https://www.hollywoodreporter.com/feed/",
            "https://ew.com/feed/",
        ],
        "news": [
            "https://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "https://feeds.reuters.com/reuters/topNews",
        ]
    }
    
    # Generation Settings
    MAX_ARTICLES_PER_CATEGORY = 3
    MIN_WORD_COUNT = 800
    MAX_WORD_COUNT = 1500


# ============================================================================
# SYSTEM PROMPTS
# ============================================================================

WRITER_SYSTEM_PROMPT = """You are a senior content writer for FutureScopeHub, a modern tech and culture blog.

Your writing style is:
- **Engaging**: Hook readers from the first sentence. Use vivid language.
- **Conversational**: Write like you're explaining to a smart friend, not a textbook.
- **Insightful**: Don't just report facts—provide context, implications, and "so what?"
- **Scannable**: Use headers, bullet points, and short paragraphs for easy reading.
- **Unique**: Add personality. Use metaphors, cultural references, and wit when appropriate.

CRITICAL RULES:
1. NEVER start with "In a world where..." or "In today's fast-paced..."
2. NEVER use phrases like "As an AI language model" or "I cannot..."
3. NEVER fabricate quotes, statistics, or sources
4. Always ground claims in the provided source material
5. Use Markdown formatting with H2 (##) and H3 (###) headers
6. Include a compelling hook in the first paragraph
7. End with a thought-provoking conclusion or call-to-action

Output ONLY the article body in Markdown. Do not include the title or frontmatter."""

EDITOR_SYSTEM_PROMPT = """You are the senior editor for FutureScopeHub. Your job is to polish drafts.

Review the draft and improve:
1. **Flow**: Ensure smooth transitions between paragraphs
2. **Clarity**: Simplify complex sentences without dumbing down
3. **Engagement**: Strengthen hooks and calls-to-action
4. **Accuracy**: Flag any claims that seem unsupported
5. **Voice**: Ensure consistent, engaging tone throughout

Also generate:
- A compelling SEO title (max 60 chars, include power words)
- A meta description (max 155 chars, include call-to-action)
- 3-5 relevant tags (lowercase, single words or hyphenated)
- A TL;DR summary (max 200 chars, punchy and informative)
- Reading time estimate

Return your response in this exact JSON format:
{
    "title": "Your SEO-optimized title here",
    "description": "Your meta description here",
    "tags": ["tag1", "tag2", "tag3"],
    "tldr": "Quick summary for scanners",
    "readingTime": "X min read",
    "content": "The full polished article in Markdown",
    "quality_score": 8.5,
    "notes": "Any editorial notes or concerns"
}"""


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def initialize_client() -> genai.Client:
    """Initialize the Gemini client."""
    if not Config.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return genai.Client(api_key=Config.GOOGLE_API_KEY)


def fetch_rss_articles(category: str, limit: int = 5) -> list[dict]:
    """Fetch and parse RSS feeds for a category."""
    articles = []
    feeds = Config.RSS_FEEDS.get(category, [])
    
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:limit]:
                articles.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", entry.get("description", "")),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": feed.feed.get("title", feed_url),
                })
        except Exception as e:
            print(f"Warning: Failed to fetch {feed_url}: {e}")
    
    # Remove duplicates based on title similarity
    seen_titles = set()
    unique_articles = []
    for article in articles:
        title_hash = hashlib.md5(article["title"].lower().encode()).hexdigest()[:8]
        if title_hash not in seen_titles:
            seen_titles.add(title_hash)
            unique_articles.append(article)
    
    return unique_articles[:Config.MAX_ARTICLES_PER_CATEGORY * 2]


def generate_draft(client: genai.Client, articles: list[dict], category: str) -> str:
    """Generate a draft article using Gemini Flash."""
    
    # Prepare context from articles
    context = "\n\n---\n\n".join([
        f"**Source: {a['source']}**\n"
        f"Title: {a['title']}\n"
        f"Summary: {a['summary']}\n"
        f"Link: {a['link']}"
        for a in articles
    ])
    
    prompt = f"""Based on these {category} news stories, write a comprehensive analysis article.

SOURCE MATERIAL:
{context}

INSTRUCTIONS:
1. Synthesize the key themes across these stories
2. Provide your unique analysis and implications
3. Write {Config.MIN_WORD_COUNT}-{Config.MAX_WORD_COUNT} words
4. Use engaging headers and formatting
5. Reference specific stories naturally (don't just list them)
6. End with forward-looking insights

Write the article now:"""

    response = client.models.generate_content(
        model=Config.MODEL_WRITER,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=WRITER_SYSTEM_PROMPT,
            temperature=0.8,
            max_output_tokens=4096,
        )
    )
    
    return response.text


def refine_article(client: genai.Client, draft: str, category: str) -> dict:
    """Refine the draft using Gemini Pro and extract metadata."""
    
    prompt = f"""Review and polish this {category} article draft. Then generate the required metadata.

DRAFT:
{draft}

Remember to return valid JSON with all required fields."""

    response = client.models.generate_content(
        model=Config.MODEL_EDITOR,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=EDITOR_SYSTEM_PROMPT,
            temperature=0.4,
            max_output_tokens=8192,
        )
    )
    
    # Parse JSON response
    text = response.text
    
    # Extract JSON from response (handle markdown code blocks)
    json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if json_match:
        text = json_match.group(1)
    else:
        # Try to find raw JSON
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
    
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        result = {
            "title": f"Latest in {category.title()}: Today's Top Stories",
            "description": f"Comprehensive analysis of today's biggest {category} news.",
            "tags": [category, "daily-digest", "analysis"],
            "tldr": f"Today's essential {category} updates synthesized.",
            "readingTime": "5 min read",
            "content": draft,
            "quality_score": 7.0,
            "notes": "JSON parsing failed, using fallback"
        }
    
    return result


def generate_frontmatter(metadata: dict, category: str, sources: list[dict]) -> str:
    """Generate Astro-compatible frontmatter."""
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Format sources for frontmatter
    sources_yaml = "\n".join([
        f'  - title: "{s["title"][:50]}..."\n    url: "{s["link"]}"'
        for s in sources[:5]
    ])
    
    frontmatter = f"""---
title: "{metadata['title']}"
description: "{metadata['description']}"
pubDate: {today}
category: "{category}"
tags: {json.dumps(metadata.get('tags', [category]))}
author: "FutureScopeHub AI"
readingTime: "{metadata.get('readingTime', '5 min read')}"
tldr: "{metadata.get('tldr', '')}"
featured: false
sources:
{sources_yaml}
---

"""
    return frontmatter


def save_article(content: str, frontmatter: str, slug: str) -> Path:
    """Save the article to the content directory."""
    
    Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = f"{today}-{slug}.md"
    filepath = Config.OUTPUT_DIR / filename
    
    full_content = frontmatter + content
    filepath.write_text(full_content, encoding="utf-8")
    
    return filepath


def generate_daily_digest(category: str) -> Optional[Path]:
    """Main function to generate a daily digest for a category."""
    
    print(f"\n{'='*50}")
    print(f"Generating {category.upper()} digest...")
    print('='*50)
    
    # Initialize client
    client = initialize_client()
    
    # Step 1: Fetch articles
    print("📡 Fetching RSS feeds...")
    articles = fetch_rss_articles(category)
    
    if not articles:
        print(f"⚠️ No articles found for {category}")
        return None
    
    print(f"   Found {len(articles)} articles")
    
    # Step 2: Generate draft
    print("✍️ Generating draft with Gemini Flash...")
    draft = generate_draft(client, articles, category)
    print(f"   Draft generated ({len(draft.split())} words)")
    
    # Step 3: Refine with Pro
    print("🔍 Refining with Gemini Pro...")
    refined = refine_article(client, draft, category)
    print(f"   Quality score: {refined.get('quality_score', 'N/A')}")
    
    # Step 4: Generate frontmatter
    frontmatter = generate_frontmatter(refined, category, articles)
    
    # Step 5: Save article
    slug = slugify(refined['title'])[:50]
    filepath = save_article(refined['content'], frontmatter, slug)
    print(f"✅ Saved to: {filepath}")
    
    return filepath


def main():
    """Main entry point for the daily digest generator."""
    
    print("\n" + "="*60)
    print("🚀 FutureScopeHub Daily Digest Generator")
    print("="*60)
    print(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    
    # Check for API key
    if not Config.GOOGLE_API_KEY:
        print("\n❌ ERROR: GOOGLE_API_KEY not set!")
        print("   Set it in your environment or GitHub Secrets")
        exit(1)
    
    # Generate digest for each category
    categories = ["tech", "entertainment", "news"]
    results = []
    
    for category in categories:
        try:
            result = generate_daily_digest(category)
            if result:
                results.append(str(result))
        except Exception as e:
            print(f"❌ Error generating {category} digest: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"Generated {len(results)} articles:")
    for r in results:
        print(f"   ✅ {r}")
    
    if not results:
        print("   ⚠️ No articles generated")
        exit(1)
    
    print("\n🎉 Daily digest complete!")


if __name__ == "__main__":
    main()
