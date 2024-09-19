import requests

def get_image_details(image_url):
    # Define the API endpoint and headers (adjust if API key or auth is required)
    base_url = "https://catalog.redhat.com/api/containers/v1/ui/images"

    # Extract the image name from the URL
    image_name = image_url.split('/')[2]  # Adjust this split based on URL structure
    tag_or_digest = image_url.split('/')[-1]

    # Build query parameters
    params = {
        'filter': f'repo_name=={image_name},digest=={tag_or_digest}'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        # Parse and print relevant information
        data = response.json()
        if data['data']:
            print(f"Image Name: {image_name}")
            for image in data['data']:
                print(f"Health Index: {image['health_index']}")
                print(f"Digest: {image['repositories'][0]['digest']}")
                print(f"Tags: {image['repositories'][0]['tags']}")
        else:
            print("No image details found.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Error: {err}")

# Example image URL
image_url = "registry.redhat.io/ansible-automation-platform-24/ee-supported-rhel9@sha256:05bd9f9b5189dbb43fe704d2db74f1a8dd41609108bf7d339cfb00694425364c"
get_image_details(image_url)
