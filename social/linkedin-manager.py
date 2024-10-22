import os
import json
import requests
from six.moves import urllib

# Replace the variables with your own values
# LINKEDIN_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_TOKEN')
# LINKEDIN_API_URL = "https://api.linkedin.com/v2/ugcPosts"
LINKEDIN_API_URL = "https://api.linkedin.com/v2/posts"
LINKEDIN_API_URL_MEMBER = "https://api.linkedin.com/v2/me"
LINKEDIN_MEDIA_UPLOAD_API_URL = "https://api.linkedin.com/v2/images?action=initializeUpload"

linkedin_company_name = "techbeatly"

def upload_image_to_linkedin(image_path, LINKEDIN_MEMBER_ID):
    print("Initialize Image Upload")

    API_URL = 'https://api.linkedin.com/v2/images?action=initializeUpload'

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202303"
    }

    # Ensure you're correctly passing the member URN in the request body
    data = json.dumps({
        "initializeUploadRequest": {
            "owner": f"urn:li:member:{LINKEDIN_MEMBER_ID}"
        }
    })

    response = requests.post(
        API_URL,
        headers=headers,
        data=data
    )

    print(response)

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

def get_linkedin_company_id():
    """
    Retrieves the Company ID
    """

    API_URL = f"https://api.linkedin.com/v2/organizations?q=vanityName&vanityName={linkedin_company_name}"

    # API_URL = "https://api.linkedin.com/v2/organizations?q=companies&keywords=" + urllib.parse.quote(linkedin_company_name)

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        API_URL,
        headers=headers
    )
    if response.status_code != 200:
        print(f"Error retrieving LinkedIn Company ID: {response.json()}")
        return None
    else:
        # company_id = response.json().get("id")
        # print(f"Retrieved LinkedIn Company ID: {company_id}")
        # return company_id
        company_urn = response.json().get("elements")[0].get("organizationalEntity")
        print(f"Retrieved LinkedIn Company URN: {company_urn}")
        return company_urn


def create_text_post(content):
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

    ## working copy
    # "lifecycleState": "DRAFT",
    data = json.dumps({
        "author": f"urn:li:person:{LINKEDIN_MEMBER_ID}",
        "lifecycleState": "PUBLISHED",
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

def create_text_post_for_company(content):
    """
    Creates a post on LinkedIn as the company page.
    """
    # Get the company URN
    company_urn = get_linkedin_company_id()

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = json.dumps({
        "author": f"{company_urn}",
        "lifecycleState": "PUBLISHED",
        "visibility": "PUBLIC",
        "commentary": content,
        "distribution": {
          "feedDistribution": "MAIN_FEED",
          "targetEntities": [],
          "thirdPartyDistributionChannels": []
        },
        "isReshareDisabledByAuthor": False
    })

    response = requests.post(
        LINKEDIN_API_URL,
        headers=headers,
        data=data
    )
    if response.status_code != 201:
        print(f"Error posting on LinkedIn as company: {response.json()}")
    else:
        print("Posted on LinkedIn as the company successfully!")

def create_post_with_image(image_path, caption):
    # Get the member ID
    LINKEDIN_MEMBER_ID = get_linkedin_member_id()

    image_url = upload_image_to_linkedin(image_path, LINKEDIN_MEMBER_ID)
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
    image_url = 'https://www.techbeatly.com/wp-content/uploads/2023/04/openshift-compliance-operator.png'

    content = "Test Post"
    # create_text_post(content)

    create_text_post_for_company(content)


    image_path = "poster-output-image.png"
    caption = "Test Image Post"
    # create_post_with_image(image_path, caption)




"""
Help
Create App: https://www.linkedin.com/developers/
Get Token: https://www.linkedin.com/developers/tools/oauth
"""