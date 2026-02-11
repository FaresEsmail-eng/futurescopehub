""""""

FutureScopeHub - Daily Digest Generator (Credit-Card-Free Edition)FutureScopeHub - Daily Digest Generator

===========================================================================================================

This script uses Google AI Studio (FREE) instead of Vertex AI.This script is the core of the automated content pipeline.

No credit card required - just a Google Account and API key from AI Studio.It fetches news, synthesizes content using Gemini 3, and generates blog posts.



How to get your FREE API Key:Requirements:

1. Go to https://aistudio.google.com/- google-genai (Vertex AI SDK)

2. Sign in with your Google Account- feedparser

3. Click "Get API Key" → "Create API Key"- python-slugify

4. Copy the key (starts with "AIzaSy...")- Pillow (for image handling)



Requirements:Environment Variables:

- google-generativeai (NOT google-cloud-aiplatform)- GOOGLE_API_KEY: Your Gemini API key from Google AI Studio or Vertex AI

- feedparser"""

- python-slugify

import os

Environment Variables:import json

- GOOGLE_API_KEY: Your FREE API key from Google AI Studioimport re

"""from datetime import datetime, timezone

from pathlib import Path

import osfrom typing import Optional

import jsonimport hashlib

import re

from datetime import datetime, timezone# Third-party imports

from pathlib import Pathtry:

from typing import Optional    import feedparser

import hashlib    from slugify import slugify

import time    from google import genai

    from google.genai import types

# Third-party importsexcept ImportError as e:

try:    print(f"Missing dependency: {e}")

    import feedparser    print("Run: pip install google-genai feedparser python-slugify")

    from slugify import slugify    exit(1)

    import google.generativeai as genai

except ImportError as e:

    print(f"Missing dependency: {e}")# ============================================================================

    print("Run: pip install google-generativeai feedparser python-slugify")# CONFIGURATION

    exit(1)# ============================================================================



class Config:

# ============================================================================    """Central configuration for the digest generator."""

# CONFIGURATION    

# ============================================================================    # API Configuration

    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

class Config:    

    """Central configuration for the digest generator."""    # Model Selection (2026 Gemini 3 family)

        MODEL_WRITER = "gemini-2.0-flash"  # Fast drafting - update to gemini-3-flash when available

    # API Configuration - FREE from Google AI Studio    MODEL_EDITOR = "gemini-2.0-pro"    # Quality refinement - update to gemini-3-pro when available

    # Get yours at: https://aistudio.google.com/apikey    

    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")    # Content Settings

        OUTPUT_DIR = Path("src/content/blog")

    # Model Selection - Available FREE in AI Studio    IMAGE_DIR = Path("public/images/posts")

    # Gemini 2.0 Flash: Fast, efficient, great for content generation    

    # Gemini 1.5 Pro: Higher quality, 1M token context window    # RSS Feeds to Monitor (Tech, Entertainment, News)

    MODEL_WRITER = "gemini-2.0-flash-exp"  # Fast drafting (FREE)    RSS_FEEDS = {

    MODEL_EDITOR = "gemini-1.5-pro"        # Quality refinement (FREE, 1M context!)        "tech": [

                "https://techcrunch.com/feed/",

    # Content Settings            "https://www.theverge.com/rss/index.xml",

    OUTPUT_DIR = Path("src/content/blog")            "https://arstechnica.com/feed/",

    IMAGE_DIR = Path("public/images/posts")            "https://feeds.wired.com/wired/index",

            ],

    # RSS Feeds to Monitor (Tech, Entertainment, News)        "entertainment": [

    RSS_FEEDS = {            "https://variety.com/feed/",

        "tech": [            "https://www.hollywoodreporter.com/feed/",

            "https://techcrunch.com/feed/",            "https://ew.com/feed/",

            "https://www.theverge.com/rss/index.xml",        ],

            "https://arstechnica.com/feed/",        "news": [

            "https://feeds.wired.com/wired/index",            "https://feeds.bbci.co.uk/news/world/rss.xml",

        ],            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",

        "entertainment": [            "https://feeds.reuters.com/reuters/topNews",

            "https://variety.com/feed/",        ]

            "https://www.hollywoodreporter.com/feed/",    }

            "https://ew.com/feed/",    

        ],    # Generation Settings

        "news": [    MAX_ARTICLES_PER_CATEGORY = 3

            "https://feeds.bbci.co.uk/news/world/rss.xml",    MIN_WORD_COUNT = 800

            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",    MAX_WORD_COUNT = 1500

        ]

    }

    # ============================================================================

    # Generation Settings# SYSTEM PROMPTS

    MAX_ARTICLES_PER_CATEGORY = 3# ============================================================================

    MIN_WORD_COUNT = 800

    MAX_WORD_COUNT = 1500WRITER_SYSTEM_PROMPT = """You are a senior content writer for FutureScopeHub, a modern tech and culture blog.

    

    # Rate Limiting (AI Studio Free Tier: ~15 RPM)Your writing style is:

    REQUEST_DELAY_SECONDS = 5  # Be respectful of free tier limits- **Engaging**: Hook readers from the first sentence. Use vivid language.

- **Conversational**: Write like you're explaining to a smart friend, not a textbook.

- **Insightful**: Don't just report facts—provide context, implications, and "so what?"

# ============================================================================- **Scannable**: Use headers, bullet points, and short paragraphs for easy reading.

# SYSTEM PROMPTS- **Unique**: Add personality. Use metaphors, cultural references, and wit when appropriate.

# ============================================================================

CRITICAL RULES:

WRITER_SYSTEM_PROMPT = """You are a senior content writer for FutureScopeHub, a modern tech and culture blog.1. NEVER start with "In a world where..." or "In today's fast-paced..."

