import feedparser

feed_url = "https://news.google.com/rss/search?q=Business+News&hl=en-US&gl=US&ceid=US:en"

blog_feed = feedparser.parse(feed_url)
    # returns title of the blog site
blog_feed.feed.title

# returns the link of the blog
# and number of entries(blogs) in the site.
blog_feed.feed.link
print(len(blog_feed.entries))
a = len(blog_feed.entries)

# Details of individual blog can
# be accessed by using attribute name
for i in range(1):
    print(blog_feed.entries[0].title)
    print(blog_feed.entries[0].link)
    print(blog_feed.entries[0].description)
