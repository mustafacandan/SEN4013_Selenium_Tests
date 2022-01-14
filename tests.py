import platform
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

base_url_client = 'http://localhost:3000'
base_url_server = 'http://localhost:5000'

example_username = 'YAHYA'
example_userpass = '1234'

admin_username = 'superAdmin'
admin_password = 'superAdmin'

if platform.system() == 'Darwin':
    browser = webdriver.Chrome('./chromedrivers/chromedriver_darwin')
elif platform.system() == 'Windows':
    browser = webdriver.Chrome('./chromedrivers/chromedriver_windows.exe')
elif platform.system() == 'Linux':
    browser = webdriver.Chrome('./chromedrivers/chromedriver_linux')
else:
    raise ValueError('Sistem algilanma hatasi')

def is_server_running(browser, base_url_client):
    browser.get(base_url_client)
    title = browser.find_element_by_xpath('//*[@id="root"]/div/form/div[1]/h1')
    check_text(title, 'Branch Tracker', 'Website is not responding')


def user_can_login(browser):
    log_out(browser)
    sleep(0.3)
    browser.get(base_url_client)
    submit_btn_xpath = '//*[@id="root"]/div/form/button'
    username_form_xpath = '//*[@id="root"]/div/form/div[2]/input'
    password_form_xpath = '//*[@id="root"]/div/form/div[3]/input'
    username_form = browser.find_element_by_xpath(username_form_xpath).send_keys(example_username)
    password_form = browser.find_element_by_xpath(password_form_xpath).send_keys(example_userpass)
    submit_btn = browser.find_element_by_xpath(submit_btn_xpath).click()
    sleep(0.2)
    assert browser.current_url == 'http://localhost:3000/userPanel', 'User Couldnt Logged In'

def not_user_cant_login(browser):
    log_out(browser)
    browser.get(base_url_client)
    submit_btn_xpath = '//*[@id="root"]/div/form/button'
    username_form_xpath = '//*[@id="root"]/div/form/div[2]/input'
    password_form_xpath = '//*[@id="root"]/div/form/div[3]/input'

    username_form = browser.find_element_by_xpath(username_form_xpath).send_keys(example_username)
    password_form = browser.find_element_by_xpath(password_form_xpath).send_keys(example_userpass)
    submit_btn = browser.find_element_by_xpath(submit_btn_xpath).click()

    sleep(0.5)
    invalid_user_msg_xpath = '//*[@id="root"]/div/form/div[1]/div'

    assert browser.current_url == 'http://localhost:3000/', 'Unvalid User Can Logged In'
    
def log_out(browser):
    try:
        logout_menu_btn = browser.find_element_by_xpath('//*[@id="root"]/nav/ul/li/div/button')
    except NoSuchElementException as e:
        logout_menu_btn = None

    if logout_menu_btn:
        logout_menu_btn.click()
        sleep(0.2)
        logout_btn = browser.find_element_by_xpath('//*[@id="root"]/nav/ul/li/div/div/button')
        logout_btn.click()


def check_text(elem_xpath, text, err_msg):
    try:
        elem = browser.find_element_by_xpath(elem_xpath)
    except NoSuchElementException as e:
        elem = None
    if elem:
        assert elem.text == text, err_msg
    else:
        assert False, err_msg

def admin_can_see_daily_reports(browser):
    log_out(browser)
    browser.get(base_url_client)
    submit_btn_xpath = '//*[@id="root"]/div/form/button'
    username_form_xpath = '//*[@id="root"]/div/form/div[2]/input'
    password_form_xpath = '//*[@id="root"]/div/form/div[3]/input'
    sleep(0.4)
    username_form = browser.find_element_by_xpath(username_form_xpath).send_keys(admin_username)
    sleep(0.1)
    password_form = browser.find_element_by_xpath(password_form_xpath).send_keys(admin_password)
    sleep(0.1)
    submit_btn = browser.find_element_by_xpath(submit_btn_xpath).click()
    sleep(0.3)
    page_head_xpath = '/html/body/div/div/div/main/div/h1'
    check_text(page_head_xpath, 'Günlük Rapor', 'Admin Couldn\'t Logged in Panel')


