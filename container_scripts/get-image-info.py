import requests
from tabulate import tabulate

def get_container_grades(repo, manifest_digest):
    base_url = f"https://catalog.redhat.com/api/containers/v1/images/registry/registry.access.redhat.com/repository/{repo}/manifest_digest/{manifest_digest}"
    headers = {
        'accept': 'application/json'
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(data)
        container_grades = data.get('container_grades', {})
        status = container_grades.get('status', 'No status available')
        status_message = container_grades.get('status_message', 'No message available')
        return status, status_message
    except Exception as err:
        return "Error", str(err)

def process_image_list(image_list_file):
    table_data = []
    with open(image_list_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '@sha256' in line:
                try:
                    parts = line.split('/')
                    if len(parts) >= 2:  # Check if the URL has enough parts
                        repo_name = f"{parts[1]}/{parts[2].split('@')[0]}"
                        print(repo_name)
                        digest = line.split('@')[1]
                        digest = digest.replace(':', '%3A')  # Encode digest colon
                        repo_name = repo_name.replace('/', '%2F')  # Encode repo name slashes
                        print(repo_name)

                        # Get the container grade status and message
                        status, status_message = get_container_grades(repo_name, digest)

                        # Add row to table
                        table_data.append([line, status, status_message])
                    else:
                        print(line)
                        print(f"Invalid image URL format: {line}")
                except IndexError as e:
                    print(f"Error parsing line: {line}, Error: {e}")
            else:
                print(line)
                print(f"Invalid image URL: {line}")

    # Print table
    headers = ["Image", "Container Grade Status", "Status Message"]
    print(tabulate(table_data, headers, tablefmt="github"))

# Path to your image list
image_list_file = "image-list.txt"
#  All Red Hat containers use the value of 'registry.access.redhat.com' (regardless of whether they are shipped only to the terms-based registry at registry.redhat.io). Partner containers use the value of 'registry.connect.redhat.com'.
# repo_name = "registry.access.redhat.com"

process_image_list(image_list_file)
