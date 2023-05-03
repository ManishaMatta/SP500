import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta


class CollectionModule:
    cmpy_short_names = []     # global variable to store company names

    @staticmethod
    # function to get the api output when weblink and the json path to process are passed
    def ds_api(web_link, json_path='', mode='d'):
        print("Fetching data from <%s> API ... " % web_link)
        req = requests.get(web_link)     # requesting the data from weblink
        if req.status_code == 200:     # checking if the request is valid
            df = pd.DataFrame(req.json()) if len(json_path) == 0 else pd.DataFrame(req.json()[json_path])   # capturing the json data from the link
            return df if mode == 'd' else df.head(500)     # returning the dataframe based on the run mode

    @staticmethod
    # function to extract company stock data from yahoo finance
    def company_yahoo_hist(cmpy_names):
        print("Fetching data from yahoo finances for %s ... " % cmpy_names)
        company_dtls = pd.DataFrame({'Date': [datetime.now().strftime("%Y-%m-%d")]})    # creating a dataframe with current date column
        company_dtls['Date'] = pd.to_datetime(company_dtls['Date'])     # casting the Date column to datetime
        for cmpy in cmpy_names:     # iterating through the list of companies
            end_date = date.today() - timedelta(days=2)
            start_date = end_date - timedelta(days=100)
            cmp_df = yf.download(tickers=cmpy, start=start_date, period='100d', end=end_date, interval='1d')[['Close', 'Volume']].add_prefix(cmpy+"_")     # downloading the stock details of the company for 100 days # period='100d'
            if company_dtls.columns.size == 1:     # checking if the df has 1 column
                company_dtls = company_dtls.merge(cmp_df, on='Date', how='outer').set_index('Date')     # merging the dataframe into the combined dataframe for 1st run
            else:
                company_dtls = company_dtls.merge(cmp_df, on='Date', how='outer')     # merging the dataframe into the combined dataframe
        company_dtls = company_dtls.sort_index()
        company_dtls = company_dtls[company_dtls.index < pd.to_datetime(end_date)]
        return company_dtls     # returning the combined dataframe

    @staticmethod
    # function to scrap a webpage when the link is provided
    def ds_wscrap(link, href, mode='d', cmpy_names=''):
        print("Fetching data by Web Scraping from %s ... " % link)
        if cmpy_names is None:     # if cmpy_names is None set as empty list
            cmpy_names = []
        ds1_link = link + href     # appending the link with href for scraping the data
        sp_company_dtls = []     # initializing the output list
        cmpy_df = pd.DataFrame()     # initializing the output dataframe
        sp_res = requests.get(ds1_link)     # requesting the data from weblink
        if sp_res.status_code == 200:     # checking if the request is valid
            sp_parser = BeautifulSoup(sp_res.content, 'html.parser')     # parsing the returned HTML with BeautifulSoup
            for sp_cmpy in sp_parser.findAll("div", {"class": "graviton"}):     # iterating through div tag with class:graviton
                try:
                    if sp_cmpy.find("h2").get_text().strip() == "Realtime Prices for S&P 500 Stocks":     # checking if the header value has the mentioned string
                        pages = sp_cmpy.find("div", {"class": "margin-top--small"})     # checking the number of pages in the table
                        total_pg = 0 if mode == 's' else pages.find_all("li", {"class": "pagination__item"})[-1].get("data-pagination-page")     # assigning the max browsing pages based on run mode
                        for i in range(1, int(total_pg) + 2):     # iterating through the pages
                            print("Extracting ", ds1_link + "?p=%s&" % i, "...")
                            sck_dtls = CollectionModule.stock_details(link, ds1_link + "?p=%s&" % i, cmpy_names)     # extracting the stock details in the page
                            sp_company_dtls = sp_company_dtls + sck_dtls[0]     # Appending the details to the output list
                            CollectionModule.cmpy_short_names += sck_dtls[1]     # capturing the company short name
                except:
                    continue
            cmpy_df = CollectionModule.company_yahoo_hist(CollectionModule.cmpy_short_names[:10])     # downloading the first 10 company details from yahoo finances
            if len(CollectionModule.cmpy_short_names) > 10:     # Adding a note if teh company list is more than 10 as we are trimming the dataset
                print("Filtering only the first 10 companies to avoid cramped data for analysis, Please repeat this step to get all data")
        return sp_company_dtls, cmpy_df     # returning the output from scraping and yahoo finances regarding the index value of S&P 500

    @staticmethod
    # function to retrieve the individual company stock details
    def stock_details(link, ds_link, cmpy_names):
        sp_res = requests.get(ds_link)     # requesting the data from weblink
        sp_company = []     # initializing the output list for stock details
        cmpy_short_names = []     # initializing the output list for company name
        if sp_res.status_code == 200:     # checking if the request is valid
            sp_parser = BeautifulSoup(sp_res.content, 'html.parser')     # parsing the returned HTML with BeautifulSoup
            for sp_cmpy in sp_parser.findAll("div", {"class": "graviton"}):     # iterating through tag div with class:graviton
                try:
                    valid_header = sp_cmpy.find("h2").get_text().strip()     # extracting the header value
                except:
                    continue
                if valid_header == "Realtime Prices for S&P 500 Stocks":     # checking if the header in the string
                    for line in sp_cmpy.find_all("tr"):     # finding the table tags
                        try:
                            cname = line.find("a").get_text().strip()     # getting the text data for a tag in the table
                        except:
                            continue
                        if (len(cmpy_names) == 0) or (cname.lower().strip() in [c.lower().strip() for c in cmpy_names]):     # if the company name is passed in the list
                            values = ()     # initializing a tuple for storing each stock detail
                            if line.find("td", {"class": "table__td"}):     # identifying if there are rows in the table
                                for val in line.find_all("td", {"class": "table__td text-right"}):     # if the table has rows
                                    values += (val.get_text().strip(),)     # updating the tuple with table content
                                c_snapshot = CollectionModule.company_details(link, line.find("a").get("href").strip())     # capturing the forcast details of the company
                                sp_company.append((cname, *values, *c_snapshot))     # combining all the retrieved data
                                cmpy_short_names.append(c_snapshot[0])     # appending the company short name to the list
                            else:
                                continue
                        else:
                            continue
                else:
                    continue
        else:
            print("error response while retrieving web page")
        return sp_company, cmpy_short_names     # returning the company details with the company name

    @staticmethod
    # function to extract the forcast details of the company
    def company_details(link, href):
        cmpy_dtls = ()     # initializing an output tuple to capture the forcast values
        snapshot_dtls = ["Volume", "B", "M", "Dividend", "Yield", "P/E", "Free", "EPS", "Book", "Cash"]     # fields to be extracted from the webpage
        try:
            req = requests.get(link + href)     # requesting the data from weblink
            if req.status_code == 200:     # checking if the request is valid
                parser = BeautifulSoup(req.content, 'html.parser')     # parsing the returned HTML with BeautifulSoup
                cmpy_short_name = parser.find("span", {"class": "price-section__category"}).find("span").get_text()[2:]     # retrieving the company name
                cmpy_dtls += (cmpy_short_name,)     # Updating the company details with the name
                sdict = {}
                if parser.find("div", {"class": "snapshot"}):     # identifying the div tag with class as snapshot
                    for s in parser.findAll("div", {"class": "snapshot__data-item"}):     # identifying the div tag with class as snapshot__data-item
                        ss = s.getText().strip().split()     # splitting the data to get its value
                        sdict[ss[1]] = ss[0]     # adding its details to the dict
                    for s in snapshot_dtls:     # iterating through the dict to get the specific values
                        cmpy_dtls += (sdict.get(s, ''),)     # updating the details to the output tuple
                else:
                    for s in snapshot_dtls:     # iterating through the dict to get the specific values
                        cmpy_dtls += (sdict.get(s, ''),)
                article_tag = parser.find("h3", {"class": "instrument-stories__title"}).find("a")     #
                article = article_tag.getText().strip().replace(':', '') + " : " + link + article_tag.get("href").strip()     # identifying the header tag with class as instrument-stories__title
                cmpy_dtls += (article,)     # updating with the article details
                for fcast in parser.findAll("details", {"class": "fontsize-12 border-white margin-top--smaller padding-left--smaller"}):     # capturing the forcast details mentioned by analysts
                    cmpy_dtls += (fcast.get_text().strip().split("\n")[-1].strip(),)     # appending the details into the tuple
        except:
            print("Error accessing specific cmpy page")
        return cmpy_dtls     # returning the output tuple with the company related data
