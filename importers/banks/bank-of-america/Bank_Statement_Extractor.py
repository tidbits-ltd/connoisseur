"""
So far this script only works with Bank of America.

Notes:
    - This program works only when the landing page is like screenshot1
    - This program works only when a verification code is requested
    - This program works only when the user takes control and enters the verification code
        and also selects the account they want the statements for
    - This program works only downloads the statements for the default year (which is the current year) that
        is selected by the webpage (Right now it is by defualt 2020 and so this program downloads only the statements
        from 2020)
    - There are some warnings that get printed to the console, but from my research it seems we can ignore them because
        they don't really affect the execution of the program
    - This program downloads the statement pdfs to the default download folder of chrome

TO DO:
- Solution for when the landing page is different that screenshot1. (I haven't managed to
get a screenshot of the other landing page)
- Research if verification will always be needed with this program and if it won't be we need
to implement a solution for when the verification page is not shown
- Solution to download statements for all the years
- Separate BankStatementExtractor.access_page(self,bank_url) into different methods within the class
- Be able to specify the folder you want to download the statements to
"""
from pyppeteer import launch
import os

class BankStatementExtractor:

    def __init__(self, bank_url,online_id,password):
        self.bank_url = bank_url
        self.online_id = online_id
        self.password = password
        self.browser = None
        self.page = None
        self.context = None

    async def access_page(self, bank_url):
        # Launching the browser
        self.browser = await launch(options={'headless': False})
        self.context = await self.browser.createIncognitoBrowserContext()
        self.page = await self.context.newPage()

        #going to the Bank Website
        await self.page.goto(url=bank_url)

        await self.page.screenshot({'path': 'screenshot2.png', 'fullself.page': True}) #This is here to take the screenshot just in case the other login page appears

        # Typing in the online_id and password and pressing Login when landing page is like screenshot1
        # (there is another landing page that comes up once in a while)
        await self.page.click(selector='div.hide-for-large-up')
        await self.page.waitForSelector(selector='#onlineId1')
        online_id_field = await self.page.querySelector(selector='#onlineId1')
        pass_id_field = await self.page.querySelector(selector='#passcode1')
        await online_id_field.click()
        await online_id_field.type(text=self.online_id)
        await pass_id_field.type(text=self.password)
        await self.page.click(selector='div.medium-2.columns')
        await self.page.waitForNavigation()

        # checking if we need verification and verifying if need be
        verify_button = await self.page.querySelector(selector='#btnARContinue > span:nth-child(1)')
        if verify_button != None:  # If it is None that means we don't need to verify
            number_selector = await self.page.querySelector(
                selector='#RequestAuthCodeForm > div:nth-child(4) > label > b')
            number = await self.page.evaluate('(element) => element.textContent', number_selector)
            await self.page.click(selector='#btnARContinue')
            print(f"A text message has been sent {str(number).strip()} for verification")
            input(
                'Please go on the Chrome browser and enter verification code, select the account you want all statements to'
                'be downloaded for and then press enter')

        #We Assume that the user has already clicked the account that they want the statements downloaded for
        #Here we click the statements and documents tab > select view all statements > go thourgh all statements visible there
            #and download to google chrome's default download directory.
        # NOTE: This is only done for whatever year that is by default selected when the account is selected. NOT ALL YEARS
        await self.page.waitForSelector(selector='[name="statements_and_documents"]')
        await self.page.click(selector='[name="statements_and_documents"]')
        await self.page.waitForSelector(selector='[id="ecc-accordionPanel0"]')
        await self.page.waitFor(4000)  # Need to find the least amount of time to wait for this to work
        await self.page.click(selector='[id="ecc-accordionPanel0"]')
        await self.page.waitForSelector(
            selector='#ecc-accordionPanel0 > div > div.content > div > div > div.block-grid > div')
        await self.page.waitFor(2000)  # Need to find the least amount of time to wait for this to work
        all_statements_for_curr_year = len(
            await self.page.xpath(expression='//*[@id="ecc-accordionPanel0"]/div/div[2]/div/div/div[1]/div'))
        download_links = await self.page.xpath(expression='//*[@id="downloadPDFAccLink"]')
        for index in range(0, all_statements_for_curr_year):
            await download_links[index].click()
            await download_links[index].click()
            await self.page.waitFor(2000)


    async def put_together(self):
        await self.access_page(self.bank_url)







