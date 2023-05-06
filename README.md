##### Homework-4 [DSCI 510 FINAL PROJECT]
# S&P 500 Stock Data Analysis

### I. Description

This data science project involves collecting and analyzing historical data of S&P 500. The S&P 500 Index is a stock market index that tracks the performance of the 500 largest companies listed on the US stock exchange.
The data is divided into multiple datasets to infer different correlation and prediction models for better data visibility.

**[GitHub link](https://github.com/ManishaMatta/SP500/tree/develop)**

The codebase is present under the **Manisha_Radhakrishna_HW5/SP500** directory
   * main class -> ./snp500.py [start point of the project]
   * output HTML file -> ./output_file.html [project output webpage]
   * execution modes modules
     * static mode -> ./runMode/staticMode.py [code for execution with static mode]
     * scrape mode -> ./runMode/scrapeMode.py [code for execution with scrape mode]
     * default mode -> ./runMode/defaultMode.py [code for execution with default mode]
   * data collection modules
     * common module -> ./dataCollection/common.py [common modules used in the project]
     * collect module -> ./dataCollection/collect.py [module used for data extraction]
   * data processing modules
     * process module -> ./dataProcessing/process.py [process modules used for data analysis]
   * data visualization modules
     * chart visualizer -> ./dataVisualization/visualize.py [module used for data visualization]
     * html module -> ./dataVisualization/html.py [module used for generating output web page]
   * code resources
     * datasets -> ./resources/dataset*.csv [datasets used for static mode]
     * outputs -> ./resources/output/<mode>/S&P_500_Analysis*.svg [analysis outputs from the codebase]
     * logs -> ./resources/logs/<mode>.txt [execution logs in each mode]
     * pictures -> ./resources/pictures/flowchart.png [flowchart]
     * html -> ./resources/html/* [content used in the webpage]

### II. Flow Chart
![flowchart.png](resources%2Fpictures%2Fflowchart.png)

### III. Requirements

The project must download and install the below listed modules and packages to
run the code. To install the packages use the following command: 

`pip install -r requirements.txt`

'./requirements.txt' -> file has a list of all the necessary packages required to run this code

**For installing _tensorflow_, please follow the below steps**
1. manually install by : `pip install tensorflow` https://www.tensorflow.org/install/pip#macos [worked in windows ,but faced few version compatibility issues in mac `-ERROR zsh: illegal hardware instruction python`. Please use the conda option if errors]

[or]

Please install conda:22.9.0v before executing this step [refer:https://conda.io/projects/conda/en/latest/user-guide/install/index.html]

2. manually install tensorflow by : `conda install tensorflow` [Please uninstall and reinstall if any issues]

Please check for the installation of `tensorflow` as it takes longer and if any issues please follow the commands in https://www.tensorflow.org/install/pip#macos link.


#### Packages Installed

Python Version : 3.11.1

Packages to be installed:
1. os
2. sys
3. pandas
4. datetime
5. random
6. requests
7. matplotlib
8. yfinance
9. tabulate
10. BeautifulSoup
11. sklearn
12. tensorflow
13. keras
14. textblob
15. scipy
16. seaborn
17. copy

### IV. Data Sources

1. S&P 500 index values : 
      * Web Crawling/ Scraping : https://markets.businessinsider.com/index/s&p_500
      * Web Scraping : https://markets.businessinsider.com/stocks/ <cmpy_name>
      * API GET : https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=Index&tkData=1059,998434,1059,333&from=20230101&to=20230328 
      * Python Library : yfinance

2. News articles regarding S&P 500 :
      * API GET : https://mediastack.com/documentation

3. S&P 500 Financial Data :
      * API GET : https://pkgstore.datahub.io/core/s-and-p-500-companies-financials/constituents-financials_json/data/ddf1c04b0ad45e44f976c1f32774ed9a/constituents-financials_json.json
      * U.S. Securities and Exchange Commission : http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK= <cmpy_name>

### V. Code Execution

The code can be run in three modes: default, scrape and static. Please execute the commands preferably from the module directory [**Manisha_Radhakrishna_HW5/SP500**]
The output analysis webpage pops-up after the code execution, and charts are also saved in the **../resource/html/** directory for future reference.
We can open the file **./output_file.html** path like `file:///<run_path>/output_file.html` on **Google Chrome** full screen for better visibility.

**NOTE**: Please enlarge the webpage for formatted display, Some graph may not be displayed on safari/Firefox hence please copy the URL to Chrome[works on both windows and mac].

* Static Mode:
  This mode would execute the datasets from sample data stored as csv files from the above sources to get partial analysis of the data.

  The static mode can be executed in 1 way:
    1. No Parameters : `python snp500.py --static`

  Execution Time : ~1370 seconds


* Scrape Mode:
  This mode would execute the complete datasets from the above-mentioned data sources for limited data to get partial analysis of the data.
  
  The scrape mode can be executed in 3 different ways:
   1. No Parameters : `python snp500.py --scrape`
   2. Classified Keywords : `python snp500.py --scrape faang` 
       **Only Amazon, Apple, Alphabet/Google will be displayed as we are scraping only one page in SCRAPE_MODE**
       [ faang => Meta (META) (formerly known as Facebook), Amazon (AMZN), Apple (AAPL), Netflix (NFLX); and Alphabet (GOOG) (formerly known as Google) ] 
        
   3. Specific S&P Companies : `python snp500.py --scrape <cmpy_1,cmpy_2>`
        [Ex. 3M,AbbVie,Accenture,Adobe] :: ***fastest in scrape mode***

  Execution Time : ~1000 seconds


* Default Mode:
  This mode would execute the complete datasets from the above-mentioned data sources for complete analysis of the data.

  The default mode can be executed in 3 different ways:
    1. No Parameters : `python snp500.py`
    2. Classified Keywords : `python snp500.py faang` 
        [ faang => Meta (META) (formerly known as Facebook), Amazon (AMZN), Apple (AAPL), Netflix (NFLX); and Alphabet (GOOG) (formerly known as Google) ]
    3. Specific S&P Companies : `python snp500.py <cmpy_1,cmpy_2>`
       [Ex. 3M,AbbVie,Accenture,Adobe]  :: ***fastest in default mode***

  Execution Time : ~900 seconds [with company list]  ~7000 secs [all S&P 500]


**NOTE**: As web scraping is done on multiple pages and LSTM model is run on all the companies passed, the execution time would increase based on number of S&P companies.
For fastest execution `python snp500.py --scrape 3M,Akamai,Accenture,Adobe,AES`

### VI. Evaluation

Below are few concepts covered in this module:

* User control in the analysis i.e, the user gets to choose subset of S&P 500 companies for the analysis else this process would run for all 500 companies.
* Data Analysis :
  * Linear Regression Model and LSTM (Long Short-Term Memory) Model for predictive analysis.
  * Spearman Rank Correlation statistical methods for correlative analysis.
  * Moving Average Statistical technique for trend analysis.
  * Natural language processing (NLP) technique for sentiment analysis.
* Displaying an output table with suggested investment advice for each S&P companies.
* Output webpage to display all the data analysis and outcomes with explanations.


### VII. Maintenance

These are the few aspects of the codebase that will require maintenance:

* Data analysis changes: We have to update the codebase in a single location if there are any future requirements for all the modes, the modular structure of the codebase makes it easier to update.
* Update in the HTML page used for web scraping: We will have to keep in track and update the codebase in case of any changes in the page structure.
* API JSON schema changes: the code is designed to be forward compatible hence, we might have to test the code in case of any updates in the schema. 
* Updating the datasets to keep track of contemporaneous data.
* Adding the comments on all function for understanding the logic used in the project.
* If any webpage is under maintenance [statuscode=400], I'm throwing an exception message with the current issue.

### VIII. Extensibility

As this is the MVP(Minimum Viable Product) version of the code. The scope of improvement in the project could be in the following areas:

* Updating the dataset-3 with more general and current data.
* Requesting access for scraping U.S. Securities and Exchange Commission website for financial data.
* Maintaining history of the data processed for better training set.
* Scheduling the module for more consistent data testing and evaluation.
* API call for dataset-2 is possible only 100 times a month, Requesting access for frequent data pulls for analysis.
* Adding constant file and parameter file for generalizing the codebase

### IX. Conclusion

Overall, the S&P 500 data analysis project is an undertaking that provides a deeper understanding of the stock market and the economy as a whole. It offers insights into the past and present performance of the stock market and provides a framework for making informed investment decisions for the future.
