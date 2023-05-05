import os
import re
from datetime import datetime
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import spearmanr
from keras.optimizers import Adam
from keras.regularizers import L2
from keras import layers, Sequential
from tensorflow.python.keras.layers import LSTM
from textblob import TextBlob
from matplotlib import pyplot as plt
import seaborn as sns
from copy import deepcopy
from dataCollection.common import CommonModule


class ProcessModule:
    @staticmethod
    def prediction_model_lstm(dataframe, cmpy_name='', name_append='', path=os.getcwd()):
        dataframe = dataframe.sort_index()
        dataframe = dataframe.groupby(['Date']).mean()
        dataframe = dataframe.reset_index()[['Date', 'Close']]
        dataframe['Date'] = dataframe['Date'].apply(CommonModule.str_to_date)
        dataframe.index = dataframe.pop('Date')
        windowed_df = CommonModule.window_df(dataframe, str(dataframe.index.values.min() + np.timedelta64(3, 'D'))[:10], str(dataframe.index.values.max())[:10], n=3)    # (datetime.strptime(dataframe.index.values.min(), "%Y-%m-%d").date() + timedelta(days=3)).strftime('%Y-%m-%d')
        dates, x, y = CommonModule.windowed_df_separate(windowed_df)
        q_80 = int(len(dates) * .8)
        q_90 = int(len(dates) * .9)
        dates_train, x_train, y_train = dates[:q_80], x[:q_80], y[:q_80]
        dates_val, x_val, y_val = dates[q_80:q_90], x[q_80:q_90], y[q_80:q_90]
        dates_test, x_test, y_test = dates[q_90:], x[q_90:], y[q_90:]
        model = Sequential([layers.Input((3, 1)), LSTM(64, return_sequences=True, input_shape=(3, 1)), layers.Dense(32, activation='relu'), layers.Dense(16, activation='relu'), layers.Dense(1)])   # , layers.LSTM(64)
        model.layers[0].kernel_regularizer = L2(0.1)
        print(model.summary())
        model.compile(loss='mse', optimizer=Adam(learning_rate=0.01), metrics=['mean_absolute_error'])
        model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=3*3*10*len(dates_train), batch_size=int(len(dates_train)/3))
        train_predictions = model.predict(x_train).flatten()
        train_predictions = [train_predictions[i] for i in range(0, len(train_predictions)-1) if i % 3 == 0]
        val_predictions = model.predict(x_val).flatten()
        val_predictions = [val_predictions[i] for i in range(0, len(val_predictions)-1) if i % 3 == 0]
        test_predictions = model.predict(x_test).flatten()
        test_predictions = [test_predictions[i] for i in range(0, len(test_predictions)-1) if i % 3 == 0]
        mse = mean_squared_error(y_test, test_predictions)
        print(f'Mean squared error: {mse:.2f}')
        recursive_predictions = []
        recursive_dates = np.concatenate([dates_val, dates_test, [pd.Timestamp(str(dataframe.index.values.max()+np.timedelta64(1, 'D'))[:10]), pd.Timestamp(str(dataframe.index.values.max()+np.timedelta64(2, 'D'))[:10]), pd.Timestamp(str(dataframe.index.values.max()+np.timedelta64(3, 'D'))[:10])]])
        for target_date in recursive_dates:
            last_window = deepcopy(x_train[-1])
            next_prediction = model.predict(np.array([last_window])).flatten()
            next_prediction = [next_prediction[i] for i in range(0, len(next_prediction)-1) if i % 3 == 0]
            recursive_predictions.append(next_prediction)
            last_window[-1] = next_prediction
        fig = plt.figure(figsize=(10, 8))
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in dates_train], train_predictions, 'ro-', alpha=0.3, label='Training Predictions')
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in dates_train], y_train, 'bo-', alpha=0.3, label='Training Observations')
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in dates_val], val_predictions, 'r*-', alpha=0.3, label='Validation Predictions')
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in dates_val], y_val, 'b*-', alpha=0.3, label='Validation Observations')
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in dates_test], test_predictions, 'rD-', alpha=0.3, label='Testing Predictions')
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in dates_test], y_test, 'bD-', alpha=0.3, label='Testing Observations')
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in recursive_dates], recursive_predictions, 'g', label='Recursive Predictions')
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("S&P %s Price Value" % cmpy_name)
        plt.legend(loc="upper right")
        plt.title("S&P %s Prediction using LSTM Model" % cmpy_name)
        fig.savefig(os.path.join(path, 'graph_lstm%s.svg' % name_append))     # saving the plot
        # plt.show()
        plt.close()
        return mse

    @staticmethod
    def prediction_model_cmpy(dataframe, model, path=os.getcwd()):
        dataframe_c1 = list(filter(lambda x: '_Close' in x, dataframe.columns.to_list()))     # selecting the dataframe with _close
        mean_square_error = []
        for k in range(0, len(dataframe_c1)):
            cmpy_name = dataframe_c1[k].replace('_Close', '')
            df = dataframe[[dataframe_c1[k]]].rename(columns={dataframe_c1[k]: "Close"})
            if model == 'lstm':
                mean_square_error.append(ProcessModule.prediction_model_lstm(df, cmpy_name=cmpy_name, name_append=("_"+cmpy_name), path=path))
            else:
                mean_square_error.append(ProcessModule.prediction_model_lin(df, cmpy_name=cmpy_name, name_append=("_"+cmpy_name), path=path))
        return sum(mean_square_error)/len(mean_square_error)

    @staticmethod
    def prediction_model_lin(input_dataframe, cmpy_name='', name_append='', path=os.getcwd()):
        input_dataframe = input_dataframe.groupby(level=0).mean()
        input_dataframe = input_dataframe.sort_index()
        dataframe = input_dataframe[['Close']].copy()
        for i in range(1, 4):
            dataframe[f't-{i}'] = dataframe['Close'].shift(i)
        train_size = int(len(dataframe) - 3 * 0.8)
        train_data, test_data = dataframe.iloc[3:train_size], dataframe.iloc[train_size:]
        x_train = train_data.drop('Close', axis=1)
        y_train = train_data['Close']
        x_test = test_data.drop('Close', axis=1)
        y_test = test_data['Close']
        lr_model = LinearRegression()
        lr_model.fit(x_train, y_train)
        y_predict = lr_model.predict(x_test)
        mse = mean_squared_error(y_test, y_predict)
        print(f'Mean squared error: {mse:.2f}')
        future_data = pd.DataFrame(index=pd.date_range(start=input_dataframe.index[-1], periods=4, freq='D'))
        for i in range(1, 4):
            future_data[f't-{i}'] = dataframe['Close'].shift(i).iloc[-1]
        future_prediction = lr_model.predict(future_data)
        print(f'Predicted values for next 3 days: {future_prediction}')
        prediction_df = pd.DataFrame({'Date': pd.date_range(start=input_dataframe.index[-1], periods=4, freq='D'), 'f_Close': future_prediction}).set_index('Date')
        fig = plt.figure(figsize=(10, 8))
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in input_dataframe.index.astype(str)], input_dataframe['Close'].astype(float), 'bo-', alpha=0.3, label='Training/Testing Observations')
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in test_data.index], y_predict, 'rD-', alpha=0.3, label='Testing Predictions')
        plt.plot([datetime.strptime(str(i)[:10], '%Y-%m-%d').date() for i in prediction_df.index.astype(str)], prediction_df['f_Close'].astype(float), 'g', label='LR Model Predictions')
        plt.xticks(rotation=45)
        plt.legend()
        plt.xlabel("Date")
        plt.ylabel("S&P %s Price Value" % cmpy_name)
        plt.legend(loc="upper right")
        plt.title("S&P %s Prediction using Linear Regression Model" % cmpy_name)
        fig.savefig(os.path.join(path, 'graph_lr%s.svg' % name_append))     # saving the plot
        # plt.show()
        plt.close()
        return mse

    @staticmethod
    def process_df(dataframe, dataframe_1):
        dataframe = dataframe.reset_index()     # removing index for the dataframe
        dataframe = dataframe.merge(dataframe_1[['CompanyShortName', 'LastUpdated']], right_on='CompanyShortName', left_on='Symbol', how='left')     # merging data set 1 with data set 3
        CommonModule.dataframe_cast(dataframe, 'LastUpdated', 'float64')   # converting LastUpdated to float
        dataframe['sp_price'] = dataframe['LastUpdated'].combine_first(dataframe['Price'])     # merging the stock price columns
        return dataframe

    @staticmethod
    def statistical_model(dataframe, path=os.getcwd()):
        corr_coefficient = []
        p_values = []
        sector_val = []
        colors = []
        for sector in dataframe['Sector'].drop_duplicates().tolist():
            corr, p_value = spearmanr(dataframe['sp_price'], dataframe['Sector'] == sector)
            corr_coefficient.append(corr)
            p_values.append(p_value)
            sector_val.append(sector)
            colors.append('blue') if corr >= 0 else colors.append('red')
        print(pd.DataFrame({'Sector': sector_val, 'Correlation Coefficient': corr_coefficient, 'p-value': p_values}).head(20))
        print('Mean p-value: ', sum(p_values)/len(p_values))
        fig = plt.figure(figsize=(10, 8))
        plt.scatter(sector_val, corr_coefficient, [1000*i for i in p_values], color=colors, alpha=0.3)
        for i in range(len(sector_val)):     # for the range on length of the dataframe
            plt.annotate(text='p-value: {}'.format(round(p_values[i], 3)), xy=(sector_val[i], corr_coefficient[i]), size=5)     # annotating the graph with the company details
        plt.axhline(y=0, color='black')
        plt.xticks(rotation=45)
        plt.xlabel("Industrial Sectors")
        plt.ylabel("Correlation Coefficient")
        plt.title("S&P Statistical Analysis of Industrial Sectors using Spearman rank correlation coefficient")
        try:
            fig.savefig(os.path.join(path, 'graph_stat_src.svg'))     # saving the plot
        except:
            print("Error saving the graph")
        # plt.show()
        plt.close()

    @staticmethod
    def trend_analysis(dataframe, path=os.getcwd()):
        dataframe = CommonModule.dataframe_cast(dataframe, 'LastUpdated', 'float64')
        dataframe = CommonModule.dataframe_cast(dataframe, 'Volume', 'float64')
        dataframe['50_day_price_ma'] = dataframe['LastUpdated'].rolling(window=int(len(dataframe['LastUpdated'])/5)).mean()
        fig, ax1 = plt.subplots(figsize=(10, 8))
        ax1.set_xlabel('Company Name')
        ax1.set_xticklabels(dataframe.index, rotation=45)
        ax1.plot(dataframe.index, dataframe['LastUpdated'], 'ro-', alpha=0.3, label='Stock Price')
        ax1.plot(dataframe.index, dataframe['50_day_price_ma'], color='black', label='Trend')
        ax1.tick_params(axis='y', labelcolor='tab:red')
        ax1.set_ylabel('Price', color='tab:Red')
        ax2 = ax1.twinx()
        ax2.set_ylabel('Volume', color='tab:blue')
        ax2.bar(dataframe.index, dataframe['Volume'], alpha=0.3, color='blue', label='Trade Volume')
        plt.xticks(rotation=55)
        plt.legend(loc="upper right")
        plt.setp(ax1.get_xticklabels(), visible=False) if len(dataframe) >= 25 else print("Generating bar plot ...")  # disabling the chart labels
        plt.setp(ax2.get_xticklabels(), visible=False) if len(dataframe) >= 25 else print("Generating bar plot ...")  # disabling the chart labels
        plt.title("S&P Trend Analysis based on company performance - latest day")
        fig.savefig(os.path.join(path, 'graph_trend.svg'))     # saving the plot
        # plt.show()
        plt.close()

    @staticmethod
    # Define function to get article text and sentiment
    def get_sentiment(web_link):
        x = 0
        str_length = len(re.findall("http", web_link))
        if str_length > 1:
            iterator = re.finditer("http", web_link)
            for i in range(0, str_length):
                x = next(iterator)
            web_link = web_link[x.span()[0]:]
        res = requests.get(web_link)
        if res.status_code == 200:
            html_page = res.content
            soup = BeautifulSoup(html_page, 'html.parser')
            text = soup.find_all(text=True)
            article = ''
            for t in text:
                article += '{} '.format(t)
            blob = TextBlob(article)
            return blob.sentiment.polarity
        else:
            return 0

    @staticmethod
    def sentiment_analysis(dataframe1, dataframe2, path=os.getcwd()):
        dataframe1 = CommonModule.dataframe_cast(dataframe1, 'LastUpdated', 'float64')
        dataframe1[['headline', 'url']] = dataframe1['NewsArticle'].str.split(' : ', expand=True)  # CompanyShortName
        html_table = dataframe1[['headline', 'url']].to_html()
        text_file = open(os.path.join(path, "news_articles.html"), "w")
        text_file.write(html_table)
        text_file.close()
        sentiments_dict = {}
        snp = 0
        dataframe1 = dataframe1.head(30)
        for name in dataframe1.index:
            sentiments_dict[name] = sentiments_dict.get(name, tuple()) + (TextBlob(dataframe1['headline'].loc[name]).sentiment.polarity, ProcessModule.get_sentiment(dataframe1['url'].loc[name]))
        dataframe2 = dataframe2[dataframe2['source'].str.contains('Stock Market')].head(10)
        for aid in dataframe2.reset_index().index:
            snp += TextBlob(dataframe2['description'].iloc[aid]).sentiment.polarity + ProcessModule.get_sentiment(dataframe2['url'].iloc[aid])
        for senti in sentiments_dict:
            total = 0
            for val in sentiments_dict[senti]:
                total += val
            sentiments_dict[senti] = total+snp
        print(sentiments_dict)
        sentiment_dataframe = pd.DataFrame.from_dict(sentiments_dict, orient='index', columns=['Sentiment Analysis'])
        h_plt = sns.heatmap(sentiment_dataframe, linewidth=1, linecolor='white')  # cmap='coolwarm'
        h_plt.set_title("S&P Sentiments based on company News Articles")
        h_plt.get_figure().savefig(os.path.join(path, 'graph_senti.svg'))     # saving the plot
        # plt.show()
        plt.close()
