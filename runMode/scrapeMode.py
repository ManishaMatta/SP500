import os
from datetime import datetime
import pandas as pd
from dataCollection.collect import CollectionModule
from dataCollection.common import CommonModule
from dataProcessing.process import ProcessModule
from dataVisualization.html import HTMLVisualize
from dataVisualization.visualize import VisualizeModule


def run(sp_cmpy=''):
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    pwd = os.getcwd()   # "/Users/Manisha/Documents/github/ManishaMatta/SP500/"
    print("Current working directory", pwd)
    html_dir = os.path.join(os.path.join(pwd, "resources"), "html")
    os.system("rm -r -f %s/*" % html_dir)
    # os.removedirs(html_dir)
    os.makedirs(html_dir) if not os.path.exists(html_dir) else print("Directory %s recreated for current run" % html_dir)

    link = "https://markets.businessinsider.com"

    # faang => Meta (META) (formerly known as Facebook), Amazon (AMZN), Apple (AAPL), Netflix (NFLX); and Alphabet (GOOG) (formerly known as Google).
    faang_list = ['Meta Platforms', 'Amazon', 'Apple', 'Netflix Inc', 'Alphabet A']
    default_list = ['3M', 'Accenture', 'Amazon', 'Apple', 'American Water Works']
    cmpy_list = default_list if len(sp_cmpy) == 0 else faang_list if sp_cmpy.lower() == 'faang' else sp_cmpy.split(',')

    print("**************************** DataSet 1-1 ****************************")
    sp_val1 = CollectionModule.ds_wscrap(link, '/index/s&p_500', 's', cmpy_list)
    sp_df11 = pd.DataFrame(sp_val1[0], columns=['CompanyName', 'PreviousClose', 'LastUpdated', 'PercentChange', 'ChangeInPrice', 'TradeTime', 'CompanyShortName', 'Volume', 'MarketCap', 'NumberofShares', 'Dividend', 'DividendYield', 'PERatio', 'FreeFloatinP', 'EPS2023', 'BookValuePerShare', 'CashFlowPerShare', 'NewsArticle', 'BuySellHold', '52WeekLow', '52WeekHigh', 'Forecast']).set_index('CompanyName')
    print(sp_df11.head(5))
    print("Total Record Count: ", len(sp_df11), " * ", len(sp_df11.columns))

    print("**************************** DataSet 1-2 ****************************")
    dts = CommonModule.date_generator("%Y%m%d", 1)
    dte = CommonModule.date_generator("%Y%m%d", 21)
    sp_df12 = CollectionModule.ds_api('https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=Index&tkData=1059,998434,1059,333&from=%s&to=%s' % (dte[0], dts[0]), mode='s')
    sp_df12['Date'] = sp_df12['Date'].str[:10]
    sp_df12 = sp_df12.set_index('Date')
    print(sp_df12.head(5))
    print("Total Record Count: ", len(sp_df12), " * ", len(sp_df12.columns))

    print("**************************** DataSet 1-3 ****************************")
    sp_df13 = sp_val1[1]
    print(sp_df13.head(5))
    print("Total Record Count: ", len(sp_df13), " * ", len(sp_df13.columns))

    print("**************************** DataSet 2 ****************************")
    print("Please uncomment them while execution as the api access is limited for a month")
    dt2 = CommonModule.date_generator("%Y-%m-%d", 5)
    sp_df2 = CollectionModule.ds_api('http://api.mediastack.com/v1/news?access_key=92f63d9d5b9f1ead582b49351a664e71&categories=business&keywords=S&P 500&countries=us&languages=en&date=%s,%s&limit=100' % (dt2[0], dt2[1]), json_path='data', mode='s')
    sp_df2['Date'] = sp_df2['published_at'].str[:10]
    sp_df2 = sp_df2.set_index('Date')
    print(sp_df2.head(5))
    print("Total Record Count: ", len(sp_df2), " * ", len(sp_df2.columns))

    # **************************** DataSet 2 ****************************
    # author                                                                                        title                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   description                                                                                                                                                   url                                 source                                                                               image  category language country               published_at
    # Date
    # 2023-04-10        Reuters                  J&J talc unit 2nd bankruptcy must be dismissed, cancer victims’ lawyers say                                                                                                       Johnson & Johnson&#8217;s renewed effort to resolve talc lawsuits through an $8.9 billion bankruptcy settlement must be dismissed as a &#8220;fraudulent scheme&#8221; that defies a court order rejecting the company&#8217;s previous attempt to settle the litigation, according to a court filing from lawyers representing cancer victims. The attorneys, in the filing on Monday, denounced J&J&#8217;s [&#8230;]                                   https://financialpost.com/pmn/business-pmn/jj-talc-unit-2nd-bankruptcy-must-be-dismissed-cancer-victims-lawyers-say  Financial Post | Canada Business News                                                                                None  business       en      us  2023-04-10T18:15:47+00:00
    # 2023-04-10        Reuters                                  Wall Street ends mixed with inflation data, earnings on tap                                                                                                                                          NEW YORK, April 10 (Reuters) &#8211; U.S. stock indexes clawed back from steep losses to a mixed close on Monday as investors digested Friday&#8217;s employment report and prepared for an eventful week of inflation data and bank earnings. Megacap momentum stocks dragged the tech-heavy Nasdaq slightly lower, while industrials helped boost the blue-chip Dow into [&#8230;]                                               https://financialpost.com/pmn/business-pmn/wall-street-ends-mixed-with-inflation-data-earnings-on-tap-2  Financial Post | Canada Business News                                                                                None  business       en      us  2023-04-10T20:21:01+00:00
    # 2023-04-10  Business Wire                                                        Coeur to Present at Gold Forum Europe                                                                                                                                     CHICAGO &#8212; Coeur Mining, Inc.’s (“Coeur” or the “Company”) (NYSE: CDE) Senior Vice President and Chief Financial Officer, Thomas S. Whelan, will present at Gold Forum Europe in Zurich, Switzerland on Tuesday, April 11, 2023 at 2:10 p.m. Central European Time. The Gold Forum Europe is an invitation-only investment conference. Presentation materials will be made [&#8230;]                                https://financialpost.com/pmn/press-releases-pmn/business-wire-news-releases-pmn/coeur-to-present-at-gold-forum-europe  Financial Post | Canada Business News                                                                                None  business       en      us  2023-04-10T20:30:35+00:00
    # 2023-04-11    Kamal Saini  Vaping: A Safe Alternative But This Could Make It More Toxic Leading To Worse Lung Function  A better, safer choice for someone seeking to give up smoking traditional tobacco products may be switching to e-cigarettes. But, it&#8217;s crucial to fully understand the advantages and disadvantages of e-cigarettes before using them. In a report published today in Respiratory Research, researchers from the University of Pittsburgh have found that the addition of mint [&#8230;]The post Vaping: A Safe Alternative But This Could Make It More Toxic Leading To Worse Lung Function appeared first on Revyuh.  https://www.revyuh.com/news/lifestyle/health-and-fitness/vaping-a-safe-alternative-but-this-could-make-it-more-toxic-leading-to-worse-lung-function/                           Revyuh Media                                                                                None  business       en      us  2023-04-11T00:00:00+00:00
    # 2023-04-11  BusinessWorld                     Discussion needed on how US can use Philippines bases – foreign minister                  WASHINGTON &#8211; Washington and Manila will need to discuss what the US may do with its access to certain military bases in the Philippines, Filipino Foreign Minister Enrique Manalo said on Monday. The Philippines last week identified four more military bases that the US may access amid shared concerns about China&#8217;s growing might. Speaking a day before the first combined meeting of US and Philippine foreign and defense ministers in seven years, Manalo urged dialogue and [&#8230;]                     https://www.bworldonline.com/the-nation/2023/04/11/515834/discussion-needed-on-how-us-can-use-philippines-bases-foreign-minister/                         Business World  https://www.bworldonline.com/wp-content/uploads/2023/04/enrique-manalo-300x169.jpg  business       en      us  2023-04-11T02:20:02+00:00
    # Total Record Count:  10

    print("**************************** DataSet 3 ****************************")
    sp_df3 = CollectionModule.ds_api(web_link='https://pkgstore.datahub.io/core/s-and-p-500-companies-financials/constituents-financials_json/data/ddf1c04b0ad45e44f976c1f32774ed9a/constituents-financials_json.json', mode='s').set_index('Name')
    sp_df3 = sp_df3[sp_df3['Symbol'].isin(CollectionModule.cmpy_short_names+['FB'] if 'META' in CollectionModule.cmpy_short_names else CollectionModule.cmpy_short_names)]
    print(sp_df3.head(5))
    print("Total Record Count: ", len(sp_df3), " * ", len(sp_df3.columns))

    print("**************************** Analysis ****************************")

    sp_df4 = ProcessModule.process_df(sp_df3, sp_df11)

    print("Executing LSTM prediction model S&P 500...")
    mse1 = ProcessModule.prediction_model_lstm(sp_df12, path=html_dir)
    print("Executing LSTM prediction model Individual Companies...")
    msec1 = ProcessModule.prediction_model_cmpy(sp_df13, 'lstm', path=html_dir)
    print("Executing LR prediction model S&P 500...")
    mse2 = ProcessModule.prediction_model_lin(sp_df12, path=html_dir)
    print("Executing LR prediction model Individual Companies...")
    msec2 = ProcessModule.prediction_model_cmpy(sp_df13, 'lin', path=html_dir)
    mse = "Better precision is received by using LSTM model as Mean squared error is : "+str(round(mse1, 3)) if mse1 < mse2 else "Better precision is received by using Linear Regression model as Mean squared error is : "+str(round(mse2, 3))

    print("Executing Trend Analysis model...")
    ProcessModule.trend_analysis(sp_df11, path=html_dir)  # do for ds 13
    VisualizeModule.visualize_sp(sp_df11, sp_df12, sp_df13, path=html_dir)
    print("Executing Correlation Statistical model...")
    ProcessModule.statistical_model(sp_df4, path=html_dir)  # add graph
    VisualizeModule.visualize_src(sp_df4, path=html_dir)
    print("Executing Sentiment Analysis...")
    ProcessModule.sentiment_analysis(sp_df11, sp_df2, path=html_dir)  # dataset - 11,2
    print("Generating the webpage...")
    HTMLVisualize.publish_html(pwd, html_dir, mse, (mse1, msec1, mse2, msec2))


# start_time = datetime.now().strftime("%Y%m%d%H%M%S")
# run()
# end_time = datetime.now().strftime("%Y%m%d%H%M%S")
# print("run time : ", (int(end_time)-int(start_time)))    # 11 secs # 948 secs

# Writing df into csv file
# os.system("mkdir ../resources/")
# CommonModule.csv_writer(sp_df11, "../resources/dataset11.csv")
