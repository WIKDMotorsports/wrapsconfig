
import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--disable-web-security"])
        page = await browser.new_page()

        # Enable console logging
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))

        await page.goto("http://localhost:8000")

        try:
            # Wait for the "Packages" tab to be visible and rendered
            packages_tab = page.locator('div[data-service="Packages"].service-tab')
            await expect(packages_tab).to_be_visible(timeout=10000)

            # Check if the package container has cards
            package_container = page.locator("#package-container")

            # Wait for at least one package card to be rendered
            await expect(package_container.locator(".package-card")).to_have_count(2, timeout=10000)

            print("Test passed: Package cards are rendered.")

        except Exception as e:
            print("Test failed.")
            print(await page.content())
            raise e

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
