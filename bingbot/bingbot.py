from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
import random
from io import BytesIO
import win32clipboard
from PIL import Image


class BingBot:

    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = self.load_driver(self.driver_path)

    @staticmethod
    def send_to_clipboard(clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    def load_driver(self, driver_path):
        service = Service(executable_path=driver_path)
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Edge(service=service, options=options)
        return driver

    def change_tone(self, tone):
        script = f"""return document.querySelector('cib-serp')
                    .shadowRoot.querySelector('cib-conversation')
                    .shadowRoot.querySelector('cib-welcome-container')
                    .shadowRoot.querySelector('cib-tone-selector')
                    .shadowRoot.querySelector('button[class="tone-{tone}"]')"""

        # WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'cib-serp')))

        element = self.driver.execute_script(script)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
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
        textarea = self.get_text_area()
        self.driver.execute_script("arguments[0].scrollIntoView();", textarea)
        self.driver.execute_script("arguments[0].click();", textarea)

        for char in message:
            sleep(random.randint(1, 3) / 100)
            textarea.send_keys(char)

    def send_query(self): # presses enter on the text area. equivalent to pressing the "send" button?
        textarea = self.get_text_area()
        self.driver.execute_script("arguments[0].scrollIntoView();", textarea)
        self.driver.execute_script("arguments[0].click();", textarea)
        textarea.send_keys(Keys.ENTER)

    def get_button(self):
        script = """
            var serp = document.querySelector("#b_sydConvCont > cib-serp");
            if (!serp) return null;
            var actionBarMain = serp.shadowRoot.querySelector("#cib-action-bar-main");
            if (!actionBarMain) return null;
            return actionBarMain.shadowRoot.querySelector("#camera-container > button");
        """
        return self.driver.execute_script(script)

    def get_paste_input(self):
        script = """return document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-visual-search').shadowRoot.querySelector('input[class="paste-input"]')"""
        element = self.driver.execute_script(script)
        return element
    
    def is_img_pasted(self):
        try:
            prefix = """return """
            script_list = """document.querySelector('cib-serp').shadowRoot.querySelector('cib-action-bar').shadowRoot.querySelector('cib-attachment-list').shadowRoot.querySelector('cib-file-item').shadowRoot.querySelector('div[class="thumbnail"]')"""
            script_list = script_list.split('.')
            for idx, _ in enumerate(script_list):
                suffix = '.'.join(script_list[:idx+1])
                script = prefix + suffix
                element = self.driver.execute_script(script)
                if element is None:
                    return False
            return True
        except:
            return False
    
    @staticmethod
    def copy_img_to_clipboard(image_path):
        image = Image.open(image_path)
        image.thumbnail((300, 300), Image.LANCZOS)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        BingBot.send_to_clipboard(win32clipboard.CF_DIB, data)
    

    def upload_img(self, image_path=None, image_url=None):
        # Get the camera button
        button = self.get_button()

        if not button:
            print("Error: Couldn't fetch the camera button.")
            return

        # Scroll to and click the camera button
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        self.driver.execute_script("arguments[0].click();", button)
        sleep(2)

        if image_url:
            # Proceed to paste the image URL
            paste_input = self.get_paste_input()
            paste_input.send_keys(image_url)
            paste_input.send_keys(Keys.ENTER)

        elif image_path:
            # Existing code to handle the image_path
            self.copy_img_to_clipboard(image_path)
            paste_input = self.get_paste_input()
            paste_input.send_keys(Keys.CONTROL + "v")

    def is_bing_responding(self):
        script = """
            var typingIndicator = document.querySelector("#b_sydConvCont > cib-serp")
                .shadowRoot
                .querySelector("#cib-action-bar-main")
                .shadowRoot
                .querySelector("div > cib-typing-indicator");
            return typingIndicator.getAttribute('aria-hidden');
        """
        return self.driver.execute_script(script) == 'false'

    def get_response(self, limit_counter=1):
        
        while True:
            try:
                script = f"""return document.querySelector('cib-serp')
            .shadowRoot.querySelector('cib-conversation')
            .shadowRoot.querySelectorAll('cib-chat-turn')[{limit_counter - 1}]
            .shadowRoot.querySelector('cib-message-group[class="response-message-group"]')
            .shadowRoot.querySelectorAll('cib-message[type="text"]');"""
                break
            except:
                sleep(1)
                
        while True:  # Wait until Bing finishes responding
            if not self.is_bing_responding(): break
            sleep(1)

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