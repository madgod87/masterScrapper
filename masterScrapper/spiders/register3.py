import scrapy
import requests

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
                pay_date = tree.xpath('.//td[2]/font/text()').get()
                amount = tree.xpath('.//td[3]/font/text()').get()

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
    
                    request_object = requests.get(final_link)
                    response_object = scrapy.Selector(request_object)
            # Declaring All Tree Elements
                    child_trees = response_object.xpath('//*[@id="ContentPlaceHolder1_grdShowRecords"]//tr')
            # Looping Over All Tree Elements
                    for child_tree in child_trees:
            # Creating Iterable Item for Checking Attendance Value
                        attendence = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
            # Checking Attendance Value
                        for j in attendence:
                            attendence_check = child_tree.xpath('.//th[$j]//text()', j=j).get()
                            if attendence_check == "Total Attendance":
            # Assigning & Declaring Global Attendance Value
                                global i
                                i = j
            # Declaring Name Value
                        name = child_tree.xpath('.//td[2]//text()').get()
            # Checking & Skipping Unwanted Name Values
                        if name is None or name == "Daily Attendence":
                            print('REJECTED')
            # Assigning Other Values with Global Attendance Value
                        else:
            # Declaring Values of New Page
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
                            jc_number = child_tree.xpath('.//td[2]//a/text()').get()
                            total_md = str((child_tree.xpath('.//td[$i]//text()', i=i).get()).split()[0])
                            wage_per_day = child_tree.xpath('.//td[$i+1]//text()', i=i).get()
                            total_amount = str((child_tree.xpath('.//td[$i+2]//text()', i=i).get()).split()[0])
                            wagelist_number = str((child_tree.xpath('.//td[$i+9]//text()', i=i).get()).split()[0])
            # Providing Output
                            yield {
                                'mr_pre_number':mr_pre_number,
                                'amount':amount,
                                'jc_number':jc_number,
                                'name':name,
                                'date_from_which_work_demanded':start_date,
                                'demanded_days':demanded_days,
                                'scheme_code':scheme_code,
                                'mr_number':mr_number,
                                'start_date':start_date,
                                'end_date':end_date,
                                'total_md':total_md,
                                'pay_date':pay_date,
                                'total_amount':total_amount,
                                'scheme_name':scheme_name,
                                'as_approve_number':as_approve_number,
                                'as_approval_date':as_approval_date,
                                'mb_number':mb_number,
                                'mb_page_number':mb_page_number,
                                'wage_per_day':wage_per_day,
                                'wagelist_number':wagelist_number
                                }

