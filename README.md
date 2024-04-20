# Telegram bot style_transfer_bot (Проверил Алексей my tg @bor_o)
## About

Welcome to our project, a Telegram bot designed for style transfer using neural networks. This bot, powered by the [Neural-Style algorithm](https://arxiv.org/abs/1508.06576 'link to article') by Gatys, Ecker, and Bethge, operates on a CPU server and leverages asynchronous programming to handle multiple requests simultaneously. Users can watch their images transform in real-time, with the option to adjust parameters affecting the style change. 

## Bot preview 

Bot handles multiple users and with commands. 
Upload style and content images or use default ones for quick start.
Use /transfer to start style transfer; adjust training epochs and resolution via inline keyboard.
Remember, higher quality takes longer.

<img src="sources/bot.gif" width="400"/>

## Style Transfer Examples

| Style | Content | Result |
|-------|---------|--------|
| <img src="sources/style0.jpg" alt="drawing" width="300"/> | <img src="sources/content0.jpg" alt="drawing" width="300"/> | <img src="sources/result0.jpg" alt="drawing" width="300"/> |
|   |   |
| <img src="sources/style1.jpg" alt="drawing" width="300"/> | <img src="sources/content1.jpg" alt="drawing" width="300"/> | <img src="sources/result1.jpg" alt="drawing" width="300"/> |
|   |   |
| <img src="sources/style2.jpg" alt="drawing" width="300"/> | <img src="sources/content2.jpg" alt="drawing" width="300"/> | <img src="sources/result2.jpg" alt="drawing" width="300"/> |


## Usage

The primary modules used include:

* **aiogram** for bot development
* **torch** and **numpy** for neural network operations
* The pre-trained vgg19 model from **torchvision**

all modules see in requirements.txt

### Running the Project

Follow these instructions to set up and run the project:

1. Create a Telegram bot through [@BotFather](https://t.me/BotFather 'link to telegram') in Telegram and remember your bot token.

2. Clone the repository:
```bash
git clone git@github.com:borolya/tg_ml_bot.git
cd tg_ml_bot
```

3. Create a **.env** file with your bot token. Use **.env.example** as a template for the **.env** file.
```
echo "TOKEN_BOT=<YOUR TOKEN>" > .env
```

4. Install all modules from requirements.txt in a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. And start the bot!
```bash
python3 app.py
```
## 

