
import os
import sys
from playwright.sync_api import sync_playwright, expect

def verify_qr_tooltip():
    with sync_playwright() as p:
        # Launch browser with web security disabled to avoid CORS issues if any (as per memory)
        browser = p.chromium.launch(headless=True, args=['--disable-web-security'])
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = context.new_page()

        # Navigate to the local server
        page.goto("http://localhost:8000")

        # Wait for the welcome message to ensure page loaded
        expect(page.locator("#welcome-message")).to_be_visible()

        # Locate the call link in the welcome section
        # The structure is .call-link-container > .call-link
        # And .qr-tooltip is a sibling of .call-link
        call_link = page.locator("#call-link-welcome .call-link")

        # Click the link to trigger the tooltip
        call_link.click()

        # Wait for the tooltip to become active/visible
        tooltip = page.locator("#call-link-welcome .qr-tooltip")
        expect(tooltip).to_have_class(re.compile(r"active"))
        expect(tooltip).to_be_visible()

        # Wait a bit for transition
        page.wait_for_timeout(500)

        # Take a screenshot
        os.makedirs("/home/jules/verification", exist_ok=True)
        screenshot_path = "/home/jules/verification/qr_tooltip_downwards.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    import re
    verify_qr_tooltip()
