from selenium import webdriver
from flask import Flask
from selenium.webdriver.chrome.options import Options
from waitress import serve
from selenium.webdriver import ActionChains
import time
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    options = Options()
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

    time.sleep(2)
    
    element_text = driver.page_source
    driver.quit()    
    return element_text

if __name__ == '__main__':
    serve(app,host = '0.0.0.0',port = 5000)