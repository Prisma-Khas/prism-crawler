from aapp.crawler.browser import Browser


browser = Browser(headless=True)

playwright, context = browser.launch()

page = context.new_page()

page.goto("https://www.facebook.com")

input("Login manually, then press ENTER...")

context.close()
playwright.stop()