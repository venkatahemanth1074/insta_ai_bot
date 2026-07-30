import os
import sys
import json
import socket
import time
import argparse
import datetime
import urllib.request
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# -------------------------------------------------------------
# Configuration and Constants
# -------------------------------------------------------------
FONT_DIR = "./fonts"
BOLD_FONT_PATH = os.path.join(FONT_DIR, "Montserrat-Bold.ttf")
MEDIUM_FONT_PATH = os.path.join(FONT_DIR, "Montserrat-Medium.ttf")
DB_FILE = "posted_news.json"
OUTPUT_IMAGE = "output_post.png"

# Curated Corpus in Vaibhav Sisinty Tanglish style
MORNING_NEWS_CORPUS = [
    {
        "id": "tcs_hiring_2026",
        "title": "TCS CRAZY HIRING UPDATE! 🚀",
        "bullets": [
            "TCS is planning to hire *40,000+ Freshers* this year bhayya! Big opportunity!",
            "Skills focus: Java, Python, and *Cloud tech* fundamentals perfect ga nerchukondi.",
            "Off-campus drives start avtunnai, prepare *strong portfolios* and resume right now.",
            "Normal preparation saripodu, project highlights showcase cheyadame key!"
        ],
        "cta": "Apply Link in Bio! @insta_ai_bot",
        "link": "https://nextstep.tcs.com/",
        "caption_explanation": "Ee post lo TCS massive fresher hiring details, required skills focus, and drives path gurinchi complete description highlights vunnai bhayya."
    },
    {
        "id": "krutrim_telugu_ai",
        "title": "AI IN TELUGU IS REAL! 🤖",
        "bullets": [
            "India's own AI model *Krutrim* launches Telugu language support bhayya!",
            "Ee tool direct ga *regional languages* lo clean codes write/debug chestundi.",
            "Local startup founders & developers ki idi *massive advantage* to build fast.",
            "Tech and language barriers complete break aypotunnai, leverage this tool!"
        ],
        "cta": "Apply Link in Bio! @insta_ai_bot",
        "link": "https://krutrim.com/",
        "caption_explanation": "Ee post lo Krutrim AI tool local language support parameters, startup advantages, and language barrier solutions details vunnai bhayya."
    },
    {
        "id": "isro_free_courses",
        "title": "ISRO FREE COURSES! 🛰️",
        "bullets": [
            "ISRO offering *Free Certified Courses* in Machine Learning & GIS modeling!",
            "No application fees, direct classes from *ISRO Scientists* bhayya.",
            "Any graduate can apply, but seats are *extremely limited* for students.",
            "Resume lo certificate code add cheskunte profile value *next level highlights*!"
        ],
        "cta": "Apply Link in Bio! @insta_ai_bot",
        "link": "https://www.iirs.gov.in/EDUSAT-News",
        "caption_explanation": "Ee post lo ISRO GIS modeling & machine learning free certified courses details, enrollment rules, and resume values clear ga outline chesam."
    },
    {
        "id": "zomato_associate_dev",
        "title": "ZOMATO 12 LPA HIRING! 🍔",
        "bullets": [
            "Zomato starts recruiting *Associate Developers* with packages up to 12 LPA!",
            "Primary requirements: *Golang & React* stack. Real-world projects are priority.",
            "Technical evaluation strictly DSA and *System Design basics* logic tests.",
            "Fast-paced startup environment and extreme growth. Apply right now!"
        ],
        "cta": "Apply Link in Bio! @insta_ai_bot",
        "link": "https://www.zomato.com/careers",
        "caption_explanation": "Ee post lo Zomato Associate Developer hiring details (12 LPA package), DSA evaluation, and Golang/React requirements outline chesam bhayya."
    }
]

EVENING_CAREER_CORPUS = [
    {
        "id": "resume_ats_hack",
        "title": "RESUME SHORTLIST HACK! 📄",
        "bullets": [
            "Resume select avvatleda bhayya? Basic *ATS shortlisting mistakes* chestunnaru.",
            "Include *measurable metrics* e.g., 'Optimized database query speed by 40%'.",
            "Job description keywords carefully research chesi resume lo *highlight* cheyandi.",
            "Response and shortlisting rates guaranteed *double avtayi* in 1 week!"
        ],
        "cta": "Templates & Link in Bio! @insta_ai_bot",
        "link": "https://novoresume.com/",
        "caption_explanation": "Ee post lo resume score increase cheyadaniki metrics addition instructions and ATS filter bypassing keywords usage analysis vundi."
    },
    {
        "id": "cold_email_strategy",
        "title": "COLD EMAIL FOR JOBS! 📧",
        "bullets": [
            "Apply-and-wait matrix nundi bayataki randi. Direct *Cold Emailing* to HRs try cheyandi.",
            "Subject line absolute hook vundali, e.g., 'Free prototype for your home screen'.",
            "Keep the email under *120 words* bhayya. Crisp, value-packed, and precise.",
            "Follow-up scheduling correctly maintain cheyandi. Callbacks pichekkistai!"
        ],
        "cta": "Templates & Link in Bio! @insta_ai_bot",
        "link": "https://hunter.io/",
        "caption_explanation": "Ee post lo HRs ki direct cold emailing templates, length constraints, hooks implementation, and follow-ups guidelines explain chesam."
    },
    {
        "id": "top_skills_2026",
        "title": "TOP 3 HACKS FOR FRESHERS! 🚀",
        "bullets": [
            "Entry-level roles target cheyadaniki basic HTML/CSS standard complete useless.",
            "Focus on *NextJS 15*, *PostgreSQL optimization*, and *AI integrations*.",
            "Building personal SaaS projects is the best *Proof of Work* showing option.",
            "Resume solid design chesthe easy ga *8 LPA+ package* crack cheyochu."
        ],
        "cta": "Roadmap & Link in Bio! @insta_ai_bot",
        "link": "https://roadmap.sh/",
        "caption_explanation": "Ee post lo freshers and software engineers high-package job crack cheyadaniki build cheyalsina key technical skills guide details checklist vundi."
    },
    {
        "id": "technical_rounds_tips",
        "title": "CRACK TECHNICAL ROUNDS! 🧠",
        "bullets": [
            "Technical rounds lo coding syntax kante *Problem Solving capability* evaluate chestaru.",
            "Don't just write code, explain *time & space complexity* step-by-step.",
            "Design principles and *API optimization techniques* detail ga nerchukondi.",
            "Clear representation and structured communication is *must* bhayya!"
        ],
        "cta": "Cheat Sheets & Link in Bio! @insta_ai_bot",
        "link": "https://leetcode.com/",
        "caption_explanation": "Ee post lo technical interview rounds lo time & space complexity, design principles, and problem solving representation tips cover chesam."
    }
]

# -------------------------------------------------------------
# Font Management
# -------------------------------------------------------------
def download_fonts():
    """Downloads Google Fonts programmatically if not present."""
    if not os.path.exists(FONT_DIR):
        os.makedirs(FONT_DIR)
        
    fonts = {
        BOLD_FONT_PATH: "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Bold.ttf",
        MEDIUM_FONT_PATH: "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Medium.ttf"
    }
    
    for path, url in fonts.items():
        if not os.path.exists(path):
            print(f"[*] Font not found. Downloading from {url}...")
            try:
                # Add a user-agent to avoid getting blocked
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                )
                with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"[+] Successfully downloaded font to {path}")
            except Exception as e:
                print(f"[!] Error downloading font: {e}. Fallback fonts will be utilized.")

