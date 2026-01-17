import httpx
from selectolax.parser import HTMLParser


def get_html(base_url:str, page: int):

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0"
    }

    resp = httpx.get(base_url + str(page), headers=headers, follow_redirects=True)
    # Parse page html
    html = HTMLParser(resp.text)
    return html


def extract_text(html, selector):
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None


def parse_page(html):
    # Locate product cards
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")

    for product in products:
        item = {
            "name" : extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
            "full-price": extract_text(product, "span[data-ui=full-price]"),
            "sale-price": extract_text(product, "span[data-ui=sale-price]"),
        }

        if item["full-price"] == None:
            item["full-price"] = extract_text(product, "span[data-ui=compare-at-price]")
        yield item


def main():
    base_url = "https://www.rei.com/c/backpacking-tents?page="
    for page in range(1, 6):
        list_page_html = get_html(base_url, page)
        data = parse_page(list_page_html)
        for item in data:
            print(item)



if __name__ == "__main__":
    main()