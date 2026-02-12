import os
import json
import re
import hashlib
import time
import requests
from datetime import datetime, timezone
from pathlib import Path

import feedparser
from slugify import slugify
from google import genai
from google.genai import types

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
NEWSDATA_KEY = os.environ.get("NEWSDATA_KEY", "")
MODEL_NAME = "gemini-2.0-flash"
CONTENT_DIR = Path("src/content/blog")
CATEGORIES = ["tech", "entertainment", "news"]

RSS_FEEDS = {
    "tech": [
        "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "https://www.theverge.com/rss/index.xml",
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
    articles = []
    seen = set()
    for feed_url in RSS_FEEDS.get(category, []):
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                h = hashlib.md5(entry.title.encode()).hexdigest()
                if h in seen:
                    continue
                seen.add(h)
                articles.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "source": feed.feed.get("title", ""),
                })
        except Exception as e:
            print(f"RSS error: {e}")
    return articles[:10]

def generate_article(category, articles):
    if not articles:
        return None
    client = genai.Client(api_key=GOOGLE_API_KEY)
    news = "\n".join([f"- {a['title']}: {a['summary'][:200]}" for a in articles[:5]])
    prompt = f"""You are a senior editor for FutureScopeHub. Write a news article about {category}.

NEWS:
{news}

Use Google Search to verify facts. Return JSON only:
{{"title": "headline", "description": "meta desc", "content": "markdown article 800+ words", "tags": ["t1","t2"], "tldr": ["point1","point2"]}}"""
    try:
        tool = types.Tool(google_search=types.GoogleSearch())
        cfg = types.GenerateContentConfig(tools=[tool], temperature=0.7)
        resp = client.models.generate_content(model=MODEL_NAME, contents=prompt, config=cfg)
        txt = resp.text.strip()
        if txt.startswith("```"):
            txt = re.sub(r"^```json?\n?", "", txt)
            txt = re.sub(r"\n?```$", "", txt)
        result = json.loads(txt)
        result["category"] = category
        result["sources"] = [a["link"] for a in articles[:3]]
        return result
    except Exception as e:
        print(f"AI error: {e}")
        return None

def write_post(data):
    if not data:
        return None
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    title = data.get("title", "Untitled")
    slug = slugify(title)[:50]
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = CONTENT_DIR / f"{date}-{slug}.md"
    if path.exists():
        return None
    tags = "\n".join([f'  - "{t}"' for t in data.get("tags", [])])
    sources = "\n".join([f'  - "{s}"' for s in data.get("sources", [])])
    tldr = "\n".join([f'  - "{p}"' for p in data.get("tldr", [])])
    content = data.get("content", "") + "\n\n---\n*AI-assisted report with automated fact-checking.*"
    md = f"""---
title: "{title.replace('"', "'")}"
description: "{data.get('description', '').replace('"', "'")}"
pubDate: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
category: "{data.get('category', 'tech')}"
tags:
{tags}
sources:
{sources}
tldr:
{tldr}
---

{content}
"""
    path.write_text(md, encoding="utf-8")
    print(f"Created: {path.name}")
    return path

def main():
    print("FutureScopeHub Autonomous News Agent")
    if not GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY not set")
        exit(1)
    for cat in CATEGORIES:
        print(f"Processing {cat}...")
        articles = fetch_news(cat)
        if articles:
            post = generate_article(cat, articles)
            if post:
                write_post(post)
                time.sleep(3)
    print("Done!")

if __name__ == "__main__":
    main()
