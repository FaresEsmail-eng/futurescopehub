# FutureScopeHub 🚀

> AI-powered blog covering **Tech**, **Entertainment**, and **News**. Fresh perspectives delivered daily.

![FutureScopeHub](https://img.shields.io/badge/Powered%20by-Gemini%203-blue?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/Automated-GitHub%20Actions-green?style=for-the-badge)
![Astro](https://img.shields.io/badge/Built%20with-Astro-purple?style=for-the-badge)

## ✨ Features

- **🤖 AI-Generated Content**: Daily articles synthesized using Gemini 3 Pro with Search Grounding
- **⚡ Lightning Fast**: Static site built with Astro, deployed to GitHub Pages
- **🎨 Modern Design**: Dark theme with neon accents, fully responsive
- **📰 Three Categories**: Tech, Entertainment, and News
- **🔄 Fully Automated**: GitHub Actions runs daily to generate fresh content
- **📊 SEO Optimized**: Proper meta tags, sitemap, and RSS feed

## 🏗️ Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Astro 5.x |
| Styling | Tailwind CSS 4.x |
| AI | Google Gemini 3 (via Vertex AI) |
| Automation | GitHub Actions |
| Hosting | GitHub Pages |
| Content | Markdown with Content Collections |

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- Python 3.12+
- Google Cloud API Key with Gemini access

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/futurescopehub.git
cd futurescopehub

# Install dependencies
npm install
pip install -r scripts/requirements.txt

# Start dev server
npm run dev
```

### Generate Content Locally

```bash
# Set your API key
export GOOGLE_API_KEY="your-api-key-here"

# Run the generator
python scripts/daily_digest.py
```

## 📁 Project Structure

```
futurescopehub/
├── .devcontainer/          # Codespaces configuration
├── .github/
│   └── workflows/
│       ├── daily-digest.yml   # Content generation workflow
│       └── deploy.yml         # Build & deploy workflow
├── public/
│   └── favicon.svg
├── scripts/
│   ├── daily_digest.py     # AI content generator
│   └── requirements.txt    # Python dependencies
├── src/
│   ├── components/         # Astro components
│   ├── content/
│   │   ├── blog/          # Generated articles (Markdown)
│   │   └── config.ts      # Content schema
│   ├── layouts/           # Page layouts
│   ├── pages/             # Routes
│   └── styles/            # Global CSS
├── astro.config.mjs
├── package.json
└── tsconfig.json
```

## ⚙️ Configuration

### GitHub Secrets

Add these secrets to your repository (`Settings → Secrets and variables → Actions`):

| Secret | Description |
|--------|-------------|
| `GOOGLE_API_KEY` | Your Gemini API key from Google AI Studio or Vertex AI |

### Activating Google Cloud Credits

1. Go to [Google Developer Profile](https://developers.google.com/profile)
2. Navigate to Benefits
3. Activate your $10/month Cloud Credits (Google One AI Premium benefit)
4. Create a project in Google Cloud Console
5. Enable the Gemini API
6. Generate an API key

## 📅 Automation Schedule

The daily digest runs automatically at **09:00 UTC** every day via GitHub Actions.

To run manually:
1. Go to `Actions` tab
2. Select `🚀 Daily Digest`
3. Click `Run workflow`

## 🔒 Content Review

By default, generated content creates a **Pull Request** instead of auto-publishing. This allows you to:

1. Review titles and content
2. Verify factual accuracy
3. Add personal notes if desired
4. Merge when ready to publish

## 📊 Cost Analysis

| Resource | Monthly Cost |
|----------|--------------|
| Gemini API (~30 posts) | ~$0.40 |
| Imagen 3 (30 images) | ~$1.20 |
| Search Grounding | ~$1.05 |
| **Total** | **~$2.65** |

*Easily covered by the $10/month Google Developer Program credit!*

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Improve the AI prompts
- Enhance the design

## 📄 License

MIT License - feel free to use this as a template for your own AI-powered blog!

---

**Built with 💜 and AI** | [FutureScopeHub](https://futurescopehub.com)
