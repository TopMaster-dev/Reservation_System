import os
import re
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta
from run import set_tag
from line import line_bot
from playwright_path import get_playwright_browsers_path

async def run():
    next_month = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=datetime.now().day)
    setDay = next_month.strftime("%Y%m%d")
    print(setDay)
    url = f"https://reserve.tokyodisneyresort.jp/hotel/list/?showWay=&roomsNum=1&adultNum=2&childNum=0&stayingDays=1&useDate={setDay}&cpListStr=&childAgeBedInform=&searchHotelCD=DHM&searchHotelDiv=&hotelName=&searchHotelName=&searchLayer=&searchRoomName=%E3%82%B9%E3%83%9A%E3%83%81%E3%82%A2%E3%83%BC%E3%83%AC%E3%83%BB%E3%83%AB%E3%83%BC%E3%83%A0%EF%BC%86%E3%82%B9%E3%82%A4%E3%83%BC%E3%83%88%E3%80%80%E3%83%9D%E3%83%AB%E3%83%88%E3%83%BB%E3%83%91%E3%83%A9%E3%83%87%E3%82%A3%E3%83%BC%E3%82%BE%E3%83%BB%E3%82%B5%E3%82%A4%E3%83%89%20%E3%83%86%E3%83%A9%E3%82%B9%E3%83%AB%E3%83%BC%E3%83%A0%20%E3%83%8F%E3%83%BC%E3%83%90%E3%83%BC%E3%82%B0%E3%83%A9%E3%83%B3%E3%83%89%E3%83%93%E3%83%A5%E3%83%BC&hotelSearchDetail=true&detailOpenFlg=0&checkPointStr=&hotelChangeFlg=false&removeSessionFlg=true&returnFlg=false&hotelShowFlg=&displayType=data-hotel&reservationStatus=1&hotelRoomCd=HODHMTGD0004N#tabCont1"

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
        
    # Set PLAYWRIGHT_BROWSERS_PATH to the correct location
    browsers_path = get_playwright_browsers_path()
    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = browsers_path

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()

        # Avoid automation detection
        await page.add_init_script("""Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""")

        print("Navigating...")
        await page.goto(url, wait_until="load", timeout=300000)
        print("loaded")
        await asyncio.sleep(120)
        # Click to open the reservation tab
        await page.wait_for_selector(set_tag["tag_name"][0], timeout=None) #
        await page.click(set_tag["tag_name"][0])

        while True:
            try:
                # Click reserve button
                await page.wait_for_selector(set_tag["tag_name"][1], timeout=None)
                await page.click(set_tag["tag_name"][1])

                if 'condition_hide_clicked' not in locals():
                    await page.wait_for_selector(set_tag["tag_name"][2], timeout=None)
                    await page.click(set_tag["tag_name"][2])
                    condition_hide_clicked = True
                # Wait until the <a> tag contains an <img>, then execute the line
                try:
                    selector = f'[data-date="{setDay}"] {set_tag["tag_name"][6]}'
                    await page.wait_for_selector(selector, timeout=None)
                    print("Found the specific reservation image!")
                except Exception as e:
                    print(f"Image inside <a> tag did not appear in time: {e}")
                td_elements = []
                for td in await page.query_selector_all(set_tag["tag_name"][3]):
                    td_class = await td.get_attribute("class")
                    if td_class and "ok" in td_class.split():
                        td_elements.append(td)
                found = False
                for td in td_elements:
                    a_tag = await td.query_selector('a')
                    if a_tag:
                        await a_tag.click()
                        bed_type = await page.text_content(set_tag["tag_name"][7])
                        # Get the 'onclick' attribute from the button
                        onclick_value = await page.get_attribute(set_tag["tag_name"][8], "onclick")
                        # Extract the date from the onclick string
                        match = re.search(r"vacancyReserve\('.*?','(\d{8})'", onclick_value)
                        if match:
                            date_value = match.group(1)
                        else:
                            date_value = None
                        await page.wait_for_selector(set_tag["tag_name"][4], timeout=10000)
                        await page.click(set_tag["tag_name"][4])
                        print("Reservation found and clicked!")
                        line_success = line_bot(bed_type, date_value)
                        if(line_success):
                            print("success send line msg!")
                        found = True
                        try:
                            await page.wait_for_selector(set_tag["tag_name"][5], timeout=None)
                            await page.click(set_tag["tag_name"][5])
                            found = False
                        except Exception as e:
                            print(f"Could not close vacancy modal: {e}")
                        break
                if found:
                    break  # Exit the loop if reservation is successful
                try:
                    await page.wait_for_selector(set_tag["tag_name"][5], timeout=None)
                    await page.click(set_tag["tag_name"][5])
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