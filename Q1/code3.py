import requests
import pdfplumber
import os
import re

# your PDF links
pdf_urls = [
"https://iitj.ac.in/PageImages/Gallery/03-2025/4_Regulation_PG_2022-onwards_20022023.pdf",
"https://iitj.ac.in/PageImages/Gallery/07-2025/Curriculum-BTech-CSE.pdf",
"https://iitj.ac.in/PageImages/Gallery/07-2025/Academic_Regulations_Final_03_09_2019.pdf",
"https://www.iitj.ac.in/PageImages/Gallery/01-2026/Detailed-curriculum-for-MTech-CSE-AY-2025-onwards-639053782130026932.pdf"
]

os.makedirs("pdf_data", exist_ok=True)


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_pdf(pdf_path):
    all_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            # 🔹 Extract normal text
            text = page.extract_text()
            if text:
                all_text += text + "\n"

            # 🔹 Extract tables
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    row_text = " ".join([str(cell) for cell in row if cell])
                    all_text += row_text + "\n"

    return clean_text(all_text)


# MAIN LOOP
for url in pdf_urls:
    try:
        print("Downloading:", url)

        response = requests.get(url)
        filename = url.split("/")[-1]
        pdf_path = f"pdf_data/{filename}"

        # save PDF
        with open(pdf_path, "wb") as f:
            f.write(response.content)

        print("Extracting:", filename)

        text = extract_pdf(pdf_path)

        if len(text) < 200:
            print("Too little text, skipping")
            continue

        # save extracted text
        txt_file = pdf_path.replace(".pdf", ".txt")

        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n\n")
            f.write(text)

        print("Saved:", txt_file)

    except Exception as e:
        print("Error:", e)


print("\nDONE: All PDFs processed!")
