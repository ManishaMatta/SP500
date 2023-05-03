import os
import webbrowser


class HTMLVisualize:
    @staticmethod
    def html_page(path, mse, mse_all):
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
            body {{
            border: 3px solid black;
            margin: 2em;
            padding: 2em;
            background-color:white;
            }}
            * {{
            box-sizing: border-box;
            }}
            .column {{
            float: left;
            width: 50%;
            padding: 0px;
            margin: 0px auto;
            }}
            /* Clearfix (clear floats) */
            .row::after {{
            content: "";
            clear: both;
            display: table;
            }}
            .container {{
            display: flex;
            align-items: right;
            }}
            .text {{
            font-size: 16px;
            padding-left: 10px;
            }}
        </style>
    <title>S&P 500 Stock Data Analysis</title>
</head>
<body>
<h1 style="text-align: center;">S&P 500 Stock Data Analysis</h1>
<h3 align="middle">The S&P 500 Index is a stock market index that tracks the performance of the 500 largest companies listed on the US
    stock exchange.
</h3>
<br>
<h2 style="text-align: left;">I.&nbsp;&nbsp;&nbsp;&nbsp; Flow Diagram</h2>
<img style="border: 2px solid black;"
     src="{path}/resources/pictures/flowchart.png" alt="FlowChart Image"
     align="middle">
<p>Apart from the passed input datasets, the execution modes with the optional selected list of S&P companies are passed
    as input. This data is then cleaned and validated for any noises or missing records. The datasets are then analysed
    to gain better understanding of the data by using statistical and machine learning models. It is then visualized
    accordingly to identify relations and draw conclusions.
</p>
<br>
<h2 style="text-align: left;">II.&nbsp;&nbsp;&nbsp;&nbsp; Data Analysis</h2>
<h3 style="text-align: left;"> &nbsp;&nbsp;&nbsp;&nbsp;(i)&nbsp;&nbsp;&nbsp;&nbsp; Prediction Analysis</h3>
<p>The below graphs represent the latest S&P data retrieved by web scraping for the selected period. The prediction models are applied on these datasets</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.&nbsp;&nbsp;&nbsp;&nbsp;The S&P 500 index for all 500 companies</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.&nbsp;&nbsp;&nbsp;&nbsp;Individual companies under S&P 500</p>
<div class="row">
    <div class="column">
        <img src="{path}/resources/html/graph_sp.svg"
             alt="Total S&P 500 Stocks" style="width:90%;border: 2px solid black;">
    </div>
    <div class="column">
        <img src="{path}/resources/html/graph_sp_all.svg"
             alt="Individual Company Stock" style="width:90%;border: 2px solid black;">
    </div>
</div>
<br>
<h4 style="text-align: left;"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp; LSTM[Long Short-Term Memory] model with Mean Squared Error evaluation</h4>
<p>LSTM (Long Short-Term Memory) is a type of Recurrent Neural Network (RNN) architecture that is designed to remember long-term dependencies. It is particularly useful in sequential data applications such as speech recognition, natural language processing, and time series prediction. </p>
<p>The below graphs represent the dataset after applying LSTM prediction models and evaluated with Mean Squared Error metric</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.&nbsp;&nbsp;&nbsp;&nbsp;The S&P 500 index for all 500 companies : Mean Squared Error={mse_1} </p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.&nbsp;&nbsp;&nbsp;&nbsp;Individual companies under S&P 500 - please scroll for all company details : Mean Squared Error={mse_2} </p>
<div class="container">
    <img style="border: 2px solid black;width:700px; height:900px;"
         src="{path}/resources/html/graph_lstm.svg" alt="LSTM Model"
         align="middle">
    <iframe class="text"
            style="background-color: white;border: 2px solid black;width:900px; height:900px;display: block;"
            src="{path}/resources/html/graph_lstm.html"
            width="90%"></iframe>
</div>
<br>
<h4 style="text-align: left;"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp; Linear Regression model with Mean Squared Error evaluation</h4>
<p>Linear Regression is a type of regression analysis used for predicting a continuous target variable (also called a response variable) from one or more predictor variables. The linear regression model assumes that there is a linear relationship between the predictor variables and the target variable. It tries to fit a straight line to the data that best describes the relationship between the variables.</p>
<p>The below graphs represent the dataset after applying Linear Regression prediction models and evaluated with Mean Squared Error metric</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.&nbsp;&nbsp;&nbsp;&nbsp;The S&P 500 index for all 500 companies : Mean Squared Error={mse_3} </p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.&nbsp;&nbsp;&nbsp;&nbsp;Individual companies under S&P 500 - please scroll for all company details : Mean Squared Error={mse_4} </p>
<div class="container">
    <img style="border: 2px solid black;width:700px; height:900px;"
         src="{path}/resources/html/graph_lr.svg"
         alt="Linear Regression Model" align="middle">
    <iframe style="background-color: white;border: 2px solid black;width:900px; height:900px;display: block;"
            src="{path}/resources/html/graph_lr.html" width="500"
            height="600"></iframe>
</div>
<br>
<h5>From comparing the 2 machine learning models</h5>
<h5>{mse}</h5>
<h3 style="text-align: left;">&nbsp;&nbsp;&nbsp;&nbsp; (ii) &nbsp;&nbsp;&nbsp;&nbsp;Correlating analysis using Spearman Rank Statistical Model</h3>
<p>Spearman rank correlation coefficient (SRCC) is a non-parametric test that measures the strength and direction of association between two ranked variables. It is used to determine the extent to which the variables are related. Like other correlation coefficients, this one varies between -1 and +1 with 0 implying no correlation. Its p-value provides if the outcome is statistically significant, it is more accurate for large samples</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.&nbsp;&nbsp;&nbsp;&nbsp;This graph plots the correlation coefficient for each sector, and the size of the bubble signifies its p-value. This depicts industrial sector's dependency on the overall stock market and its influence possibility.</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.&nbsp;&nbsp;&nbsp;&nbsp;This graph plots the coverage of each sector and company in the overall stock market. </p>
<div class="row">
    <div class="column">
        <img src="{path}/resources/html/graph_stat_src.svg"
             alt="Correlation Analysis" style="width:90%;border: 2px solid black;">
    </div>
    <div class="column">
        <img src="{path}/resources/html/graph_pie.svg"
             alt="pie chart" style="width:90%;border: 2px solid black;">
    </div>
