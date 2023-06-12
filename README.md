# Stable Diffusion Discord Bot
A python discord bot with many features which uses A1111 as backend and uses my prompt templates for beautiful generations - even with short prompts.

## Features
It has many features:
- It generates 2 images
- Abitlity to upscale the images
- Abitlity to create small variations of the images
- Retrying with the same settings
- Beautiful images with simple prompts thanks to the prompt templates
- Works with the A1111 - no need for 2 stable diffusion installations
- Blocks direct messages 
- Generate random images using a finetuned GPT 2 which runs on cpu (Thanks to: FredZhang7/distilgpt2-stable-diffusion-v2)

## How to use this
First you need to install all the python dependencies:
`pip install -r requirements.txt`

### Bot settings variables 
The bot settings are defined in:
- `.env.development` : settings for development and testing 
- `.env.deploy` : settings for deployed bot
(copy the `.env.template` file for initial definition)

Most default settings can be kept, but you **must specify** the `BOT_KEY` which you obtain from the discord bot app setup. (You first have to create a discord bot at discord.com/developers/ but I won't explain this here. Just make sure that the bot has access to commands and can type messages / embed things. Don't forget to add the bot to your discord using the generated link in the devoloper portal with the correct rights, but I think that should be clear.  General instructions can be found on [RealPython: how to make a discort bot](https://realpython.com/how-to-make-a-discord-bot-python/))

Finally, start the bot using `python3 bot.py` - after this you can use the bot using /generate or /generate_random. 

To change / add styles, add the style to the command array in bot.py and add the preprompt, afterprompt and negative_prompt to prompts.py. There you can also find the prompts for the other styles.

Since this is my first Discord bot, things could probably be solved in a simpler/better way. So feel free to submit a pull request to fix some issues.

## Tips
Load hassanblend (https://huggingface.co/hassanblend/HassanBlend1.5.1.2) in stable diffusion as this is the model all the prompts are tuned on.

## Demo
Feel free to test it out in the #sd-art channel in TheBloke's Discord (https://discord.gg/F7jfGhaGRX)

## Screenshots
<img src="https://raw.githubusercontent.com/CyberTimon/Stable-Diffusion-Discord-Bot/main/examples/example1.png" alt="App Screenshot" width="50%">

<img src="https://raw.githubusercontent.com/CyberTimon/Stable-Diffusion-Discord-Bot/main/examples/example2.png" alt="App Screenshot" width="50%">

<img src="https://raw.githubusercontent.com/CyberTimon/Stable-Diffusion-Discord-Bot/main/examples/example3.png" alt="App Screenshot" width="50%">
