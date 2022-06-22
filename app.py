from selenium import webdriver
from flask import Flask
from selenium.webdriver.chrome.options import Options
from waitress import serve
from selenium.webdriver import ActionChains
import time
from flask import request
import csv

app = Flask(__name__)


@app.route('/')
def hello():
    options = Options()
    # local mac uncomment this
    # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("https://accounts.bukalapak.com/login?comeback=https%3A%2F%2Fwww.bukalapak.com%2F")
    driver.maximize_window()

    username = request.args.get('u')
    password = request.args.get('p')

    usernameElement = driver.find_element_by_id('LoginID')
    usernameElement.send_keys(username)
    

    driver.find_element_by_id('submit_button').click()
    time.sleep(2)

    passwordElement = driver.find_element_by_id('Password')
    passwordElement.send_keys(password)

    driver.find_element_by_id('btn-login').click()
    time.sleep(1)

    driver.get("https://www.bukalapak.com/payment/invoices?from=navbar")

    time.sleep(3)

    # find parent first
    container = driver.find_element_by_xpath("/html/body/div[2]/section/div/div[2]/fragment-loader/div/div/div[5]/div/div")

    # then grab the children, sorry sounds wrong
    all_children_by_xpath = container.find_elements_by_xpath("./child::*")

    # move them to csv, only rawdata for now
    with open('output.csv', 'wb') as data_file:
        writer = csv.writer(data_file, delimiter='\n')
        writer.writerows(map(lambda x: [x.text], all_children_by_xpath))

    element_text = driver.page_source
    driver.quit()    
    return element_text

if __name__ == '__main__':
    serve(app,host = '0.0.0.0',port = 5000)