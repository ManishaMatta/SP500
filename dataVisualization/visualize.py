import random
import matplotlib.pyplot as plt
from tabulate import tabulate
import os

# prediction model
class ProcessModule:

    @staticmethod
    def process_df1(mode, dataframe1, dataframe2, dataframe3):

        figure1, axis1 = plt.subplots(2)
        dataframe1['LastUpdated'] = dataframe1['LastUpdated'] if dataframe1['LastUpdated'].dtype.name == 'float64' else dataframe1['LastUpdated'].str.replace(',', '', regex=True).astype('float64')
        dataframe1['colour'] = dataframe1['LastUpdated'] / dataframe1['LastUpdated'].mean()
        # dataframe = dataframe.replace(np.nan, 0, regex=True)
        # dataframe['Volume'] = dataframe.Volume.replace({',': ''}, regex=True).astype({"Volume": float64})
        # dataframe['V'] = dataframe['Volume'].combine_first(dataframe['LastUpdated']*dataframe['NumberofShares']*dataframe['CashFlowPerShare'])
        # plt.scatter(x=dataframe.index.tolist(), y=dataframe['LastUpdated'], s=dataframe['V'], c=dataframe['colour'], alpha=0.8, edgecolors="grey", linewidth=2)
        n = 1 if mode == 'default' else 10
        axis1[0].scatter(x=dataframe1.index.tolist(), y=dataframe1['LastUpdated'], s=[i * n for i in dataframe1['LastUpdated'].tolist()], c=dataframe1['colour'], alpha=0.8, edgecolors="grey", linewidth=2)
        axis1[0].scatter(x=dataframe1.index.tolist(), y=dataframe1['LastUpdated'], s=0.5)
        axis1[0].set_xlabel('S&P Companies')
        axis1[0].set_ylabel('Stock Price')
        val = dataframe1['CompanyShortName'].shape
        for i in range(val[0]):
            axis1[0].annotate(text='{}'.format(dataframe1['CompanyShortName'].iloc[i]), xy=(i, dataframe1['LastUpdated'].iloc[i]), size=5)
        axis1[0].set_title('Price Variance of S&P 500 Companies')
        axis1[1].axis('off')
        axis1[1].set_title('Analysis of S&P 500 Companies', y=1.04)
        df = dataframe1.reset_index()[['CompanyName', 'NewsArticle', 'BuySellHold', '52WeekLow', '52WeekHigh', 'Forecast']]
        print(tabulate(df[['CompanyName', 'NewsArticle', 'Forecast', 'BuySellHold', '52WeekLow', '52WeekHigh']].head(50), headers='keys', tablefmt='psql', showindex=False))
        df['BuySellHold'] = df["BuySellHold"].str.split(pat="consensus rating of ", expand=True)[1].str.split(pat=" ").str[0].str[0:-1]
        df['52WeekLow'] = df["52WeekLow"].str.split(pat=" stock was ", expand=True)[1].str.split(pat=" ").str[0].str[0 : -1]
        df['52WeekHigh'] = df["52WeekHigh"].str.split(pat=" stock was ", expand=True)[1].str.split(pat=" ").str[0].str[0 : -1]
        df['Forecast'] = df["Forecast"].str.split(pat=" The median estimate ", expand=True)[0]
        table = axis1[1].table(cellText=df[['CompanyName', 'BuySellHold', '52WeekLow', '52WeekHigh']].head(10).to_numpy(), colLabels=['S&P 500 Company', 'Analyst Suggestion', '52Week Low Price', '52Week High Price'], loc='center')
        table.scale(1, 1)
        table.set_fontsize(16)
        plt.setp([a.get_xticklabels() for a in figure1.axes[:-1]], visible=False)
        figure1.savefig('%s/resources/output/%s/S&P_500_Analysis1.svg' % (os.getcwd(), mode))

        figure2, axis2 = plt.subplots()     # add prediction model to this
        dataframe2['mean'] = (dataframe2['Close']+dataframe2['Open']+dataframe2['High']+dataframe2['Low'])/4
        dataframe2['mean'].plot(label='Stock Mean Price')
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['Open'], c=dataframe2['Open'], marker='D', label='Stock Open Price')
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['Close'], c=dataframe2['Close'], marker='o', label='Stock Close Price')
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['High'], c=dataframe2['High'], marker='+', label='Stock High Price')
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['Low'], c=dataframe2['Low'], marker='*', label='Stock Low Price')
        axis2.set_title("Correlation of Stock Price for S&P 500")
        axis2.set_ylabel("S&P Stock Price")
        figure2.legend(loc="upper right")
        figure2.savefig('%s/resources/output/%s/S&P_500_Analysis2.svg' % (os.getcwd(), mode))

        if len(dataframe3) > 0:
            figure3, axis3 = plt.subplots(2)
            df3_c1 = list(filter(lambda x: '_Close' in x, dataframe3.columns.to_list()))
            df3_c2 = dataframe3[[*df3_c1]]
            df3_c2.columns = df3_c2.columns.map(lambda x: x.replace('_Close', '')).tolist()
            df3_c2.plot(ax=axis3[0])
            axis3[0].get_legend().remove()
            axis3[0].set_title("Correlation of Stock EOD Closing Prices")
            axis3[0].set_ylabel("Stock Price")
            df3_v1 = list(filter(lambda x: '_Volume' in x, dataframe3.columns.to_list()))
            df3_v2 = dataframe3[[*df3_v1]]
            df3_v2.columns = df3_v2.columns.map(lambda x: x.replace('_Volume', '')).tolist()
            df3_v2.plot(ax=axis3[1])
            axis3[1].get_legend().remove()
            axis3[1].set_title("Correlation of Stock Volume")
            axis3[1].set_ylabel("Stock Volume")
            figure3.subplots_adjust(hspace=0.4)
            figure3.legend(labels=df3_c2.columns.to_list(), loc="upper right")
            figure3.savefig('%s/resources/output/%s/S&P_500_Analysis3.svg' % (os.getcwd(), mode))
        else:
            print("More than 10 S&P companies present. The graph would get crowded, hence please verify the raw data from file")

        # plt.show()
        # plt.close()

    @staticmethod
    def process_df3(mode, dataframe, dataframe_1):
        figure5, axis5 = plt.subplots()
        dataframe = dataframe.reset_index()
        dataframe = dataframe.merge(dataframe_1[['CompanyShortName', 'LastUpdated']], right_on='CompanyShortName', left_on='Symbol', how='left')
        dataframe['LastUpdated'] = dataframe['LastUpdated'] if dataframe['LastUpdated'].dtype.name == 'float64' else dataframe['LastUpdated'].str.replace(',', '', regex=True).astype('float64')
        dataframe['sp_price'] = dataframe['LastUpdated'].combine_first(dataframe['Price'])
        colour = {}
        for i in dataframe['Sector'].drop_duplicates().tolist():
            r = random.randint(0, 255)/255
            g = random.randint(0, 255)/255
            b = random.randint(0, 255)/255
            a = random.uniform(0.5, 0.8)
            colour[i] = (r, g, b, a)
        dataframe = dataframe.sort_values(by='Sector')
        dataframe['colour'] = dataframe['Sector'].apply(lambda x: colour[x] if x in colour else (0.1, 0.1, 0.1, 0.3))
        custom_legend = {}
        if len(dataframe) >= 25:
            wedges, texts = axis5.pie(dataframe['sp_price'].tolist(), radius=1.2, colors=dataframe['colour'].tolist())
        else:
            wedges, texts, autotexts = axis5.pie(dataframe['sp_price'].tolist(), labels=dataframe['Name'].tolist(), radius=0.8, colors=dataframe['colour'].tolist(), autopct='%1.1f%%', wedgeprops={'linewidth': 1, 'edgecolor': 'black'})
        axis5.set_title('Sectors in S&P 500')
        for wedge, label in zip(wedges, dataframe['Sector'].tolist()):
            custom_legend[label] = axis5.plot([], [], marker='s', markersize=10, linestyle='none', color=wedge.get_facecolor(), label=label)[0]
        figure5.legend(title='SECTOR', loc='upper right', bbox_to_anchor=(1.0, 1.0), handles=list(custom_legend.values()))
        figure5.savefig('%s/resources/output/%s/S&P_500_Analysis5.svg' % (os.getcwd(), mode))
        plt.show()

    @staticmethod
    def process_df2():
        #     sp_df12['dt'] = sp_df12['Date'].str[:10]
        # sp_df12 = sp_df12['Close'].ewm(alpha=0.8).mean()
        # sp_df12.plot(kind='line', x='dt', y='Close', color='red', title='test2') # scatter plot
        # # sp_df12.merge()
        # plt.show()
        # # sp_df12.plot(kind='pie', x='dt', y='Close', color='red', title='test3') # scatter plot
        # # plt.show() # show the plot
        return ''

    @staticmethod
    def process_all():
        return ''

# ProcessModule.plot_pie()
