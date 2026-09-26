import os
import feedparser
import tweepy

# Blogger RSS Feed URL
RSS_FEED_URL = "https://bsnotification.blogspot.com/feeds/posts/default?alt=rss"
HISTORY_FILE = "posted_urls.txt"

# Twitter API Credentials
API_KEY = os.environ.get("TWITTER_API_KEY")
API_SECRET = os.environ.get("TWITTER_API_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

def get_posted_urls():
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_posted_url(url):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{url}\n")

def main():
    feed = feedparser.parse(RSS_FEED_URL)
    if not feed.entries:
        print("Feed empty ya load nahi hui.")
        return

    posted_urls = get_posted_urls()

    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    # Naye posts check karna (oldest to newest)
    for entry in reversed(feed.entries):
        link = entry.link
        title = entry.title

        if link not in posted_urls:
            tweet_text = f"📢 New Post: {title}\n\n🔗 Read here: {link}"
            
            # Twitter 280 character limit check
            if len(tweet_text) > 280:
                short_title = title[:200] + "..."
                tweet_text = f"📢 New Post: {short_title}\n\n🔗 Read here: {link}"

            try:
                response = client.create_tweet(text=tweet_text)
                print(f"Tweet posted successfully: {title}")
                save_posted_url(link)
            except Exception as e:
                print(f"Error posting to X: {e}")

if __name__ == "__main__":
    main()
