
import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--disable-web-security"])
        page = await browser.new_page()

        log_file = open("browser.log", "w")

        # Enable console logging
        page.on("console", lambda msg: log_file.write(f"{msg.text}\n"))

        await page.goto("http://localhost:8000")

        try:
            # Wait for the "Packages" tab to be visible and rendered
            packages_tab = page.locator('div[data-service="Packages"].service-tab')
            await expect(packages_tab).to_be_visible(timeout=10000)

            # Check if the package container has cards
            package_container = page.locator("#package-container")

            # Wait for at least one package card to be rendered
            await expect(package_container.locator(".package-card")).to_have_count(1, timeout=10000)

            print("Test passed: Package cards are rendered.")

        except Exception as e:
            print("Test failed.")
            print(await page.content())

        finally:
            log_file.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
