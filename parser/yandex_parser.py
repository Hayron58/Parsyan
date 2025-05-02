  ```python
   from selenium import webdriver
   from bs4 import BeautifulSoup
   import time
   
   class YandexParser:
       def __init__(self):
           self.driver = webdriver.Chrome()
   
       def parse_company(self, query, city):
           url = f"https://yandex.ru/maps/213/moscow/search/{query}"
           self.driver.get(url)
           time.sleep(3)
           
           companies = []
           soup = BeautifulSoup(self.driver.page_source, 'html.parser')
           
           for item in soup.find_all('div', class_='business-card'):
               company = {
                   'name': item.find('h1').text,
                   'address': item.find('address').text,
                   'phone': item.find('phone').text,
                   'website': item.find('website').get('href', None),
                   'yandex_url': self.driver.current_url
               }
               companies.append(company)
           
           return companies
