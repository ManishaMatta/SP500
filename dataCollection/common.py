import numpy as np
import pandas as pd
from datetime import timedelta, datetime


class CommonModule:

    @staticmethod
    # function to generate start and end date from current date when date formate and interval is mentioned
    def date_generator(date_format, interval):
        ed = datetime.now().strftime(date_format)     # getting the current date in the specific formate
        sd = (datetime.now() - timedelta(days=interval)).strftime(date_format)     # getting the prev date based on interval in the specific formate
        return tuple([sd, ed])     # returning the dates as tuple

    @staticmethod
    # function to write a dataframe into a csv file mentioned
    def csv_writer(dataframe, filename):
        # file_path = os.getcwd()+"/resources/"+filename
        dataframe.to_csv(filename)  # index=False     # saving the dataframe as csv

    @staticmethod
    # function to read a csv file as a dataframe
    def csv_reader(filename):
        # file_path = os.getcwd()+"/resources/"+filename
        dataframe = pd.read_csv(filename)     # reading the csv as dataframe
        return dataframe

    @staticmethod
    def str_to_date(date_str):
        var = str(date_str).split('-')
        return datetime(year=int(var[0]), month=int(var[1]), day=int(var[2].split(' ')[0]))

    @staticmethod
    def window_df(dataframe, first_date, last_date, n=3):
        first_date = CommonModule.str_to_date(first_date)
        last_date = dataframe.index[-1] if dataframe.index[-1] < CommonModule.str_to_date(last_date) else CommonModule.str_to_date(last_date)
        first_date = first_date if len(dataframe.loc[:first_date]) == n+1 else str(dataframe.head(4).index.values.max())[:10]
        target_date = first_date
        last_time = False
        dates = []
        xx, yy = [], []
        while True:
            df_subset = dataframe.loc[:target_date].tail(n+1)
            if len(df_subset) != n+1:
                print(f'Error: Window of size {n} is too large for date {target_date}')
                return
            values = df_subset['Close'].to_numpy()
            x, y = values[:-1], values[-1]
            dates.append(target_date)
            xx.append(x)
            yy.append(y)
            next_week = dataframe.loc[target_date:].head(7)  # next_week = dataframe.loc[target_date:end_date]   # target_date+timedelta(days=7)
            next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
            next_date_str = next_datetime_str.split('T')[0]
            next_date = CommonModule.str_to_date(next_date_str)
            if last_time:
                break
            target_date = next_date
            if target_date == last_date:
                last_time = True
        ret_df = pd.DataFrame({})
        ret_df['Target Date'] = dates
        xx = np.array(xx)
        for i in range(0, n):
            ret_df[f'Target-{n-i}'] = xx[:, i]
        ret_df['Target'] = yy
        return ret_df

    @staticmethod
    def windowed_df_separate(windowed_dataframe):
        df_as_np = windowed_dataframe.to_numpy()
        dates = df_as_np[:, 0]
        middle_matrix = df_as_np[:, 1:-1]
        x = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))
        y = df_as_np[:, -1]
        return dates, x.astype(np.float32), y.astype(np.float32)

    @staticmethod
    def dataframe_cast(dataframe, column, datatype):
        if dataframe[column].dtype.name == datatype:
            dataframe[column] = dataframe[column]
        else:
            if 'float' in datatype:
                dv = 0.0
            elif 'int' in datatype:
                dv = 0
            elif 'str' in datatype:
                dv = ''
            else:
                dv = np.nan
            dataframe[column] = dataframe[column].str.replace(',', '', regex=True).replace('', dv, regex=False).astype(datatype)
        return dataframe
