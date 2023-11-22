from playwright.sync_api import sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    goto("http://127.0.0.1:8000/login/?next=/")
    page.get_by_label("Username:").click()
    page.get_by_label("Username:").fill("alice")
    page.get_by_label("Username:").press("Tab")
    page.get_by_label("Password:").fill("Qamania123")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("link", name="Create new tests").click()
    page.locator("#id_name").click()
    page.locator("#id_name").fill("new")
    page.locator("#id_name").press("Tab")
    page.get_by_label("Test description").fill("newnewnewnewnewnew")
    page.get_by_role("button", name="Create").click()
    page.get_by_role("link", name="Test Cases").click()
    page.get_by_role("cell", name="new", exact=True).click()
    page.get_by_role("row", name="14 new newnewnewnewnewnew alice Norun None PASS FAIL Details Delete").get_by_role("button").nth(1).click()
    page.get_by_role("row", name="14 new newnewnewnewnewnew alice FAIL None PASS FAIL Details Delete").get_by_role("button").nth(3).click()

    assert page.query_selector('//td[text()="hello"]') is not None
    # ---------------------
    context.close()
    browser.close()



def test_new_testcases():
    with sync_playwright() as playwright:
        run(playwright)