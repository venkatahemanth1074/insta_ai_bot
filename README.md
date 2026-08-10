# 📸 Insta AI Bot — Autonomous Social Media & Link-in-Bio Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automated_Browser-green?logo=playwright&logoColor=white)](https://playwright.dev/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-Generative_AI-8E75B2?logo=google&logoColor=white)](https://ai.google.dev/)
[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Live_Deploy-brightgreen?logo=github&logoColor=white)](https://venkatahemanth1074.github.io/insta_ai_bot/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An autonomous, end-to-end social media publishing engine that scrapes trending tech news, synthesizes localized high-engagement copy using **Google Gemini AI**, procedurally renders vector graphics (1080×1350) with **Pillow (PIL)**, publishes live to **Instagram** using **Playwright**, and auto-deploys dynamic **Link-in-Bio** landing pages via **GitHub Pages**.

🔗 **Live Demo (Link-in-Bio)**: [https://venkatahemanth1074.github.io/insta_ai_bot/](https://venkatahemanth1074.github.io/insta_ai_bot/)

---

## 🚀 Key Features

* **🤖 Multi-Modal AI Content Synthesis**: Connects to Google Gemini API to dynamically summarize real-time Indian tech industry news and career development hacks into bilingual (English + Telugu), high-converting social copy with zero duplicate topics.
* **🎨 Procedural Vector Graphics Engine**: Custom rendering engine built with Pillow (PIL) generating 1080×1350 px Instagram portrait posts. Features glowing radial background spheres, glassmorphic frosted cards, auto-scaling typography, and dynamic multi-template layouts (Infographic List Cards & Social Thread Screenshots) with zero raster image dependencies.
* **🌐 Resilient Headless Browser Automation**: Leverages Playwright to automate Instagram feed posting, complete with cookie session persistence, aspect ratio conversion (4:5 portrait mode), intelligent selector retries, and modal dismissals.
* **🔄 Decoupled Fault-Tolerant Scheduler**: Independent state tracking for Morning (Tech News) and Evening (Career Hacks) updates with safety intervals (3-hour minimum gap) and Least-Recently-Used (LRU) fallback algorithms to eliminate dropped or skipped posts.
* **⚡ Startup Network Connectivity Poller**: Integrated socket-based connection poller that pauses the bot upon boot if offline and automatically resumes once internet connectivity is detected.
* **📊 Automatic Link-in-Bio Deployment**: Compiles an updated, mobile-responsive HTML5 landing page with article links and analytics tracking, pushing automatically to GitHub Pages on every live post.

---

## 🏗️ Architecture & Workflow

```
[ Google News RSS / Trending Sources ]
                   │
                   ▼
       [ Google Gemini AI Engine ] ──► (Bilingual Content & Caption Synthesis)
                   │
                   ▼
     [ Procedural Graphics Canvas ] ──► (1080x1350 PIL Glassmorphic Image)
                   │
                   ▼
        [ Playwright Automation ] ──► (Uploads 4:5 Portrait Post to Instagram)
                   │
                   ▼
    [ Static Webpage & Git Engine ] ──► (Auto-Commits & Deploys to GitHub Pages)
```

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Generative AI** | Google Gemini API (`google-generativeai` / REST) |
| **Browser Automation** | Microsoft Playwright (Chromium) |
| **Graphic Generation** | Pillow (PIL), NumPy |
| **Web Scraping & Feeds**| `urllib`, `xml.etree.ElementTree`, BeautifulSoup4 |
| **CI/CD & Hosting** | GitHub Pages, Git Automation |
| **Database / State** | JSON Local History Store with LRU Cache |

---

## 📂 Project Structure

```
insta_ai_bot/
├── app.py                  # Main execution engine, scraper, AI generator & scheduler
├── posted_news.json        # Database tracking past titles, timestamps & post metadata
├── index.html              # Auto-generated responsive Link-in-Bio landing page
├── cookies.json            # Encrypted Instagram session cookies for Playwright
├── fonts/                  # Montserrat fonts (Bold, Medium, Regular)
├── .env.example            # Environment variable template
└── README.md               # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/venkatahemanth1074/insta_ai_bot.git
cd insta_ai_bot
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory (based on `.env.example`):
```env
GEMINI_API_KEY=your_gemini_api_key_here
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
```

---

## 🚦 Usage

### Automated Schedule Mode (Default)
Runs an intelligent startup check, validates internet connection, checks the today's completion checklist, and executes missing posts:
```bash
python app.py --mode auto
```

### Manual Mode Override
Force-execute a specific post type immediately (bypasses interval checks):
```bash
# Post Morning Tech News
python app.py --mode morning

# Post Evening Career Hacks
python app.py --mode evening
```

---

## 👨‍💻 Author

* **Venkata Hemanth**
* GitHub: [@venkatahemanth1074](https://github.com/venkatahemanth1074)
* Live Link-in-Bio: [https://venkatahemanth1074.github.io/insta_ai_bot/](https://venkatahemanth1074.github.io/insta_ai_bot/)

---

## 📄 License
This project is licensed under the MIT License.
