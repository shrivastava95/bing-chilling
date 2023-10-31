from bingbot import BingBot
import argparse
from time import sleep

def load_args():
      parser = argparse.ArgumentParser()
      parser.add_argument('--driver-path', type=str, default="C:/ai_sem_8/edgedriver_win32/msedgedriver.exe")
      parser.add_argument('--bing-chat-url', type=str, default='https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx')
      args = parser.parse_args()
      return args

# Sample Usage of the Bot:
def main(args):
        if __name__ == '__main__':
                bot = BingBot(args.driver_path)

                # open bing chat
                bot.driver.get(args.bing_chat_url)

                # set the tone for bing chat
                bot.change_tone('precise') # balanced, creative, precise

                # upload image to bing chat 
                # Note: for local images: use `image_path` argument instead of `image_url`.
                img_url = 'https://media.discordapp.net/attachments/1049583034170621952/1164958033936400426/IMG_3010.jpg'
                bot.upload_img(image_url=img_url)
                
                # waits indefinitely until the image is uploaded to bing chat
                while bot.is_img_pasted() == False: 
                        sleep(1)

                # write a question about the image to bing chat
                bot.write_text('Please tell me about this image in 30 words or less.')

                # presses enter to send the query
                bot.send_query()

                # get response from bing (automatically waits until bing finishes responding)
                response = bot.get_response() 
                print(response)

if __name__ == '__main__':
       args = load_args()
       main(args)