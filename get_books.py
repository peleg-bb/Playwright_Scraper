from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")
    titles = []
    prices = []

    data = []
    while True:
        for book in page.locator('article.product_pod').all():
            title = book.locator('h3 a').get_attribute('title')
            price = book.locator('.price_color').text_content()
            data.append({
                'title': title,
                'price': float(price.replace('£', '').strip()),
            })
        button = page.locator('.next a')

        if button.count() > 0:
            button.click()
        else:
            break

        # wait for the page to load
        page.wait_for_selector('article.product_pod')
    # convert to json
    json_data = json.dumps(data, indent=4)
    # write to file
    with open('books.json', 'w') as f:
        f.write(json_data)
    browser.close()




