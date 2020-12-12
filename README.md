# news-bot-twitter
A bot that gets news based on what you wants, and tweets it.

Using an api and access keys from twitter, this program allows the bot to tweet by itself.
It uses the datanews api and library to get the articles, getting some preference from user to base what it is gathering.
This has a database that stores articles that have already been tweeted, and checks for new articles.

Gets the first article that hasn't been tweeted yet, stores it into the database, and tweets the title, along with a link directing you
to the page.
