from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")


    data = []
    while True:
        books = page.locator('article.product_pod')
        for b in range(books.count()):
            book = books.nth(b)
            title = book.locator('h3 a').get_attribute('title')
            price = book.locator('.price_color').text_content()
            book.locator('h3 a').click()
            try:
                description = page.wait_for_selector('#product_description ~ p', timeout=3000).text_content()
            except Exception as e:
                description = ''
                print("Description not found")
            data.append({
                'title': title,
                'description': description,
                'price': float(price.replace('£', '').strip()),
            })
            page.go_back()
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




