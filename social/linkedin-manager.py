import os
import json
import requests

# Replace the variables with your own values
# LINKEDIN_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
# LINKEDIN_API_URL = "https://api.linkedin.com/v2/ugcPosts"
LINKEDIN_API_URL = "https://api.linkedin.com/v2/posts"
LINKEDIN_API_URL_MEMBER = "https://api.linkedin.com/v2/me"
LINKEDIN_MEDIA_UPLOAD_API_URL = "https://api.linkedin.com/v2/images?action=initializeUpload"


def upload_image_to_linkedin(image_path):
    
    # Initialize Image Upload
    API_URL = 'https://api.linkedin.com/rest/images?action=initializeUpload'
    """
    Uploads an image to LinkedIn and returns the URL of the uploaded image.
    """
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    data = json.dumps({
        "initializeUploadRequest": {
            "owner": "urn:li:person:{LINKEDIN_MEMBER_ID}"
        }
    })
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            API_URL,
            headers=headers,
            data=data
        )
        if response.status_code != 201:
            print(f"Error uploading image to LinkedIn: {response.json()}")
            return None
        else:
            image_url = response.headers.get('location')
            print(image_url)
            return image_url

def get_linkedin_member_id():
    """
    Retrieves the member ID of the authenticated LinkedIn user.
    """
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        LINKEDIN_API_URL_MEMBER,
        headers=headers
    )
    if response.status_code != 200:
        print(f"Error retrieving LinkedIn member ID: {response.json()}")
        return None
    else:
        member_id = response.json().get("id")
        print(f"Retrieved LinkedIn member ID: {member_id}")
        return member_id

        
def create_post(content):
    # Get the member ID
    LINKEDIN_MEMBER_ID = get_linkedin_member_id()

    """
    Creates a post on LinkedIn using the API.
    """
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    # "lifecycleState": "PUBLISHED",
    data = json.dumps({
        "author": f"urn:li:person:{LINKEDIN_MEMBER_ID}",
        "lifecycleState": "DRAFT",
        "visibility": "PUBLIC",
        "commentary": content,
        "distribution": {
          "feedDistribution": "MAIN_FEED",
          "targetEntities": [],
          "thirdPartyDistributionChannels": []
        },
        "isReshareDisabledByAuthor": False
       

    })
    # data = json.dumps({
    #     "author": f"urn:li:person:{LINKEDIN_MEMBER_ID}",
    #     "lifecycleState": "DRAFT",
    #     "visibility": "PUBLIC",
    #     "commentary": content,
    #     "specificContent": {
    #         "com.linkedin.ugc.ShareContent": {
    #             "shareCommentary": {
    #                 "text": content
    #             },
    #             "shareMediaCategory": "NONE"
    #         }
    #     },

    # })    
        # "visibility": {
        #     "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        # }        
    response = requests.post(
        LINKEDIN_API_URL,
        headers=headers,
        data=data
    )
    if response.status_code != 201:
        print(f"Error posting on LinkedIn: {response.json()}")
    else:
        print("Posted on LinkedIn successfully!")

def create_post_with_image(image_path, caption):
    # Get the member ID
    LINKEDIN_MEMBER_ID = get_linkedin_member_id()

    image_url = upload_image_to_linkedin(image_path)
    if not image_url:
        return
    
    """
    Creates a post with an image on LinkedIn using the API.
    """
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = json.dumps({
        "author": f"urn:li:person:{LINKEDIN_MEMBER_ID}",
        "lifecycleState": "DRAFT",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": caption
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": caption
                        },                        
                        "media": f"urn:li:digitalmediaAsset:{image_url}"
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    })
    response = requests.post(
        LINKEDIN_API_URL,
        headers=headers,
        data=data
    )
    if response.status_code != 201:
        print(f"Error posting on LinkedIn: {response.json()}")
    else:
        print("Posted on LinkedIn successfully!")

if __name__ == '__main__':
    content = "Here's a post on LinkedIn using the API!"
    create_post(content)

    # image_path = "poster-output-image.png"
    # caption = "Here's a post with an image on LinkedIn using the API!"
    # create_post_with_image(image_path, caption)




"""
Help
Create App: https://www.linkedin.com/developers/
Get Token: https://www.linkedin.com/developers/tools/oauth
"""