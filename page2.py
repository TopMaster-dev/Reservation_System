import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta
import calendar

async def run():
    # Calculate the target month
    target_date = datetime.now().replace(day=1) + timedelta(days=64)
    # Get last day of the target month
    last_day = calendar.monthrange(target_date.year, target_date.month)[1]
    # Use the current day or last day of target month, whichever is smaller
    target_day = min(datetime.now().day, last_day)
    next_month = target_date.replace(day=target_day)
    setDay = next_month.strftime("%Y%m%d")
    print(setDay)
    url = f"https://reserve.tokyodisneyresort.jp/hotel/list/?showWay=&roomsNum=1&adultNum=2&childNum=0&stayingDays=1&useDate={setDay}&cpListStr=&childAgeBedInform=&searchHotelCD=DHM&searchHotelDiv=&hotelName=&searchHotelName=&searchLayer=&searchRoomName=%E3%82%B9%E3%83%9A%E3%83%81%E3%82%A2%E3%83%BC%E3%83%AC%E3%83%BB%E3%83%AB%E3%83%BC%E3%83%A0%EF%BC%86%E3%82%B9%E3%82%A4%E3%83%BC%E3%83%88%E3%80%80%E3%83%9D%E3%83%AB%E3%83%88%E3%83%BB%E3%83%91%E3%83%A9%E3%83%87%E3%82%A3%E3%83%BC%E3%82%BE%E3%83%BB%E3%82%B5%E3%82%A4%E3%83%89%20%E3%83%86%E3%83%A9%E3%82%B9%E3%83%AB%E3%83%BC%E3%83%A0%20%E3%83%8F%E3%83%BC%E3%83%90%E3%83%BC%E3%82%B0%E3%83%A9%E3%83%B3%E3%83%89%E3%83%93%E3%83%A5%E3%83%BC&hotelSearchDetail=true&detailOpenFlg=0&checkPointStr=&hotelChangeFlg=false&removeSessionFlg=true&returnFlg=false&hotelShowFlg=&displayType=data-hotel&reservationStatus=1&hotelRoomCd=HODHMTGD0004N#tabCont1"

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()

        # Avoid automation detection
        await page.add_init_script("""Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""")

        print("Navigating...")
        await page.goto(url, wait_until="load", timeout=300000)
        await asyncio.sleep(60)  # Keep browser open for 1 hour

        # Click to open the reservation tab
        await page.wait_for_selector('a[href="#tabCont1"]', timeout=10000)
        await page.click('a[href="#tabCont1"]')

        while True:
            try:
                # Click reserve button
                await page.wait_for_selector('li.js-reserveButton', timeout=10000)
                await page.click('li.js-reserveButton')

                if 'condition_hide_clicked' not in locals():
                    await page.wait_for_selector('li a.js-conditionHide', timeout=10000)
                    await page.click('li a.js-conditionHide')
                    condition_hide_clicked = True
                await asyncio.sleep(5)
                td_elements = []
                for td in await page.query_selector_all("table.vacancyCalTable td"):
                    td_class = await td.get_attribute("class")
                    if td_class and "ok" in td_class.split():
                        td_elements.append(td)
                found = False
                for td in td_elements:
                    a_tag = await td.query_selector('a')
                    if a_tag:
                        await a_tag.click()
                        await page.wait_for_selector("li button.btnReserve", timeout=10000)
                        await page.click("li button.btnReserve")
                        print("Reservation found and clicked!")
                        found = True
                        break
                if found:
                    break  # Exit the loop if reservation is successful
                try:
                    await page.wait_for_selector("#js-vacancyModal p.closeModal", timeout=10000)
                    await page.click("#js-vacancyModal p.closeModal")
                except Exception as e:
                    print(f"Could not close vacancy modal: {e}")
            except Exception as e:
                print(f"Error occurred: {e}")
            await asyncio.sleep(1)  # Wait before retrying

        print("Finished scraping. Browser will stay open.")
        await asyncio.sleep(30)  # Keep browser open for 1 hour

def main(): 
    asyncio.run(run())

if __name__ == "__main__":
    main()