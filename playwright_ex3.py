from playwright.sync_api import Playwright, sync_playwright, expect
from time import sleep
from playwright_stealth import stealth_sync
import random

def human_like_delay(min_seconds = 0.5, max_seconds = 1.5):
    sleep(random.uniform(min_seconds, max_seconds))

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless = False)
    #browser = playwright.firefox.launch(headless = False)
    
    #context = browser.new_context()
    
    context = browser.new_context(
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    )
    
    page = context.new_page()
    stealth_sync(page)
    page.set_viewport_size({"width": 1920, "height": 1080})    
    page.goto("https://seller.walmart.com/home")
    human_like_delay(1, 2)
    page.locator("input[type=\"text\"]").click()
    page.locator("input[type=\"text\"]").fill("")
    human_like_delay(1, 2)
    page.locator("input[type=\"password\"]").click()
    human_like_delay(1, 2)
    page.locator("input[type=\"password\"]").fill("")
    human_like_delay(1, 2)
    page.get_by_role("button", name="LOG IN").click()
    try:
        page.frame(url="about:blank").get_by_role("button", name="Human challenge").click()
    except:
        pass
    page.click("text=Inventory")
    #page.click("text=Download")
    #page.click("text=All items")
    #page.click("text=Download")
    sleep(30)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