def check_invalid_credential_message(browser):
    log_out(browser)
    sleep(0.3)
    browser.get(base_url_client)
    submit_btn_xpath = '//*[@id="root"]/div/form/button'
    username_form_xpath = '//*[@id="root"]/div/form/div[2]/input'
    password_form_xpath = '//*[@id="root"]/div/form/div[3]/input'

    username_form = browser.find_element_by_xpath(username_form_xpath).send_keys(example_username)
    sleep(0.1)
    password_form = browser.find_element_by_xpath(password_form_xpath).send_keys(example_userpass)
    sleep(0.1)
    submit_btn = browser.find_element_by_xpath(submit_btn_xpath).click()

    sleep(0.5)
    invalid_user_msg_xpath = '//*[@id="root"]/div/form/div[1]/div'
    check_text(invalid_user_msg_xpath, 'username or password incorrect', 'Invalid Message Dont Showed Up')

def admin_can_create_user(browser):
    admin_can_see_daily_reports(browser)
    sleep(0.3)
    url = 'http://localhost:3000/controlPanel/users'
    browser.get(url)
    sleep(0.2)
    name_surname = '/html/body/div/div/div/main/form/div[1]/input'
    region_name = '/html/body/div/div/div/main/form/div[2]/input'
    username = '/html/body/div/div/div/main/form/div[3]/input'
    password = '/html/body/div/div/div/main/form/div[4]/input'
    submit = '//*[@id="root"]/div/div/main/form/button'
    browser.find_element_by_xpath(name_surname).send_keys('John Doe')
    browser.find_element_by_xpath(region_name).send_keys('Sample Region')
    browser.find_element_by_xpath(username).send_keys('johndoe3')
    browser.find_element_by_xpath(password).send_keys('superPassword')
    sleep(0.2)
    browser.find_element_by_xpath(submit).click()
    sleep(0.2)
    table = '/html/body/div/div/div/main/table/tbody'
    user_info = 'John Doe Sample Region johndoe3 superPassword'
    assert user_info in browser.find_element_by_xpath(table).text, 'User Not Created'

def admin_can_add_new_branch(browser):
    admin_can_see_daily_reports(browser)
    sleep(0.3)
    url = 'http://localhost:3000/controlPanel/users'
    browser.get(url)
    sleep(0.2)
    branch_code = '/html/body/div/div/div/main/table/tbody/tr[1]/td[5]/table/tbody/tr[1]/td/form/div/input[1]'
    branch_name = '/html/body/div/div/div/main/table/tbody/tr[1]/td[5]/table/tbody/tr[1]/td/form/div/input[2]'
    branch_submit = '/html/body/div/div/div/main/table/tbody/tr[1]/td[5]/table/tbody/tr[1]/td/form/div/div/button'
    
    browser.find_element_by_xpath(branch_code).send_keys('9999')
    browser.find_element_by_xpath(branch_name).send_keys('Sample Branch')
    browser.find_element_by_xpath(branch_submit).click()
    sleep(0.2)
    table = '/html/body/div/div/div/main/table/tbody'
    branch_info = '9999 Sample Branch'
    assert branch_info in browser.find_element_by_xpath(table).text, 'Branch Not Created'

def user_can_see_their_branches(browser):
    log_out(browser)
    sleep(0.3)
    user_can_login(browser)
    browser.get('http://localhost:3000/userPanel')
    sleep(0.2)
    table = '//*[@id="root"]/div/div/main/form/table/tbody'
    table_data = browser.find_element_by_xpath(table).text
    braches = table_data.split()[:-1]

    users_braches = ['MUSTAFA', 'KEMAL', 'BAŞIBÜYÜK', 'FINDIKLI', 'İKBAL', 'ESATPAŞA', 'GEBZE', 'ADAPAZARI', 'İZMİT']
    users_braches.sort()
    braches.sort()
    assert users_braches == braches, "User can see other branches or cant see theirs"
    
def user_can_enter_earning(browser):
    success_msg = '/html/body/div/div/div/main/div[2]'
    branch_earning = '/html/body/div/div/div/main/form/table/tbody/tr[1]/td[2]/input'
    submit = '/html/body/div/div/div/main/form/table/tbody/tr[9]/td/button'
    browser.find_element_by_xpath(branch_earning).send_keys('-1')
    browser.find_element_by_xpath(submit).click()
    sleep(0.1)
    try:
        elem = browser.find_element_by_xpath(success_msg)
        elem_exist = True
    except NoSuchElementException as e:
        elem_exist = False
    sleep(0.2)
    if elem_exist:
        assert elem.text != 'Başarı ile kayıt edildi', 'User Can Enter Negative Value'

# is_server_running(browser)
# user_can_login(browser)
# not_user_cant_login(browser)
# check_invalid_credential_message(browser)
# admin_can_see_daily_reports(browser)
# admin_can_create_user(browser)
# admin_can_add_new_branch(browser)

browser.quit()
