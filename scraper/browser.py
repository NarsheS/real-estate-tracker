from playwright.sync_api import sync_playwright


def get_page_html(url: str) -> str:
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            viewport={
                "width": 1280,
                "height": 900
            },
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            )
        )


        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )


        page.wait_for_selector(
            "section.olx-adcard",
            timeout=30000
        )


        return page.content()