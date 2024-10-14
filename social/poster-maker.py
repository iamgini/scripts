#!usr/bin/env
import os
import sys
import getopt
# text wrap
import textwrap
# For files
import glob

# install library - pip install pillow
# import libraries
from PIL import Image, ImageFont, ImageDraw, ImageFilter

# url
from urllib.request import urlopen

# for fetching site name
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# to select random images
import random

border_left = 120
starting_point = 120
light_template_folder = 'light-templates'
dark_template_folder = 'dark-templates'
light_template_image_list = sorted(glob.glob(light_template_folder + '/*'))
dark_template_image_list = sorted(glob.glob(dark_template_folder + '/*'))
# print(light_template_image_list)
# print(dark_template_image_list)

target_image = os.path.expanduser('~/Downloads/poster-output-image.png')
# logo_image = 'images/techbeatly-logo-v4.1-black.png'

default_hashtags_string = "#learningeveryday #devops #techbeatly #socialkonf"
keywords = ['Ansible', 'Automation', 'OpenShift', 'Virtualization', 'Multi-cluster', 'DevOps', 'kubernetes', 'jenkins', 'cicd', 'gitops']

# site_url = "https://towardsdatascience.com/adding-text-on-image-using-python-2f5bf61bf448"
# "https://www.redhat.com/en/resources/4-benefits-using-rh-solutions-on-aws?sc_cid=7013a0000026Hr2AAE"

# set font
font_title = ImageFont.truetype('fonts/Figtree-Black.ttf',size=72)
font_site = ImageFont.truetype('fonts/Figtree-Regular.ttf',size=32)
font_link = ImageFont.truetype('fonts/Figtree-Regular.ttf',size=24)

# text_title = 'Obama warns far-left candidates says average American does not want to tear down the system'
# text_link = 'https://developers.redhat.com/articles/2022/08/01/containerize-net-applications-without-writing-dockerfiles?sc_cid=7013a000002i7tiAAA'

# function to wrap the text
def wraptext(input_text,wrap_width):
    wrapper = textwrap.TextWrapper(width=wrap_width)
    word_list = wrapper.wrap(text=input_text)
    caption_new = ''
    for ii in word_list[:-1]:
        caption_new = caption_new + ii + '\n'
    caption_new += word_list[-1]
    return caption_new

def createPoster(url,template_image,poster_output_file,font_color):

    # check if URL already provided, else collect
    if len(url) < 1:
        print("Missing url!")
        text_link = input("Enter the URL: ")
        if len(text_link) <1:
            print('Missing url...exiting')
            sys.exit()
        else:
            print("\nFetching details from: " + text_link)
    else:
       text_link =  url
       print("Fetching details from: " + text_link)



    # target_image = '/home/gmadappa/Downloads/poster-output-image.png'

    # try:
    if text_link:

        # making requests instance
        reqs = requests.get(text_link)
        # using the BeautifulSoup module
        soup = BeautifulSoup(reqs.text, 'html.parser')

        # displaying the title
        # print("Title of the website is : ")

        titles_from_url = []
        for title in soup.find_all('title'):
            # print(title.get_text())
            # title_from_url = title_from_url + title.get_text() + '\n'
            titles_from_url.append(title.get_text())

        title_from_url = titles_from_url[0]


        # fetch description
        text_meta_description = ""
        metas = soup.find_all('meta') #Get Meta Description
        for m in metas:
            if m.get ('name') == 'description':
                text_meta_description = m.get('content')
            elif m.get ('property') == 'og:description':
                text_meta_description = m.get('content')

        # fetch site domain
        text_domain = urlparse(text_link).netloc
        #print(text_domain)


        # open image
        img = Image.open(template_image)

        # wrap the texts
        text_title_wrapped = wraptext(title_from_url,25)
        text_domain_wrapped = wraptext(text_domain,80)
        text_link_wrapped = wraptext(text_link,80)


        # draw image object
        I1 = ImageDraw.Draw(img)

        # add text to image
        ## domain name
        text_y = starting_point + 100
        I1.text((border_left,text_y), text_domain_wrapped, font=font_site, fill=font_color)

        ## Post Title
        text_y = text_y + 100
        I1.text((border_left, text_y), text_title_wrapped, font=font_title, fill=font_color)

        # ## debug
        # text_y = text_y + 100
        # I1.text((border_left, text_y), 'debug', font=font_title, fill=font_color)

        # add the height for title x number of lines
        text_title_wrapped_line_height = 70 * len(text_title_wrapped.splitlines())

        ## Post description
        # print(len(text_meta_description))
        if len(text_meta_description) > 10:
            text_y = text_y + text_title_wrapped_line_height + 50
            text_meta_description_wrapped = wraptext(text_meta_description,60)
            I1.text((border_left, text_y), text_meta_description_wrapped, font=font_site, fill=font_color)

            # calculate size and height of description text
            text_meta_description_wrapped_line_height = 30 * len(text_meta_description_wrapped.splitlines())
        else:
            text_meta_description_wrapped_line_height = 0
            text_y = text_y + text_title_wrapped_line_height + 50

        ## add URL text
        text_y = text_y + text_meta_description_wrapped_line_height + 50
        I1.text((border_left, text_y), text_link_wrapped, font=font_link, fill=font_color)

        ## add logo
        # image_logo = Image.open(logo_image)
        # img.paste(image_logo,(0,0),image_logo)
        # save image
        img.save(poster_output_file)

        # Dynamic hashtags
        dynamic_hashtags = generate_hashtags(title_from_url + " " + text_meta_description, keywords)

        # Convert set to a formatted string of hashtags
        hashtags_string = ' '.join(dynamic_hashtags)

        # Resulting hashtags
        # print(hashtags_string)

        # output for posting
        print("\n================= Copy below text for the post =================")
        print("\n" + title_from_url)
        print("\n" + text_meta_description)
        print("\nRead more: " + text_link)
        # print("\n" + text_domain)
        print("\nFollow @techbeatly for #learningeveryday")
        print("Follow @socialkonf for #communitylearning")
        print("\n" + default_hashtags_string )
        print(hashtags_string + "\n")
        print("\n================================================================")
    # except Exception as e:
    #     print(e)
    #     print("Invalid URL or site not reachable!")

