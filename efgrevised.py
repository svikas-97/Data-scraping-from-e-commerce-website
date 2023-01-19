from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

# OPEN WEB BROWSER
print('opening website...')
website = 'https://www.efghousewares.co.uk/Account/Login'
path = 'C:\Program Files\chromedriver'
driver = webdriver.Chrome(path)
driver.get(website)
driver.maximize_window()
time.sleep(3)
print('website opened....')

# OPEN TEXT FILE WITH USERNAME AND PASSWORD
print('opening text file with username and password.....')
with open('efghousewares.txt') as f:
    username = f.readline().split(':')[1].strip()
    password = f.readline().split(':')[1].strip()

# LOG INTO WEBSITE
print('logging into website')
user = driver.find_element(By.ID, 'UserName')
user.clear()
user.send_keys(username)

time.sleep(1)

pword = driver.find_element(By.ID, 'Password')
pword.clear()
pword.send_keys(password)

time.sleep(1)

driver.find_element(By.ID, 'dupbtn').click()

time.sleep(3)

print('successfully logged in .......')

# OPEN DEPARTMENTS LINK
print('collecting urls for main categories...')
driver.get('https://www.efghousewares.co.uk/shop-by-department-5513')
time.sleep(2)

# FIND LOAD MORE BUTTON AND CLICK ON IT
try:
    for _ in range(5):
        load_more_button = driver.find_element(By.ID, 'loadMoreLink')
        load_more_button.click()
        time.sleep(3)
except:
    pass
time.sleep(2)

# GET LINKS FOR MAIN CATEGORIES
main_page_soup = bs(driver.page_source, 'html.parser')
main_category_soup = main_page_soup.find('ul', id='product-category-ul')

l_main_category_links = []
main_category_links = main_category_soup.find_all('a')
main_category_link = [l_main_category_links.append(link['href']) for link in main_category_links]

# GET SUB CATEGORY LINKS
print('collecting links for sub categories.......')
l_sub_category_links = []
sub_link_count = 0
for sub_category_link in l_main_category_links:
    sub_link_count = sub_link_count+1
    
    # open link
    driver.get(sub_category_link)
    
    sub_soup = bs(driver.page_source, 'html.parser')
    
    if sub_soup.find('ul', id='product-category-ul'):
        try:
            for _ in range(10):
                load_more_btn = driver.find_element(By.ID, 'loadMoreLink')
                load_more_btn.click()
                time.sleep(3)
        except Exception as e:
            pass

        # get sub category links
        sub_category_soup = sub_soup.find('ul', id='product-category-ul')
        sub_category_links = sub_category_soup.find_all('a')
        sub_category_link = [l_sub_category_links.append(link['href']) for link in sub_category_links]

    else:
        l_sub_category_links.append(sub_category_link)
print('list length of l_sub category links: ', len(l_sub_category_links))

# GET PRODUCT PAGE LINKS
print('collecting product page links ..........')
l_product_page_links = []
page_link_count = 0
for page_links in l_sub_category_links:
    page_link_count = page_link_count+1
    driver.get(page_links)
    
    product_main_page_soup = bs(driver.page_source, 'html.parser')
    
    total_pages = product_main_page_soup.find('li', class_='current').find('a')['aria-label'].split(',')[0].split(' ')[-1].strip()
    
    for pages in range(1, int(total_pages)+1):
        page_link = (f'{page_links}#{pages}')
        l_product_page_links.append(page_link)

print('list length of l_product_page_links: ', len(l_product_page_links))

# GET PRODUCT LINKS
driver.get('https://www.efghousewares.co.uk/shop-by-department-5513')
time.sleep(3)
driver.get('https://www.efghousewares.co.uk/shop-by-department/artificial-flowers')
time.sleep(3)
print('collecting product links.......')
l_product_links = []
count_product_page_link = 0
for product_link in l_product_page_links:
    count_product_page_link = count_product_page_link+1
    print(count_product_page_link, product_link)
    
    driver.get(product_link)
    time.sleep(2)
    
    product_page_soup = bs(driver.page_source, 'html.parser')
    
    product_links = product_page_soup.find('div', class_='productListGallery clearfix').find_all('a')
    
    product_link = [l_product_links.append(link['href']) for link in product_links[::3]]
    time.sleep(2)
    driver.back()
    driver.back()

# SAVING LINKS TO TEXT FILE
print('saving urls to text file.....')
with open('efg product links.txt', 'w') as f:
    for link in l_product_links:
        f.write(link+'\n')
driver.quit()

