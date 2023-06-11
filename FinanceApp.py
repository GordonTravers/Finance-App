from yahoo_fin import stock_info #yahoo finance is where all the stock information besides the news will come from in this code
from tkinter import * #Allows for the user interface to be set up
import requests #Allows for retrived news data to be used

#Api key for retrieving news 
NEWS_API_KEY = "41bf0f11861b4b68aa8c602a9168ffcd"  #For this key I just searched news API key and used one of the free ones


#Retrieves the stock data
def get_historical_data(symbol, start_date, end_date): #All data variables
    data = stock_info.get_data(symbol, start_date, end_date) #Gets data from desired time periods
    return data 

#I used Chatgpt to help retrieving and returning the news 
#Retrieves stock news 
def get_stock_news(symbol): #The variable symbol represents the stock symbol (Ticker)
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles')
        return articles
    else:
        return None

#I used Chatgpt to compare the stock requested to the S&P 500 at the same time
#Procedure for naming 
def compare_performance():
    symbol = e1.get()
    #4 lines below get the information from the stock and the S&P 500
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    
    stock_data = get_historical_data(symbol, start_date, end_date)
    sp500_data = get_historical_data("^GSPC", start_date, end_date)  #S&P 500 symbol is ^GSPC
    
    if stock_data is not None and sp500_data is not None:
        #Calculates the performance of the stock and the S&P 500 during the specified time period
        stock_return = (stock_data['adjclose'][-1] / stock_data['adjclose'][0] - 1) * 100
        sp500_return = (sp500_data['adjclose'][-1] / sp500_data['adjclose'][0] - 1) * 100
        
        #Displays the historical information of the stock
        stock_info_text.delete("1.0", "end")  # Clear previous text
        stock_info_text.insert("end", stock_data.to_string())
        
        #Displays the performance comparison
        result_label.config(text=f"{symbol} return: {stock_return:.2f}%\nS&P 500 return: {sp500_return:.2f}%")
        
        #Gets and displays the stock news
        articles = get_stock_news(symbol)
        if articles is not None:
            news_text.delete("1.0", "end") 
            for article in articles:
                title = article.get('title')
                description = article.get('description')
                news_text.insert("end", f"{title}\n{description}\n\n")
        else:
            news_text.delete("1.0", "end") 
            news_text.insert("end", "Error retrieving news")
    else:
        result_label.config(text="Error retrieving data")

#Code below is for the organization of a the user interface
#Chatgpt was used for the code below as it is relatively repetitive and could be completed by Chatgpt much quicker than by myself

master = Tk() #TK is used to set up the user interface 

#Code for positioning the test prompts in the user interface
Label(master, text="Company Symbol: ").grid(row=0, sticky=W)
Label(master, text="Start Date: ").grid(row=1, sticky=W)
Label(master, text="End Date: ").grid(row=2, sticky=W)
Label(master, text="Stock Historical Data: ").grid(row=4, column=0, sticky=W)
Label(master, text="Performance Comparison: ").grid(row=4, column=1, sticky=W)
Label(master, text="Stock News: ").grid(row=6, column=0, sticky=W)

#Set up for the input of the stock ticker
e1 = Entry(master, width=30)
e1.grid(row=0, column=1)

#Where the user enters their desired start date
start_date_entry = Entry(master, width=30)
start_date_entry.grid(row=1, column=1)

#Where the user enters their desired end date
end_date_entry = Entry(master, width=30)
end_date_entry.grid(row=2, column=1)

#Setup for the show button
b = Button(master, text="Show", command=compare_performance)
b.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

#Where the stock information is recieved
stock_info_text = Text(master, height=10, width=70)
stock_info_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

#Results for the users requested information
result_label = Label(master, text="", font=("Helvetica", 12))
result_label.grid(row=5, column=2, padx=5, pady=5)

#Where the news text is outputed
news_text = Text(master, height=10, width=70)
news_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

mainloop() #How the user interface is updated
