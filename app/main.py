import requests
from bs4 import BeautifulSoup
import csv

url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}


def get_pages_count() -> int:
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    pages = int(soup.find_all("li", class_="page-item")[-2].text)
    return pages


def get_model_name(name, description) -> str:
    if not "..." in name:
        return name
    
    return description.split(",")[0]


def scrape_page(url: str, params: dict) -> list:
    req_1 = requests.get(url, headers=headers, params=params)
    soup_1 = BeautifulSoup(req_1.text, "lxml")

    laptops = soup_1.find_all("div", class_="product-wrapper")
    data = []
    for laptop in laptops:
        model_name = laptop.find("a", class_="title").text
        price = laptop.find("h4", class_="price").text
        description = laptop.find("p", class_="description").text
        data.append({
            "model_name": get_model_name(model_name, description),
            "price": price,
            "description": description
        })

    return data


def main() -> None:
    all_data = []
    for i in range(1, get_pages_count() + 1):
        page_data = scrape_page(url, {"page": i})
        all_data.extend(page_data)

    with open('laptops.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Model Name', 'Description', 'Price'])
        for item in all_data:
            writer.writerow(
                [item['model_name'], item['description'], item['price']])


if __name__ == "__main__":
    main()
