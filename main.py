import httpx
from selectolax.parser import HTMLParser

url = "https://www.rei.com/c/backpacking-tents"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0"
}

resp = httpx.get(url, headers=headers)



# Parse page html
html = HTMLParser(resp.text)

# Locate products
products = html.css("li.VcGDfKKy_dvNbxUqm29K")

def extract_text(html, selector):
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None



for product in products:
    item = {
        "name" : extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
        "full-price": extract_text(product, "span[data-ui=full-price]"),
        "sale-price": extract_text(product, "span[data-ui=sale-price]"),
    }

    if item["full-price"] == None:
        item["full-price"] = extract_text(product, "span[data-ui=compare-at-price]")
    print(item)