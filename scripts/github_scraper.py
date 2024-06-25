"""
Script to scrape the github repositories of the projects in the showcase_urls.txt file and generate a markdown file with a grid of cards with the information of the repositories.

Does not rely on the GitHub API, so it is limited to the information that can be scraped from the GitHub website.

Inspired in part from https://brightdata.com/blog/how-tos/how-to-scrape-github-repositories-in-python
"""

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

with open("scripts/showcase_urls.txt", "r") as file:
    target_urls = file.readlines()
    target_urls = [url.strip() for url in target_urls]
main_info = """# Showcase

This page is a showcase of some projects and research done using the OpenML libary. Did you use OpenML in your work and want to share it with the community? We would love to have you!

Simply create a pull request with the necessary information and we will add it to this page.\n"""


def get_github_info(target_url):
    """
    Get the name, description and number of stars of a GitHub repository from its URL.
    """
    print(target_url)
    page = requests.get(target_url)
    soup = BeautifulSoup(page.text, "html.parser")
    name_html_element = soup.select_one('[itemprop="name"]')
    name = name_html_element.text.strip()

    bordergrid_html_element = soup.select_one(".BorderGrid")
    about_html_element = bordergrid_html_element.select_one("h2")
    description_html_element = about_html_element.find_next_sibling("p")
    description = description_html_element.get_text().strip()

    star_icon_html_element = bordergrid_html_element.select_one(".octicon-star")
    stars_html_element = star_icon_html_element.find_next_sibling("strong")
    stars = stars_html_element.get_text().strip().replace(",", "")

    return name, description, stars


def return_details(target_urls):
    """
    For a list of GitHub URLs, return a dictionary with the name, description and number of stars of the repositories.
    """
    target_urls = list(set(target_urls))  # remove duplicates
    urls = {}
    for target_url in target_urls:
        name, description, stars = get_github_info(target_url)
        if len(name) > 0:
            urls[target_url] = {
                "name": name,
                "description": description,
                "stars": stars,
            }
    # sort by stars
    urls = dict(
        sorted(urls.items(), key=lambda item: int(item[1]["stars"]), reverse=True)
    )
    return urls


def return_div(url, urls):
    """
        Return a div element with the information of a GitHub repository. Creates a card with the name, description and number of stars of the repository.

        Example CSS

    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
      }

      .card {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 20px;
        width: 300px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      }

      .card h2 {
        margin-top: 0;
      }

      .card p {
        margin-bottom: 0;}

        .github-logo {
          height: 15px;
          width: 13px;
          margin-left: 10px;
      }

      iframe[seamless] {
        border: none;
    }
    """
    info = urls[url]
    return f"""
    \n<div class="card">
    <h2><a href="{url}">{info['name']} <img class="github-logo" src="../img/logo-github.svg"> <small>{info['stars']} stars</small></a></h2>
    <p>{info['description']}</p>
    </div>\n
    """


def generate_page(info):
    """
    Generate a page with a grid of cards with the information of the repositories.
    """

    page = """<div class="card-container">\n"""
    for target_url in tqdm(info.keys(), total=len(info)):
        page += return_div(target_url, info)
    page += "</div>"
    return page


info = return_details(target_urls)
# print(generate_page(info))
with open("showcase.md", "w") as file:
    file.write(main_info)
    file.write(generate_page(info))

# test = ["https://github.com/openml/openml-python"]
# print(return_details(test))
