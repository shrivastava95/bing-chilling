# Bing Chilling: Bing Chat AI Webscraper

**A Python-based Selenium-powered tool for seamless interaction with Bing Chat AI, allowing both image and text inputs.**


---

**Table of Contents**
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)
- [Contributing](#contributing)
- [Code Structure](#code-structure)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Introduction

Bing Chilling is a Python project that leverages the Selenium WebDriver to automate interactions with Microsoft Bing's AI Chatbot. Designed to mimic human interaction, it enables users to send both text and images to the Bing Chat AI and receive comprehensive responses. This project is invaluable for researchers, developers, and hobbyists interested in exploring conversational AI dynamics.

## Features

- **Text Queries**: Send text-based queries and receive detailed responses from Bing Chat AI.
- **Image Queries**: Ability to upload images from URLs or local storage and ask contextual questions.
- **Flexible Tone Setting**: Set the chatbot's response tone to either balanced, creative, or precise.
- **Automated Interactions**: Fully automated interactions with the Bing Chat AI, including uploading images, sending queries, and fetching responses.
- **Customizable**: Easily customizable for various applications and research purposes.
- **Debugging Tools**: Included debug functions for easier troubleshooting during implementation.

## Installation

**Prerequisites:**
- Python 3.x
- Selenium WebDriver
- Microsoft Edge WebDriver

```bash
# Clone the repository
git clone https://github.com/shrivastava95/bing-chilling.git
cd bing-chilling

# Install dependencies
pip install -r requirements.txt
```

## Usage

**Basic Usage:**
```python
from bingbot import BingBot
import argparse

def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver-path', type=str, default="msedgedriver.exe")
    parser.add_argument('--bing-chat-url', type=str, default='https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx')
    args = parser.parse_args()
    return args

def main(args):
    bot = BingBot(args.driver_path)

    # Open Bing Chat
    bot.driver.get(args.bing_chat_url)

    # Set the tone for Bing Chat (options: balanced, creative, precise)
    bot.change_tone('precise')

    # Write a question to Bing Chat
    bot.write_text('Can you provide information about the Eiffel Tower?')

    # Press enter to send the query
    bot.send_query()

    # Get response from Bing (waits until Bing finishes responding)
    response = bot.get_response()
    print(response)

if __name__ == '__main__':
    args = load_args()
    main(args)
```

**For more detailed usage instructions, please refer to [example.py](example.py) and [user_input_example.py](user_input_example.py).**

## Demo


- **Text Interaction with Bing Chat AI**:


https://github.com/Arti787/bing-chilling/assets/84004494/db1b77bf-cf3b-434a-b1c2-a8fbad257ef8


- **Image Upload and Query**:


https://github.com/Arti787/bing-chilling/assets/84004494/2b259133-b3b8-41cd-b988-fc5248ef8289


## Contributing

Interested in contributing? We welcome all forms of contributions including bug fixes, feature requests, and documentation improvements. Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Code Structure

- `bingbot.py`: Core module containing the `BingBot` class with all functionalities.
- `example.py`: Sample script demonstrating the basic usage of `BingBot`.
- `user_input_example.py`: An interactive script that allows users to continuously send queries to Bing Chat AI.


## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

Special thanks to [contributors](CONTRIBUTORS.md) and the open-source community for their valuable contributions. This project wouldn't be possible without them.

---

**Happy Chatting with Bing AI! 🤖🎉**