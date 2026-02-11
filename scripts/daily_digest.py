import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import hashlib
import time

import feedparser
from slugify import slugify
import google.generativeai as genai


GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
MODEL_NAME = "gemini-1.5-flash"
CONTENT_DIR = Path("src/content/blog")
CATEGORIES = ["tech", "entertainment", "news"]

RSS_FEEDS = {
    "tech": [
        "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "https://www.theverge.com/rss/index.xml",
        "https://techcrunch.com/feed/",
    ],
    "entertainment": [
        "https://www.polygon.com/rss/index.xml",
        "https://kotaku.com/rss",
    ],
    "news": [
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    ],
}


def fetch_news(category):
    feeds = RSS_FEEDS.get(category, [])
    articles = []
    seen = set()
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                title_hash = hashlib.md5(entry.title.encode()).hexdigest()
                if title_hash in seen:
                    continue
                seen.add(title_hash)
                articles.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "source": feed.feed.get("title", ""),
                })
        except Exception as e:
            print(f"Warning: {e}")
    return articles[:10]


def generate_post(category, articles):
    if not articles:
        return None
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
    articles_text = "\n\n".join([f"**{a['title']}**\n{a['summary']}" for a in articles[:5]])
    prompt = f"""Write a blog post for FutureScopeHub about {category} news.

News:
{articles_text}

Return JSON: {{"title": "...", "description": "...", "content": "...", "tags": [...], "tldr": [...]}}"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```json?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        result = json.loads(text)
        result["category"] = category
        result["sources"] = [a["link"] for a in articles[:3]]
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None


def write_post(post_data):
    if not post_data:
        return None
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    title = post_data.get("title", "Untitled")
    slug = slugify(title)[:50]
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = f"{date_str}-{slug}.md"
    filepath = CONTENT_DIR / filename
    if filepath.exists():
        return None
    tags = "\n".join([f'  - "{t}"' for t in post_data.get("tags", [])])
    sources = "\n".join([f'  - "{s}"' for s in post_data.get("sources", [])])
    tldr = "\n".join([f'  - "{p}"' for p in post_data.get("tldr", [])])
    content = f"""---
title: "{title.replace('"', "'")}"
description: "{post_data.get('description', '').replace('"', "'")}"
pubDate: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
category: "{post_data.get('category', 'tech')}"
tags:
{tags}
sources:
{sources}
tldr:
{tldr}
---

{post_data.get('content', '')}
"""
    filepath.write_text(content, encoding="utf-8")
    print(f"Created: {filename}")
    return filepath


def main():
    print("FutureScopeHub Daily Digest")
    if not GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY not set!")
        exit(1)
    for category in CATEGORIES:
        print(f"Processing {category}...")
        articles = fetch_news(category)
        if articles:
            post = generate_post(category, articles)
            if post:
                write_post(post)
                time.sleep(2)
    print("Done!")


if __name__ == "__main__":
    main()
