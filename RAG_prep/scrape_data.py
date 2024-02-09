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
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Edge(options=options)

    driver.get(url)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "support-fragment"))
        )
        content = element.get_attribute('innerHTML')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    return content


def extract_information(html_content, url):
    content = BeautifulSoup(html_content, 'html.parser')
    
    title = content.title.string if content.title else "No title"
    page_content = ' '.join([p.text for p in content.find_all('p')])
    sections = []
    for header in content.find_all(['h1', 'h2', 'h3']):
        section_text = []
        for sibling in header.find_next_siblings():
            if sibling.name and sibling.name.lower() in ['h1', 'h2', 'h3']:
                break
            if sibling.name:
                section_text.append(sibling.get_text(separator=" ", strip=True))
        sections.append({
            "header": header.get_text(strip=True),
            "text": " ".join(section_text)
        })

    keywords_meta = content.find("meta", {"name":"keyword"})
    keywords = keywords_meta["content"].split(",") if keywords_meta else []

    scraped_date = datetime.now().isoformat()

    document = {
        "id": generate_hash_id(url),
        "url": url,
        "title": title,
        "content": page_content,
        "metadata": {
            "scrapedDate": scraped_date,
            "keywords": keywords,
            "description": content.find("meta", {"name":"description"})["content"] if content.find("meta", {"name":"description"}) else ""
        },
        "sections": sections
    }
    return document


def generate_hash_id(url):
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
    output_dir = 'RAG'
    os.makedirs(output_dir, exist_ok=True)

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
