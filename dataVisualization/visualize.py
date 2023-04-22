import os
import random
import matplotlib.pyplot as plt
from tabulate import tabulate


# prediction model
class ProcessModule:

    @staticmethod
    # function to process and visualize the 1st dataset wrt S&P index values
    def process_df1(mode, dataframe1, dataframe2, dataframe3):

        figure1, axis1 = plt.subplots(2)     # generating a plot with 2 subplots
        dataframe1['LastUpdated'] = dataframe1['LastUpdated'] if dataframe1['LastUpdated'].dtype.name == 'float64' else dataframe1['LastUpdated'].str.replace(',', '', regex=True).astype('float64')     # Updating the LastUpdated column to float datatype
        dataframe1['colour'] = dataframe1['LastUpdated'] / dataframe1['LastUpdated'].mean()     # adding the RGBA colour code for the LastUpdated vaues
        # dataframe = dataframe.replace(np.nan, 0, regex=True)
        # dataframe['Volume'] = dataframe.Volume.replace({',': ''}, regex=True).astype({"Volume": float64})
        # dataframe['V'] = dataframe['Volume'].combine_first(dataframe['LastUpdated']*dataframe['NumberofShares']*dataframe['CashFlowPerShare'])
        # plt.scatter(x=dataframe.index.tolist(), y=dataframe['LastUpdated'], s=dataframe['V'], c=dataframe['colour'], alpha=0.8, edgecolors="grey", linewidth=2)
        n = 1 if mode == 'default' else 10     # updating the multiplication factor based on the execution mode
        # scatter plot for LastUpdated [stock price] where the size of the bubble represents the volume of stocks traded
        axis1[0].scatter(x=dataframe1.index.tolist(), y=dataframe1['LastUpdated'], s=[i * n for i in dataframe1['LastUpdated'].tolist()], c=dataframe1['colour'], alpha=0.8, edgecolors="grey", linewidth=2)
        axis1[0].scatter(x=dataframe1.index.tolist(), y=dataframe1['LastUpdated'], s=0.5)     # scatter plot to point the actual point in map
        axis1[0].set_xlabel('S&P Companies')     # setting the x-axis label
        axis1[0].set_ylabel('Stock Price')     # setting the y-axis label
        val = dataframe1['CompanyShortName'].shape     # getting the shape of the dataframe
        for i in range(val[0]):     # for the range on length of the dataframe
            axis1[0].annotate(text='{}'.format(dataframe1['CompanyShortName'].iloc[i]), xy=(i, dataframe1['LastUpdated'].iloc[i]), size=5)     # annotating the graph with the company details
        axis1[0].set_title('Price Variance of S&P 500 Companies')     # setting the title of the graph
        axis1[1].axis('off')     # turning the x-axis off as its a table
        axis1[1].set_title('Analysis of S&P 500 Companies', y=1.04)     # setting the title of the chart
        df = dataframe1.reset_index()[['CompanyName', 'NewsArticle', 'BuySellHold', '52WeekLow', '52WeekHigh', 'Forecast']]     # selecting the required columns from the main dataframe.
        print(tabulate(df[['CompanyName', 'NewsArticle', 'Forecast', 'BuySellHold', '52WeekLow', '52WeekHigh']].head(50), headers='keys', tablefmt='psql', showindex=False))
        df['BuySellHold'] = df["BuySellHold"].str.split(pat="consensus rating of ", expand=True)[1].str.split(pat=" ").str[0].str[0:-1]     # updating the column BuySellHold for the display
        df['52WeekLow'] = df["52WeekLow"].str.split(pat=" stock was ", expand=True)[1].str.split(pat=" ").str[0].str[0: -1]     # updating the column 52WeekLow for the display
        df['52WeekHigh'] = df["52WeekHigh"].str.split(pat=" stock was ", expand=True)[1].str.split(pat=" ").str[0].str[0: -1]     # updating the column 52WeekHigh for the display
        df['Forecast'] = df["Forecast"].str.split(pat=" The median estimate ", expand=True)[0]     # updating the column Forecast for the display
        table = axis1[1].table(cellText=df[['CompanyName', 'BuySellHold', '52WeekLow', '52WeekHigh']].head(10).to_numpy(), colLabels=['S&P 500 Company', 'Analyst Suggestion', '52Week Low Price', '52Week High Price'], loc='center')     # generating the table for the sub-plot
        table.scale(1, 1)     # resetting the table size
        table.set_fontsize(16)     # updating the table font size
        plt.setp([a.get_xticklabels() for a in figure1.axes[:-1]], visible=False)     # disabling the chart labels
        figure1.savefig('%s/resources/output/%s/S&P_500_Analysis1.svg' % (os.getcwd(), mode))     # saving the plot

        figure2, axis2 = plt.subplots()     # add prediction model to this     # generating a plot
        dataframe2['mean'] = (dataframe2['Close']+dataframe2['Open']+dataframe2['High']+dataframe2['Low'])/4     # calculating the mean of all attributes
        dataframe2['mean'].plot(label='Stock Mean Price')     # plotting the mean graph
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['Open'], c=dataframe2['Open'], marker='D', label='Stock Open Price')     # plotting the open graph
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['Close'], c=dataframe2['Close'], marker='o', label='Stock Close Price')     # plotting the close graph
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['High'], c=dataframe2['High'], marker='+', label='Stock High Price')     # plotting the high graph
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['Low'], c=dataframe2['Low'], marker='*', label='Stock Low Price')     # plotting the low graph
        axis2.set_title("Correlation of Stock Price for S&P 500")     # updating the plot title
        axis2.set_ylabel("S&P Stock Price")     # updating the plot y-axis
        figure2.legend(loc="upper right")     # moving the legend to upper right corner
        figure2.savefig('%s/resources/output/%s/S&P_500_Analysis2.svg' % (os.getcwd(), mode))     # saving the plot

        if len(dataframe3) > 0:     # checking the length of the dataframe
            figure3, axis3 = plt.subplots(2)     # generating a plot with 2 subplots
            df3_c1 = list(filter(lambda x: '_Close' in x, dataframe3.columns.to_list()))     # selecting the dataframe with _close
            df3_c2 = dataframe3[[*df3_c1]]     # unwrapping the columns
            df3_c2.columns = df3_c2.columns.map(lambda x: x.replace('_Close', '')).tolist()     # updating the column names to remove _close
            df3_c2.plot(ax=axis3[0])     # plotting the graph
            axis3[0].get_legend().remove()     # removing the legend
            axis3[0].set_title("Correlation of Stock EOD Closing Prices")     # updating the graph title
            axis3[0].set_ylabel("Stock Price")     # updating the graph y-label
            df3_v1 = list(filter(lambda x: '_Volume' in x, dataframe3.columns.to_list()))     # selecting the dataframe with _volume
            df3_v2 = dataframe3[[*df3_v1]]     # unwrapping the columns
            df3_v2.columns = df3_v2.columns.map(lambda x: x.replace('_Volume', '')).tolist()     # updating the column names to remove _volume
            df3_v2.plot(ax=axis3[1])     # plotting the graph
            axis3[1].get_legend().remove()     # removing the legend
            axis3[1].set_title("Correlation of Stock Volume")     # updating the graph title
            axis3[1].set_ylabel("Stock Volume")     # updating the graph y-label
            figure3.subplots_adjust(hspace=0.4)     # increasing the distance between subplots
            figure3.legend(labels=df3_c2.columns.to_list(), loc="upper right")     # creating a common legend
            figure3.savefig('%s/resources/output/%s/S&P_500_Analysis3.svg' % (os.getcwd(), mode))     # saving the plot
        else:
            print("More than 10 S&P companies present. The graph would get crowded, hence please verify the raw data from file")

        # plt.show()
        # plt.close()

    @staticmethod
    # function to process data set 3
    def process_df3(mode, dataframe, dataframe_1):
        figure5, axis5 = plt.subplots()     # generating a plot
        dataframe = dataframe.reset_index()     # removing index for the dataframe
        dataframe = dataframe.merge(dataframe_1[['CompanyShortName', 'LastUpdated']], right_on='CompanyShortName', left_on='Symbol', how='left')     # merging data set 1 with data set 3
        dataframe['LastUpdated'] = dataframe['LastUpdated'] if dataframe['LastUpdated'].dtype.name == 'float64' else dataframe['LastUpdated'].str.replace(',', '', regex=True).astype('float64')     # converting LastUpdated to float
        dataframe['sp_price'] = dataframe['LastUpdated'].combine_first(dataframe['Price'])     # merging the stock price columns
        colour = {}
        for i in dataframe['Sector'].drop_duplicates().tolist():     # iterating through distinct sectors
            r = random.randint(0, 255)/255     # generating random red value
            g = random.randint(0, 255)/255     # generating random green value
            b = random.randint(0, 255)/255     # generating random blue value
            a = random.uniform(0.5, 0.8)     # random exposure selection
            colour[i] = (r, g, b, a)     # assigning sector with colors
        dataframe = dataframe.sort_values(by='Sector')     # sorting the dataframe by sector
        dataframe['colour'] = dataframe['Sector'].apply(lambda x: colour[x] if x in colour else (0.1, 0.1, 0.1, 0.3))     # updating the dataframe to include colors
        custom_legend = {}
        if len(dataframe) >= 25:     # checking the length of dataframe
            wedges, texts = axis5.pie(dataframe['sp_price'].tolist(), radius=1.2, colors=dataframe['colour'].tolist())     # generating a piechart without labels
        else:
            wedges, texts, autotexts = axis5.pie(dataframe['sp_price'].tolist(), labels=dataframe['Name'].tolist(), radius=0.8, colors=dataframe['colour'].tolist(), autopct='%1.1f%%', wedgeprops={'linewidth': 1, 'edgecolor': 'black'})     # generating a piechart with labels
        axis5.set_title('Sectors in S&P 500')     # updating the chart title
        for wedge, label in zip(wedges, dataframe['Sector'].tolist()):     # iterating for each color sector combo
            custom_legend[label] = axis5.plot([], [], marker='s', markersize=10, linestyle='none', color=wedge.get_facecolor(), label=label)[0]     # manually assigning legend values
        figure5.legend(title='SECTOR', loc='upper right', bbox_to_anchor=(1.0, 1.0), handles=list(custom_legend.values()))     # generating the legend
        figure5.savefig('%s/resources/output/%s/S&P_500_Analysis5.svg' % (os.getcwd(), mode))     # saving the chart
        plt.show()     # plotting the graphs

    @staticmethod
    # function for visualizing data set 2
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
    # function for generating models with all data sets
    def process_all():
        return ''

# ProcessModule.plot_pie()
