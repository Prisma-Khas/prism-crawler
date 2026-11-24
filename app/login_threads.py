from aapp.crawler.browser_threads import Browser


browser = Browser(headless=False)

playwright, context = browser.launch()

page = context.new_page()

page.goto("https://www.threads.com")

input("Login manually, then press ENTER...")

context.close()
playwright.stop()