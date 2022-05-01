import scrapy
import requests
from scrapy.crawler import CrawlerProcess

links = []
class RegisterscrapperSpider(scrapy.Spider):
    name = 'registerScrapper'
# Bhandaria Kastekumari GP
    start_urls = ['http://mnregaweb4.nic.in/netnrega/writereaddata/citizen_out/MW_3216004003_GP_1920_eng.html']

    mrNumbers = []

# Declaring First Function
    def parse(self, response):
        trees = response.xpath('//table[2]//tr')
# Looping through Each TREE Element
        for tree in trees:
# Finding Scheme Name Element
            workname = tree.xpath('.//td/text()').get()
# Condition to Ignore Scheme Name Element
            if workname == " Work Name:":
                print('Skipped!!')
# Main Scrapper Section
            else:
                link = tree.xpath('.//td[1]/font/a/@href').get()
                mr_pre_number = tree.xpath('.//td[1]/font/a/text()').get()

                if mr_pre_number not in self.mrNumbers:

                    self.mrNumbers.append(mr_pre_number)
    
    # Converting Link into String
                    strlink = str(link)
    # Deducting the first 6(../../) characters from the link
                    new_str_link = strlink[6:]
    # Converting & Declaring Prefix of the Link
                    mainlink = str("http://mnregaweb4.nic.in/netnrega/")
    # Concatinating Both Links
                    final_link = f"{mainlink}{new_str_link}"

                    links.append(final_link)

        link_length = len(links)
        if link_length>1000:
            pass

class SingleScrapper(scrapy.Spider):
    name = 'singleScrapper'
    def parse(self, counter, counterMax):
        for link in links:
            if counter<counterMax:
                request_object = requests.get(link)
                response_object = scrapy.Selector(request_object)
                for item in response_object.xpath('//*[@id="ContentPlaceHolder1_grdShowRecords"]//tr'):
                    attendence = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
                    for j in attendence:
                        attendence_check = item.xpath('.//th[$j]//text()', j=j).get()
                        if attendence_check == "Total Attendance":
                            global i
                            i = j
                    name = item.xpath('.//td[2]//text()').get()
                    if name is None or name == "Daily Attendence":
                        print('REJECTED')
                    else:
                        demanded_days = i - 5
                        mr_number = response_object.xpath('//*[@id="ContentPlaceHolder1_lblMsrNo2"]/text()').get()
                        start_date = response_object.xpath('//*[@id="ContentPlaceHolder1_lbldatefrom"]/text()').get()
                        end_date = response_object.xpath('//*[@id="ContentPlaceHolder1_lbldateto"]/text()').get()
                        as_approve_number = response_object.xpath('//*[@id="ContentPlaceHolder1_lblSanctionno"]/text()').get()
                        as_approval_date = response_object.xpath('//*[@id="ContentPlaceHolder1_lblSanctionDate"]/text()').get()
                        scheme_code = response_object.xpath('//*[@id="ContentPlaceHolder1_lblWorkCode"]/text()').get()
                        scheme_name = response_object.xpath('//*[@id="ContentPlaceHolder1_lblWorkName"]/text()').get()
                        mb_number = response_object.xpath('//*[@id="ContentPlaceHolder1_mbno"]/text()').get()
                        mb_page_number = response_object.xpath('//*[@id="ContentPlaceHolder1_page_no"]/text()').get()
                        jc_number = item.xpath('.//td[2]//a/text()').get()
                        payment_date = item.xpath('.//td[$i+11]//text()', i=i).get()
                        total_md = str((item.xpath('.//td[$i]//text()', i=i).get()).split()[0])
                        wage_per_day = item.xpath('.//td[$i+1]//text()', i=i).get()
                        total_amount = str((item.xpath('.//td[$i+5]//text()', i=i).get()).split()[0])
                        wagelist_number = str((item.xpath('.//td[$i+9]//text()', i=i).get()).split()[0])
                        yield {
                            'jc_number':jc_number,
                            'name':name,
                            'date_from_which_work_demanded':start_date,
                            'demanded_days':demanded_days,
                            'scheme_code':scheme_code,
                            'mr_number':mr_number,
                            'start_date':start_date,
                            'end_date':end_date,
                            'payment_date':payment_date,
                            'total_md':total_md,
                            'total_amount':total_amount,
                            'scheme_name':scheme_name,
                            'as_approve_number':as_approve_number,
                            'as_approval_date':as_approval_date,
                            'mb_number':mb_number,
                            'mb_page_number':mb_page_number,
                            'wage_per_day':wage_per_day,
                            'wagelist_number':wagelist_number
                            }

scrapper1 = SingleScrapper()
scrapper2 = SingleScrapper()
Scrapper3 = SingleScrapper()
Scrapper4 = SingleScrapper()
Scrapper5 = SingleScrapper()
Scrapper6 = SingleScrapper()
Scrapper7 = SingleScrapper()
Scrapper8 = SingleScrapper()
Scrapper9 = SingleScrapper()
Scrapper10 = SingleScrapper()
Scrapper11 = SingleScrapper()
Scrapper12 = SingleScrapper()
Scrapper13 = SingleScrapper()

process = CrawlerProcess()
process.crawl(scrapper1.parse(1, 201))
process.crawl(scrapper2.parse(201, 401))
process.crawl(Scrapper3.parse(401, 601))
process.crawl(Scrapper4.parse(601, 801))
process.crawl(Scrapper5.parse(801, 1001))
process.crawl(Scrapper6.parse(1001, 1201))
process.crawl(Scrapper7.parse(1201, 1401))
process.crawl(Scrapper8.parse(1401, 1601))
process.crawl(Scrapper9.parse(1601, 1801))
process.crawl(Scrapper10.parse(1801, 2001))
process.crawl(Scrapper11.parse(2001, 2201))
process.crawl(Scrapper12.parse(2201, 2401))
process.crawl(Scrapper13.parse(2401, 2601))
process.start()