# 🕷️ Website Update Crawler

A multithreaded Python web crawler that monitors websites for updates in specific HTML elements (by class or ID) and sends email notifications when changes are detected.

## 📦 Features

- Continuous monitoring of multiple websites
- Detects changes in HTML content based on `class` or `id`
- Sends automated email alerts when updates are found
- Summarizes detected changes using Google Gemini (AI integration)
- Supports multiple recipients
- Environment-based configuration

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:KievL/web-crawler.git
cd web-crawler
```

### 2. Create and configure your .env file

```markdown
WEBSITE_URLS=https://site1.com,https://site2.com
EMAIL_FROM=youremail@gmail.com
EMAILS_TO=recipient1@gmail.com,recipient2@gmail.com
PASSWORD=your_email_password
TARGET_STRINGS=target1,target2
SLEEP_TIME=60
SLEEP_TIME_AFTER_DETECTION=1800
CLASS_OR_ID=class
GEMINI_KEY=your_gemini_api_key
AI_PROMPT=Summarize the following website content update...
```

- `WEBSITE_URLS`: List of websites to monitor (comma-separated)

- `TARGET_STRINGS`: List of class or ID names to look for (must match the order of URLs)

- `CLASS_OR_ID`: Either class or id, depending on what attribute you want to track

- `SLEEP_TIME`: Interval (in seconds) between checks when no changes are detected

- `SLEEP_TIME_AFTER_DETECTION`: Delay after a change is detected before rechecking

- `EMAIL_FROM`: Gmail address used to send emails

- `EMAILS_TO`: Comma-separated list of email recipients

- `PASSWORD`: Your email password (preferably an App Password if using Gmail)

- `GEMINI_KEY`: Your Gemini API key.

- `AI_PROMPT`: Prompt that will be sent to the IA model to make the summary. This prompt will be concatenated with the old and new target HTML contents.


### 3. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ensure your requirements.txt contains:

```txt
requests
beautifulsoup4
python-dotenv
```

### 4. Run the crawler

python main.py

## 🐳 Running with Docker

```bash
docker build -t crawler .
docker run -d --env-file .env crawler
```

Make sure you have a valid .env file in the same directory.

## ⚠️ Warnings

If you're using Gmail, make sure to enable App Passwords.