#OPEN LINKS FROM TEXT FILE
l_product_links_from_text_file = []
with open('efg product links.txt', 'r') as f:
    links = f.read().split('\n')
    for link in links:
        l_product_links_from_text_file.append(link)

    
# COLLECTING PRODUCT DATA
print('collecting product data......')
# OPEN PRODUCT LINK
def open_link(link):
    driver.get(link)

# GET PAGE SOUP
def page_soup(link):
    soup = bs(driver.page_source, 'html.parser')
    return soup

# GET PRODUCT DATA
def product_data(link):
    open_link(link)
    product_page_soup = page_soup(link)
    
    try:
        url = driver.current_url
    except:
        url = '-'
    
    try:
        product_name = product_page_soup.title.text.split('|')[0].strip()
    except:
        product_name = '-'
    
    try:
        product_code = product_page_soup.find('div', class_='productCode').text.split(':')[1].strip()
    except:
        product_code = '-'
    
    try:
        product_price = product_page_soup.find('span', class_='excUnitPrice').text
    except:
        product_price = '-'
    
    try:
        sku = product_page_soup.find('div', class_='frounius-detail-bottom').find('p').text.split(':')[1].strip()
    except:
        sku = '-'
    
    try:
        barcode = product_page_soup.find('div', class_='frounius-detail-bottom').find_all('p')[1].text.split(':')[1].strip()
    except:
        barcode = '-'
    
    try:
        supplier_code = product_page_soup.find('div', class_='frounius-detail-bottom').find_all('p')[2].text.split(':')[1].strip()
    except:
        supplier_code = '-'
    
    try:
        img_link = product_page_soup.find('img', id='both')['src']
    except:
        img_link = '-'
    
    l_qty = []
    l_price = []

    try:
        product_page_soup.find('div', class_='price-breack')
        price_table_soup = product_page_soup.find('div', class_='price-breack')
        tags = price_table_soup.find_all('tr')
        text = [l.text.strip() for l in tags]
        for num in range(1,len(text)):
            l_qty.append(text[num].split('\n')[0])
            l_price.append(text[num].split('\n')[1])
        if len(l_price) == 2:
            price_1 = l_price[0].replace('£', '')
            qty_1 = l_qty[0]
            price_2 = l_price[1].replace('£', '')
            qty_2 = l_qty[1]
            price_3 = '-'
            qty_3 = '-'
        elif len(l_price)==3:
            price_1 = l_price[0].replace('£', '')
            qty_1 = l_qty[0]
            price_2 = l_price[1].replace('£', '')
            qty_2 = l_qty[1]
            price_3 = l_price[2].replace('£', '')
            qty_3 = l_qty[2]
    except Exception as e:
        price_1 = '-'
        price_2 = '-'
        price_3 = '-'
        qty_1 = '-'
        qty_2 = '-'
        qty_3 = '-'
    
    data = {
        'URL':url,
        'Name':product_name,
        'Product Code':product_code,
        'Price':product_price,
        'SKU':sku,
        'Barcode':barcode,
        'Supplier Code':supplier_code,
        'Image Link':img_link,
        'Quantity ':qty_1,
        'Price ':price_1,
        'Quantity  ':qty_2,
        'Price  ':price_2,
        'Quantity   ':qty_3,
        'Price   ':price_3
    }
    return data

# OPEN WEB BROWSER
print('opening website...')
website = 'https://www.efghousewares.co.uk/Account/Login'
path = 'C:\Program Files\chromedriver'
driver = webdriver.Chrome(path)
driver.get(website)
driver.maximize_window()
time.sleep(3)
print('website opened....')

# OPEN TEXT FILE WITH USERNAME AND PASSWORD
print('opening text file with username and password.....')
with open('efghousewares.txt') as f:
    username = f.readline().split(':')[1].strip()
    password = f.readline().split(':')[1].strip()

# LOG INTO WEBSITE
print('logging into website')
user = driver.find_element(By.ID, 'UserName')
user.clear()
user.send_keys(username)

time.sleep(1)

pword = driver.find_element(By.ID, 'Password')
pword.clear()
pword.send_keys(password)

time.sleep(1)

driver.find_element(By.ID, 'dupbtn').click()

time.sleep(3)

print('successfully logged in .......')

l_product_data = []
count = 0
for product_link in l_product_links_from_text_file[:-1]:
    count+=1
    print(count, product_link)
    l_product_data.append(product_data(product_link))
    
efg_dataframe = pd.DataFrame(l_product_data)
efg_dataframe.to_csv('efg data csv.csv', index=False)