2. NEVER use phrases like "As an AI language model" or "I cannot..."

Your writing style is:3. NEVER fabricate quotes, statistics, or sources

- **Engaging**: Hook readers from the first sentence. Use vivid language.4. Always ground claims in the provided source material

- **Conversational**: Write like you're explaining to a smart friend, not a textbook.5. Use Markdown formatting with H2 (##) and H3 (###) headers

- **Insightful**: Don't just report facts—provide context, implications, and "so what?"6. Include a compelling hook in the first paragraph

- **Scannable**: Use headers, bullet points, and short paragraphs for easy reading.7. End with a thought-provoking conclusion or call-to-action

- **Unique**: Add personality. Use metaphors, cultural references, and wit when appropriate.

Output ONLY the article body in Markdown. Do not include the title or frontmatter."""

CRITICAL RULES:

1. NEVER start with "In a world where..." or "In today's fast-paced..."EDITOR_SYSTEM_PROMPT = """You are the senior editor for FutureScopeHub. Your job is to polish drafts.

2. NEVER use phrases like "As an AI language model" or "I cannot..."

3. NEVER fabricate quotes, statistics, or sources - only use info from the provided articlesReview the draft and improve:

4. Use Markdown formatting with H2 (##) and H3 (###) headers1. **Flow**: Ensure smooth transitions between paragraphs

5. Include a compelling hook in the first paragraph2. **Clarity**: Simplify complex sentences without dumbing down

6. End with a thought-provoking conclusion or call-to-action3. **Engagement**: Strengthen hooks and calls-to-action

7. Keep paragraphs SHORT (2-3 sentences max)4. **Accuracy**: Flag any claims that seem unsupported

5. **Voice**: Ensure consistent, engaging tone throughout

Output ONLY the article body in Markdown. Do not include the title or frontmatter."""

Also generate:

EDITOR_SYSTEM_PROMPT = """You are the senior editor for FutureScopeHub. Your job is to polish drafts and generate metadata.- A compelling SEO title (max 60 chars, include power words)

- A meta description (max 155 chars, include call-to-action)

Review the draft and:- 3-5 relevant tags (lowercase, single words or hyphenated)

1. Improve flow and transitions- A TL;DR summary (max 200 chars, punchy and informative)

2. Strengthen the hook and conclusion- Reading time estimate

3. Ensure consistent, engaging tone

4. Fix any awkward phrasingReturn your response in this exact JSON format:

{

Then generate metadata. Return your response in this EXACT JSON format (no markdown code blocks):    "title": "Your SEO-optimized title here",

    "description": "Your meta description here",

{    "tags": ["tag1", "tag2", "tag3"],

    "title": "Catchy SEO title (max 60 chars, use power words)",    "tldr": "Quick summary for scanners",

    "description": "Meta description with call-to-action (max 155 chars)",    "readingTime": "X min read",

    "tags": ["tag1", "tag2", "tag3"],    "content": "The full polished article in Markdown",

    "tldr": "Punchy 1-sentence summary for scanners (max 200 chars)",    "quality_score": 8.5,

    "readingTime": "X min read",    "notes": "Any editorial notes or concerns"

    "content": "The full polished article in Markdown format"}"""

}"""



# ============================================================================

# ============================================================================# CORE FUNCTIONS

# CORE FUNCTIONS# ============================================================================

# ============================================================================

def initialize_client() -> genai.Client:

def initialize_client() -> None:    """Initialize the Gemini client."""

    """Initialize the Gemini client with AI Studio API key."""    if not Config.GOOGLE_API_KEY:

    if not Config.GOOGLE_API_KEY:        raise ValueError("GOOGLE_API_KEY environment variable is required")

        raise ValueError(    

            "GOOGLE_API_KEY environment variable is required!\n"    return genai.Client(api_key=Config.GOOGLE_API_KEY)

            "Get your FREE key at: https://aistudio.google.com/apikey"

        )

    def fetch_rss_articles(category: str, limit: int = 5) -> list[dict]:

    genai.configure(api_key=Config.GOOGLE_API_KEY)    """Fetch and parse RSS feeds for a category."""

    print("✅ Connected to Google AI Studio (FREE tier)")    articles = []

    feeds = Config.RSS_FEEDS.get(category, [])

    

def fetch_rss_articles(category: str, limit: int = 5) -> list[dict]:    for feed_url in feeds:

    """Fetch and parse RSS feeds for a category."""        try:

    articles = []            feed = feedparser.parse(feed_url)

    feeds = Config.RSS_FEEDS.get(category, [])            for entry in feed.entries[:limit]:

                    articles.append({

    for feed_url in feeds:                    "title": entry.get("title", ""),

        try:                    "summary": entry.get("summary", entry.get("description", "")),

            feed = feedparser.parse(feed_url)                    "link": entry.get("link", ""),

            for entry in feed.entries[:limit]:                    "published": entry.get("published", ""),

                # Clean HTML from summary                    "source": feed.feed.get("title", feed_url),

                summary = entry.get("summary", entry.get("description", ""))                })

                summary = re.sub(r'<[^>]+>', '', summary)[:500]  # Strip HTML, limit length        except Exception as e:

                            print(f"Warning: Failed to fetch {feed_url}: {e}")

                articles.append({    

                    "title": entry.get("title", ""),    # Remove duplicates based on title similarity

                    "summary": summary,    seen_titles = set()

                    "link": entry.get("link", ""),    unique_articles = []

                    "published": entry.get("published", ""),    for article in articles:

                    "source": feed.feed.get("title", feed_url),        title_hash = hashlib.md5(article["title"].lower().encode()).hexdigest()[:8]

                })        if title_hash not in seen_titles:

        except Exception as e:            seen_titles.add(title_hash)

            print(f"   ⚠️ Failed to fetch {feed_url}: {e}")            unique_articles.append(article)

        

    # Remove duplicates based on title similarity    return unique_articles[:Config.MAX_ARTICLES_PER_CATEGORY * 2]

    seen_titles = set()

    unique_articles = []

    for article in articles:def generate_draft(client: genai.Client, articles: list[dict], category: str) -> str:

        title_hash = hashlib.md5(article["title"].lower().encode()).hexdigest()[:8]    """Generate a draft article using Gemini Flash."""

        if title_hash not in seen_titles:    

            seen_titles.add(title_hash)    # Prepare context from articles

            unique_articles.append(article)    context = "\n\n---\n\n".join([

            f"**Source: {a['source']}**\n"

    return unique_articles[:Config.MAX_ARTICLES_PER_CATEGORY * 3]        f"Title: {a['title']}\n"

        f"Summary: {a['summary']}\n"

        f"Link: {a['link']}"

def generate_draft(articles: list[dict], category: str) -> str:        for a in articles

    """Generate a draft article using Gemini Flash (FREE)."""    ])

        

    # Prepare context from articles    prompt = f"""Based on these {category} news stories, write a comprehensive analysis article.

    context = "\n\n---\n\n".join([

        f"**Source: {a['source']}**\n"SOURCE MATERIAL:

        f"Title: {a['title']}\n"{context}

        f"Summary: {a['summary']}\n"

        f"Link: {a['link']}"INSTRUCTIONS:

        for a in articles[:5]  # Limit to 5 articles to stay within limits1. Synthesize the key themes across these stories

    ])2. Provide your unique analysis and implications

    3. Write {Config.MIN_WORD_COUNT}-{Config.MAX_WORD_COUNT} words

    prompt = f"""Based on these {category} news stories, write a comprehensive analysis article.4. Use engaging headers and formatting

5. Reference specific stories naturally (don't just list them)

SOURCE MATERIAL:6. End with forward-looking insights

{context}

Write the article now:"""

INSTRUCTIONS:

1. Synthesize the key themes across these stories    response = client.models.generate_content(

2. Provide your unique analysis and implications        model=Config.MODEL_WRITER,

3. Write {Config.MIN_WORD_COUNT}-{Config.MAX_WORD_COUNT} words        contents=prompt,

4. Use engaging headers (##) and formatting        config=types.GenerateContentConfig(

5. Reference specific stories naturally (don't just list them)            system_instruction=WRITER_SYSTEM_PROMPT,

6. End with forward-looking insights            temperature=0.8,

            max_output_tokens=4096,

Write the article now:"""        )

    )

    model = genai.GenerativeModel(    

        model_name=Config.MODEL_WRITER,    return response.text

        system_instruction=WRITER_SYSTEM_PROMPT

    )

    def refine_article(client: genai.Client, draft: str, category: str) -> dict:

    response = model.generate_content(    """Refine the draft using Gemini Pro and extract metadata."""

        prompt,    

        generation_config=genai.GenerationConfig(    prompt = f"""Review and polish this {category} article draft. Then generate the required metadata.

            temperature=0.8,

            max_output_tokens=4096,DRAFT:

        ){draft}

    )

    Remember to return valid JSON with all required fields."""

    return response.text

    response = client.models.generate_content(

        model=Config.MODEL_EDITOR,

def refine_article(draft: str, category: str) -> dict:        contents=prompt,

    """Refine the draft using Gemini Pro (FREE) and extract metadata."""        config=types.GenerateContentConfig(

                system_instruction=EDITOR_SYSTEM_PROMPT,

    prompt = f"""Review and polish this {category} article draft. Then generate the required metadata.            temperature=0.4,

            max_output_tokens=8192,

DRAFT:        )

{draft}    )

    

Return ONLY valid JSON with these fields: title, description, tags, tldr, readingTime, content    # Parse JSON response

Do NOT wrap in markdown code blocks."""    text = response.text

    

    model = genai.GenerativeModel(    # Extract JSON from response (handle markdown code blocks)

        model_name=Config.MODEL_EDITOR,    json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)

        system_instruction=EDITOR_SYSTEM_PROMPT    if json_match:

    )        text = json_match.group(1)

        else:

    response = model.generate_content(        # Try to find raw JSON

        prompt,        json_match = re.search(r'\{.*\}', text, re.DOTALL)

        generation_config=genai.GenerationConfig(        if json_match:

            temperature=0.4,            text = json_match.group(0)

            max_output_tokens=8192,    

        )    try:

    )        result = json.loads(text)

        except json.JSONDecodeError:

    text = response.text        # Fallback if JSON parsing fails

            result = {

    # Extract JSON from response (handle markdown code blocks if present)            "title": f"Latest in {category.title()}: Today's Top Stories",

    json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)            "description": f"Comprehensive analysis of today's biggest {category} news.",

    if json_match:            "tags": [category, "daily-digest", "analysis"],

        text = json_match.group(1)            "tldr": f"Today's essential {category} updates synthesized.",

    else:            "readingTime": "5 min read",

        # Try to find raw JSON            "content": draft,

        json_match = re.search(r'\{.*\}', text, re.DOTALL)            "quality_score": 7.0,

        if json_match:            "notes": "JSON parsing failed, using fallback"

            text = json_match.group(0)        }

        

    try:    return result

        result = json.loads(text)

        # Validate required fields

        required = ["title", "description", "tags", "content"]def generate_frontmatter(metadata: dict, category: str, sources: list[dict]) -> str:

        for field in required:    """Generate Astro-compatible frontmatter."""

            if field not in result:    

                raise ValueError(f"Missing field: {field}")    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    except (json.JSONDecodeError, ValueError) as e:    

        print(f"   ⚠️ JSON parsing issue: {e}, using fallback")    # Format sources for frontmatter

        # Fallback if JSON parsing fails    sources_yaml = "\n".join([

        result = {        f'  - title: "{s["title"][:50]}..."\n    url: "{s["link"]}"'

            "title": f"Today's {category.title()} Roundup: What You Need to Know",        for s in sources[:5]

            "description": f"The latest developments in {category} that are shaping our world.",    ])

            "tags": [category, "daily-digest", "analysis"],    

            "tldr": f"Your essential {category} update for today.",    frontmatter = f"""---

            "readingTime": "5 min read",title: "{metadata['title']}"

            "content": draft,description: "{metadata['description']}"

        }pubDate: {today}

    category: "{category}"

    # Ensure all fields have defaultstags: {json.dumps(metadata.get('tags', [category]))}

    result.setdefault("readingTime", "5 min read")author: "FutureScopeHub AI"

    result.setdefault("tldr", result.get("description", "")[:200])readingTime: "{metadata.get('readingTime', '5 min read')}"

    result.setdefault("tags", [category])tldr: "{metadata.get('tldr', '')}"

    featured: false

    return resultsources:

