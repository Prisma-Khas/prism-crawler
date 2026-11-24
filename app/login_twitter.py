from app.crawler.browser_twitter import Browser


def main():

    browser = Browser(headless=False)

    playwright, context = browser.launch()

    page = context.new_page()

    try:

        page.goto("https://x.com/home")

        print("=" * 60)
        print("Login to X manually.")
        print("After the Home page appears, press ENTER.")
        print("=" * 60)

        input()

        page.goto("https://x.com/home")

        if "login" in page.url or "flow" in page.url:
            print("❌ Login not detected.")
        else:
            print("✅ Login successful.")
            print("Profile saved to twitter_profile.")

    finally:

        context.close()
        playwright.stop()


if __name__ == "__main__":
    main()