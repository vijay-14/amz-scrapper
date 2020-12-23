import smtplib
import os
import time

import requests
from bs4 import BeautifulSoup

URL = """https://www.amazon.com/gp/product/B08CFSZLQ4/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1"""

headers = {
    'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66""",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}


def check_price():
    """Checks the price of an amazon product falls below some value."""
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id='productTitle').get_text()
    price = soup.find(id='priceblock_ourprice').get_text()
    converted_price = float(price[1:6])
    if converted_price < 349:
        send_email(converted_price, URL)


def send_email(custom_text, product_page):
    """Sends email using smtplib and uses outlook as from account."""
    usr_id = os.getenv('outlook_usrid')
    pwd = os.getenv('outlook_pwd')
    subject = 'Google Pixel 4a Price Watch'
    text = """
            Hello,

            Google Pixel 4a Price fell below $349.

            New Price: ${price}

            Product Page: {p_page}
                
            Thank You
            Pricewatch Bot""".format(price=custom_text, p_page=product_page)
    message = 'Subject: {}\n\n{}'.format(subject, text)

    try:
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    except Exception as e:
        print(e)
        smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
    #type(smtpObj)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(usr_id, pwd)
    smtpObj.sendmail(usr_id, usr_id, message)  # Or recipient@outlook

    smtpObj.quit()
    pass


if __name__ == '__main__':
    while True:
        check_price()
        time.sleep(60 * 60 * 24)  # Checks once a day
