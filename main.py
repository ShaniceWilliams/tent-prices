import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin
from dataclasses import dataclass, asdict, fields
import json
import csv


@dataclass
class Product:
    name: str | None
    item_num: str | None
    price: str | None
    rating: float | None


def get_html(url:str, **kwargs):
    """
    Get object containing html of specified url page

    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0"
    }
    
    if kwargs.get("page"):
        resp = httpx.get(url + str(kwargs.get("page")), headers=headers, follow_redirects=True)
    else:
        resp = httpx.get(url, headers=headers, follow_redirects=True)

    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Page Limit Exceeded! Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        return False

    # Parse page html
    html = HTMLParser(resp.text)
    return html


def extract_text(html: HTMLParser, selector: str):
    """
    Extract text from HTMLParser Object using specified css selector.
    """
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None


def parse_list_page(html: HTMLParser):
    """
    Yields the url of each product on the product list page.
    """
    # Locate product cards
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")
    for product in products:
        yield urljoin("https://www.rei.com", product.css_first("a").attributes["href"])


def parse_product_page(html:HTMLParser) -> Product:
    """
    Yield product details
    """
    new_product = Product(
        name=extract_text(html, "h1#product-page-title"),
        item_num=extract_text(html, "a.cdr-breadcrumb__link_16-2-1"),
        price=extract_text(html, "span#buy-box-product-price"),
        rating=extract_text(html, "span.cdr-rating__number_16-2-1"),
    )
    return asdict(new_product)


def export_to_json(products: list):
    with open("products.json", "w") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    print("Saved to JSON.")


def export_to_csv(products: list):
    field_names = [field.name for field in fields(Product)]
    with open("products.csv", "w") as f:
        writer = csv.DictWriter(f, field_names)
        writer.writeheader()
        writer.writerows(products)
    print("Saved to CSV.")

def append_to_csv(product):
    field_names = [field.name for field in fields(Product)]
    with open("products.csv", "a") as f:
        writer = csv.DictWriter(f, field_names)
        writer.writerow(product)

def main():
    # products = []
    base_url = "https://www.rei.com/c/backpacking-tents?page="
    for x in range(1, 2):
        list_page_html = get_html(base_url, page=x)
        if list_page_html is False:
            break
        product_urls = parse_list_page(list_page_html)
        for product_url in product_urls:
            product_html = get_html(product_url)
            append_to_csv(parse_product_page(product_html))
            time.sleep(1)

    # export_to_json(products)
    # export_to_csv(products)



if __name__ == "__main__":
    main()