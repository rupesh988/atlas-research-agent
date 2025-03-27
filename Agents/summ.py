import requests
from bs4 import BeautifulSoup

def get_limited_info(urls):
    combined_text = ""
    for url in urls:
        print(f"fetching url ->   {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract title and first few paragraphs
            title = soup.title.string if soup.title else "No Title"
            paragraphs = soup.find_all("p")[:3] 
            content = " ".join(p.get_text() for p in paragraphs)

            combined_text += f"\n\n--- {title} ({url}) ---\n\n{content}"
        except requests.exceptions.RequestException as e:
            print("error in fetching")
            combined_text += f"\n\n--- Error fetching {url}: {e} ---\n\n"
    print("searched the resouces pages")
    return combined_text