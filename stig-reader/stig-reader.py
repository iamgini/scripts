import xml.etree.ElementTree as ET

xml_input_file = "stig-data.xml"
# Define the namespace
ns = {'ns': 'http://checklists.nist.gov/xccdf/1.1'}
# def extract_plain_texts(root):
#     """Extracts plain-text fields."""
#     plain_texts = {}
#     for elem in root.findall(".//plain-text"):
#         _id = elem.get("id")
#         text = elem.text.strip() if elem.text else "N/A"
#         plain_texts[_id] = text
#     return plain_texts

# def extract_profiles(root):
#     """Extracts profiles and their selected items."""
#     profiles = []
#     for profile in root.findall(".//Profile"):
#         profile_data = {
#             'id': profile.get('id'),
#             'title': profile.findtext('title', default="N/A"),
#             'description': profile.findtext('description', default="N/A"),
#             'selects': [select.get('idref') for select in profile.findall('select')]
#         }
#         profiles.append(profile_data)
#     return profiles

# def extract_groups(root):
#     """Extracts groups and their associated details."""
#     groups = []
#     for group in root.findall(".//Group"):
#         group_data = {
#             'id': group.get('id'),
#             'title': group.findtext('title', default="N/A"),
#             'description': group.findtext('description', default="N/A"),
#             'rules': []
#         }
#         for rule in group.findall(".//Rule"):
#             rule_data = {
#                 'id': rule.get('id'),
#                 'severity': rule.get('severity', "N/A"),
#                 'title': rule.findtext('title', default="N/A"),
#                 'description': rule.findtext('description', default="N/A"),
#                 'fixtext': rule.findtext('fixtext', default="N/A"),
#                 'check': rule.find('.//check-content') is not None,
#                 'check_text': rule.findtext('.//check-content', default="N/A")
#             }
#             group_data['rules'].append(rule_data)
#         groups.append(group_data)
#     return groups

# def convert_to_markdown(title, description, plain_texts, profiles, groups):
#     """Converts extracted XML data to README.md format."""
#     md_content = f"# {title or 'No Title'}\n\n## Description\n{description or 'No Description'}\n\n"

#     # Add plain-text fields
#     md_content += "## Metadata\n"
#     md_content += f"- Release Info: {plain_texts.get('release-info', 'N/A')}\n"
#     md_content += f"- Generator: {plain_texts.get('generator', 'N/A')}\n"
#     md_content += f"- Conventions Version: {plain_texts.get('conventionsVersion', 'N/A')}\n\n"

#     # Add profiles
#     md_content += "## Profiles\n"
#     if profiles:
#         for profile in profiles:
#             md_content += f"### {profile['title']} (ID: {profile['id']})\n"
#             md_content += f"- Description: {profile['description'] or 'No description available'}\n"
#             md_content += "- Selected items:\n"
#             for item in profile['selects']:
#                 md_content += f"  - {item}\n"
#             md_content += "\n"
#     else:
#         md_content += "No Profiles Available.\n\n"

#     # Add groups
#     md_content += "## Security Groups\n"
#     if groups:
#         for group in groups:
#             md_content += f"### {group['title']} (ID: {group['id']})\n"
#             md_content += f"- Description: {group['description'] or 'No description available'}\n"
#             for rule in group['rules']:
#                 md_content += f"  - **Rule ID**: {rule['id']}\n"
#                 md_content += f"    - Severity: {rule['severity']}\n"
#                 md_content += f"    - Title: {rule['title']}\n"
#                 md_content += f"    - Description: {rule['description']}\n"
#                 md_content += f"    - Fix Text: {rule['fixtext'] or 'N/A'}\n"
#                 if rule['check']:
#                     md_content += f"    - Check Text: {rule['check_text'] or 'N/A'}\n"
#                 md_content += "\n"
#     else:
#         md_content += "No Security Groups Available.\n\n"

#     return md_content
def extract_metadata(root):
    """Extracts title, description, and status from the Benchmark node."""

    # Extract title, description, and status using the defined namespace
    title = root.find('ns:title', ns)
    description = root.find('ns:description', ns)
    status = root.find('ns:status', ns)

    # Return extracted values, defaulting to 'N/A' if not found
    return {
        'title': title.text.strip() if title is not None else 'N/A',
        'description': description.text.strip() if description is not None else 'N/A',
        'status': status.text.strip() if status is not None else 'N/A'
    }

def clean_xml(file_path):
    """Removes any potential BOM or hidden characters from the XML file."""
    with open(file_path, 'rb') as f:
        content = f.read()

    # Remove BOM (Byte Order Mark) if present
    content = content.lstrip(b'\xef\xbb\xbf')

    # Decode content to a string for processing by ElementTree
    return content.decode('utf-8')

def main():
    # Load and clean the XML file
    xml_content = clean_xml(xml_input_file)

    # print(xml_content)
    # with open("out.xml", "w") as f:
    #     f.write(xml_content)

    # tree = ET.parse(xml_input_file)
    # Parse the cleaned XML content
    root = ET.fromstring(xml_content)

    # Extract metadata from the Benchmark node
    metadata = extract_metadata(root)

    # Display extracted values for verification
    print(f"Title: {metadata['title']}")
    print(f"Description: {metadata['description']}")
    print(f"Status: {metadata['status']}")

    # Extract the title and description
    # title = root.findtext('title')
    # description = root.findtext('description')

    # # Extract metadata, profiles, and group details
    # plain_texts = extract_plain_texts(root)
    # profiles = extract_profiles(root)
    # groups = extract_groups(root)

    # # Convert extracted information to markdown
    # md_content = convert_to_markdown(title, description, plain_texts, profiles, groups)

    # # Write the markdown content to README.md
    # with open("README.md", "w") as f:
    #     f.write(md_content)
    # print("README.md has been generated.")

if __name__ == "__main__":
    main()
