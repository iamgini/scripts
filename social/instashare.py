#!usr/bin/env

import sys
import getopt
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

# to select random images
import random

border_left = 120
starting_point = 120
# template_image_list = ['poster-template-1', 'poster-template-2','poster-template-3','poster-template-4','poster-template-5','poster-template-6','poster-template-7','poster-template-8']
template_image_list = ['poster-template-1', 'poster-template-2','poster-template-3']
#template_image = 'images/poster-template-3.png'
template_image = 'images/' + random.choice(template_image_list) + ".png"

target_image = '/home/gmadappa/Downloads/poster-output-image.png'
# target_image = './poster-output-image.png'
# logo_image = 'images/techbeatly-logo-v4.1-black.png'


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

def createPoster(url,template_number,output):

    # check if URL already provided, else collect
    if len(url) < 1:
        print("Missing url!")
        text_link = input("Enter the URL: ")
        if len(text_link) <1:
            print('Missing url...exiting')
            sys.exit()
        else:
            print("Fetching details from: " + text_link)
    else:
       text_link =  url
       print("Fetching details from: " + text_link)

    # check if template mentioned, else use random
    if len(template_number) > 0:
        template_image = 'images/poster-template-' + template_number + ".png"
    else:
        template_image = 'images/' + random.choice(template_image_list) + ".png"
    
    # target_image = '/home/gmadappa/Downloads/poster-output-image.png'
        
    # try:
    if text_link:

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
        I1.text((border_left,text_y), text_domain_wrapped, font=font_site, fill=(0, 0, 0))
        ## Post Title
        text_y = text_y + 100
        I1.text((border_left, text_y), text_title_wrapped, font=font_title, fill=(0, 0, 0))

        # add the height for title x number of lines
        text_title_wrapped_line_height = 70 * len(text_title_wrapped.splitlines())

        ## Post description
        # print(len(text_meta_description))
        if len(text_meta_description) > 10:
            text_y = text_y + text_title_wrapped_line_height + 50
            text_meta_description_wrapped = wraptext(text_meta_description,60)
            I1.text((border_left, text_y), text_meta_description_wrapped, font=font_site, fill=(0, 0, 0))
            
            # calculate size and height of description text
            text_meta_description_wrapped_line_height = 30 * len(text_meta_description_wrapped.splitlines())
        else:
            text_meta_description_wrapped_line_height = 0
            text_y = text_y + text_title_wrapped_line_height + 50
        
        ## add URL text
        text_y = text_y + text_meta_description_wrapped_line_height + 50
        I1.text((border_left, text_y), text_link_wrapped, font=font_link, fill=(0, 0, 0))

        ## add logo
        # image_logo = Image.open(logo_image)
        # img.paste(image_logo,(0,0),image_logo)
        # save image
        img.save(target_image)

        # output for posting
        print("\n================= Copy below text for the post =================")
        print("\n" + title_from_url)
        print("" + text_meta_description)
        print("\n" + text_link)
        print("\n" + text_domain)
        print("\nFollow @techbeatly for #learningeveryday")
        print("Follow @socialkonf for #communitylearning")
        print("\n#learning #devops #techbeatly #socialkonf\n")
        print("\n================================================================")
    # except Exception as e:
    #     print(e)
    #     print("Invalid URL or site not reachable!")    



def myfunc(argv):
    arg_url = ""
    arg_output = ""
    arg_template = ""
    arg_help = "{0} -u <url> -t <background-template-number> -o <output-file>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hu:t:o:", ["help", "url=", 
        "template=", "output="])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                # print the help message and exit
                print(arg_help + str("hi"))  
                sys.exit(2)
            elif opt in ("-u", "--url"):
                arg_url = arg
            elif opt in ("-t", "--template"):
                arg_template = arg
            elif opt in ("-o", "--output"):
                arg_output = arg

            # print('url:', arg_url)
            # print('template:', arg_template)
            # print('output:', arg_output)
                  
            
            # call createPoster function with details
            createPoster(arg_url,arg_template,arg_output)

    except Exception as e:
        print(e)
        print(arg_help)
        sys.exit(2)

    # for opt, arg in opts:
    #     if opt in ("-h", "--help"):
    #         print(arg_help)  # print the help message
    #         sys.exit(2)
    #     elif opt in ("-i", "--input"):
    #         arg_input = arg
    #     elif opt in ("-u", "--user"):
    #         arg_user = arg
    #     elif opt in ("-o", "--output"):
    #         arg_output = arg

    # print('input:', arg_input)
    # print('user:', arg_user)
    # print('output:', arg_output)



# Fetch the URL from arguments if any
# if len(sys.argv)>1:
#     text_link = sys.argv[1]
# else:
#     print("Missing url!")
#     text_link = input("Enter the URL: ")
#     if len(text_link) <1:
#         print('Missing url...exiting')
#         sys.exit()
#     else:
#         print("Fetching details from: " + text_link)

# # Fetch specific image template from arguments if any
# if len(sys.argv)>2:
#     text_link = sys.argv[1]
# else:
#     print("Missing url!")
#     text_link = input("Enter the URL: ")
#     if len(text_link) <1:
#         print('Missing url...exiting')
#         sys.exit()
#     else:
#         print("Fetching details from: " + text_link)

# template_image = 'images/' + random.choice(template_image_list)

if __name__ == "__main__":
    myfunc(sys.argv)