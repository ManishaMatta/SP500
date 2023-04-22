import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import timedelta, datetime


class CommonModule:
    cmpy_short_names = []     # global variable to store company names

    @staticmethod
    # function to generate start and end date from current date when date formate and interval is mentioned
    def date_generator(date_format, interval):
        ed = datetime.now().strftime(date_format)     # getting the current date in the specific formate
        sd = (datetime.now() - timedelta(days=interval)).strftime(date_format)     # getting the prev date based on interval in the specific formate
        return tuple([sd, ed])     # returning the dates as tuple

    @staticmethod
    # function to get the api output when weblink and the json path to process are passed
    def ds_api(web_link, json_path='', mode='d'):
        print("Fetching data from <%s> API ... " % web_link)
        req = requests.get(web_link)     # requesting the data from weblink
        if req.status_code == 200:     # checking if the request is valid
            df = pd.DataFrame(req.json()) if len(json_path) == 0 else pd.DataFrame(req.json()[json_path])   # capturing the json data from the link
            return df if mode == 'd' else df.head(100)     # returning the dataframe based on the run mode

    @staticmethod
    # function to extract company stock data from yahoo finance
    def company_yahoo_hist(cmpy_names):
        print("Fetching data from yahoo finances for %s ... " % cmpy_names)
        company_dtls = pd.DataFrame({'Date': [datetime.now()]})     # creating a df with current date column
        company_dtls['Date'] = company_dtls['Date'].dt.strftime('%Y-%m-%d')
        company_dtls['Date'] = pd.to_datetime(company_dtls['Date'])    # pd.to_datetime(company_dtls['Date'])   .strftime("%-Y-%m-%d")  # casting the Date column to datetime
        for cmpy in cmpy_names:     # iterating through the list of companies
            cmp_df = yf.download(tickers=cmpy, period='100d', interval='1d')[['Close', 'Volume']].add_prefix(cmpy+"_")     # downloading the
            if company_dtls.columns.size == 1:     #
                company_dtls = company_dtls.merge(cmp_df, on='Date', how='outer').set_index('Date')     #
            else:
                company_dtls = company_dtls.merge(cmp_df, on='Date', how='outer')     #
        return company_dtls     #

    @staticmethod
    #
    def ds_wscrap(link, href, mode='d', cmpy_names=''):
        print("Fetching data by Web Scraping from %s ... " % link)     #
        if cmpy_names is None:     #
            cmpy_names = []     #
        ds1_link = link + href     #
        sp_company_dtls = []     #
        cmpy_df = pd.DataFrame()     #
        sp_res = requests.get(ds1_link)     #
        if sp_res.status_code == 200:     #
            sp_parser = BeautifulSoup(sp_res.content, 'html.parser')     #
            for sp_cmpy in sp_parser.findAll("div", {"class": "graviton"}):     #
                try:
                    if sp_cmpy.find("h2").get_text().strip() == "Realtime Prices for S&P 500 Stocks":     #
                        pages = sp_cmpy.find("div", {"class": "margin-top--small"})     #
                        total_pg = 0 if mode == 's' else pages.find_all("li", {"class": "pagination__item"})[-1].get("data-pagination-page")     #
                        for i in range(1, int(total_pg) + 2):     #
                            print("Extracting ", ds1_link + "?p=%s&" % i, "...")     #
                            sck_dtls = CommonModule.stock_details(link, ds1_link + "?p=%s&" % i, cmpy_names)     #
                            sp_company_dtls = sp_company_dtls + sck_dtls[0]     #
                            CommonModule.cmpy_short_names += sck_dtls[1]     #
                except:
                    continue
            cmpy_df = CommonModule.company_yahoo_hist(CommonModule.cmpy_short_names[:10])     #
            if len(CommonModule.cmpy_short_names) > 10:     #
                print("Filtering only the first 10 companies to avoid cramped data for analysis, Please repeat this step to get all data")
        return sp_company_dtls, cmpy_df     #

    @staticmethod
    #
    def stock_details(link, ds_link, cmpy_names):
        sp_res = requests.get(ds_link)     #
        sp_company = []     #
        cmpy_short_names = []     #
        if sp_res.status_code == 200:     #
            sp_parser = BeautifulSoup(sp_res.content, 'html.parser')     #
            for sp_cmpy in sp_parser.findAll("div", {"class": "graviton"}):     #
                try:
                    valid_header = sp_cmpy.find("h2").get_text().strip()     #
                except:
                    continue     #
                if valid_header == "Realtime Prices for S&P 500 Stocks":     #
                    for line in sp_cmpy.find_all("tr"):     #
                        try:
                            cname = line.find("a").get_text().strip()     #
                        except:
                            continue     #
                        if (len(cmpy_names) == 0) or (cname.lower().strip() in [c.lower().strip() for c in cmpy_names]):     #
                            values = ()     #
                            if line.find("td", {"class": "table__td"}):     #
                                for val in line.find_all("td", {"class": "table__td text-right"}):     #
                                    values += (val.get_text().strip(),)     #
                                c_snapshot = CommonModule.company_details(link, line.find("a").get("href").strip())     #
                                sp_company.append((cname, *values, *c_snapshot))     #
                                cmpy_short_names.append(c_snapshot[0])     #
                            else:
                                continue
                        else:
                            continue
                else:
                    continue
        else:
            print("error response while retrieving web page")
        return sp_company, cmpy_short_names     #

    @staticmethod
    #
    def company_details(link, href):
        cmpy_dtls = ()     #
        snapshot_dtls = ["Volume", "B", "M", "Dividend", "Yield", "P/E", "Free", "EPS", "Book", "Cash"]     #
        try:
            req = requests.get(link + href)     #
            if req.status_code == 200:     #
                parser = BeautifulSoup(req.content, 'html.parser')     #
                cmpy_short_name = parser.find("span", {"class": "price-section__category"}).find("span").get_text()[2:]     #
                cmpy_dtls += (cmpy_short_name,)     #
                if parser.find("div", {"class": "snapshot"}):     #
                    sdict = {}     #
                    for s in parser.findAll("div", {"class": "snapshot__data-item"}):     #
                        ss = s.getText().strip().split()     #
                        sdict[ss[1]] = ss[0]     #
                    for s in snapshot_dtls:     #
                        cmpy_dtls += (sdict.get(s, ''),)     #
                article_tag = parser.find("h3", {"class": "instrument-stories__title"}).find("a")     #
                article = article_tag.getText().strip() + " : " + link + article_tag.get("href").strip()     #
                cmpy_dtls += (article,)     #
                # forecast
                for fcast in parser.findAll("details", {"class": "fontsize-12 border-white margin-top--smaller padding-left--smaller"}):     #
                    cmpy_dtls += (fcast.get_text().strip().split("\n")[-1].strip(),)     #
        except:
            print("Error accessing specific cmpy page")
        return cmpy_dtls     #

    @staticmethod
    #
    def csv_writer(dataframe, filename):     #
        # file_path = os.getcwd()+"/resources/"+filename
        dataframe.to_csv(filename)  # index=False     #

    @staticmethod
    #
    def csv_reader(filename):
        # file_path = os.getcwd()+"/resources/"+filename
        dataframe = pd.read_csv(filename)     #
        return dataframe