{sources_yaml}

---

def generate_frontmatter(metadata: dict, category: str, sources: list[dict]) -> str:

    """Generate Astro-compatible frontmatter.""""""

        return frontmatter

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    

    # Format sources for frontmatter (only include valid URLs)def save_article(content: str, frontmatter: str, slug: str) -> Path:

    sources_yaml = ""    """Save the article to the content directory."""

    for s in sources[:5]:    

        if s.get("link", "").startswith("http"):    Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

            title = s["title"][:50].replace('"', "'")    

            sources_yaml += f'  - title: "{title}"\n    url: "{s["link"]}"\n'    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        filename = f"{today}-{slug}.md"

    # Clean title and description for YAML    filepath = Config.OUTPUT_DIR / filename

    title = metadata['title'].replace('"', "'")[:100]    

    description = metadata['description'].replace('"', "'")[:200]    full_content = frontmatter + content

    tldr = metadata.get('tldr', '').replace('"', "'")[:300]    filepath.write_text(full_content, encoding="utf-8")

        

    frontmatter = f"""---    return filepath

title: "{title}"

description: "{description}"

pubDate: {today}def generate_daily_digest(category: str) -> Optional[Path]:

category: "{category}"    """Main function to generate a daily digest for a category."""

tags: {json.dumps(metadata.get('tags', [category])[:5])}    

