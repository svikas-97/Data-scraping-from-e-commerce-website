#!/usr/bin/env python
# coding: utf-8

# In[27]:


from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd

with open(r'efghousewares user and pwd.txt', 'r') as f:  # Replace Enter file name with your file name
    user_line = f.readline()
    user = user_line.split(':')
    username = user[1].strip()

    pwd_line = f.readline()
    pwd_str = pwd_line.split(':')
    pwd = pwd_str[1].strip()

driver = webdriver.Chrome('C:\Program Files\chromedriver.exe')

driver.get("https://www.efghousewares.co.uk/Account/Login")
driver.find_element(by=By.CSS_SELECTOR,
                    value="#UserName").send_keys(username)
driver.find_element(by=By.CSS_SELECTOR,
                    value="#Password").send_keys(pwd)
driver.find_element(by=By.CSS_SELECTOR, value="#dupbtn").click()

l_excepted_urls = []

l_name = []
l_product_code = []
l_price = []
l_sku = []
l_barcode = []
l_supp = []
l_image = []
quantity_price_l = []
l_quantity = []
l_quantity_price = []

with open("links.txt", "r") as file:
    urls = file.read()
for url in urls.split("\n"): 
    try:
        driver.get(url)
        try:
            name = driver.find_element(by=By.CSS_SELECTOR,
                                     value=".frounius-detail h1").text
            l_name.append(name)
        except:
            l_name.append('-')
    #         name = "none"
        try:
            productcode = driver.find_element(by=By.CSS_SELECTOR,
                                                value="div.productCode").text
            l_product_code.append(productcode.split(":")[1])
        except:
            l_product_code.append('-')
        try:
            price = driver.find_element(by=By.CSS_SELECTOR,
                                          value="span.excUnitPrice").text
            l_price.append(price)
        except:
            l_price.append('-')
    #         price = "none"
        try:
            sku = driver.find_element(
                by=By.CSS_SELECTOR,
                value=".frounius-img p:nth-of-type(1)").text
            l_sku.append(sku.split(':')[1])
        except:
            l_sku.append('-')
    #         sku = "none"
        try:
            barcode = driver.find_element(
                by=By.CSS_SELECTOR,
                value=".frounius-img p:nth-of-type(2)").text
            l_barcode.append(barcode.split(':')[1])
        except:
            l_barcode.append('-')
    #         barcode = "none"
        try:
            supp = driver.find_element(by=By.CSS_SELECTOR,
                                        value="p:nth-of-type(3)").text
            l_supp.append(supp.split(':')[1])
            
        except:
            l_supp.append('-')
            print('-')
    #         supp = "none"
        try:
            image = driver.find_element(by=By.CSS_SELECTOR,
                                        value="img#both").get_attribute("src")
            l_image.append(image)
        except:
            l_image.append('-')
    #         image = "none"
        try:
            if driver.find_elements(by=By.CSS_SELECTOR,value="tr:nth-of-type(n+3)"):
                quantity_price = ''
                for element in driver.find_elements(by=By.CSS_SELECTOR,value="tr:nth-of-type(n+3)"):
                    quantity_price = quantity_price + element.text
                    quantity_price_l.append(quantity_price)
                for n in range(len(quantity_price_l)):
                    l_quantity.append(quantity_price_l[n].split()[0])
                    l_quantity_price.append(quantity_price_l[n].split()[1])
                quantity_price_l.clear()
                print(supp, 'ok!')
            else:
                l_quantity.append('-')
                l_quantity_price.append('-')
                print(supp, 'ok!')
        except:
            print('N/A')
                
    except Exception as e:
        print('url:',url)
        l_excepted_urls.append(url)
        
        try:
            for ex_url in l_excepted_urls:
                driver.get(ex_url)
                try:
                    name = driver.find_element(by=By.CSS_SELECTOR,
                                             value=".frounius-detail h1").text
                    l_name.append(name)
                except:
                    l_name.append('-')
            #         name = "none"
                try:
                    productcode = driver.find_element(by=By.CSS_SELECTOR,
                                                        value="div.productCode").text
                    l_product_code.append(productcode.split(":")[1])
                except:
                    l_product_code.append('-')
                try:
                    price = driver.find_element(by=By.CSS_SELECTOR,
                                                  value="span.excUnitPrice").text
                    l_price.append(price)
                except:
                    l_price.append('-')
            #         price = "none"
                try:
                    sku = driver.find_element(
                        by=By.CSS_SELECTOR,
                        value=".frounius-img p:nth-of-type(1)").text
                    l_sku.append(sku.split(':')[1])
                except:
                    l_sku.append('-')
            #         sku = "none"
                try:
                    barcode = driver.find_element(
                        by=By.CSS_SELECTOR,
                        value=".frounius-img p:nth-of-type(2)").text
                    l_barcode.append(barcode.split(':')[1])
                except:
                    l_barcode.append('-')
            #         barcode = "none"
                try:
                    supp = driver.find_element(by=By.CSS_SELECTOR,
                                                value="p:nth-of-type(3)").text
                    l_supp.append(supp.split(':')[1])
                except:
                    l_supp.append('-')
                    print('2nd try: -')
            #         supp = "none"
                try:
                    image = driver.find_element(by=By.CSS_SELECTOR,
                                                value="img#both").get_attribute("src")
                    l_image.append(image)
                except:
                    l_image.append('-')
                try:
                    if driver.find_elements(by=By.CSS_SELECTOR,value="tr:nth-of-type(n+3)"):
                        quantity_price = ''
                        for element in driver.find_elements(by=By.CSS_SELECTOR,value="tr:nth-of-type(n+3)"):
                            quantity_price = quantity_price + element.text
                            quantity_price_l.append(quantity_price)
                        for n in range(len(quantity_price_l)):
                            l_quantity.append(quantity_price_l[n].split()[0])
                            l_quantity_price.append(quantity_price_l[n].split()[1])
                        quantity_price_l.clear()
                        print('2nd try: ',supp, 'ok!')
                    else:
                        l_quantity.append('-')
                        l_quantity_price.append('-')
                        print('2nd try: ',supp, 'ok!')
                except:
                    print('N/A')
                
        except Exception as es:
            print('ex_url: ',ex_url)
        
        
        
        
driver.quit()

time.sleep(1)

data = {
        "name": l_name,
        "productcode": l_product_code,
        "price": l_price,
        "sku": l_sku,
        "barcode": l_barcode,
        "supp": l_supp,
        "image": l_image,
        "quantity": l_quantity,
        "quantity price":l_quantity_price
    }
df = pd.DataFrame(data)
df.to_excel("efgwarehouse outputs.xlsx", index=False)


# In[24]:


df


# In[22]:


print(len(l_barcode))
print(len(l_image))
print(len(l_name))
print(len(l_price))
print(len(l_product_code))
print(len(l_quantity))
print(len(l_quantity_price))
print(len(l_sku))
print(len(l_supp))

