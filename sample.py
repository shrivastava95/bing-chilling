from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from time import sleep, time
import pyautogui
import random
from io import BytesIO
import win32clipboard
from PIL import Image


class BingBot:

    def __init__(self):
        self.driver = self.load_driver()

    @staticmethod
    def send_to_clipboard(clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    def load_driver(self):
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Edge(executable_path=r'msedgedriver.exe', options=options)
        return driver

    def change_tone(self, tone): # must be one of ['balanced', 'creative', 'precise']
        script = f"""return document.querySelector('cib-serp')
                .shadowRoot.querySelector('cib-conversation')
                .shadowRoot.querySelector('cib-welcome-container')
                .shadowRoot.querySelector('cib-tone-selector')
                .shadowRoot.querySelector('button[class="tone-{tone}"]')"""

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'cib-serp')))

        element = self.driver.execute_script(script)
        self.driver.execute_script("arguments[0].click();", element)

    def debug_script(self, tone):
        query_levels = [
            "document.querySelector('cib-serp')",
            ".shadowRoot.querySelector('cib-conversation')",
            ".shadowRoot.querySelector('cib-welcome-container')",
            ".shadowRoot.querySelector('cib-tone-selector')",
            f".shadowRoot.querySelector('button[class=\"tone-{tone}\"]')"
        ]
        current_query = ""
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'cib-serp')))

        for level in query_levels:
            current_query += level
            element = self.driver.execute_script(f"return {current_query}")

            if element is None:
                print(f"Failed at query level: {current_query}")
                return None

        return element

    def get_text_area(self):
        script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-text-input').shadowRoot.querySelector('textarea[name="searchbox"]')"""
        element = self.driver.execute_script(script)
        return element

    def write_text(self, message):
        sleep(5)
        textarea = self.get_text_area()

        # Ensure element is visible and clickable
        self.driver.execute_script("arguments[0].scrollIntoView();", textarea)
        self.driver.execute_script("arguments[0].click();", textarea)

        for char in message:
            sleep(random.randint(1, 3) / 10)
            textarea.send_keys(char)

        textarea.send_keys(Keys.ENTER)

    def get_button(self):
        script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('button[aria-label="Добавить изображение для поиска"]')"""
        element = self.driver.execute_script(script)
        return element

    def get_paste_input(self):
        script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-visual-search').shadowRoot.querySelector('input[class="paste-input"]')"""
        element = self.driver.execute_script(script)
        return element

    @staticmethod
    def copy_img_to_clipboard(image_path):
        image = Image.open(image_path)
        image.thumbnail((300, 300), Image.LANCZOS) # makes the image smaller while maintaining aspect ratio
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        BingBot.send_to_clipboard(win32clipboard.CF_DIB, data)

    def upload_img(self, message, image_path):
        self.copy_img_to_clipboard(image_path)
        # click on the button
        button = self.get_button()
        self.driver.execute_script("arguments[0].click();", button)
        sleep(0.2)
        # click on the thing
        paste_input = self.get_paste_input()
        # paste image
        self.driver.execute_script("arguments[0].click();", paste_input)
        paste_input.send_keys(Keys.CONTROL + "v")
        sleep(0.2)
        # enter message
        self.write_text(message)

    def get_response(self, limit_counter=1, wait_time=45):
        # refer to https://github.com/deshwalmahesh/Bing-Bot/blob/main/helpers.py to understand limit counter
        timer_start = time()
        sleep_time = (wait_time - (time() - timer_start))
        sleep(max(0, sleep_time))

        bot_response_script = f"""
        var turns = document.querySelector('cib-serp')
        .shadowRoot.querySelector('cib-conversation')
        .shadowRoot.querySelectorAll('cib-chat-turn')[{limit_counter - 1}]
        .shadowRoot.querySelector('cib-message-group[class="response-message-group"]')
        .shadowRoot.querySelectorAll('cib-message[type="text"]');

        var texts = [];
        for (var i = 0; i < turns.length; i++) {{
            var shared = turns[i].shadowRoot.querySelector('cib-shared[serp-slot="none"]');
            if (shared) {{
                texts.push(shared.innerText);
            }}
        }}
        return texts;"""
        try:
            response = "\n".join(self.driver.execute_script(bot_response_script)).strip()
            return response
        except Exception as e:
            print(e)
            return "Unable to get response. Try increasing the wait 'delay' or Force Reload Bing"

# Usage:
bot = BingBot()
bot.driver.get('https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx')
sleep(5)
bot.change_tone('precise') # balanced, creative, precise
bot.upload_img('what is this', 'Discord_KsbjZQlq08.png')
# get response
response = bot.get_response()
print(response)