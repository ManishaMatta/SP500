import os
import random
import matplotlib.pyplot as plt


# prediction model
class VisualizeModule:

    @staticmethod
    # function to process and visualize the 1st dataset wrt S&P index values
    def visualize_sp(dataframe1, dataframe2, dataframe3, path=os.getcwd()):

        figure1, axis1 = plt.subplots(figsize=(10, 8))     # generating a plot with 2 subplots
        dataframe1['LastUpdated'] = dataframe1['LastUpdated'] if dataframe1['LastUpdated'].dtype.name == 'float64' else dataframe1['LastUpdated'].str.replace(',', '', regex=True).astype('float64')     # Updating the LastUpdated column to float datatype
        dataframe1['colour'] = dataframe1['LastUpdated'] / dataframe1['LastUpdated'].mean()     # adding the RGBA colour code for the LastUpdated vaues
        n = 1 if len(dataframe1) >= 50 else 10     # updating the multiplication factor based on the execution mode
        # scatter plot for LastUpdated [stock price] where the size of the bubble represents the volume of stocks traded
        axis1.scatter(x=dataframe1.index.tolist(), y=dataframe1['LastUpdated'], s=[i * n for i in dataframe1['LastUpdated'].tolist()], c=dataframe1['colour'], alpha=0.8, edgecolors="grey", linewidth=2)
        axis1.scatter(x=dataframe1.index.tolist(), y=dataframe1['LastUpdated'], s=0.5)     # scatter plot to point the actual point in map
        axis1.set_xlabel('S&P Companies')     # setting the x-axis label
        axis1.set_ylabel('Stock Price')     # setting the y-axis label
        val = dataframe1['CompanyShortName'].shape     # getting the shape of the dataframe
        for i in range(val[0]):     # for the range on length of the dataframe
            axis1.annotate(text='{}'.format(dataframe1['CompanyShortName'].iloc[i]), xy=(i, dataframe1['LastUpdated'].iloc[i]), size=5)     # annotating the graph with the company details
        plt.xticks(rotation=45)
        axis1.set_title('S&P 500 Companies Price Variance')     # setting the title of the graph
        plt.setp(axis1.get_xticklabels(), visible=False) if len(dataframe1) >= 25 else print("Generating scatter plot ...")  # disabling the chart labels
        figure1.savefig(os.path.join(path, 'graph_pv.svg'))     # saving the plot
        # plt.show()
        plt.close()

        df = dataframe1.reset_index()[['CompanyName', 'CompanyShortName', 'BuySellHold', 'LastUpdated', '52WeekLow', '52WeekHigh']]     # selecting the required columns from the main dataframe.
        df['BuySellHold'] = df["BuySellHold"].str.split(pat="consensus rating of ", expand=True)[1].str.split(pat=" ").str[0].str[0:-1]     # updating the column BuySellHold for the display
        df['52WeekLow'] = df["52WeekLow"].str.split(pat=" stock was ", expand=True)[1].str.split(pat=" ").str[0].str[0: -1]     # updating the column 52WeekLow for the display
        df['52WeekHigh'] = df["52WeekHigh"].str.split(pat=" stock was ", expand=True)[1].str.split(pat=" ").str[0].str[0: -1]     # updating the column 52WeekHigh for the display
        df = df.rename(columns={"CompanyName": "Company Name", "CompanyShortName": "Company Short Name", 'BuySellHold': 'Buy-Sell-Hold', 'LastUpdated': 'Current Price', '52WeekLow': '52-Week Low', '52WeekHigh': '52-Week High'})
        print(df.head(len(df)))
        html_table = df.set_index('Company Name').to_html()
        text_file = open(os.path.join(path, "table.html"), "w")
        text_file.write(html_table)
        text_file.close()

        # axis1[1].axis('off')     # turning the x-axis off as its a table
        # axis1[1].set_title('Analysis of S&P 500 Companies', y=1.04)     # setting the title of the chart
        # df = dataframe1.reset_index()[['CompanyName', 'NewsArticle', 'BuySellHold', '52WeekLow', '52WeekHigh', 'Forecast']]     # selecting the required columns from the main dataframe.
        # print(tabulate(df[['CompanyName', 'NewsArticle', 'Forecast', 'BuySellHold', '52WeekLow', '52WeekHigh']].head(50), headers='keys', tablefmt='psql', showindex=False))
        # df['BuySellHold'] = df["BuySellHold"].str.split(pat="consensus rating of ", expand=True)[1].str.split(pat=" ").str[0].str[0:-1]     # updating the column BuySellHold for the display
        # df['52WeekLow'] = df["52WeekLow"].str.split(pat=" stock was ", expand=True)[1].str.split(pat=" ").str[0].str[0: -1]     # updating the column 52WeekLow for the display
        # df['52WeekHigh'] = df["52WeekHigh"].str.split(pat=" stock was ", expand=True)[1].str.split(pat=" ").str[0].str[0: -1]     # updating the column 52WeekHigh for the display
        # df['Forecast'] = df["Forecast"].str.split(pat=" The median estimate ", expand=True)[0]     # updating the column Forecast for the display
        # table = axis1[1].table(cellText=df[['CompanyName', 'BuySellHold', '52WeekLow', '52WeekHigh']].head(10).to_numpy(), colLabels=['S&P 500 Company', 'Analyst Suggestion', '52Week Low Price', '52Week High Price'], loc='center')     # generating the table for the sub-plot
        # table.scale(1, 1)     # resetting the table size
        # table.set_fontsize(16)     # updating the table font size
        # plt.setp([a.get_xticklabels() for a in figure1.axes[:-1]], visible=False)     # disabling the chart labels
        # # figure1.savefig('../resources/output/%s/S&P_500_Analysis1.svg')     # saving the plot  % (os.getcwd(), mode)
        # plt.show()

        figure2, axis2 = plt.subplots(figsize=(10, 8))     # add prediction model to this     # generating a plot
        dataframe2 = dataframe2.groupby(by='Date').mean()
        dataframe2['mean'] = (dataframe2['Close']+dataframe2['Open']+dataframe2['High']+dataframe2['Low'])/4     # calculating the mean of all attributes
        dataframe2['mean'].plot(label='Stock Mean Price')     # plotting the mean graph
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['Open'], c=dataframe2['Open'], marker='D', label='Stock Open Price')     # plotting the open graph
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['Close'], c=dataframe2['Close'], marker='o', label='Stock Close Price')     # plotting the close graph
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['High'], c=dataframe2['High'], marker='+', label='Stock High Price')     # plotting the high graph
        axis2.scatter(x=dataframe2.index.tolist(), y=dataframe2['Low'], c=dataframe2['Low'], marker='*', label='Stock Low Price')     # plotting the low graph
        axis2.set_title("S&P 500 Stock Price")     # updating the plot title
        axis2.set_ylabel("S&P Stock Price")     # updating the plot y-axis
        plt.xticks(rotation=45)
        figure2.legend(loc="upper right")     # moving the legend to upper right corner
        figure2.savefig(os.path.join(path, 'graph_sp.svg'))
        # plt.show()
        plt.close()

        if len(dataframe3) > 0:     # checking the length of the dataframe
            figure3, axis3 = plt.subplots(2, figsize=(10, 8))     # generating a plot with 2 subplots
            df3_c1 = list(filter(lambda x: '_Close' in x, dataframe3.columns.to_list()))     # selecting the dataframe with _close
            df3_c2 = dataframe3[[*df3_c1]]     # unwrapping the columns
            df3_c2.columns = df3_c2.columns.map(lambda x: x.replace('_Close', '')).tolist()     # updating the column names to remove _close
            df3_c2.plot(ax=axis3[0])     # plotting the graph
            axis3[0].get_legend().remove()     # removing the legend
            axis3[0].set_title("S&P 500 company-level Stock Prices ")     # updating the graph title
            axis3[0].set_ylabel("Stock Price")     # updating the graph y-label
            df3_v1 = list(filter(lambda x: '_Volume' in x, dataframe3.columns.to_list()))     # selecting the dataframe with _volume
            df3_v2 = dataframe3[[*df3_v1]]     # unwrapping the columns
            df3_v2.columns = df3_v2.columns.map(lambda x: x.replace('_Volume', '')).tolist()     # updating the column names to remove _volume
            df3_v2.plot(ax=axis3[1])     # plotting the graph
            axis3[1].get_legend().remove()     # removing the legend
            axis3[1].set_title("S&P 500 company-level Stock Volume")     # updating the graph title
            axis3[1].set_ylabel("Stock Volume")     # updating the graph y-label
            figure3.subplots_adjust(hspace=0.4)     # increasing the distance between subplots
            figure3.legend(labels=df3_c2.columns.to_list(), loc="upper right")     # creating a common legend
            figure3.savefig(os.path.join(path, 'graph_sp_all.svg'))
            plt.xticks(rotation=45)
            # plt.show()
        else:
            print("More than 10 S&P companies present. The graph would get crowded, hence please verify the raw data from file")
        # plt.show()
        plt.close()

    @staticmethod
    # function to process data set 3
    def visualize_src(dataframe, path=os.getcwd()):
        figure, axis = plt.subplots(figsize=(10, 8))     # generating a plot
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
            wedges, texts = axis.pie(dataframe['sp_price'].tolist(), radius=1.2, colors=dataframe['colour'].tolist())     # generating a piechart without labels
        else:
            wedges, texts, autotexts = axis.pie(dataframe['sp_price'].tolist(), labels=dataframe['Name'].tolist(), radius=0.8, colors=dataframe['colour'].tolist(), autopct='%1.1f%%', wedgeprops={'linewidth': 1, 'edgecolor': 'black'})     # generating a piechart with labels
        axis.set_title('Sectors in S&P 500')     # updating the chart title
        for wedge, label in zip(wedges, dataframe['Sector'].tolist()):     # iterating for each color sector combo
            custom_legend[label] = axis.plot([], [], marker='s', markersize=10, linestyle='none', color=wedge.get_facecolor(), label=label)[0]     # manually assigning legend values
        figure.legend(title='SECTOR', loc='upper right', bbox_to_anchor=(1.0, 1.0), handles=list(custom_legend.values()))     # generating the legend
        figure.savefig(os.path.join(path, 'graph_pie.svg'))     # saving the plot
        # plt.show()     # plotting the graphs
        plt.close()