# -------------------------------------------------------------
# Scraping Tech News (RSS Feed)
# -------------------------------------------------------------
def scrape_trending_tech_news():
    """Fetches real trending Indian tech and startup news headlines from Google News RSS."""
    print("[*] Scraping latest Indian tech news/trends from Google News...")
    feed_url = "https://news.google.com/rss/search?q=Indian+tech+industry+hiring+startup&hl=en-IN&gl=IN&ceid=IN:en"
    headlines = []
    try:
        req = urllib.request.Request(
            feed_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            for item in root.findall('.//item')[:5]:
                title = item.find('title').text
                # Clean up title (remove source suffix like " - Economic Times")
                if " - " in title:
                    title = title.split(" - ")[0]
                headlines.append(title)
        print(f"[+] Scraped {len(headlines)} trending topics successfully.")
        for idx, h in enumerate(headlines, 1):
            print(f"    {idx}. {h}")
    except Exception as e:
        print(f"[!] Warning: News scraping failed ({e}). Proceeding using robust template corpus.")
    return headlines

# -------------------------------------------------------------
# Database History Management
# -------------------------------------------------------------
def normalize_text(text):
    """Lowercases text, removes emojis, punctuation, symbols, and extra spaces for matching."""
    if not text:
        return ""
    import re
    # Lowercase
    text = text.lower()
    # Remove emojis and non-ascii
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove highlight asterisks
    text = text.replace('*', '')
    # Remove all non-alphanumeric characters
    text = re.sub(r'[^a-z0-9]', '', text)
    return text.strip()

def is_duplicate_content(new_item, history_db):
    """Checks if the new item title or any of its bullets matches already posted items."""
    if not new_item or not history_db:
        return False
        
    posted_items = history_db.get("posted_items", [])
    
    # 1. Clean and check the new title
    new_title_clean = normalize_text(new_item.get("title", ""))
    if not new_title_clean:
        return False
        
    for past_item in posted_items:
        past_title_clean = normalize_text(past_item.get("title", ""))
        if new_title_clean == past_title_clean:
            print(f"[!] Duplicate detected by Title: '{new_item.get('title')}' matches past title '{past_item.get('title')}'")
            return True
            
    # 2. Clean and check the new bullets
    new_bullets_clean = [normalize_text(b) for b in new_item.get("bullets", []) if normalize_text(b)]
    
    for past_item in posted_items:
        past_bullets_clean = [normalize_text(b) for b in past_item.get("bullets", []) if normalize_text(b)]
        for new_b in new_bullets_clean:
            # Skip very short generic sentences
            if len(new_b) < 10:
                continue
            if new_b in past_bullets_clean:
                print(f"[!] Duplicate detected by Bullet Content: '{new_b}' has been used in a previous post!")
                return True
                
    return False

def load_db():
    default_db = {
        "morning_news_history": [],
        "evening_career_history": [],
        "last_post_time": None,
        "last_morning_post_date": None,
        "last_evening_post_date": None,
        "posted_items": [],
        "posted_titles": []
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for k, v in default_db.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            print("[!] Error reading database file. Reinitializing...")
    return default_db

def save_db(db):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        print(f"[!] Error saving database file: {e}")

def generate_link_in_bio_html(db):
    """Generates a beautiful, responsive Link-in-Bio index.html page based on posted history."""
    print("[*] Generating updated Link-in-Bio webpage (index.html)...")
    try:
        items = db.get("posted_items", [])
        # Filter items that actually have links and titles
        valid_items = [item for item in items if item.get("title") and item.get("link")]
        
        # Sort by date/timestamp descending (newest first)
        valid_items.sort(key=lambda x: x.get("date", ""), reverse=True)

        # Build cards HTML
        cards_html = []
        for item in valid_items:
            title = item["title"]
            # Clean emojis and highlights from the display title
            clean_title = clean_text_for_font(title).replace('*', '')
            link = item["link"]
            date_str = item.get("date", "")
            # Format date for display (e.g. YYYY-MM-DD)
            display_date = date_str.split(" ")[0] if date_str else ""
            mode = item.get("mode", "morning")
            
            # Badge setup
            if mode == "morning":
                badge_class = "badge-tech"
                badge_text = "Tech News"
            else:
                badge_class = "badge-career"
                badge_text = "Career Advice"
                
            card = f"""
            <a href="{link}" target="_blank" class="card-link">
                <div class="card-content">
                    <div class="card-header-row">
                        <span class="badge {badge_class}">{badge_text}</span>
                        <span class="card-date">{display_date}</span>
                    </div>
                    <h2 class="card-title">{clean_title}</h2>
                    <div class="card-action">
                        <span>Open Resource</span>
                        <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" class="arrow-icon"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                    </div>
                </div>
            </a>
            """
            cards_html.append(card)

        # Join cards
        all_cards_str = "\n".join(cards_html) if cards_html else '<p class="no-links">No links available yet. Stay tuned!</p>'

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>insta_ai_bot | Recommended Links</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'Outfit', sans-serif;
            background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #2e082e 100%);
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
        }}
        .container {{
            width: 100%;
            max-width: 580px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        /* Header Profile */
        .profile {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .avatar {{
            width: 96px;
            height: 96px;
            border-radius: 50%;
            background: linear-gradient(45deg, #00e5ff, #ff007f);
            margin: 0 auto 16px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.2rem;
            font-weight: 800;
            color: #0b132b;
            box-shadow: 0 8px 24px rgba(0, 229, 255, 0.3);
            border: 3px solid rgba(255, 255, 255, 0.1);
        }}
        .handle {{
            font-size: 1.4rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}
        .bio {{
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.7);
            max-width: 320px;
            line-height: 1.4;
        }}
        /* Links List */
        .links-list {{
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .card-link {{
            text-decoration: none;
            color: inherit;
            display: block;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 22px 24px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
        }}
        .card-link::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, rgba(0, 229, 255, 0.08), rgba(255, 0, 127, 0.08));
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        .card-link:hover {{
            transform: translateY(-4px);
            border-color: rgba(255, 255, 255, 0.18);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 229, 255, 0.1);
        }}
        .card-link:hover::before {{
            opacity: 1;
        }}
        .card-content {{
            position: relative;
            z-index: 1;
        }}
        .card-header-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        /* Badges */
        .badge {{
            font-size: 0.75rem;
            font-weight: 700;
            padding: 5px 12px;
            border-radius: 30px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge-tech {{
            background: rgba(0, 229, 255, 0.12);
            color: #00e5ff;
            border: 1px solid rgba(0, 229, 255, 0.25);
        }}
        .badge-career {{
            background: rgba(255, 0, 127, 0.12);
            color: #ff007f;
            border: 1px solid rgba(255, 0, 127, 0.25);
        }}
        .card-date {{
            font-size: 0.85rem;
            color: rgba(255, 255, 255, 0.5);
            font-weight: 600;
        }}
        .card-title {{
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.4;
            color: #ffffff;
            margin-bottom: 14px;
        }}
        .card-action {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.88rem;
            font-weight: 700;
            color: rgba(255, 255, 255, 0.85);
            transition: color 0.2s ease;
        }}
        .card-link:hover .card-action {{
            color: #00e5ff;
        }}
        .arrow-icon {{
            transition: transform 0.3s ease;
        }}
        .card-link:hover .arrow-icon {{
            transform: translateX(4px);
        }}
        .no-links {{
            text-align: center;
            color: rgba(255, 255, 255, 0.5);
            padding: 40px;
            font-style: italic;
        }}
        /* Footer */
        footer {{
            margin-top: 60px;
            text-align: center;
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.4);
            letter-spacing: 0.5px;
        }}
        footer a {{
            color: rgba(255, 255, 255, 0.6);
            text-decoration: none;
            transition: color 0.2s ease;
        }}
        footer a:hover {{
            color: #00e5ff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Profile info -->
        <div class="profile">
            <div class="avatar">🤖</div>
            <h1 class="handle">@insta_ai_bot</h1>
            <p class="bio">Daily Indian Tech Updates & Career Hacks perfect ga. Follow @insta_ai_bot for job notifications!</p>
        </div>

        <!-- Links List -->
        <div class="links-list">
            {all_cards_str}
        </div>

        <!-- Footer -->
        <footer>
            <p>© {datetime.datetime.now().year} <a href="https://instagram.com/insta_ai_bot" target="_blank">@insta_ai_bot</a>. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>"""
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("[+] Link-in-Bio index.html generated successfully!")
        return True
    except Exception as e:
        print(f"[!] Error generating Link-in-Bio HTML: {e}")
        return False

def push_to_git():
    """Attempts to add, commit, and push index.html and posted_news.json to Git remote repository.
    Fails silently (without raising exceptions) if Git is not configured or fails.
    """
    print("[*] Attempting to push updates to GitHub...")
    import subprocess
    try:
        # Check if git is available and if it is initialized
        if not os.path.exists(".git"):
            print("[*] Skipping Git push: Not a Git repository (no .git folder).")
            return False
            
        # Add files
        subprocess.run(["git", "add", "index.html", "posted_news.json"], capture_output=True, check=True)
        
        # Check if there are changes to commit
        status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status_res.stdout.strip():
            print("[*] Skipping Git push: No changes to commit.")
            return True
            
        subprocess.run(["git", "commit", "-m", "Auto-update Link-in-Bio index.html and database"], capture_output=True, check=True)
        
        # Push to remote branch
        push_res = subprocess.run(["git", "push"], capture_output=True, text=True)
        if push_res.returncode == 0:
            print("[+] Successfully pushed updates to GitHub Pages!")
            return True
        else:
            print(f"[!] Warning: Git push failed: {push_res.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[!] Warning: Git automation failed: {e}")
        return False

# -------------------------------------------------------------
# Gemini AI Post Generation
# -------------------------------------------------------------
def generate_content_with_gemini(mode, scraped_news=None, history_db=None):
    """Calls Gemini API to dynamically generate a post in Tanglish format."""
    load_env()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[*] No GEMINI_API_KEY found in environment variables. Skipping AI generation.")
        return None

    # Compile a blacklist of already posted titles and bullets to prevent repetition
    posted_titles = []
    posted_bullets = []
    if history_db:
        for item in history_db.get("posted_items", []):
            if "title" in item:
                posted_titles.append(item["title"])
            if "bullets" in item:
                posted_bullets.extend(item["bullets"])

    blacklist_instructions = ""
    if posted_titles or posted_bullets:
        blacklist_instructions = "\nCRITICAL: Do NOT generate a post that has a title similar to, or contains bullet points/career tips similar to, the following already posted content:\n"
        if posted_titles:
            blacklist_instructions += "Previously Posted Titles:\n"
            for t in posted_titles[-30:]: # send up to last 30 titles
                blacklist_instructions += f"- {t}\n"
        if posted_bullets:
            blacklist_instructions += "Previously Posted Career/News Tips:\n"
            for b in posted_bullets[-50:]: # send up to last 50 bullets
                blacklist_instructions += f"- {b}\n"
        blacklist_instructions += "Please ensure the generated content is 100% unique, fresh, and different from the above lists."

    print(f"[*] Calling Gemini API to generate a new '{mode}' post dynamically...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    if mode == "morning":
        news_str = "\n".join([f"- {h}" for h in (scraped_news or [])])
        prompt = (
            "You are an expert Instagram content creator. Generate a viral tech news post based on these trending headlines:\n"
            f"{news_str}\n\n"
            f"{blacklist_instructions}\n\n"
            "Format the output strictly as a JSON object matching this schema:\n"
            "{\n"
            "  \"title\": \"A high-energy hook title (max 30 characters, capitalized, DO NOT use emojis as the font doesn't support them)\",\n"
            "  \"bullets\": [\n"
            "    \"4 bullet points. Style: Use high-energy, fun, professional 'Tanglish' (Telugu mixed with English) speaking tone. Write Telugu words using the English/Latin alphabet only (e.g. write 'bhayya', 'perfect ga', 'next level', 'pichekkistai'). NEVER use the native Telugu alphabet/script, and DO NOT use emojis in bullets. Format: Surround key words or metrics in asterisks like *this* to highlight them (e.g. '*40,000+ Freshers*'). Keep each bullet under 100 characters.\"\n"
            "  ],\n"
            "  \"cta\": \"A clean Call to Action pointing to the bio (e.g., 'Apply Link in Bio! @insta_ai_bot'), DO NOT use emojis\",\n"
            "  \"link\": \"A real, active link/URL related to the news topic where users can read more or apply.\",\n"
            "  \"caption_explanation\": \"A short, engaging explanation (1-2 sentences in Tanglish) of what this post is about and what type of content the post consists of, to be used in the Instagram caption. Tell the reader what they will find in the post image. DO NOT repeat the bullet points verbatim.\"\n"
            "}"
        )
    else:
        prompt = (
            "You are an expert career coach. Generate a viral career advice, resume hack, or interview tips post.\n"
            "Target interesting topics like resume shortlisting, ATS hacks, cold emailing, fresher job tips, or interview preparation.\n\n"
            f"{blacklist_instructions}\n\n"
            "Format the output strictly as a JSON object matching this schema:\n"
            "{\n"
            "  \"title\": \"A high-energy hook title (max 30 characters, capitalized, DO NOT use emojis as the font doesn't support them)\",\n"
            "  \"bullets\": [\n"
            "    \"4 bullet points. Style: Use high-energy, fun, professional 'Tanglish' (Telugu mixed with English) speaking tone. Write Telugu words using the English/Latin alphabet only (e.g. write 'bhayya', 'perfect ga', 'next level', 'pichekkistai'). NEVER use the native Telugu alphabet/script, and DO NOT use emojis in bullets. Format: Surround key words or metrics in asterisks like *this* to highlight them (e.g. '*double avtayi*'). Keep each bullet under 100 characters.\"\n"
            "  ],\n"
            "  \"cta\": \"A clean Call to Action pointing to the bio (e.g., 'Templates & Link in Bio! @insta_ai_bot' or 'Roadmap & Link in Bio! @insta_ai_bot'), DO NOT use emojis\",\n"
            "  \"link\": \"A real, active link/URL related to the career topic where users can get resources, templates, or roadmaps.\",\n"
            "  \"caption_explanation\": \"A short, engaging explanation (1-2 sentences in Tanglish) of what this post is about and what type of content the post consists of, to be used in the Instagram caption. Tell the reader what they will find in the post image. DO NOT repeat the bullet points verbatim.\"\n"
            "}"
        )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING"},
                    "bullets": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    },
                    "cta": {"type": "STRING"},
                    "link": {"type": "STRING"},
                    "caption_explanation": {"type": "STRING"}
                },
                "required": ["title", "bullets", "cta", "caption_explanation"]
            }
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            
        candidate = res_data.get("candidates", [{}])[0]
        text_content = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
        
        post_data = json.loads(text_content)
        if "title" in post_data and "bullets" in post_data and "cta" in post_data and "caption_explanation" in post_data:
            bullets = post_data["bullets"]
            if len(bullets) < 4:
                bullets += ["Follow our account for more daily hacks! 🚀"] * (4 - len(bullets))
            post_data["bullets"] = bullets[:4]
            post_data["id"] = "ai_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            print("[+] Successfully generated custom post content via Gemini!")
            return post_data
    except Exception as e:
        print(f"[!] Warning: Gemini AI generation failed: {e}. Falling back to standard corpus.")
    return None

# ---------------------------------------------------------------------------------------------
# Text Wrapping and Styling Logic for Pillow
# -------------------------------------------------------------
def wrap_text(text, font, max_width, draw):
    """Wraps text word-by-word while preserving highlighting tags (*text*)."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line_words = current_line + [word]
        # Clean highlight asterisks for correct width estimation
        clean_line = " ".join(test_line_words).replace('*', '')
        
        # Get line width
        if hasattr(draw, 'textbbox'):
            w = draw.textbbox((0, 0), clean_line, font=font)[2]
        else:
            w = draw.textsize(clean_line, font=font)[0]
            
        if w <= max_width:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_styled_line(draw, x, y, line_text, font, default_color, highlight_color):
    """Draws a single line of text with custom highlighted terms in asterisks."""
    parts = line_text.split('*')
    cursor_x = x
    
    for i, part in enumerate(parts):
        # Even parts are standard text, odd parts are highlighted
        color = highlight_color if (i % 2 == 1) else default_color
        draw.text((cursor_x, y), part, font=font, fill=color)
        
        # Advance cursor by the width of this segment
        if hasattr(draw, 'textbbox'):
            w = draw.textbbox((0, 0), part, font=font)[2]
        else:
            w = draw.textsize(part, font=font)[0]
        cursor_x += w

# -------------------------------------------------------------
# Image Generation Engine
# -------------------------------------------------------------
def clean_text_for_font(text):
    """Strips emojis and native Telugu script to avoid rendering empty boxes on the image."""
    if not text:
        return ""
    cleaned = []
    for c in text:
        o = ord(c)
        # Skip emoji ranges: 2600-27BF, 1F300-1F9FF, 1FA00-1FFFF
        # Skip native Telugu characters: 0C00-0C7F
        # Skip characters above 0xFFFF
        if (0x2600 <= o <= 0x27BF) or (0x1F300 <= o <= 0x1F9FF) or (0x1FA00 <= o <= 0x1FFFF) or (0x0C00 <= o <= 0x0C7F) or (o > 0xFFFF):
            continue
        cleaned.append(c)
    return "".join(cleaned).strip()

# -------------------------------------------------------------
# Image Generation Engine
# -------------------------------------------------------------
def draw_glow_blob(img, cx, cy, radius, color, max_alpha):
    """Draws a soft glowing radial blob on the image."""
    width, height = img.size
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    
    steps = 40
    for i in range(steps):
        r = int(radius * (steps - i) / steps)
        alpha = int(max_alpha * (i / steps) ** 3)
        odraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (alpha,))
        
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def generate_post(mode, item):
    """Dynamically draws a premium social media post using text & vector card styling."""
    width, height = 1080, 1350
    
    # 1. Base Gradient Background (sleek very dark base)
    gradient = Image.new('RGB', (1, height))
    if mode == "morning":
        r1, g1, b1 = 8, 12, 28
        r2, g2, b2 = 14, 18, 38
        accent_color = (0, 229, 255)       # Neon Cyan
        highlight_color = (255, 234, 0)     # Neon Yellow
        badge_text = "TELUGU TECH NEWS"
        
        # Glow blob setup: Neon blue, Indigo & Cyan glows
        glows = [
            {"cx": 150, "cy": 150, "radius": 450, "color": (0, 191, 255), "max_alpha": 45},
            {"cx": 900, "cy": 700, "radius": 500, "color": (138, 43, 226), "max_alpha": 40},
            {"cx": 400, "cy": 1200, "radius": 400, "color": (0, 255, 255), "max_alpha": 35}
        ]
    else:
        r1, g1, b1 = 20, 14, 20
        r2, g2, b2 = 30, 18, 32
        accent_color = (255, 0, 127)       # Neon Pink
        highlight_color = (0, 243, 255)     # Neon Cyan
        badge_text = "CAREER HACKS"
        
        # Glow blob setup: Violet, pink & indigo glows
        glows = [
            {"cx": 930, "cy": 200, "radius": 450, "color": (255, 20, 147), "max_alpha": 45},
            {"cx": 150, "cy": 800, "radius": 500, "color": (148, 0, 211), "max_alpha": 40},
            {"cx": 700, "cy": 1250, "radius": 400, "color": (75, 0, 130), "max_alpha": 35}
        ]
        
    for y in range(height):
        r = int(r1 + (r2 - r1) * (y / height))
        g = int(g1 + (g2 - g1) * (y / height))
        b = int(b1 + (b2 - b1) * (y / height))
        gradient.putpixel((0, y), (r, g, b))
        
    img = gradient.resize((width, height))
    
    # Draw background glowing blobs dynamically!
    for blob in glows:
        img = draw_glow_blob(img, blob["cx"], blob["cy"], blob["radius"], blob["color"], blob["max_alpha"])
        
    draw = ImageDraw.Draw(img)
    
    # 2. Font Initialization
    try:
        font_badge = ImageFont.truetype(BOLD_FONT_PATH, 30)
        font_cta = ImageFont.truetype(BOLD_FONT_PATH, 36)
        font_footer = ImageFont.truetype(MEDIUM_FONT_PATH, 28)
        font_bullet_num = ImageFont.truetype(BOLD_FONT_PATH, 24)
        font_sub = ImageFont.truetype(MEDIUM_FONT_PATH, 22)
    except Exception:
        print("[!] Using default standard font since custom fonts are not accessible.")
        font_badge = font_cta = font_footer = font_bullet_num = font_sub = ImageFont.load_default()
        
    # Select layout variety dynamically based on item ID hash
    layout_style = hash(item.get("id", "default")) % 2
    
    # 3. Draw Main Glassmorphic Card Background & Border
    card_x1, card_y1 = 70, 180
    card_w, card_h = 940, 990
    card_x2, card_y2 = card_x1 + card_w, card_y1 + card_h
    
    glass_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glass_layer)
    gdraw.rounded_rectangle(
        [card_x1, card_y1, card_x2, card_y2],
        radius=35,
        fill=(15, 17, 26, 140)
    )
    gdraw.rounded_rectangle(
        [card_x1, card_y1, card_x2, card_y2],
        radius=35,
        outline=(255, 255, 255, 25),
        width=2
    )
    img = Image.alpha_composite(img.convert('RGBA'), glass_layer).convert('RGB')
    draw = ImageDraw.Draw(img)

    # 4. Render Layouts
    if layout_style == 0:
        # ==========================================
        # Layout 0: Infographic List Card
        # ==========================================
        
        # Draw Header Badge Box (above card)
        badge_w = 420
        badge_h = 60
        badge_x1 = (width - badge_w) // 2
        badge_y1 = 85
        badge_x2, badge_y2 = badge_x1 + badge_w, badge_y1 + badge_h
        
        glow_badge = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        gbdraw = ImageDraw.Draw(glow_badge)
        gbdraw.rounded_rectangle(
            [badge_x1 - 3, badge_y1 - 3, badge_x2 + 3, badge_y2 + 3],
            radius=30,
            fill=accent_color + (60,)
        )
        img = Image.alpha_composite(img.convert('RGBA'), glow_badge).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        draw.rounded_rectangle(
            [badge_x1, badge_y1, badge_x2, badge_y2],
            radius=30,
            fill=(10, 12, 18)
        )
        
        if hasattr(draw, 'textbbox'):
            tw = draw.textbbox((0, 0), badge_text, font=font_badge)[2]
            th = draw.textbbox((0, 0), badge_text, font=font_badge)[3]
        else:
            tw, th = draw.textsize(badge_text, font=font_badge)
        draw.text((badge_x1 + (badge_w - tw)//2, badge_y1 + (badge_h - th)//2 - 2), badge_text, font=font_badge, fill=accent_color)
        
        # Headline Title
        title_text = clean_text_for_font(item["title"])
        title_x = 120
        title_y = 235
        max_title_width = width - (title_x * 2)
        
        for t_size in [56, 48, 42]:
            try:
                font_title = ImageFont.truetype(BOLD_FONT_PATH, t_size)
            except Exception:
                font_title = ImageFont.load_default()
            title_line_height = t_size + 10
            wrapped_titles = wrap_text(title_text, font_title, max_title_width, draw)
            if len(wrapped_titles) <= 2:
                break
                
        current_title_y = title_y
        for line in wrapped_titles:
            draw.text((title_x, current_title_y), line, font=font_title, fill=(255, 255, 255))
            current_title_y += title_line_height
            
        # Divider Line
        divider_y = current_title_y + 15
        div_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        ddraw = ImageDraw.Draw(div_layer)
        ddraw.line([(title_x, divider_y), (width - title_x, divider_y)], fill=(255, 255, 255, 35), width=2)
        img = Image.alpha_composite(img.convert('RGBA'), div_layer).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Bullets
        bullets_start_y = divider_y + 35
        available_height = 1000 - bullets_start_y
        
        selected_medium_size = 34
        selected_line_spacing = 44
        selected_bullet_gap = 25
        
        for m_size in [34, 30, 26, 24]:
            try:
                font_medium = ImageFont.truetype(MEDIUM_FONT_PATH, m_size)
            except Exception:
                font_medium = ImageFont.load_default()
                
            line_spacing = m_size + 10
            bullet_gap = m_size - 6
            
            total_height = 0
            text_x = title_x + 85
            max_wrap_width = width - text_x - 120
            
            for i, bullet in enumerate(item["bullets"]):
                cleaned_bullet = clean_text_for_font(bullet)
                wrapped_lines = wrap_text(cleaned_bullet, font_medium, max_wrap_width, draw)
                total_height += len(wrapped_lines) * line_spacing
                if i < len(item["bullets"]) - 1:
                    total_height += bullet_gap
                    
            if total_height <= available_height:
                selected_medium_size = m_size
                selected_line_spacing = line_spacing
                selected_bullet_gap = bullet_gap
                break
        else:
            selected_medium_size = 24
            selected_line_spacing = 34
            selected_bullet_gap = 14
            try:
                font_medium = ImageFont.truetype(MEDIUM_FONT_PATH, 24)
            except Exception:
                font_medium = ImageFont.load_default()
                
        print(f"[*] Premium layout 0 scaling: title_size={t_size}, bullet_size={selected_medium_size}, bullets_height={total_height}/{available_height}")
        
        bullets_y = bullets_start_y
        text_x = title_x + 85
        max_wrap_width = width - text_x - 120
        
        for idx, bullet in enumerate(item["bullets"]):
            cleaned_bullet = clean_text_for_font(bullet)
            
            # Draw Pill Badge
            pill_w, pill_h = 60, 48
            pill_x = title_x
            pill_y = bullets_y - 2
            
            glow_pill = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            gpdraw = ImageDraw.Draw(glow_pill)
            gpdraw.rounded_rectangle(
                [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
                radius=12,
                outline=accent_color + (70,),
                width=2
            )
            gpdraw.rounded_rectangle(
                [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
                radius=12,
                fill=(10, 12, 18, 160)
            )
            img = Image.alpha_composite(img.convert('RGBA'), glow_pill).convert('RGB')
            draw = ImageDraw.Draw(img)
            
            num_str = f"0{idx + 1}"
            if hasattr(draw, 'textbbox'):
                nw = draw.textbbox((0, 0), num_str, font=font_bullet_num)[2]
                nh = draw.textbbox((0, 0), num_str, font=font_bullet_num)[3]
            else:
                nw, nh = draw.textsize(num_str, font=font_bullet_num)
            draw.text(
                (pill_x + (pill_w - nw)//2, pill_y + (pill_h - nh)//2 - 1),
                num_str,
                font=font_bullet_num,
                fill=accent_color
            )
            
            # Draw wrapped lines
            wrapped_lines = wrap_text(cleaned_bullet, font_medium, max_wrap_width, draw)
            current_y = bullets_y
            for line in wrapped_lines:
                draw_styled_line(draw, text_x, current_y, line, font_medium, (255, 255, 255), highlight_color)
                current_y += selected_line_spacing
                
            bullet_height = max(pill_h, current_y - bullets_y)
            bullets_y += bullet_height + selected_bullet_gap
            
    else:
        # ==========================================
        # Layout 1: Organic Social Thread Screenshot
        # ==========================================
        
        # Profile header inside card
        header_y = 225
        avatar_cx = 160
        avatar_cy = header_y + 30
        avatar_r = 30
        
        # Solid colored vector badge for profile avatar (No photos/images!)
        glow_avatar = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        gawdraw = ImageDraw.Draw(glow_avatar)
        gawdraw.ellipse([avatar_cx - avatar_r, avatar_cy - avatar_r, avatar_cx + avatar_r, avatar_cy + avatar_r], fill=accent_color + (140,))
        gawdraw.ellipse([avatar_cx - avatar_r + 4, avatar_cy - avatar_r + 4, avatar_cx + avatar_r - 4, avatar_cy + avatar_r - 4], fill=(10, 12, 18, 255))
        img = Image.alpha_composite(img.convert('RGBA'), glow_avatar).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Draw a bold letter 'A' inside avatar circle for a neat look
        avatar_txt = "A"
        if hasattr(draw, 'textbbox'):
            aw = draw.textbbox((0, 0), avatar_txt, font=font_bullet_num)[2]
            ah = draw.textbbox((0, 0), avatar_txt, font=font_bullet_num)[3]
        else:
            aw, ah = draw.textsize(avatar_txt, font=font_bullet_num)
        draw.text((avatar_cx - aw//2, avatar_cy - ah//2 - 2), avatar_txt, font=font_bullet_num, fill=accent_color)
        
        # Profile Names
        prof_name = "@insta_ai_bot"
        prof_sub = "Daily Tech & Career Guide"
        draw.text((avatar_cx + 45, header_y + 4), prof_name, font=font_badge, fill=(255, 255, 255))
        draw.text((avatar_cx + 45, header_y + 34), prof_sub, font=font_sub, fill=(160, 170, 190))
        
        # Headline Title
        title_text = clean_text_for_font(item["title"])
        title_x = 130
        title_y = header_y + 95
        max_title_width = width - (title_x * 2)
        
        for t_size in [48, 42, 38]:
            try:
                font_title = ImageFont.truetype(BOLD_FONT_PATH, t_size)
            except Exception:
                font_title = ImageFont.load_default()
            title_line_height = t_size + 10
            wrapped_titles = wrap_text(title_text, font_title, max_title_width, draw)
            if len(wrapped_titles) <= 2:
                break
                
        current_title_y = title_y
        for line in wrapped_titles:
            draw.text((title_x, current_title_y), line, font=font_title, fill=highlight_color)
            current_title_y += title_line_height
            
        # Divider Line
        divider_y = current_title_y + 15
        div_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        ddraw = ImageDraw.Draw(div_layer)
        ddraw.line([(title_x, divider_y), (width - title_x, divider_y)], fill=(255, 255, 255, 30), width=1)
        img = Image.alpha_composite(img.convert('RGBA'), div_layer).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Bullets
        bullets_start_y = divider_y + 35
        available_height = 1000 - bullets_start_y
        
        selected_medium_size = 32
        selected_line_spacing = 42
        selected_bullet_gap = 25
        
        for m_size in [32, 28, 26, 24]:
            try:
                font_medium = ImageFont.truetype(MEDIUM_FONT_PATH, m_size)
            except Exception:
                font_medium = ImageFont.load_default()
                
            line_spacing = m_size + 10
            bullet_gap = m_size - 4
            
            total_height = 0
            text_x = title_x + 65
            max_wrap_width = width - text_x - 120
            
            for i, bullet in enumerate(item["bullets"]):
                cleaned_bullet = clean_text_for_font(bullet)
                wrapped_lines = wrap_text(cleaned_bullet, font_medium, max_wrap_width, draw)
                total_height += len(wrapped_lines) * line_spacing
                if i < len(item["bullets"]) - 1:
                    total_height += bullet_gap
                    
            if total_height <= available_height:
                selected_medium_size = m_size
                selected_line_spacing = line_spacing
                selected_bullet_gap = bullet_gap
                break
        else:
            selected_medium_size = 24
            selected_line_spacing = 34
            selected_bullet_gap = 14
            try:
                font_medium = ImageFont.truetype(MEDIUM_FONT_PATH, 24)
            except Exception:
                font_medium = ImageFont.load_default()
                
        print(f"[*] Premium layout 1 scaling: title_size={t_size}, bullet_size={selected_medium_size}, bullets_height={total_height}/{available_height}")
        
        # Draw Thread Line on left
        dot_positions = []
        bullets_y = bullets_start_y
        text_x = title_x + 65
        max_wrap_width = width - text_x - 120
        
        # Pre-calculate dot positions to draw thread line cleanly
        temp_y = bullets_y
        for idx, bullet in enumerate(item["bullets"]):
            cleaned_bullet = clean_text_for_font(bullet)
            dot_positions.append(temp_y + selected_medium_size // 2 - 1)
            
            wrapped_lines = wrap_text(cleaned_bullet, font_medium, max_wrap_width, draw)
            bullet_height = len(wrapped_lines) * selected_line_spacing
            temp_y += bullet_height + selected_bullet_gap
            
        # Draw thread connecting line
        thread_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        tldraw = ImageDraw.Draw(thread_layer)
        tldraw.line([(title_x, dot_positions[0]), (title_x, dot_positions[-1])], fill=accent_color + (80,), width=3)
        img = Image.alpha_composite(img.convert('RGBA'), thread_layer).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Draw bullets with glowing thread dots
        bullets_y = bullets_start_y
        for idx, bullet in enumerate(item["bullets"]):
            cleaned_bullet = clean_text_for_font(bullet)
            dot_y = dot_positions[idx]
            
            # Glowing dot on thread line
            dot_r = 7
            glow_dot = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            gdowdraw = ImageDraw.Draw(glow_dot)
            gdowdraw.ellipse([title_x - dot_r - 2, dot_y - dot_r - 2, title_x + dot_r + 2, dot_y + dot_r + 2], fill=accent_color + (100,))
            gdowdraw.ellipse([title_x - dot_r + 1, dot_y - dot_r + 1, title_x + dot_r - 1, dot_y + dot_r - 1], fill=(255, 255, 255, 255))
            img = Image.alpha_composite(img.convert('RGBA'), glow_dot).convert('RGB')
            draw = ImageDraw.Draw(img)
            
            # Draw bullet text lines
            wrapped_lines = wrap_text(cleaned_bullet, font_medium, max_wrap_width, draw)
            current_y = bullets_y
            for line in wrapped_lines:
                draw_styled_line(draw, text_x, current_y, line, font_medium, (255, 255, 255), highlight_color)
                current_y += selected_line_spacing
                
            bullet_height = current_y - bullets_y
            bullets_y += bullet_height + selected_bullet_gap

    # ==========================================
    # Draw Shared CTA and Footer Elements
    # ==========================================
    
    # 8. Draw Call to Action (CTA) Box at bottom (inside card)
    cta_w = 860
    cta_h = 100
    cta_x1 = (width - cta_w) // 2
    cta_y1 = 1040
    cta_x2, cta_y2 = cta_x1 + cta_w, cta_y1 + cta_h
    
    glow_cta = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    gctadraw = ImageDraw.Draw(glow_cta)
    gctadraw.rounded_rectangle(
        [cta_x1 - 3, cta_y1 - 3, cta_x2 + 3, cta_y2 + 3],
        radius=16,
        outline=accent_color + (100,),
        width=3
    )
    gctadraw.rounded_rectangle(
        [cta_x1, cta_y1, cta_x2, cta_y2],
        radius=16,
        fill=(10, 12, 18, 200)
    )
    img = Image.alpha_composite(img.convert('RGBA'), glow_cta).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    cta_text = clean_text_for_font(item["cta"])
    if hasattr(draw, 'textbbox'):
        ctw = draw.textbbox((0, 0), cta_text, font=font_cta)[2]
        cth = draw.textbbox((0, 0), cta_text, font=font_cta)[3]
    else:
        ctw, cth = draw.textsize(cta_text, font=font_cta)
    
    draw.text(
        (cta_x1 + (cta_w - ctw)//2, cta_y1 + (cta_h - cth)//2 - 2), 
        cta_text, 
        font=font_cta, 
        fill=highlight_color
    )

    # 9. Draw Footer Profile Username Pill (below card)
    footer_text = "@insta_ai_bot"
    footer_w = 300
    footer_h = 52
    footer_x1 = (width - footer_w) // 2
    footer_y1 = 1240
    footer_x2, footer_y2 = footer_x1 + footer_w, footer_y1 + footer_h
    
    draw.rounded_rectangle(
        [footer_x1, footer_y1, footer_x2, footer_y2],
        radius=26,
        fill=(15, 17, 26),
        outline=(255, 255, 255, 25),
        width=1
    )
    
    if hasattr(draw, 'textbbox'):
        fw = draw.textbbox((0, 0), footer_text, font=font_footer)[2]
        fh = draw.textbbox((0, 0), footer_text, font=font_footer)[3]
    else:
        fw, fh = draw.textsize(footer_text, font=font_footer)
        
    draw.text(
        (footer_x1 + (footer_w - fw)//2, footer_y1 + (footer_h - fh)//2 - 2), 
        footer_text, 
        font=font_footer, 
        fill=(255, 255, 255, 220)
    )
    
    # Save the generated post image
    img.save(OUTPUT_IMAGE, "PNG")
    print(f"[+] Output post image saved successfully as: '{OUTPUT_IMAGE}'")

# -------------------------------------------------------------
# Instagram Upload and Env Integration
# -------------------------------------------------------------
def load_env():
    """Manually parses a local .env file (or .env.example as fallback) to set OS environment variables securely."""
    env_file = ".env"
    if not os.path.exists(env_file) and os.path.exists(".env.example"):
        env_file = ".env.example"
        print("[*] .env file not found. Falling back to loading from .env.example.")
        
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip("'").strip('"')
                    os.environ[key.strip()] = val
        print(f"[+] Loaded environment variables from {env_file} file.")

def upload_to_instagram(image_path, caption):
    """Posts the generated image and caption live to Instagram using Playwright browser automation."""
    load_env()
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    
    if not username or not password or username == "your_username_here":
        print("[*] No custom Instagram credentials found in env. Skipping live upload.")
        return False
        
    print("[*] Attempting to publish live post to Instagram via Playwright...")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[*] 'playwright' module not found. Installing dynamically...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
            from playwright.sync_api import sync_playwright
            print("[+] Successfully installed 'playwright' and chromium browser.")
        except Exception as e:
            print(f"[!] Failed to auto-install 'playwright': {e}. Cannot upload automatically.")
            return False

    # Determine headless mode (default to headed/False to bypass Instagram bot detection, but can be set to True)
    headless_env = os.getenv("PLAYWRIGHT_HEADLESS", "False")
    is_headless = headless_env.lower() in ("true", "1", "yes")
    print(f"[*] Launching Chromium browser (headless={is_headless})...")

    try:
        with sync_playwright() as p:
            # Launch browser with maximized window argument for headed runs
            launch_args = ["--start-maximized"] if not is_headless else []
            browser = p.chromium.launch(headless=is_headless, args=launch_args)
            
            # Configure context with custom User-Agent
            user_agent = os.getenv("INSTAGRAM_USER_AGENT")
            if not user_agent:
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            
            # Setup context arguments: use no_viewport for headed runs so it fills the screen
            context_args = {
                "user_agent": user_agent
            }
            if not is_headless:
                context_args["no_viewport"] = True
            else:
                context_args["viewport"] = {"width": 1920, "height": 1080}
                
            context = browser.new_context(**context_args)
            
            # Stealth: Bypass navigator.webdriver detection for headless runs
            context.add_init_script("delete navigator.__proto__.webdriver")
            
            # Try to load cookies from cookies.json or cookies.json.txt or cookies.bak
            cookies_file = "cookies.json"
            if not os.path.exists(cookies_file):
                if os.path.exists("cookies.json.txt"):
                    cookies_file = "cookies.json.txt"
                elif os.path.exists("cookies.bak"):
                    cookies_file = "cookies.bak"
            
            if os.path.exists(cookies_file):
                print(f"[*] Injecting browser cookies from '{cookies_file}'...")
                try:
                    with open(cookies_file, "r") as f:
                        cookies_data = json.load(f)
                    
                    playwright_cookies = []
                    for c in cookies_data:
                        domain = c.get("domain", "")
                        if "instagram.com" not in domain:
                            continue
                        # Ensure domain matches formatting
                        if not domain.startswith(".") and not domain.startswith("www") and domain:
                            domain = "." + domain
                        playwright_cookies.append({
                            "name": c["name"],
                            "value": c["value"],
                            "domain": domain,
                            "path": c.get("path", "/"),
                            "secure": c.get("secure", True),
                            "httpOnly": c.get("httpOnly", False),
                            "sameSite": "None" if c.get("sameSite") == "no_restriction" else "Lax"
                        })
                    context.add_cookies(playwright_cookies)
                    print("[+] Cookie injection completed.")
                except Exception as e:
                    print(f"[!] Warning: Failed to parse cookie file: {e}")

            page = context.new_page()
            try:
                print("[*] Navigating to Instagram...")
                page.goto("https://www.instagram.com/", wait_until="networkidle")
                page.wait_for_timeout(5000)

                # Check if login is required by looking for logged-in indicators
                is_logged_in = False
                try:
                    selectors_query = f"svg[aria-label='New post'], svg[aria-label='Home'], a[href='/{username}/'], a[href*='/direct/inbox/']"
                    page.wait_for_selector(selectors_query, timeout=10000)
                    is_logged_in = True
                    print("[+] Authenticated successfully using injected cookies!")
                except Exception:
                    print("[*] Home page logged-in indicator not found. Checking login page redirect...")

                if not is_logged_in:
                    # Go to login page explicitly to bypass signup or account chooser
                    print("[*] Navigating to login page...")
                    page.goto("https://www.instagram.com/accounts/login/", wait_until="networkidle")
                    page.wait_for_timeout(5000)
                    
                    # Check if visiting the login page auto-redirected us to the home page (cookies active)
                    try:
                        selectors_query = f"svg[aria-label='New post'], svg[aria-label='Home'], a[href='/{username}/']"
                        page.wait_for_selector(selectors_query, timeout=8000)
                        is_logged_in = True
                        print("[+] Authenticated successfully after login page auto-redirect!")
                    except Exception:
                        print("[*] Not logged in automatically. Showing credentials form...")

                if not is_logged_in:
                    print("[*] Logging in via credentials form...")
                    
                    # If we see "Use another profile" (profile chooser), click it to show standard login inputs
                    try:
                        chooser_btn = None
                        for sel in ["button:has-text('Use another profile')", "text=Use another profile", "role=button[name*='Use another profile' i]"]:
                            try:
                                btn = page.locator(sel).first
                                if btn.is_visible():
                                    chooser_btn = btn
                                    break
                            except Exception:
                                pass
                        
                        if chooser_btn:
                            print("[*] Profile chooser page detected. Clicking 'Use another profile'...")
                            chooser_btn.click()
                            page.wait_for_timeout(3000)
                    except Exception as chooser_err:
                        print(f"[*] Warning: Profile chooser detection error: {chooser_err}")
                    
                    # Check if username input is visible. If not, but password input is visible, we might be on a password-only login page
                    try:
                        # Wait for password field to appear (under standard name or fallback name)
                        password_selector = "input[name='password'], input[name='pass']"
                        page.wait_for_selector(password_selector, timeout=15000)
                        
                        # Find the actual visible username field (if any)
                        username_selector = None
                        for sel in ["input[name='username']", "input[name='email']"]:
                            try:
                                if page.locator(sel).is_visible():
                                    username_selector = sel
                                    break
                            except Exception:
                                pass
                        
                        # Find the actual visible password field
                        actual_password_selector = None
                        for sel in ["input[name='password']", "input[name='pass']"]:
                            try:
                                if page.locator(sel).is_visible():
                                    actual_password_selector = sel
                                    break
                            except Exception:
                                pass

                        if actual_password_selector and not username_selector:
                            print("[*] Password-only form detected. Entering password...")
                            page.fill(actual_password_selector, password)
                        elif actual_password_selector and username_selector:
                            print(f"[*] Standard login form detected (username selector: '{username_selector}', password selector: '{actual_password_selector}'). Entering credentials...")
                            page.fill(username_selector, username)
                            page.fill(actual_password_selector, password)
                        else:
                            raise Exception("Could not locate username/password fields")
                            
                        # Click the visible submit button
                        submit_clicked = False
                        for btn_sel in [
                            "div[role='button']:has-text('Log in')", 
                            "div[role='button']:has-text('Log In')", 
                            "[aria-label='Log In']", 
                            "[aria-label='Log in']",
                            "button[type='submit']",
                            "input[type='submit']"
                        ]:
                            try:
                                btn = page.locator(btn_sel).first
                                if btn.is_visible():
                                    print(f"[*] Clicking visible submit button using selector: '{btn_sel}'")
                                    btn.click()
                                    submit_clicked = True
                                    break
                            except Exception:
                                pass
                        
                        if not submit_clicked:
                            print("[*] Warning: Visible submit button not found. Trying fallback click...")
                            page.locator("div[role='button']:has-text('Log in'), [aria-label='Log In'], button[type='submit']").first.click()
                    except Exception as login_form_err:
                        # Fallback standard login
                        print(f"[*] Custom form check failed ({login_form_err}). Trying standard login fallback...")
                        page.wait_for_selector("input[name='username']", timeout=10000)
                        page.fill("input[name='username']", username)
                        page.fill("input[name='password']", password)
                        page.click("button[type='submit']")

                    print("[*] Clicked login. Waiting for redirect...")
                    
                    # Wait for redirect to happen (either standard home page redirect or security code page)
                    try:
                        # Wait for either home page navigation OR code entry input to appear
                        combined_query = f"svg[aria-label='New post'], svg[aria-label='Home'], a[href='/{username}/'], input[name*='code'], input[name*='verification'], input[aria-label*='Code']"
                        page.wait_for_selector(combined_query, timeout=40000)
                        
                        # Check if we landed on the code entry page
                        is_checkpoint = False
                        try:
                            if page.locator("input[name*='code'], input[name*='verification'], input[aria-label*='Code']").first.is_visible():
                                is_checkpoint = True
                        except Exception:
                            pass
                            
                        if is_checkpoint:
                            print("[!] SECURITY CODE REQUIRED: Please enter the security code sent to your email/phone in the browser window, click Continue, and wait...")
                            # Wait up to 3 minutes for the user to complete verification
                            selectors_query = f"svg[aria-label='New post'], svg[aria-label='Home'], a[href='/{username}/']"
                            page.wait_for_selector(selectors_query, timeout=180000)
                            print("[+] Logged in successfully after manual code verification!")
                        else:
                            print("[+] Logged in successfully via credentials form!")
                            
                        is_logged_in = True
                    except Exception as redirect_err:
                        raise Exception(f"Login redirect timed out: {redirect_err}")
                    
                    # Save the new cookies back to cookies.json
                    try:
                        new_cookies = context.cookies()
                        with open("cookies.json", "w") as f:
                            json.dump(new_cookies, f, indent=2)
                        print("[+] Successfully saved updated session cookies to 'cookies.json'!")
                    except Exception as cookie_save_err:
                        print(f"[!] Warning: Could not save updated cookies: {cookie_save_err}")

                # Define helper to dismiss popups dynamically
                def dismiss_popups():
                    for popup_text in ["Not Now", "Not now", "Cancel"]:
                        try:
                            selectors = [
                                f"button:has-text('{popup_text}')",
                                f"div[role='button']:has-text('{popup_text}')",
                                f"[role='button']:has-text('{popup_text}')",
                                f"text={popup_text}"
                            ]
                            for sel in selectors:
                                btn = page.locator(sel).first
                                if btn.is_visible():
                                    print(f"[*] Dismissing '{popup_text}' popup using selector: '{sel}'")
                                    btn.click()
                                    page.wait_for_timeout(2000)
                                    return True
                        except Exception:
                            pass
                    return False

                # Dismiss popups twice with a wait to handle late loaders
                dismiss_popups()
                page.wait_for_timeout(2000)
                dismiss_popups()

                # Start creation flow
                print("[*] Opening creation dialog...")
                create_btn = None
                selectors = [
                    "svg[aria-label='New post']",
                    "a[href='#']:has-text('Create')",
                    "span:has-text('Create')",
                    "div[role='button']:has-text('Create')",
                    "text=Create"
                ]
                
                # Attempt to find and click Create button (dismissing popups and retrying if click is blocked)
                click_success = False
                for attempt in range(3):
                    for sel in selectors:
                        try:
                            locator = page.locator(sel).first
                            if locator.is_visible():
                                create_btn = locator
                                print(f"[*] Found Create button using selector: '{sel}'. Clicking it (attempt {attempt+1})...")
                                # Use force click if dialogue overlay is still fading out
                                create_btn.click(force=True)
                                click_success = True
                                break
                        except Exception:
                            pass
                    
                    if click_success:
                        break
                    
                    # If not successful, late-loading popups might have blocked us. Dismiss popups and wait
                    print("[*] Create button click blocked or not found. Checking for popups to dismiss...")
                    dismiss_popups()
                    page.wait_for_timeout(2000)
                
                if not click_success:
                    print("[!] Warning: Could not click Create button via normal selectors. Trying fallback click...")
                    # Fallback force click
                    page.locator("a:has-text('Create'), svg[aria-label='New post'], span:has-text('Create')").first.click(force=True)
                
                page.wait_for_timeout(3000)

                # Check if "Post" option from the dropdown menu appears (Creator/Professional account check)
                try:
                    post_option = page.locator("a[role='link']:text-is('Post'), a[role='link']:has(svg[aria-label='Post'])").first
                    if post_option.is_visible():
                        print("[*] Creator account dropdown detected. Clicking 'Post' item...")
                        post_option.click()
                        page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"[*] No post dropdown detected, continuing: {e}")

                # Upload the generated post image using file inputs
                print("[*] Uploading image file...")
                file_input = page.locator("input[type='file']")
                file_input.wait_for(state="attached", timeout=10000)
                file_input.set_input_files(image_path)
                page.wait_for_timeout(2000)

                # Try to set aspect ratio to 4:5 (Instagram web defaults all uploads to 1:1 square)
                try:
                    print("[*] Adjusting aspect ratio to 4:5...")
                    # Locates the crop toggle button at bottom left of preview
                    crop_btn = page.locator("button:has(svg[aria-label='Select crop']), svg[aria-label='Select crop']").first
                    crop_btn.wait_for(state="visible", timeout=5000)
                    crop_btn.click()
                    page.wait_for_timeout(1000)
                    
                    # Click the '4:5' option
                    ratio_btn = page.locator("button:has-text('4:5'), span:has-text('4:5'), [role='button']:has-text('4:5')").first
                    ratio_btn.wait_for(state="visible", timeout=5000)
                    ratio_btn.click()
                    page.wait_for_timeout(1000)
                    print("[+] Aspect ratio successfully adjusted to 4:5!")
                except Exception as crop_err:
                    print(f"[!] Warning: Could not adjust aspect ratio: {crop_err}. Continuing with default crop.")

                # Click "Next" on Crop Dialog
                print("[*] Processing crop screen...")
                next_btn = page.locator("div[role='dialog'] div[role='button']:has-text('Next')").first
                next_btn.wait_for(state="visible", timeout=10000)
                next_btn.click()
                page.wait_for_timeout(2000)

                # Click "Next" on Filter Dialog
                print("[*] Processing filter screen...")
                next_btn.wait_for(state="visible", timeout=10000)
                next_btn.click()
                page.wait_for_timeout(2000)

                # Fill Caption
                print("[*] Typing caption description...")
                caption_area = page.locator("div[aria-label='Write a caption...']").first
                caption_area.wait_for(state="visible", timeout=10000)
                caption_area.fill(caption)
                page.wait_for_timeout(1000)

                # Dismiss hashtag autocomplete dropdown by blurring input
                try:
                    caption_area.blur()
                    page.wait_for_timeout(2000)
                except Exception:
                    pass

                # Click Share
                print("[*] Publishing post live...")
                share_btn = page.locator("div[role='dialog'] div[role='button']:has-text('Share')").first
                share_btn.click(force=True)
                page.wait_for_timeout(4000)

                # Retry click if the share button is still visible (meaning click was swallowed by focus/blur transition)
                try:
                    if share_btn.is_visible():
                        print("[*] Share button still visible (possibly click swallowed by dropdown blur). Retrying Share click...")
                        share_btn.click(force=True)
                except Exception:
                    pass

                # Wait for upload completion (either success text appears or redirected to profile page)
                print("[*] Waiting for Instagram upload verification...")
                try:
                    # Wait for either the success popup or redirect to profile
                    page.locator("div:has-text('Your post has been shared'), div:has-text('Post shared'), a[href*='" + username + "']").first.wait_for(state="visible", timeout=45000)
                    print("[+] Success! Post has been published live to your Instagram feed!")
                except Exception as e:
                    page.wait_for_timeout(5000)
                    if username in page.url:
                        print("[+] Success! Redirected to profile page, post is live!")
                    else:
                        raise e
                
                # Close browser context
                context.close()
                browser.close()
                return True
            except Exception as e:
                # Capture error screenshot to help debug
                try:
                    screenshot_path = "screenshot.png"
                    page.screenshot(path=screenshot_path)
                    print(f"[!] Error screenshot saved to: '{screenshot_path}'")
                except Exception as screenshot_err:
                    print(f"[!] Could not take screenshot: {screenshot_err}")
                context.close()
                browser.close()
                raise e
            
    except Exception as e:
        print(f"[!] Error publishing to Instagram via Playwright: {e}")
        return False

# -------------------------------------------------------------
# Main Execution Entrypoint
# -------------------------------------------------------------
def run_single_post(mode, history_db):
    """Executes a single post flow (scrape, select, render, upload, and update history)."""
    history_key = "morning_news_history" if mode == "morning" else "evening_career_history"

    # 1. Scrape news (needed for logging and for Gemini prompt context)
    scraped_news = None
    if mode == "morning":
        scraped_news = scrape_trending_tech_news()

    # 2. Try to generate post dynamically via Gemini with retry check for duplicates
    selected_item = None
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        for attempt in range(1, 4):
            print(f"[*] Gemini AI generation attempt {attempt}/3...")
            candidate_item = generate_content_with_gemini(mode, scraped_news, history_db)
            if candidate_item:
                if not is_duplicate_content(candidate_item, history_db):
                    selected_item = candidate_item
                    print(f"[+] Selected unique Content ID (Gemini AI): '{selected_item['id']}' | Title: '{selected_item['title']}'")
                    break
                else:
                    print(f"[!] Generated item '{candidate_item.get('title')}' is a duplicate. Retrying...")
            else:
                print("[*] Gemini AI generation returned None, retrying/falling back...")
        
    # 3. Fallback to corpus if Gemini fails or is disabled, or generates duplicates
    if not selected_item:
        corpus = MORNING_NEWS_CORPUS if mode == "morning" else EVENING_CAREER_CORPUS
        already_posted_ids = set(history_db.get(history_key, []))
        
        # Filter by both ID and Content duplicate checks
        available_items = []
        for item in corpus:
            if item["id"] not in already_posted_ids and not is_duplicate_content(item, history_db):
                available_items.append(item)

        if not available_items:
            print(f"[!] Warning: No unused items in '{mode}' corpus (or all are duplicates). Selecting least-recently-used corpus item as fallback, PRESERVING history.")
            # Find the corpus item that was posted the longest time ago (least recently used)
            last_posted_dates = {}
            for past_item in history_db.get("posted_items", []):
                past_id = past_item.get("id")
                past_date = past_item.get("date", "")
                if past_id:
                    if past_id not in last_posted_dates or past_date > last_posted_dates[past_id]:
                        last_posted_dates[past_id] = past_date
                        
            best_item = corpus[0]
            oldest_date = "9999-99-99 99:99:99"
            
            for item in corpus:
                item_id = item["id"]
                item_date = last_posted_dates.get(item_id, "")
                if not item_date:
                    best_item = item
                    break
                elif item_date < oldest_date:
                    oldest_date = item_date
                    best_item = item
                    
            selected_item = best_item
        else:
            selected_item = available_items[0]
        print(f"[*] Selected Content ID (Fallback): '{selected_item['id']}' | Title: '{selected_item['title']}'")

    # Render the Instagram Post image
    generate_post(mode, selected_item)

    # Create Caption and Prepare Upload
    caption_explanation = selected_item.get("caption_explanation", "")
    caption_lines = [
        selected_item["title"],
        "",
        caption_explanation,
        "",
        "🔗 Apply Link is in Bio! 👉 @insta_ai_bot",
        "",
        f"🔥 {selected_item['cta']}",
        "",
        "Follow @insta_ai_bot for daily tech updates & career growth hacks! 🚀",
        "#indianstartups #fresherjobs #softwareengineer #growthschool #techintelugu"
    ]
    
    instagram_caption = "\n".join(caption_lines)
    print(f"\n[*] Prepared Instagram Caption:\n{'-'*50}\n{instagram_caption}\n{'-'*50}\n")

    # Upload Live
    upload_success = upload_to_instagram(OUTPUT_IMAGE, instagram_caption)

    # Update database tracking
    if upload_success:
        history_db[history_key].append(selected_item["id"])
        
        # Save full details and title to database
        new_item_details = {
            "id": selected_item["id"],
            "title": selected_item["title"],
            "bullets": selected_item["bullets"],
            "cta": selected_item.get("cta", ""),
            "link": selected_item.get("link", ""),
            "caption_explanation": caption_explanation,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode
        }
        history_db.setdefault("posted_items", []).append(new_item_details)
        history_db.setdefault("posted_titles", []).append(selected_item["title"])
        
        print("[+] Database tracking and full content logs updated successfully.")
        
        # Save database to disk
        save_db(history_db)
        # Generate Link-in-Bio index.html page
        generate_link_in_bio_html(history_db)
        # Push index.html and database to GitHub Pages
        push_to_git()
        
        return True
    else:
        print("[!] Warning: Instagram upload failed. Not updating database tracking to allow retrying this post later.")
        return False

def wait_for_network(timeout_seconds=None):
    """Waits in a loop until internet connectivity is established."""
    print("[*] Checking internet connectivity...")
    check_hosts = [("8.8.8.8", 53), ("1.1.1.1", 53), ("google.com", 80)]
    start_time = time.time()
    
    first_msg = True
    while True:
        for host, port in check_hosts:
            try:
                socket.setdefaulttimeout(3)
                socket.create_connection((host, port), timeout=3)
                print("[+] Internet connection detected! Proceeding with bot operations.")
                return True
            except Exception:
                continue
        
        if timeout_seconds and (time.time() - start_time) >= timeout_seconds:
            print(f"[!] Warning: Timeout of {timeout_seconds}s reached without internet connection.")
            return False

        if first_msg:
            print("[!] No internet connection detected. Pausing bot execution until internet is connected...")
            first_msg = False
            
        time.sleep(10)

def main():
    # Load environment variables immediately on startup
    load_env()

    parser = argparse.ArgumentParser(description="Instagram automation bot image generator sidecar.")
    parser.add_argument(
        "--mode", 
        type=str, 
        choices=["morning", "evening", "auto"], 
        default="auto", 
        help="Specify the script run schedule mode (morning / evening / auto)."
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    if hasattr(sys.stderr, 'reconfigure'):
        try:
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print(f"=== Instagram Bot Active: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # Pause execution on startup until internet connection is active
    wait_for_network()
    
    # Download Montserrat fonts programmatically if missing
    download_fonts()

    # Load posting history database
    history_db = load_db()
    mode = args.mode

    if mode == "auto":
        print("[*] Running in auto scheduler mode (startup/activation check)...")
        
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        last_morning_date = history_db.get("last_morning_post_date")
        last_evening_date = history_db.get("last_evening_post_date")
        
        need_morning = (last_morning_date != today_str)
        need_evening = (last_evening_date != today_str)
        
        if not need_morning and not need_evening:
            print("[!] Skip: Both morning and evening posts have already been successfully shared today. Exiting.")
            print("=== Execution Complete ===\n")
            return
            
        # Enforce a 3-hour minimum safety interval between any two uploads
        last_post_time_str = history_db.get("last_post_time")
        if last_post_time_str:
            try:
                clean_time_str = last_post_time_str.replace(" ", "T")
                last_post_time = datetime.datetime.fromisoformat(clean_time_str)
                time_diff = datetime.datetime.now() - last_post_time
                hours_diff = time_diff.total_seconds() / 3600.0
                if hours_diff < 3.0:
                    print(f"[!] Skip: Last upload was only {hours_diff:.2f} hours ago (minimum safety gap is 3 hours). Exiting.")
                    print("=== Execution Complete ===\n")
                    return
            except Exception as e:
                print(f"[*] Warning: Could not parse last_post_time '{last_post_time_str}': {e}. Proceeding.")

        print(f"[*] Scheduler checklist: Morning post needed = {need_morning} | Evening post needed = {need_evening}")
        
        morning_success = False
        
        if need_morning:
            print("[*] Running morning post...")
            morning_success = run_single_post("morning", history_db)
            if morning_success:
                history_db["last_morning_post_date"] = today_str
                history_db["last_post_time"] = datetime.datetime.now().isoformat()
                save_db(history_db)
                
            if morning_success and need_evening:
                print("[*] Morning post successful. Waiting 60 seconds before starting evening post...")
                import time
                time.sleep(60)
                
        if need_evening:
            print("[*] Running evening post...")
            evening_success = run_single_post("evening", history_db)
            if evening_success:
                history_db["last_evening_post_date"] = today_str
                history_db["last_post_time"] = datetime.datetime.now().isoformat()
                save_db(history_db)

    else:
        # Manual run of specific mode
        print(f"[*] Running manual override for mode: {mode}")
        success = run_single_post(mode, history_db)
        if success:
            today_str = datetime.datetime.now().strftime("%Y-%m-%d")
            history_db["last_post_time"] = datetime.datetime.now().isoformat()
            history_db["last_post_mode"] = mode
            if mode == "morning":
                history_db["last_morning_post_date"] = today_str
            else:
                history_db["last_evening_post_date"] = today_str
            save_db(history_db)

    print("=== Execution Complete ===\n")

if __name__ == "__main__":
    main()