</div>
<br>
<h3 style="text-align: left;">&nbsp;&nbsp;&nbsp;&nbsp; (iii) &nbsp;&nbsp;&nbsp;&nbsp;Trend analysis based on Stock Trade</h3>
<p>Moving Average Statistical technique is used to identify and quantify patterns or trends in data over time. It involves calculating the average of a fixed number of data points at a time and plotting the resulting values to identify the trend.</p>
<p>But due to limited data captured I am capturing the trend across all companies w.r.t stock price and trade. Through cumulating this data over time we can calculate the trend across individual companies too.</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.&nbsp;&nbsp;&nbsp;&nbsp;This graph plots the trend [black line]. When the trend line is higher it is preferable to SELL and alternatively BUY when trend line is lower.</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.&nbsp;&nbsp;&nbsp;&nbsp;This graph helps in understanding potential trading opportunities like if prices are increasing while volume is decreasing, it may indicate a lack of investor confidence in the upward trend, and prices may soon fall.</p>
<div class="row">
    <div class="column">
        <img src="{path}/resources/html/graph_trend.svg"
             alt="line graph" style="width:90%;border: 2px solid black;">
    </div>
    <div class="column">
        <img src="{path}/resources/html/graph_pv.svg"
             alt="scatter graph" style="width:90%;border: 2px solid black;">
    </div>
</div>
<p>If the volume data isn't displayed in the graph, it signifies that the data wasn't published while retrieving. Try rerunning the code of we can extract the outcome from the 2nd graph. </p>
<br>
<h3 style="text-align: left;">&nbsp;&nbsp;&nbsp;&nbsp; (iv)&nbsp;&nbsp;&nbsp;&nbsp; Sentiment analysis based on News Articles</h3>
<p>Sentiment analysis is a natural language processing (NLP) technique used to determine the emotional tone behind a piece of writing. It involves identifying and extracting the sentiment (positive, negative, or neutral) from text data. Analyzing news articles for sentiment, provides valuable insights into how current events both positive or negative are impacting the stock market.</p>
<p>Due to the current inflation, the news articles published currently do not indicate any overall positive aspect.</p>
<div class="container">
    <img style="border: 2px solid black;width:700px; height:600px;"
         src="{path}/resources/html/graph_senti.svg" alt="Sentiment"
         align="middle">
    <iframe style="background-color: white;border: 2px solid black;width:900px; height:600px;display: block;"
            src="{path}/resources/html/news_articles.html" width="500"
            height="600"></iframe>
</div>
<br>
<br>
<h2 style="text-align: left;">III.&nbsp;&nbsp;&nbsp;&nbsp; Outcome</h2>
<p>From analysing the insights offered on the past and present performance of the stock market data using all the above techniques. The table below summarises the analysis by indicating the preferred activity for investors to developing investment strategies that align with their financial goals and risk tolerance.</p>
<iframe style="background-color: white;border: 2px solid black;width:900px; height:600px;display: block;"
        src="{path}/resources/html/table.html" width="900"
        height="600"></iframe>
<br>
<br>
<h5 align="middle">This report provides a framework for making informed investment decisions in the future. However, it is important to note that past performance does not guarantee future results, and trends can change over time due to a variety of factors.</h5>
<h2 align="middle">Thank You</h2>
</body>
</html>
"""
        html = html_template.format(
            path=path,
            mse=mse,
            mse_1=round(mse_all[0], 3),
            mse_2=round(mse_all[1], 3),
            mse_3=round(mse_all[2], 3),
            mse_4=round(mse_all[3], 3)
        )
        return html

    @staticmethod
    def graph_scroll(pwd, file_path):
        files = os.listdir(file_path)
        lr_file = [file for file in files if file.__contains__("graph_lr_")]
        lstm_file = [file for file in files if file.__contains__("graph_lstm_")]
        lr_tags = """<div class="row">"""
        lstm_tags = """<div class="row">"""
        for i in range(0, len(lr_file)):
            f_path = file_path + lr_file[i]
            coll_tag = f"""<div class="column"><img src={f_path} alt="Correlation Analysis" style="width:90%;border: 2px solid black;"></div>"""
            lr_tags += coll_tag
            f_path = file_path + lstm_file[i]
            coll_tag = f"""<div class="column"><img src={f_path} alt="Correlation Analysis" style="width:90%;border: 2px solid black;"></div>"""
            lstm_tags += coll_tag
        lr_tags += """</div>"""
        lstm_tags += """</div>"""
        text_file = open(pwd+"/resources/html/graph_lr.html", "w")
        text_file.write(lr_tags)
        text_file.close()
        text_file = open(pwd+"/resources/html/graph_lstm.html", "w")
        text_file.write(lstm_tags)
        text_file.close()

    @staticmethod
    def publish_html(pwd, mse, mse_all):
        path = pwd+"/resources/html/"  # replace with your folder path
        HTMLVisualize.graph_scroll(pwd, path)
        with open(pwd+"/output_file.html", 'w') as f:
            f.write(HTMLVisualize.html_page(pwd, mse, mse_all))
        webbrowser.open('file://' + pwd + "output_file.html")
