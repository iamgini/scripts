#!usr/bin/env

# text wrap
import textwrap

# install library - pip install pillow
# import libraries
from PIL import Image, ImageFont, ImageDraw 

# url
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

template_image='poster-template.png'
target_image='image-processed.png'
site_url = "https://towardsdatascience.com/adding-text-on-image-using-python-2f5bf61bf448"
# "https://www.redhat.com/en/resources/4-benefits-using-rh-solutions-on-aws?sc_cid=7013a0000026Hr2AAE"

# set font
font_title = ImageFont.truetype('fonts/Figtree-Black.ttf',size=60)
font_link = ImageFont.truetype('fonts/Figtree-Regular.ttf',size=24)

text_title = 'Obama warns far-left candidates says average American does not want to tear down the system'
text_link = 'https://access.redhat.com/documentation/en-us/reference_architectures/2021/html/deploying_ansible_automation_platform_2.1/prerequisites'

# making requests instance
reqs = requests.get(site_url)
# using the BeautifulSoup module
soup = BeautifulSoup(reqs.text, 'html.parser')
 
# displaying the title
#print("Title of the website is : ")
title_from_url = ""
for title in soup.find_all('title'):
    print(title.get_text())
    title_from_url = title_from_url + title.get_text() + '\n'

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
text_link_wrapped = wraptext(text_link,80)

# draw image object
I1 = ImageDraw.Draw(img)

# add text to image
I1.text((100, 300), text_title_wrapped, font=font_title, fill=(0, 0, 0))

I1.text((100, 600), text_link_wrapped, font=font_link, fill=(0, 0, 0))

# save image
img.save(target_image)