# Function to generate hashtags dynamically
def generate_hashtags(combined_text, keywords):
    # Split the text into words
    words = combined_text.split()
    # Generate hashtags only from the keywords found in the text
    hashtag_set = {f"#{word.lower()}" for word in words if word in keywords}
    return hashtag_set

def init_poster(argv):
    arg_url = ""
    # Set default output file
    arg_output = target_image
    arg_mode = ""
    arg_template = ""
    template_list = ""
    arg_help = "{0} -u <url> -t <background-template-number> -o <output-file> -m <dark or light>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hu:t:o:m:", ["help", "url=",
        "template=", "output=","mode="])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                # print the help message and exit
                print(str("\nExample usage:\n\n") + arg_help)
                sys.exit(2)
            elif opt in ("-u", "--url"):
                arg_url = arg
                # print('url:', arg_url)
            elif opt in ("-t", "--template"):
                arg_template = arg
                # print('template:', arg_template)
            elif opt in ("-m", "--mode"):
                arg_mode = arg
                # print('mode:', arg_mode)
            elif opt in ("-o", "--output"):
                arg_output = arg
                # print('output:', arg_output)

        if arg_mode == "dark":
            template_file_list = dark_template_image_list
            font_color = (255, 255, 255)
        if arg_mode == "light":
            template_file_list = light_template_image_list
            font_color = (0, 0, 0)
        else:
            # default = dark
            template_file_list = dark_template_image_list
            font_color = (255, 255, 255)
        # print('L:', template_file_list)

        # check if template number mentioned, else use random
        if len(arg_template) > 0:
            template_image_number = int(arg_template) - 1
        else:
            template_image_number = random.randint(0, len(template_file_list) - 1)
        # print('TN:', template_image_number, ", color:", font_color)

        # set the template
        try:
            template_file = template_file_list[template_image_number]
        except Exception as index_error:
            print(index_error)
            print("Image number doesn't exist; using random template!")
            template_image_number = random.randint(0, len(template_file_list) - 1)
            template_file = template_file_list[template_image_number]
        # print('T:', template_file)

        # print('O:', arg_output)

        # call createPoster function with details
        createPoster(arg_url,template_file,arg_output,font_color)

    except Exception as e:
        print(e)
        print(arg_help)
        sys.exit(2)



if __name__ == "__main__":
    init_poster(sys.argv)