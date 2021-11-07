from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep as time_sleep
from random import uniform as random_uniform
from random import randint as random_randint
from random import choice as random_choice
from tqdm import tqdm
from json import loads as json_loads
from json import dumps as json_dumps
from os import name as os_name
from os import getcwd as os_getcwd
from sys import argv as sys_argv

"""
CASES:
1) Ты понравился 2 девушкам, показать их?
"""

VK_DOMAIN = r"https://vk.com"
VK_BOT_URL = "https://vk.com/im?sel=-91050183"
BOT_KEYBOARD_BUTTONS_XPATH = r'/html/body/div[11]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div'
VK_BUTTONS_XPATH = fr'{BOT_KEYBOARD_BUTTONS_XPATH}/div[1]'
VK_LIKE_BUTTON_XPATH = fr'{BOT_KEYBOARD_BUTTONS_XPATH}/div[1]'
VK_MESSAGE_BUTTON_XPATH = fr'{BOT_KEYBOARD_BUTTONS_XPATH}/div[2]'
VK_DISLIKE_BUTTON_XPATH = fr'{BOT_KEYBOARD_BUTTONS_XPATH}/div[3]'
VK_BOT_SPAM_XPATH = r'/html/body/div[11]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div'
phrases = ['Привет, я провожу перепись населения и хочу начать с тебя!',
           'Привет, поменяй, пожалуйста, мое свободное время на общение с тобой?',
           'Ты очень ошибаешься, если думаешь, что я хочу с тобой знакомиться. Я хочу пригласить тебя на свидание!',
           'Не, ну если все время молчать, с тобой никто не познакомится. Я помогу, привет!',
           'А если бы я был такой красивой девушкой, как ты, то познакомился бы с собой!',
           'Как думаешь, за какие вопросы парни получают пощёчины?',
           'У тебя такие красивые глаза! Особенно левый!',
           'Наверное, плохо быть твоей подругой, ведь ты всех затмила!',
           'Знаешь, твои волосы идеально подходят под цвет моей подушки.',
           'А я вот собираю гарем. Не хватает только тебя.',
           ]


def get_driver():  # TODO fix me
    system_name = os_name.lower()
    if 'win' in system_name:
        driver_path = f'{os_getcwd()}/chromedriver.exe'
    else:
        driver_path = f'{os_getcwd()}/chromedriver'
    options = Options()
    options.add_argument("user-data-dir=selenium")
    # options.headless = True
    return webdriver.Chrome(executable_path=driver_path, options=options)


def like_vk_user(count):  # Not in use
    if random_randint(0, 1) == 1 or driver.find_element_by_xpath(VK_BOT_SPAM_XPATH).text:  # Same button for the spam
        driver.find_element_by_xpath(VK_LIKE_BUTTON_XPATH).click()


def write_vk_message(text):
    driver.find_element_by_xpath(VK_MESSAGE_BUTTON_XPATH).click()
    for char in text:
        driver.find_element_by_id('im_editable-91050183').send_keys(char)
        time_sleep(random_uniform(0.075, 0.15))
    driver.find_element_by_id('im_editable-91050183').send_keys(Keys.ENTER)


def dislike_user():
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, VK_DISLIKE_BUTTON_XPATH)))
    elem = driver.find_element_by_xpath(VK_DISLIKE_BUTTON_XPATH)
    if elem.text != 'Я больше не хочу никого искать.':
        elem.click()
    else:
        driver.find_element_by_xpath(VK_LIKE_BUTTON_XPATH).click()


def skip_spam():
    if captcha_elements := driver.find_elements_by_class_name('box_layout'):  # Skip captcha
        driver.execute_script("arguments[0].setAttribute('onclick','boxQueue.skip=false;')", captcha_elements[0])
        driver.find_element_by_class_name('big_text').send_keys('foo', Keys.ENTER)
    for button in driver.find_elements_by_xpath(BOT_KEYBOARD_BUTTONS_XPATH):
        if button.text.lower() in ('продолжить просмотр анкет',
                                   'смотреть анкеты',
                                   'хороший совет',
                                   'вернуться назад'):
            button.click()
            break
        elif button.text == '1':
            driver.quit()


def start_vk_liker(count):
    for _ in tqdm(iterable=range(int(count)), desc='swipes done', unit='swipe'):  # tqdm for progress bar
        try:
            # if driver.find_element_by_xpath(VK_MESSAGE_BUTTON_XPATH)
            if random_randint(0, 1) == 1:
                # like_vk_user(count)
                skip_spam()
                write_vk_message(text=random_choice(phrases))
            else:
                dislike_user()
            time_sleep(random_uniform(2, 3))
        except Exception as e:
            print(e)


def load_cookies(cookie_filename: str):
    try:
        with open(cookie_filename, 'r') as cookie_file_obj:  # First try to load cookie
            for cookie in json_loads(cookie_file_obj.read()):
                driver.add_cookie(cookie)
    except FileNotFoundError:
        pass


def save_cookies(cookie_filename: str):
    try:
        with open(cookie_filename, 'w+') as cookie_file_obj:
            cookie_file_obj.write(json_dumps(driver.get_cookies()))
    except FileNotFoundError:  # Prevent error if can not save cookie
        pass


def check_success_login():
    once_flag = True
    while True:
        try:  # throw error if no "sign out" icon
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'top_profile_link')))
            return
        except TimeoutException:
            if once_flag:
                print('it seems you are not logged in, for the program to work, you need to log in to the site.\n'
                      'Waiting until you are logged in...')
                once_flag = False


def login(cookie_filename, url):
    driver.get(url)
    load_cookies(cookie_filename=cookie_filename)
    driver.get(url)  # reload page with a new cookie (no refresh because of possible redirect by cookies)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()  # Skip phone asking
    driver.get(url)  # reload page with a new cookie (no refresh because of possible redirect by cookies)
    check_success_login()  # Infinite waiting
    save_cookies(cookie_filename=cookie_filename)


if __name__ == '__main__':
    likes_count = 100 or input("Сколько лайков поставить?")
    driver = get_driver()
    login(cookie_filename='cookies_vk.txt', url=VK_BOT_URL)
    start_vk_liker(count=likes_count)
    driver.quit()