author: "FutureScopeHub AI"    print(f"\n{'='*50}")

readingTime: "{metadata.get('readingTime', '5 min read')}"    print(f"Generating {category.upper()} digest...")

tldr: "{tldr}"    print('='*50)

featured: false    

sources:    # Initialize client

{sources_yaml}---    client = initialize_client()

    

"""    # Step 1: Fetch articles

    return frontmatter    print("📡 Fetching RSS feeds...")

    articles = fetch_rss_articles(category)

    

def save_article(content: str, frontmatter: str, slug: str) -> Path:    if not articles:

    """Save the article to the content directory."""        print(f"⚠️ No articles found for {category}")

            return None

    Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)    

        print(f"   Found {len(articles)} articles")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")    

    filename = f"{today}-{slug}.md"    # Step 2: Generate draft

    filepath = Config.OUTPUT_DIR / filename    print("✍️ Generating draft with Gemini Flash...")

        draft = generate_draft(client, articles, category)

    full_content = frontmatter + content    print(f"   Draft generated ({len(draft.split())} words)")

    filepath.write_text(full_content, encoding="utf-8")    

        # Step 3: Refine with Pro

    return filepath    print("🔍 Refining with Gemini Pro...")

    refined = refine_article(client, draft, category)

    print(f"   Quality score: {refined.get('quality_score', 'N/A')}")

def generate_daily_digest(category: str) -> Optional[Path]:    

    """Main function to generate a daily digest for a category."""    # Step 4: Generate frontmatter

        frontmatter = generate_frontmatter(refined, category, articles)

    print(f"\n{'='*50}")    

    print(f"📰 Generating {category.upper()} digest...")    # Step 5: Save article

    print('='*50)    slug = slugify(refined['title'])[:50]

        filepath = save_article(refined['content'], frontmatter, slug)

    # Step 1: Fetch articles    print(f"✅ Saved to: {filepath}")

    print("📡 Fetching RSS feeds...")    

    articles = fetch_rss_articles(category)    return filepath

    

    if not articles:

        print(f"   ⚠️ No articles found for {category}")def main():

        return None    """Main entry point for the daily digest generator."""

        

    print(f"   ✅ Found {len(articles)} articles")    print("\n" + "="*60)

        print("🚀 FutureScopeHub Daily Digest Generator")

    # Respect rate limits    print("="*60)

    time.sleep(Config.REQUEST_DELAY_SECONDS)    print(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")

        

    # Step 2: Generate draft with Gemini Flash (FREE)    # Check for API key

    print(f"✍️  Drafting with {Config.MODEL_WRITER}...")    if not Config.GOOGLE_API_KEY:

    try:        print("\n❌ ERROR: GOOGLE_API_KEY not set!")

        draft = generate_draft(articles, category)        print("   Set it in your environment or GitHub Secrets")

        word_count = len(draft.split())        exit(1)

        print(f"   ✅ Draft complete ({word_count} words)")    

    except Exception as e:    # Generate digest for each category

        print(f"   ❌ Draft generation failed: {e}")    categories = ["tech", "entertainment", "news"]

        return None    results = []

        

    # Respect rate limits    for category in categories:

    time.sleep(Config.REQUEST_DELAY_SECONDS)        try:

                result = generate_daily_digest(category)

    # Step 3: Refine with Gemini Pro (FREE)            if result:

    print(f"🔍 Refining with {Config.MODEL_EDITOR}...")                results.append(str(result))

    try:        except Exception as e:

        refined = refine_article(draft, category)            print(f"❌ Error generating {category} digest: {e}")

        print(f"   ✅ Refinement complete")    

    except Exception as e:    # Summary

        print(f"   ⚠️ Refinement failed, using draft: {e}")    print("\n" + "="*60)

        refined = {    print("📊 SUMMARY")

            "title": f"Today in {category.title()}: Key Developments",    print("="*60)

            "description": f"Your daily {category} briefing.",    print(f"Generated {len(results)} articles:")

            "tags": [category, "news"],    for r in results:

            "tldr": f"Essential {category} updates.",        print(f"   ✅ {r}")

            "readingTime": "5 min read",    

            "content": draft,    if not results:

        }        print("   ⚠️ No articles generated")

            exit(1)

    # Step 4: Generate frontmatter    

    frontmatter = generate_frontmatter(refined, category, articles)    print("\n🎉 Daily digest complete!")

    

    # Step 5: Save article

    slug = slugify(refined['title'])[:50]if __name__ == "__main__":

    filepath = save_article(refined['content'], frontmatter, slug)    main()

    print(f"💾 Saved: {filepath.name}")
    
    return filepath


def main():
    """Main entry point for the daily digest generator."""
    
    print("\n" + "="*60)
    print("🚀 FutureScopeHub Daily Digest Generator")
    print("   💸 Using Google AI Studio (100% FREE)")
    print("="*60)
    print(f"📅 Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    
    # Check for API key
    if not Config.GOOGLE_API_KEY:
        print("\n❌ ERROR: GOOGLE_API_KEY not set!")
        print("\n📋 How to get your FREE API key:")
        print("   1. Go to https://aistudio.google.com/")
        print("   2. Sign in with Google")
        print("   3. Click 'Get API Key' → 'Create API Key'")
        print("   4. Set it as environment variable or GitHub Secret")
        exit(1)
    
    # Initialize AI Studio connection
    try:
        initialize_client()
    except Exception as e:
        print(f"\n❌ Failed to connect: {e}")
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
        
        # Delay between categories to respect rate limits
        time.sleep(Config.REQUEST_DELAY_SECONDS)
    
    # Summary
    print("\n" + "="*60)
    print("📊 GENERATION SUMMARY")
    print("="*60)
    print(f"✅ Generated {len(results)} articles:")
    for r in results:
        print(f"   📄 {Path(r).name}")
    
    if not results:
        print("   ⚠️ No articles generated")
        exit(1)
    
    print("\n🎉 Daily digest complete!")
    print("💡 Tip: These articles are in src/content/blog/")
    print("   Run 'npm run dev' to preview them locally.")


if __name__ == "__main__":
    main()
