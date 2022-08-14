#!usr/bin/env

import sys
# text wrap
import textwrap

# install library - pip install pillow
# import libraries
from PIL import Image, ImageFont, ImageDraw, ImageFilter

# url
from urllib.request import urlopen

# for fetching site name
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

border_left = 120
template_image = 'images/poster-template-3.png'
target_image = '/home/gmadappa/Downloads/poster-output-image.png'
# logo_image = 'images/techbeatly-logo-v4.1-black.png'
text_meta_description = ""

# site_url = "https://towardsdatascience.com/adding-text-on-image-using-python-2f5bf61bf448"
# "https://www.redhat.com/en/resources/4-benefits-using-rh-solutions-on-aws?sc_cid=7013a0000026Hr2AAE"

# set font
font_title = ImageFont.truetype('fonts/Figtree-Black.ttf',size=60)
font_site = ImageFont.truetype('fonts/Figtree-Regular.ttf',size=32)
font_link = ImageFont.truetype('fonts/Figtree-Regular.ttf',size=24)

# text_title = 'Obama warns far-left candidates says average American does not want to tear down the system'
text_link = 'https://developers.redhat.com/articles/2022/08/01/containerize-net-applications-without-writing-dockerfiles?sc_cid=7013a000002i7tiAAA'

if len(sys.argv)>1:
    text_link = sys.argv[1]
else:
    print("Missing url!")
    sys.exit()

# making requests instance
reqs = requests.get(text_link)
# using the BeautifulSoup module
soup = BeautifulSoup(reqs.text, 'html.parser')
 
# displaying the title
#print("Title of the website is : ")
title_from_url = ""
for title in soup.find_all('title'):
    #print(title.get_text())
    title_from_url = title_from_url + title.get_text() + '\n'

# fetch description
metas = soup.find_all('meta') #Get Meta Description
for m in metas:
    if m.get ('name') == 'description':
        text_meta_description = m.get('content')
        #print(text_meta_description)
        

# fetch site domain
text_domain = urlparse(text_link).netloc
#print(text_domain)

# open image
img = Image.open(template_image)

def wraptext(input_text,wrap_width):
    wrapper = textwrap.TextWrapper(width=wrap_width) 
    word_list = wrapper.wrap(text=input_text) 
    caption_new = ''
    for ii in word_list[:-1]:
        caption_new = caption_new + ii + '\n'
    caption_new += word_list[-1]
    return caption_new

# wrap the texts
text_title_wrapped = wraptext(title_from_url,30)
text_domain_wrapped = wraptext(text_domain,80)
text_link_wrapped = wraptext(text_link,80)


# draw image object
I1 = ImageDraw.Draw(img)

# add text to image
## domain name
I1.text((border_left, 300), text_domain_wrapped, font=font_site, fill=(0, 0, 0))
## Post Title
I1.text((border_left, 380), text_title_wrapped, font=font_title, fill=(0, 0, 0))

## Post description
if len(text_meta_description) > 1:
    text_meta_description_wrapped = wraptext(text_meta_description,60)
    I1.text((border_left, 600), text_meta_description_wrapped, font=font_site, fill=(0, 0, 0))
## link
I1.text((border_left, 800), text_link_wrapped, font=font_link, fill=(0, 0, 0))

## add logo
# image_logo = Image.open(logo_image)
# img.paste(image_logo,(0,0),image_logo)
# save image
img.save(target_image)

# output for posting
print("\n" + title_from_url)
print("\n" + text_meta_description)
print("\n" + text_link)
print("\n" + text_domain)
print("\nFollow @techbeatly for learning")
print("\n#learning #devops #techbeatly\n")