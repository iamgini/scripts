import feedparser
from jinja2 import Template
import string
from bs4 import BeautifulSoup
import os

import html
import re

# color text
import colorama
from colorama import Fore, Style
from colorama import init
init(autoreset=True)

my_author_name = 'Gineesh Madapparambath'
my_author_name_short = 'gini'
# blog_git_location = '/Users/gini/codes/ginigangadharan.github.io/_posts/'
blog_git_location = os.path.expanduser('~') + '/workarea/iamgini/_posts/'
wp_author_atom_feed = "https://www.techbeatly.com/author/" + my_author_name_short + "/feed/atom/"
#rss_feed_url = 'https://www.techbeatly.com/feed/atom/?paged=3'
#rss_feed_url = 'https://www.techbeatly.com/feed/atom/?paged=10'
# 

article_category_max_count = 3
entry_update_count = 0
article_featured = 'false'
## fetch the rss content
#print('Number of RSS posts :', len(NewsFeed.entries))
#entry = NewsFeed.entries[1]
#print(entry)

rss_feed_page_counter = 1
rss_feed_url = wp_author_atom_feed + '?paged=' + str(rss_feed_page_counter)
# https://www.techbeatly.com/author/gini/feed/atom/?paged=2

NewsFeed = feedparser.parse(rss_feed_url)
print('Number of RSS posts :', len(NewsFeed.entries))

while len(NewsFeed.entries) > 0:
# while rss_feed_page_counter == 1:
#if len(NewsFeed.entries) > 0:
  for entry in NewsFeed.entries:
    article_featured = 'false'

    ## check if this author story, then take it
    if entry.author == my_author_name:
      print(Fore.GREEN + 'Batch ' + str(rss_feed_page_counter) + '::' + 'Updating::' + entry.published[0:10] + Fore.RED + "::" +  entry.title)
      # print(Fore.RED, 'Updating: (Batch:',rss_feed_page_counter,')',entry.published[0:10], entry.title)
      
      entry_update_count = entry_update_count + 1
      article_title = entry.title.replace('  ',' ') 
      # title_cleaned = article_title.translate(str.maketrans('', '', string.punctuation))
      title_cleaned = html.unescape(entry.title)
      title_cleaned = title_cleaned.replace('“', '-')
      title_cleaned = title_cleaned.replace('”', '-')
      title_cleaned = title_cleaned.replace("'", '-')
      title_cleaned = "\"" + title_cleaned + "\""

      
      # print(entry.title)
      # print(html.unescape(entry.title))
      print(Fore.BLUE + '  Title  : ' + Fore.RESET +  title_cleaned)

      
      article_published_date_for_file = entry.published[0:10]
      # Clean the title for file name
      article_new_blog_file = html.unescape(entry.title)
      article_new_blog_file = re.sub(r'[^\w\s]', '', article_new_blog_file)
      article_new_blog_file = article_new_blog_file.replace(' ','-')
      article_new_blog_file = article_new_blog_file.replace('--','-')
      print(Fore.BLUE + "  File   : " + Fore.RESET + article_published_date_for_file + '-' + article_new_blog_file + '.md')

      article_author = my_author_name_short
  
      category_count = 0
      article_tags = []
      article_categories = []
      try:
        for tag in entry.tags:
          article_tags.append(tag.term.lower())
          
          if tag.term.lower() == 'featured':
            article_featured = 'true'
          if category_count < article_category_max_count:
            article_categories.append(tag.term)
            category_count = category_count + 1
          #print(tag.term)
      except:
        article_tags = []
      #finally:
      #  article_categories = article_tags   
      article_external_url = entry.link
      article_published_date = entry.published

      article_summary_raw = BeautifulSoup(entry.summary, 'html.parser')
      article_summary = article_summary_raw.find('p').get_text()
      # print("Summary: " + article_summary)
      
      ## fetching image
      article_content = BeautifulSoup(entry.content[0].value, 'html.parser')
      #print('\n\n\n\n\n\n', article_content)
      images = article_content.find_all('img', src=True)
      #print('Number of Images: ', len(images))
      # for image in images:
      #  print(image)
      # select src tag
      image_src = [x['src'] for x in images]
      # print(image_src[0])

      try:
        article_image = image_src[0]
        print(Fore.BLUE + "  Image  : " + Fore.RESET + article_image)
      except:
        article_image = ''
        print(Fore.BLUE + "  Image  : " + Fore.RESET + article_image)
      
      #for image in image_src:
       # print(image)

      with open('blog-template.md.j2') as file:
        template = Template(file.read())
  
      templated_output = template.render( article_title = title_cleaned,
                                          article_author = article_author,
                                          article_categories = article_categories,
                                          article_image = article_image,
                                          article_tags = article_tags,
                                          article_external_url= article_external_url,
                                          article_summary = article_summary,
                                          article_published_date = article_published_date,
                                          article_featured = article_featured
                                        )
      # print(templated_output)    
      
      new_blog = open(blog_git_location + article_published_date_for_file + '-' + article_new_blog_file + '.md', "w")
      new_blog.write(templated_output)
      new_blog.close()
    else:
      #print('Skipping\t:', entry.title)
      print('Skipping: (' +  str(rss_feed_page_counter) + ') ' + entry.published[0:10] + ": " + entry.title)

  rss_feed_page_counter = rss_feed_page_counter + 1
  # rss_feed_url = 'https://www.techbeatly.com/feed/atom/?paged=' + str(rss_feed_page_counter)
  rss_feed_url = wp_author_atom_feed + '?paged=' + str(rss_feed_page_counter)
 
  NewsFeed = feedparser.parse(rss_feed_url)
  print('Number of RSS posts :', len(NewsFeed.entries))

print('Total entries updated: ', entry_update_count)