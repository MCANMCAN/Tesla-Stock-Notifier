import requests 
from datetime import datetime , timedelta
import smtplib
def send_mail(title,message,url) : 
    my_email = "[mail adress]"      # needs email adress with required access permissions . 
    my_password = "[passwords]" #needs passwords.  
    with smtplib.SMTP("smtp.gmail.com",port=587) as connector:
        connector.starttls()   
        connector.login(user=my_email,password=my_password)
        connector.sendmail(
            from_addr= my_email,
            to_addrs= ["can.tanriverdi01@gmail.com"],
            msg=f"Subject:{title} \n\n {message} \n for more : \n {url}" 
        ) 
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
news_apikey ="c4a86e69078d4f0c9757156097c6a71d "
get_time = datetime.date 
now = datetime.today()
d1 = now.strftime("%Y-%d-%m")
print(d1)
yesterday = now- timedelta(days=1)
print("y",yesterday)
d2 = yesterday.strftime("%Y-%d-%m")
## STEP 1: Used https://www.alphavantage.co to receive stock prices. 
STOCK_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY" 
PARAMS_STOCK = { "symbol" : STOCK ,
                 "apikey": "H5SF5EHG3W5EUOGD" 
                 }
request = requests.get(url=STOCK_URL, params=PARAMS_STOCK)
stock_data = request.json()
today_stock = stock_data["Time Series (Daily)"][d1]['4. close']
yesterday_stock = stock_data["Time Series (Daily)"][d2]['4. close']
difference = round(1 - (float(yesterday_stock)/float(today_stock)),2)
print(difference)
if difference < 0 : 
    sms_title = f"{STOCK} DOWN {difference} today:(" 
else : 
    sms_title =f"{STOCK} UP {difference} today:)"            
## STEP 2: Used https://newsapi.org to receive latest news for company. 
news_url = ('https://newsapi.org/v2/everything?'
       f'q={COMPANY_NAME}&'
       f'from={now.strftime("%Y-%m-%d")}&'
       'sortBy=publishedAt&'
       f'apiKey={news_apikey}&'
       'language=en'
)

response = requests.get(news_url)
news = response.json()

new_desc = news["articles"][1]["description"]
new_url = news["articles"][1]["url"]
print(f"{sms_title}\n{new_desc} \n {new_url}")
## SMTPLIB TO SEND EMAIL . 
send_mail(sms_title,new_desc,new_url)

#Optional: Format the SMS message like this: 

