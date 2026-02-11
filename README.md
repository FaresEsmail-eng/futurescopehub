# FutureScopeHub 🚀# FutureScopeHub 🚀



> AI-powered blog covering **Tech**, **Entertainment**, and **News**. > AI-powered blog covering **Tech**, **Entertainment**, and **News**. Fresh perspectives delivered daily.

> 

> **100% Credit-Card-Free** - Uses Google AI Studio's free tier!![FutureScopeHub](https://img.shields.io/badge/Powered%20by-Gemini%203-blue?style=for-the-badge)

![GitHub Actions](https://img.shields.io/badge/Automated-GitHub%20Actions-green?style=for-the-badge)

![FutureScopeHub](https://img.shields.io/badge/Powered%20by-Gemini%202.0-blue?style=for-the-badge)![Astro](https://img.shields.io/badge/Built%20with-Astro-purple?style=for-the-badge)

![No Credit Card](https://img.shields.io/badge/Cost-$0%20Forever-green?style=for-the-badge)

![GitHub Actions](https://img.shields.io/badge/Automated-GitHub%20Actions-purple?style=for-the-badge)## ✨ Features



## 💸 Zero Cost Architecture- **🤖 AI-Generated Content**: Daily articles synthesized using Gemini 3 Pro with Search Grounding

- **⚡ Lightning Fast**: Static site built with Astro, deployed to GitHub Pages

This project is designed for developers who **cannot or prefer not to use a credit card** for cloud services. It leverages:- **🎨 Modern Design**: Dark theme with neon accents, fully responsive

- **📰 Three Categories**: Tech, Entertainment, and News

| Service | Cost | How |- **🔄 Fully Automated**: GitHub Actions runs daily to generate fresh content

|---------|------|-----|- **📊 SEO Optimized**: Proper meta tags, sitemap, and RSS feed

| **Google AI Studio** | FREE | Gemini 2.0 Flash + 1.5 Pro, no billing required |

| **GitHub Actions** | FREE | 2000+ min/month for public repos |## 🏗️ Tech Stack

| **GitHub Pages** | FREE | Static hosting with CDN |

| **RSS Feeds** | FREE | Public news sources || Component | Technology |

|-----------|------------|

**Total Monthly Cost: $0.00** 🎉| Framework | Astro 5.x |

| Styling | Tailwind CSS 4.x |

## ✨ Features| AI | Google Gemini 3 (via Vertex AI) |

| Automation | GitHub Actions |

- 🤖 **AI-Generated Content**: Daily articles using Gemini 2.0 (FREE via AI Studio)| Hosting | GitHub Pages |

- ⚡ **Lightning Fast**: Static site built with Astro| Content | Markdown with Content Collections |

- 🎨 **Modern Design**: Dark neon theme, fully responsive

- 📰 **Three Categories**: Tech, Entertainment, and News## 🚀 Quick Start

- 🔄 **Fully Automated**: GitHub Actions runs daily

- 📊 **SEO Ready**: Sitemap, RSS, meta tags included### Prerequisites



## 🚀 Quick Start- Node.js 20+

- Python 3.12+

### Prerequisites- Google Cloud API Key with Gemini access



- Node.js 20+### Local Development

- Python 3.10+

- Google Account (for AI Studio API key)```bash

- GitHub Account# Clone the repository

git clone https://github.com/yourusername/futurescopehub.git

### Step 1: Get Your FREE API Keycd futurescopehub



1. Go to **[aistudio.google.com](https://aistudio.google.com/)**# Install dependencies

2. Sign in with your Google Accountnpm install

3. Click **"Get API Key"** → **"Create API Key"**pip install -r scripts/requirements.txt

4. Copy the key (starts with `AIzaSy...`)

# Start dev server

> ⚠️ **No credit card required!** AI Studio is completely free.npm run dev

```

### Step 2: Local Development

### Generate Content Locally

```bash

# Clone the repository```bash

git clone https://github.com/FaresEsmail-eng/futurescopehub.git# Set your API key

cd futurescopehubexport GOOGLE_API_KEY="your-api-key-here"



# Install dependencies# Run the generator

npm installpython scripts/daily_digest.py

pip install -r scripts/requirements.txt```



# Start dev server## 📁 Project Structure

npm run dev

``````

futurescopehub/

### Step 3: Test Content Generation├── .devcontainer/          # Codespaces configuration

├── .github/

```bash│   └── workflows/

# Set your API key│       ├── daily-digest.yml   # Content generation workflow

export GOOGLE_API_KEY="AIzaSy_your_key_here"│       └── deploy.yml         # Build & deploy workflow

├── public/

# On Windows PowerShell:│   └── favicon.svg

$env:GOOGLE_API_KEY = "AIzaSy_your_key_here"├── scripts/

│   ├── daily_digest.py     # AI content generator

# Run the generator│   └── requirements.txt    # Python dependencies

python scripts/daily_digest.py├── src/

```│   ├── components/         # Astro components

│   ├── content/

## 📁 Project Structure│   │   ├── blog/          # Generated articles (Markdown)

│   │   └── config.ts      # Content schema

```│   ├── layouts/           # Page layouts

futurescopehub/│   ├── pages/             # Routes

├── .github/workflows/      # Automation│   └── styles/            # Global CSS

│   ├── daily-digest.yml    # Content generation (daily)├── astro.config.mjs

│   └── deploy.yml          # Build & deploy├── package.json

├── scripts/└── tsconfig.json

│   ├── daily_digest.py     # 🤖 AI content generator```

│   └── requirements.txt    # Python deps

├── src/## ⚙️ Configuration

│   ├── components/         # UI components

│   ├── content/blog/       # Generated articles### GitHub Secrets

│   ├── layouts/            # Page layouts

│   ├── pages/              # RoutesAdd these secrets to your repository (`Settings → Secrets and variables → Actions`):

│   └── styles/             # CSS

└── public/                 # Static assets| Secret | Description |

```|--------|-------------|

| `GOOGLE_API_KEY` | Your Gemini API key from Google AI Studio or Vertex AI |

## ⚙️ GitHub Setup

### Activating Google Cloud Credits

### Add Your API Key as a Secret

1. Go to [Google Developer Profile](https://developers.google.com/profile)

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**2. Navigate to Benefits

2. Click **"New repository secret"**3. Activate your $10/month Cloud Credits (Google One AI Premium benefit)

3. Name: `GOOGLE_API_KEY`4. Create a project in Google Cloud Console

4. Value: Your AI Studio API key5. Enable the Gemini API

5. Click **"Add secret"**6. Generate an API key



### Enable GitHub Pages## 📅 Automation Schedule



1. Go to **Settings** → **Pages**The daily digest runs automatically at **09:00 UTC** every day via GitHub Actions.

2. Source: **GitHub Actions**

3. The site will deploy automatically on push to `main`To run manually:

1. Go to `Actions` tab

## 🔄 How Automation Works2. Select `🚀 Daily Digest`

3. Click `Run workflow`

Every day at 09:00 UTC, GitHub Actions:

## 🔒 Content Review

1. 📡 Fetches latest news from RSS feeds

2. 🤖 Generates articles using Gemini 2.0 FlashBy default, generated content creates a **Pull Request** instead of auto-publishing. This allows you to:

3. ✨ Refines with Gemini 1.5 Pro

4. 📝 Creates a Pull Request for review1. Review titles and content

5. ✅ You merge → Site deploys automatically2. Verify factual accuracy

3. Add personal notes if desired

## 📊 AI Studio Free Tier Limits4. Merge when ready to publish



| Limit | Value | Impact |## 📊 Cost Analysis

|-------|-------|--------|

| Requests/min | ~15 RPM | Script includes delays || Resource | Monthly Cost |

| Requests/day | ~1,500 RPD | More than enough for daily digest ||----------|--------------|

| Context Window | 1M tokens | Can analyze huge documents || Gemini API (~30 posts) | ~$0.40 |

| Models | Gemini 2.0 Flash, 1.5 Pro | State-of-the-art quality || Imagen 3 (30 images) | ~$1.20 |

| Search Grounding | ~$1.05 |

## 🌍 For Developers in Restricted Regions| **Total** | **~$2.65** |



This project is specifically designed for developers who:*Easily covered by the $10/month Google Developer Program credit!*



- 🏦 Cannot get international credit cards## 🤝 Contributing

- 💳 Have debit cards blocked for foreign transactions

- 🌐 Live in regions with banking restrictions (Egypt, etc.)Contributions are welcome! Feel free to:



**No Payoneer, no virtual cards, no workarounds needed!**- Report bugs

- Suggest features

## 🆚 Why AI Studio over Vertex AI?- Improve the AI prompts

- Enhance the design

| Feature | AI Studio (FREE) | Vertex AI (Paid) |

|---------|-----------------|------------------|## 📄 License

| Credit Card | ❌ Not required | ✅ Required |

| Billing Account | ❌ Not required | ✅ Required |MIT License - feel free to use this as a template for your own AI-powered blog!

| Models | Gemini 2.0/1.5 | Gemini 2.0/1.5 |

| Context Window | 1M tokens | 1M tokens |---

| Rate Limits | 15 RPM | Higher |

| Data Privacy | Lower | Higher |**Built with 💜 and AI** | [FutureScopeHub](https://futurescopehub.com)


**For prototyping and personal projects, AI Studio is perfect!**

## 🛠️ Alternative: GitHub Models

If you want to use GPT-4o or Llama instead, check out [GitHub Models](https://github.com/marketplace/models):

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],  # Your GitHub PAT
)
```

**Also 100% free with your GitHub account!**

## 📄 License

MIT License - Use this as a template for your own AI blog!

---

**Built with 💜 and zero dollars** | [FutureScopeHub](https://faresEsmail-eng.github.io/futurescopehub)
