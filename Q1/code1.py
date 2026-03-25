import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import os

# for scraping faculty websites

faculty_sites = [
    "https://sites.google.com/view/sharmapuneet/home",
    "https://sites.google.com/view/nil-kamal-hazra/home",
    "https://sites.google.com/view/abhisheksarkar",
    "https://home.iitj.ac.in/~goravb/",
    "https://3dcomputervision.github.io/",
    "https://home.iitj.ac.in/~richa/",
    "https://sites.google.com/site/dipsankarban/",
    "https://anandmishra22.github.io/",
    "https://sites.google.com/view/angshumanpaul/research",
    "https://sites.google.com/iitj.ac.in/rims/rims-head",
    "https://home.iitj.ac.in/~sy/",
    "https://angansengupta.wixsite.com/aces",
    "https://sudiptabhattachary0.wixsite.com/website-1",
    "https://www.sushmitajhalab.com/",
    "https://bharatsrajpurohit.weebly.com/research.html",
    "https://sites.google.com/view/angshumanpaul/",
    "https://sites.google.com/view/lawqueenkanesh/"
    
]

# common tab names (VERY IMPORTANT)
COMMON_TABS = [
    "home", "education", "experience", "research",
    "publications", "teaching", "students"
]

os.makedirs("faculty_sites", exist_ok=True)


def extract_text(soup):
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator=" ")


def scrape_google_site(base_url):
    collected = []

    for tab in COMMON_TABS:
        url = base_url.rstrip("/") + "/" + tab

        try:
            print("Scraping:", url)
            res = requests.get(url, timeout=5)

            if res.status_code != 200:
                continue

            soup = BeautifulSoup(res.text, "html.parser")
            text = extract_text(soup)

            if len(text) > 200:
                collected.append(text)

            time.sleep(1)

        except Exception as e:
            print("Error:", e)

    return collected


for site in faculty_sites:
    print("\nProcessing:", site)

    data = []

    if "sites.google.com" in site:
        data = scrape_google_site(site)
    else:
        # fallback: just scrape homepage
        try:
            res = requests.get(site)
            soup = BeautifulSoup(res.text, "html.parser")
            text = extract_text(soup)
            if len(text) > 200:
                data.append(text)
        except:
            pass

    filename = site.replace("https://", "").replace("/", "_")

    with open(f"faculty_sites/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(f"URL: {site}\n\n")
        for t in data:
            f.write(t + "\n\n")

print("\nDONE!")
