import requests
from bs4 import BeautifulSoup

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Luke_Skywalker"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Extract important sections
# content_div = soup.find("div", {"class": "mw-parser-output"})
# sections = ["Early life", "Biography", "Powers and abilities",
#             "Weapons and equipment", "Portrayals"]
# important_content = ""

# for section in sections:
#     section_header = content_div.find(
#         "span", {"id": section.replace(" ", "_")})
#     if section_header:
#         section_content = ""
#         next_sibling = section_header.next_sibling
#         while next_sibling and next_sibling.name != "h2":
#             section_content += str(next_sibling)
#             next_sibling = next_sibling.next_sibling
#         important_content += f"\n{section}\n{section_content}\n"


# page_text = soup.get_text()

# # Remove extra blank lines
# lines = page_text.split('\n')
# lines = [line for line in lines if line.strip()]
# cleaned_text = '\n'.join(lines)


# with open("luke_skywalker_page.txt", 'w', encoding="utf-8") as file:
#     file.write(cleaned_text)

for element in soup.find_all("div", class_="printfooter"):
    element.decompose()

for script in soup(["script", "style"]):
    script.decompose()
# Get the text content of the page
page_text = soup.get_text()

# Remove extra blank lines
lines = page_text.split('\n')
lines = [line for line in lines if line.strip()]
cleaned_text = '\n'.join(lines)

# Open a new file in write mode and store the cleaned text
with open("luke_skywalker_page.txt", "w", encoding="utf-8") as file:
    file.write(cleaned_text)
