# import webdriver 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
# from cookies import cookies
from time import sleep, time
import pyautogui
import random
from io import BytesIO
import win32clipboard
from PIL import Image


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def load_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Edge(options=options)
    return driver

def change_tone(driver, tone): # must be one of ['balanced', 'creative', 'precise']
    script = f"""return document.querySelector('cib-serp')
.shadowRoot.querySelector('cib-conversation')
.shadowRoot.querySelector('cib-welcome-container')
.shadowRoot.querySelector('cib-tone-selector')
.shadowRoot.querySelector('button[class="tone-{tone}"]')"""
    element = driver.execute_script(script)
    element.click()

def get_text_area(driver):
    script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-text-input').shadowRoot.querySelector('textarea[name="searchbox"]')"""
    element = driver.execute_script(script)
    return element

def write_text(driver, message):
    sleep(5)
    textarea = get_text_area(driver)
    textarea.click()
    pyautogui.typewrite(message+'\n', interval=random.randint(1, 2) / 10)
    pyautogui.press('enter')

def get_button(driver):
    script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('button[aria-label="Add an image to search"]')"""
    element = driver.execute_script(script)
    return element

def get_paste_input(driver):
    # script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-flyout').shadowRoot.querySelector('cib-visual-search').shadowRoot.querySelector('input[class="paste-input"]')"""
    # script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-flyout').shadowRoot.querySelector('cib-visual-search')"""
    script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-flyout')"""
    script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-visual-search').shadowRoot.querySelector('input[class="paste-input"]')"""
    # script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-flyout').shadowRoot.querySelector('[product="bing"]')"""
    # script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-flyout')"""
    # script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('[class="visual-search"]')"""
    # script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar')"""
    element = driver.execute_script(script)
    # children = element.find_elements(By.XPATH, './/*')
    # for child in children:
    #     if 'cib-visual-search' in child
    return element

def copy_img_to_clipboard(image_path):
    image = Image.open(image_path)
    image.thumbnail((300, 300), Image.ANTIALIAS) # makes the image smaller while maintaining aspect ratio
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)

def upload_img(driver, message, image_path):
    copy_img_to_clipboard(image_path)
    # click on the button
    button = get_button(driver)
    button.click()
    # click on the thing
    paste_input = get_paste_input(driver)
    paste_input.click()
    sleep(5)
    # copy image to clipboard
    copy_img_to_clipboard(image_path)
    # paste image
    paste_input.send_keys(Keys.CONTROL+"v")
    # enter message
    write_text(driver, message)


def get_response(driver, limit_counter=1, wait_time=45): 
    # refer to https://github.com/deshwalmahesh/Bing-Bot/blob/main/helpers.py to understand limit counter
    '''
    Get recent Response from the model. 
    '''
    timer_start = time()
    sleep_time = (wait_time - (time() - timer_start))
    sleep(max(0, sleep_time))
    # Have escaped one { with another {
    bot_response_script = f"""
var turns = document.querySelector('cib-serp')
.shadowRoot.querySelector('cib-conversation')
.shadowRoot.querySelectorAll('cib-chat-turn')[{limit_counter - 1}]
.shadowRoot.querySelector('cib-message-group[class="response-message-group"]')
.shadowRoot.querySelectorAll('cib-message[type="text"]');

var texts = [];
for (var i = 0; i < turns.length; i++) {{{{
    var shared = turns[i].shadowRoot.querySelector('cib-shared[serp-slot="none"]');
    if (shared) {{{{
        texts.push(shared.innerText);
    }}}}
}}}}
return texts;"""
    try:
        response = "\n".join(driver.execute_script(bot_response_script)).strip()
        return response
    except Exception as e: 
        print(e)
        return "Unable to get response. Try increasing the wait 'delay' or Force Reload Bing"





























edgeDriver = load_driver()
edgeDriver.get('https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx')

# wait until the text area loads.
sleep(5)

# set the tone to one of "creative", "balanced", "precise"
tone = 'precise'
change_tone(edgeDriver, tone)

# upload an image to the thing along with a message
url = r'streamlit_annotation\streamlit crash course\blob.jpeg'
message = 'How can AI benefit us?'
upload_img(edgeDriver, message, url)

# get response
response = get_response(edgeDriver)
print(response)

# read the message response

# old
# # type the message into the box
# write_text(edgeDriver, message)



# sleep(5)

####################3    
# def add_all_cookies(driver):
#     for name, value in cookies.items():
#         driver.add_cookie({'name': name, 'value': value})



