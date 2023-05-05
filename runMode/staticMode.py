import os
from datetime import datetime
import pandas as pd
from dataCollection.common import CommonModule
from dataProcessing.process import ProcessModule
from dataVisualization.html import HTMLVisualize
from dataVisualization.visualize import VisualizeModule


def run():

    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    pwd = os.getcwd()  # "/Users/Manisha/Documents/github/ManishaMatta/SP500/"
    print("Current working directory", pwd)
    html_dir = os.path.join(os.path.join(pwd, "resources"), "html")
    os.system("rm -r -f %s/*" % html_dir)
    # os.rmdir(html_dir)
    os.makedirs(html_dir) if not os.path.exists(html_dir) else print("Directory %s recreated for current run" % html_dir)

    resource_path = os.path.join(os.path.abspath(__file__).split('runMode')[0], "resources")

    print("**************************** DataSet 1-1 ****************************")
    sp_df11 = CommonModule.csv_reader("%s/dataset11.csv" % resource_path).set_index('CompanyName')
    print(sp_df11.head(5))
    print("Total Record Count: ", len(sp_df11), " * ", len(sp_df11.columns))

    print("**************************** DataSet 1-2 ****************************")
    sp_df12 = CommonModule.csv_reader("%s/dataset12.csv" % resource_path).set_index('Date')
    print(sp_df12.head(5))
    print("Total Record Count: ", len(sp_df12), " * ", len(sp_df12.columns))

    print("**************************** DataSet 1-3 ****************************")
    sp_df13 = CommonModule.csv_reader("%s/dataset13.csv" % resource_path).set_index('Date')
    print(sp_df13.head(5))
    print("Total Record Count: ", len(sp_df13), " * ", len(sp_df13.columns))

    print("**************************** DataSet 2 ****************************")
    sp_df2 = CommonModule.csv_reader("%s/dataset2.csv" % resource_path).set_index('Date')
    print(sp_df2.head(5))
    print("Total Record Count: ", len(sp_df2), " * ", len(sp_df2.columns))

    print("**************************** DataSet 3 ****************************")
    sp_df3 = CommonModule.csv_reader("%s/dataset3.csv" % resource_path).set_index('Name')
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
# run()       # 1375 secs
# end_time = datetime.now().strftime("%Y%m%d%H%M%S")
# print("run time : ", (int(end_time)-int(start_time)))
