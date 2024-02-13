from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import hashlib


def fetch_and_parse(url):
    """Fetches HTML content from a given URL using Selenium with headless Edge browser, and returns the inner HTML of a specific element."""
    options = Options()
    options.add_argument("--headless")  # Enable headless mode for background operation.
    options.add_argument("--disable-gpu")

    driver = webdriver.Edge(options=options)
    driver.get(url)

    try:
        # Wait for the specific element to be loaded on the page.
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "support-fragment"))
        )
        content = element.get_attribute('innerHTML')  # Extract the inner HTML of the element.
    except Exception as e:
        print(f"An error occurred: {e}")
        content = None  # Ensure content is None if an error occurs.
    finally:
        driver.quit()
    return content


def extract_information(html_content, url):
    """Parses HTML content to extract and structure information such as title, content, and metadata."""
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string if soup.title else "No title"
    
    # Extract the main content and section headers with their text.
    page_content = ' '.join([p.text for p in soup.find_all('p')])
    sections = [{
        "header": header.get_text(strip=True),
        "text": " ".join(sibling.get_text(separator=" ", strip=True) for sibling in header.find_next_siblings() if sibling.name and sibling.name.lower() in ['p', 'ul', 'ol'])
    } for header in soup.find_all(['h1', 'h2', 'h3'])]

    # Extract keywords and description from meta tags.
    keywords_meta = soup.find("meta", {"name": "keywords"})
    keywords = keywords_meta["content"].split(",") if keywords_meta else []
    description = soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else ""

    document = {
        "id": generate_hash_id(url),
        "url": url,
        "title": title,
        "content": page_content,
        "metadata": {
            "scrapedDate": datetime.now().isoformat(),
            "keywords": keywords,
            "description": description
        },
        "sections": sections
    }
    return document


def generate_hash_id(url):
    """Generates a SHA-256 hash of the URL to use as a unique ID."""
    return hashlib.sha256(url.encode()).hexdigest()


urls = [
    "https://www.commbank.com.au/support.credit-cards.find-credit-card-account-balance.html",
    "https://www.commbank.com.au/support.banking.explain-pending-transactions.html",
    "https://www.commbank.com.au/support.bank-accounts.account-proof-of-balance.html",
    "https://www.commbank.com.au/support.digital-banking.change-netbank-password.html",
    "https://www.commbank.com.au/support.business.change-business-address.html",
    "https://www.commbank.com.au/support.banking.open-commonwealth-bank-account.html",
    "https://www.commbank.com.au/support.banking.term-deposit-for-overseas-cutomers.html",
    "https://www.commbank.com.au/support.digital-banking.find-interest-rates-in-netbank.html",
    "https://www.commbank.com.au/support.super.withdraw-from-super-or-investment-policy.html",
    "https://www.commbank.com.au/support.home-loan.explain-interest-in-advance.html",
    "https://www.commbank.com.au/support.home-loan.home-loan-application-approval.html",
    "https://www.commbank.com.au/support.home-loan.digital-home-loan-documents.html",
    "https://www.commbank.com.au/support.personal-loan.pay-out-personal-loan.html",
    "https://www.commbank.com.au/support.digital-banking.set-up-regular-netbank-transfers.html",
    "https://www.commbank.com.au/support.digital-banking.register-app-notifications.html",
    "https://www.commbank.com.au/support.digital-banking.selling-phone-or-tablet-removing-commbank-app.html",
    "https://www.commbank.com.au/support.digital-banking.pay-mobile-using-commbank-app.html",
    "https://www.commbank.com.au/support.credit-cards.change-credit-limit.html",
    "https://www.commbank.com.au/support.credit-cards.exceeding-credit-limit.html",
    "https://www.commbank.com.au/support.tmc.charged-atm-fees-with-travel-money-card.html",
    "https://www.commbank.com.au/support.banking.what-is-a-bsb-number.html",
    "https://www.commbank.com.au/support.cards.activate-card.html",
    "https://www.commbank.com.au/support.bank-accounts.how-do-i-close-my-commbank-account.html",
]


if __name__ == '__main__':
    output_dir = 'RAG_prep'
    os.makedirs(output_dir, exist_ok=True) # Ensure the output directory exists.

    documents = []

    for url in urls:
        content = fetch_and_parse(url)
        if content:
            document = extract_information(content, url)
            documents.append(document)
        else:
            print(f'Error scraping {url}')

    with open(os.path.join(output_dir, 'all_documents.json'), 'w', encoding='utf-8') as file:
        json.dump(documents, file, indent=4, ensure_ascii=False)
