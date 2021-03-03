# finanical-sentiment-charts

Cooperation project with the University of New South Wales aimed to analyse influence between social sentiment and financial tendency.

<img src="https://raw.githubusercontent.com/zolars/typora-user-images/master/20190715132829.png"/>

## Usage

1.  Get the code from Github clone or download zip by clicking [this](https://github.com/zolars/financial-sentiment/archive/master.zip).

    ```
    $ git clone https://github.com/zolars/finanical-sentiment.git
    ```

2.  You need to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and [MySQL](http://dev.mysql.com/downloads/mysql/) on your computer.

    ```
    $ conda -V
    conda 4.7.10
    ```

    You need to set "root" as the MySQL password. Or change the password in the code.

    ```
    $ mysql -u root -p
    Enter password:root
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    ```

3.  Create the environment.

    ```
    $ cd finanical-sentiment-charts
    $ conda env create -f environment.yml
    $ conda activate finance
    $ python -V
    Python 3.6.8 :: Anaconda, Inc.
    ```

    If you want to update your environment, use:

    ```
    $ conda env update -f environment.yml
    ```

4.  Download dependencies.

    ```
    $ python -m textblob.download_corpora
    ```

5.  Create a new DATABASE with MySQL.

    ```
    $ mysql -u root -p
    Enter password:root
    mysql> create DATABASE posts;
    mysql> use posts;
    Database changed
    ```

6.  Run the app
    ```
    $ cd finanical-sentiment-charts
    $ conda activate finance
    $ python app.py
    ```

## Twitter Advanced Search Options

### How to use 'Advanced Search' to generate query?

1.  With this website, input any keywords you want to search for.
    ![](https://raw.githubusercontent.com/zolars/typora-user-images/master/20190724022657.png)
2.  Click 'Search for' button.
3.  In the new page, copy the query you need as below:
    ![](https://raw.githubusercontent.com/zolars/typora-user-images/master/20190724023017.png)

### Code Options

| Operator                               | Finds tweets...                                                           |
| -------------------------------------- | ------------------------------------------------------------------------- |
| twitter search                         | containing both "twitter" and "search". This is the default operator.     |
| **"**happy hour**"**                   | containing the exact phrase "happy hour".                                 |
| love **OR** hate                       | containing either "love" or "hate" (or both).                             |
| beer **-** root                        | containing "beer" but not "root".                                         |
| **#** haiku                            | containing the hashtag "haiku".                                           |
| **from:** alexiskold                   | sent from person "alexiskold".                                            |
| **to:** techcrunch                     | sent to person "techcrunch".                                              |
| **@** mashable                         | referencing person "mashable".                                            |
| "happy hour" **near:** "san francisco" | containing the exact phrase "happy hour" and sent near "san francisco".   |
| **near:** NYC **within:** 15mi         | sent within 15 miles of "NYC".                                            |
| superhero **since:** 2010-12-27        | containing "superhero" and sent since date "2010-12-27" (year-month-day). |
| ftw **until:** 2010-12-27              | containing "ftw" and sent up to date "2010-12-27".                        |
| movie -scary **:)**                    | containing "movie", but not "scary", and with a positive attitude.        |
| flight **:(**                          | containing "flight" and with a negative attitude.                         |
| traffic **?**                          | containing "traffic" and asking a question.                               |
| hilarious **filter:links**             | containing "hilarious" and linking to URLs.                               |
| news **source:twitterfeed**            | containing "news" and entered via TwitterFeed                             |

### Where is the export Excel files?

They locate at `./out/`.

## Requirements

### Objective

To develop a platform which gathers live financial data and social network/online information/media information which will be displayed in a HTML format. The dataset will be used to analyze the relationship between online social sentiment of a certain stock, share, currency, crypto, and that stock price over a period of time.

Basically, this data aims to find is how social sentiment impacts price of:

- Stock exchanges

  - Shares within those exchanges

- Global currencies
- Cryptocurrencies

In order to find the social sentiment of a stock, the coding will need to use key words to identify that the social media post is actually talking about that stock. I propose that the best way to classify whether the post is speaking about a financial stock would be through the stock abbreviation code, the name of the stock, the name of the CEO, I can provide more information on this later.

### Other elements the research hopes to address

- Spikes (quick increases) in positive and negative social sentiment
- Price spikes of a market, stock, share, currency, crypto, etc
- Rank the importance of different social media accounts over others

  - Lots of followers online
  - Reposts of their post
  - Amount of likes and interactions with a post
  - There is more information about this online

- Use key words rank the level and importance of the sentiment

### Requirements of the platform

- Data from a number of different international stock exchanges
- Data from a number of different online social platforms

  - Twitter
  - Reddit
  - Sina Weibo
  - Media websites?
  - Investing websites?
  - More
    - It will be important for the platform be able to find these posts and where they are coming from in the

- The option to see the historical overview of the stock price and social sentiment

### Platform interface

- Landing page:
  - Have a dashboard which highlights:
    - The current spikes in price and social sentiment
  - Have an option to choose between different stock exchanges, currencies and cryptocurrencies
- Once you click on the stock exchange, currency option: the next page will then need to be a dashboard of that exchange that has been selected

  - Features:
    - Highlighting the spikes in price and social sentiment of currencies in that exchange.
    - Have an option to choose between all the different stocks in that exchange.

- The next is a detailed page which outlines information about each of the stocks
  - Historical overview
  - Chart data of the stock price
  - Chart data of the stock sentiment
  - Link to posts about the stocks

### Long-term elements of the project

- Is it possible to build a machine learning algorithm to identify when the social sentiment might go up or down?
- Is it possible to analyze how different key words might affect the stock price more than other key works
- Is it possible to put a weighting on different social sentiment, when something about a stock is posted by a reputable source how that then impacts on the stock price? i.e. extreme, massive
