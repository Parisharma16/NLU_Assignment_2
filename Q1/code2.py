import requests
from bs4 import BeautifulSoup
import os
import re
import time

# ALL YOUR LINKS
urls = [
# CSE
"https://www.iitj.ac.in/computer-science-engineering/",
"https://www.iitj.ac.in/computer-science-engineering/en/postgraduate-programs",
"https://www.iitj.ac.in/computer-science-engineering/en/undergraduate-programs",
"https://www.iitj.ac.in/computer-science-engineering/en/doctoral-programs",
"https://www.iitj.ac.in/People/List?dept=computer-science-engineering&ln=en",

# EE
"https://www.iitj.ac.in/electrical-engineering/",
"https://www.iitj.ac.in/electrical-engineering/en/postgraduate-program",
"https://www.iitj.ac.in/electrical-engineering/en/undergraduate-program",
"https://www.iitj.ac.in/electrical-engineering/en/doctoral-program",
"https://www.iitj.ac.in/People/List?dept=electrical-engineering&ln=en",

# Chemical
"https://www.iitj.ac.in/chemical-engineering/",
"https://www.iitj.ac.in/chemical-engineering/en/postgraduate-program",
"https://www.iitj.ac.in/chemical-engineering/en/undergraduate-program",
"https://www.iitj.ac.in/chemical-engineering/en/doctoral-program",
"https://www.iitj.ac.in/People/List?dept=chemical-engineering&ln=en",

# Bio
"https://www.iitj.ac.in/bioscience-bioengineering/",
"https://www.iitj.ac.in/bioscience-bioengineering/en/postgraduate-program",
"https://www.iitj.ac.in/bioscience-bioengineering/en/undergraduate-program",
"https://www.iitj.ac.in/bioscience-bioengineering/en/doctoral-program",
"https://www.iitj.ac.in/People/List?dept=bioscience-bioengineering&ln=en",

# Math
"https://www.iitj.ac.in/mathematics/",
"https://www.iitj.ac.in/mathematics/en/postgraduate-programs",
"https://www.iitj.ac.in/mathematics/en/undergraduate-programs",
"https://www.iitj.ac.in/mathematics/en/doctoral-programs",
"https://www.iitj.ac.in/People/List?dept=mathematics&ln=en",
]

# create folder
os.makedirs("iitj_pages", exist_ok=True)


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_text(soup):
    # remove unwanted elements
    for tag in soup(["script", "style", "nav", "footer", "header", "img"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # remove short junk lines
    lines = text.split("\n")
    lines = [l.strip() for l in lines if len(l.strip()) > 40]

    return clean_text(" ".join(lines))


# 🚀 MAIN LOOP
for url in urls:
    try:
        print("Scraping:", url)

        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        text = extract_text(soup)

        if len(text) < 200:
            print("Skipped (too little content)")
            continue

        # clean filename
        filename = url.replace("https://", "").replace("/", "_").replace("?", "_")

        filepath = f"iitj_pages/{filename}.txt"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n\n")
            f.write(text)

        print("Saved:", filepath)

        time.sleep(1)

    except Exception as e:
        print("Error:", e)


print("\nDONE: All pages scraped cleanly!")
