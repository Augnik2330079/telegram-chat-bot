import time
import requests
import feedparser

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Notification sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def fetch_rss_feed(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        return [entry for entry in feed.entries]
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return []

def monitor_website(feed_url, token, chat_id):
    print("Monitoring RSS feed for updates...")
    latest_titles = set()

    while True:
        entries = fetch_rss_feed(feed_url)
        if not entries:
            print("No entries found or an error occurred.")
        else:
            new_titles = set(entry.title for entry in entries)
            new_entries = [entry for entry in entries if entry.title not in latest_titles]

            for entry in new_entries:
                message = f"<b>New Article:</b> {entry.title}\n<a href='{entry.link}'>Read more</a>"
                send_telegram_message(token, chat_id, message)

            latest_titles = new_titles

        time.sleep(60)

if __name__ == "__main__":
    FEED_URL = "https://feeds.bbci.co.uk/news/rss.xml"
    TELEGRAM_BOT_TOKEN = ""
    TELEGRAM_CHAT_ID = ""

    monitor_website(FEED_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
