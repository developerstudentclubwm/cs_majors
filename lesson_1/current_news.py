# Lesson for Political Science, Government, and International Relations

"""
Lesson goals:
- Understand how to read and write from files
- Get urls from a page
- Format the urls by mutating strings in Python
- Extract information from articles
- Gather information from articles and find ways to interpret it to answer a question
- Have a basic understanding of Natural Language Processing
"""

# Created by Clare Heinbaugh on August 26, 2020

# These are python libraries that we want to import; documentation for each library is linked with this lesson
from bs4 import BeautifulSoup  # We will use Beautiful Soup to pull out website URLs
from newspaper import Article  # We will use Newspaper3k to get information from the article and our input URL

# Start by googling any current events topic. For this example I googled Black Lives Matter and clicked on the News tab.
# Then, I copy and pasted the article url between the quotes and assigned it to the variable "url"
url = 'https://www.google.com/search?q=black+lives+matter&safe=active&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjYypfu-_XqAhXxmOAKHSEyDeMQ_AUoAXoECBgQAw&biw=1332&bih=805'
article = Article(url)  # Now we use the newspaper library to pull out the article
article.download()
html_page = article.html

# We want to parse through the html to find references to links that we can look through; specify parser with the features tag
soup = BeautifulSoup(html_page, features="lxml")

# We want to put all the URLs we find in a text file that we can save and reference again in the future
# The 'w' tag specifies that we want to write to our file; this file will be created in the same folder unless it already exists there
sources_file = open('sources.txt', 'w')

# In html, the "a" tag refers to a link. We're looking for links, so we want to pull "a" tags.
for link in soup.findAll('a'):
    current_link = link.get('href')  # We find all the links on the page using the beautiful soup library
    sources_file.write(current_link + '\n')

# Remember to close our file after writing to it
sources_file.close()

"""
Now we want to check the file and see what was extracted. You may notice that there is some extra information beyond
just urls we can parse through. Taking a closer look, all the urls we want for articles are prefaced by the following
string of characters "/url?q=", but we can easily remove this with a little python code. They also all end with "&sa"
and more stuff, so we need to remove that as well. The urls to the websites we want are printed twice.

QUESTION: HOW CAN WE ENSURE WE'RE ONLY PULLING INFORMATION FROM EACH URL ONCE?
SOLUTION: A SET

A set in python only holds unique values.
"""

# Now we want to read in the file contents that we previously wrote to. To do this, let's use the read ("r") tag.
# Just in case the file does not already exist (like if you only copy and paste the following code in your project),
# we will use a "try-except" block to read from our file.
try:
    sources_file = open('sources.txt', 'r')
except:
    print('Please make a file called sources.txt and populate it with article urls.')

# Now let's read through the file and assign the entire text to a variable
contents = sources_file.read()
sources_file.close()  # remember to close our file again

# Each url is printed on it's own line so we want to create a list of all the lines by splitting on the line break character
all_urls_set = set(contents.split("\n"))  # The split command generates a list
substring_to_remove_from_beginning = "/url?q="
substring_to_remove_from_end = "&sa"  # And everything that comes after is also junk


cleaned_urls_list = [] # We will store our cleaned URLs here
for url in all_urls_set:
    # First let's check for the substring "/url?q=" which we can use to identify relevant urls
    if substring_to_remove_from_beginning in url:
        cleaned_url = url.replace(substring_to_remove_from_beginning,
                                  "")  # We want to remove the substring at the beginning and replace it with an empty string
        cleaned_url = cleaned_url.split(substring_to_remove_from_end)[0]  # We want to pull everything before "&qa
        cleaned_urls_list.append(cleaned_url)

# On your own: save our list of urls to a new file called cleaned_sources.txt

# Solution: Join all the urls on the newline character ("\n)
all_cleaned_urls = "\n".join(cleaned_urls_list)  # This is a string
cleaned_urls_file = open('cleaned_sources.txt', 'w')
cleaned_urls_file.write(all_cleaned_urls)
cleaned_urls_file.close()

# Now we can actually use the urls we collected
for news_article_url in cleaned_urls_list:
    try:
        # Let's get some basics from the article after we cleaned it
        print(news_article_url)
        current_article = Article(news_article_url)
        current_article.download()
        current_article.parse()
        print(current_article.title)
        print(current_article.authors)
        print(current_article.text)

        # On your own: What line do I need to add to get the publish date of the article?
        # Solution:
        print(current_article.publish_date)

        # Now let's get use Newspaper3k to get some fancier information from the article

        """NLP is short for natural language processing and refers to using computers and software to interact with text.
        We can use machine learning tools to understand langugage better."""
        current_article.nlp()

        # This is where it gets interesting when we pull out the keywords from each article
        print(current_article.keywords)

        # Let's see what the discussion is about and compare

    except:
        print("No information extracted from the following url " + news_article_url)
