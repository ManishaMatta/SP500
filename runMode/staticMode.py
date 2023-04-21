import os
from datetime import datetime
import pandas as pd
from dataCollection.common import CommonModule
from dataVisualization.visualize import ProcessModule


def run():

    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    mode = 'static'

    print("**************************** DataSet 1-1 ****************************")
    sp_df11 = CommonModule.csv_reader("%s/resources/dataset11.csv" % os.getcwd()).set_index('CompanyName')
    print(sp_df11.head(5))
    print("Total Record Count: ", len(sp_df11))

    print("**************************** DataSet 1-2 ****************************")
    sp_df12 = CommonModule.csv_reader("%s/resources/dataset12.csv" % os.getcwd()).set_index('Date')
    print(sp_df12.head(5))
    print("Total Record Count: ", len(sp_df12))

    print("**************************** DataSet 1-3 ****************************")
    sp_df13 = CommonModule.csv_reader("%s/resources/dataset13.csv" % os.getcwd()).set_index('Date')
    print(sp_df13.head(5))
    print("Total Record Count: ", len(sp_df13))

    print("**************************** DataSet 2 ****************************")
    sp_df2 = CommonModule.csv_reader("%s/resources/dataset2.csv" % os.getcwd()).set_index('Date')
    print(sp_df2.head(5))
    print("Total Record Count: ", len(sp_df2))

    print("**************************** DataSet 3 ****************************")
    sp_df3 = CommonModule.csv_reader("%s/resources/dataset3.csv" % os.getcwd()).set_index('Name')
    print(sp_df3.head(5))
    print("Total Record Count: ", len(sp_df3))

    print("**************************** Analysis ****************************")

    pwd = os.getcwd()
    os.system("mkdir %s/resources/output/%s/" % (pwd, mode))
    ProcessModule.process_df1(mode, sp_df11, sp_df12, sp_df13)
    ProcessModule.process_df3(mode, sp_df3, sp_df11)
    # ProcessModule.process_df2(sp_df11)
    # ProcessModule.process_all(sp_df11)



# start_time = datetime.now().strftime("%-Y%m%d%H%M%S")
# run()
# end_time = datetime.now().strftime("%-Y%m%d%H%M%S")
# print("run time : ", (int(end_time)-int(start_time)))     # 6 secs
