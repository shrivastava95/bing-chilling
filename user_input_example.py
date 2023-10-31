from bingbot import BingBot
import argparse
from time import sleep


def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver-path', type=str, default="C:/ai_sem_8/edgedriver_win32/msedgedriver.exe")
    parser.add_argument('--bing-chat-url', type=str,
                        default='https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx')
    args = parser.parse_args()
    return args


def main(args):
    bot = BingBot(args.driver_path)

    # open bing chat
    bot.driver.get(args.bing_chat_url)

    # set the tone for bing chat
    bot.change_tone('precise')  # balanced, creative, precise

    # Loop for continuous interaction
    while True:
        user_input = input("Enter your query (or 'img_url:<image_url>' for image queries or 'quit' to exit): ")

        if user_input.lower() == 'quit':
            print("Exiting...")
            break

        response, limit_counter = bot.interact(user_input)
        print(f"Response {limit_counter-1}: {response}")


if __name__ == '__main__':
    args = load_args()
    main(args)
