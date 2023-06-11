from transformers import AutoTokenizer, GPT2Tokenizer, GPT2LMHeadModel
from PIL import Image, PngImagePlugin
from prompts import make_prompt, make_orientation
from datetime import datetime
import requests
import discord
import string
import random
import base64
import io
import os
from dotenv import load_dotenv

# load environment settings
# first use .env.development if found, else use .env.deploy
# NOTE: These file are NOT versioned by git, since they contain your local settings
dotenv_path = os.getenv('ENVIRONMENT_FILE', os.path.join(os.getcwd(), '.env.development'))
if not os.path.exists(dotenv_path):
    dotenv_path = os.path.join(os.getcwd(), '.env.deploy')

load_dotenv(dotenv_path=dotenv_path, override=True)
SD_HOST = os.environ.get('HOST', 'localhost')
SD_PORT = int(os.environ.get('PORT', '7680'))
SD_VARIATION_STRENGTH = float(os.environ.get('SD_VARIATION_STRENGTH', '0.065'))
SD_UPSCALER = os.environ.get('SD_UPSCALER','R-ESRGAN 4x+')
BOT_KEY = os.environ.get('BOT_KEY', None)

# Apply Settings:
webui_url = f"http://{SD_HOST}:{SD_PORT}"   # URL/Port of the A1111 webui
upscaler_model = SD_UPSCALER                # How much should the varied image varie from the original?
variation_strength = SD_VARIATION_STRENGTH  # Name of the upscaler. I recommend "4x_NMKD-Siax_200k" but you have to download it manually.
discord_bot_key = BOT_KEY                   # Set this to the discord bot key from the bot you created on the discord devoloper page.

# Initialize
bot = discord.Bot()
os.system('clear')
print ("Bot is running")
characters = string.ascii_letters + string.digits
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = GPT2LMHeadModel.from_pretrained('FredZhang7/distilgpt2-stable-diffusion-v2')
with open('current_requests.txt', 'r') as file:
    total_requests = int(file.read())
    
# The single upscale button after generating a variation
class UpscaleOnlyView(discord.ui.View):
    def __init__(self, filename, **kwargs):
        super().__init__(**kwargs)
        self.filename = filename

    @discord.ui.button(label="Upscale", style=discord.ButtonStyle.primary, emoji="🖼️") 
    async def button_upscale(self, button, interaction):
        await interaction.response.send_message(f"Upscaling the image...", ephemeral=True, delete_after=3)
        upscaled_image = await upscale(self.filename)
        with open(upscaled_image, 'rb') as f:
            image_bytes = f.read()
        message = await interaction.followup.send(f"Upscaled This Generation:", file=discord.File(io.BytesIO(image_bytes), f'upscaled.png'))

# The upscale L and upscale R button after retrying
class UpscaleOnlyView2(discord.ui.View):
    def __init__(self, filename, filename2, **kwargs):
        super().__init__(**kwargs)
        self.filename = filename
        self.filename2 = filename2

    @discord.ui.button(label="Upscale L", style=discord.ButtonStyle.primary, emoji="🖼️") 
    async def button_upscale2(self, button, interaction):
        await interaction.response.send_message(f"Upscaling the image...", ephemeral=True, delete_after=3)
        upscaled_image = await upscale(self.filename)
        with open(upscaled_image, 'rb') as f:
            image_bytes = f.read()
        message = await interaction.followup.send(f"Upscaled This Generation:", file=discord.File(io.BytesIO(image_bytes), f'upscaled.png'))
                                                                                                  
    @discord.ui.button(label="Upscale R", style=discord.ButtonStyle.primary, emoji="🖼️") 
    async def button_upscale3(self, button, interaction):
        await interaction.response.send_message(f"Upscaling the image...", ephemeral=True, delete_after=3)
        upscaled_image = await upscale(self.filename2)
        with open(upscaled_image, 'rb') as f:
            image_bytes = f.read()
        message = await interaction.followup.send(f"Upscaled This Generation:", file=discord.File(io.BytesIO(image_bytes), f'upscaled.png'))

# The main button rows, contains Upscale L/R, Variation L/R and Retry
# Variation generates almost the same image again using same settings / seed. In addition, this uses an variation strengt.
# We have to refernce all the settings like you see below to generate the correct image again - or we need a reference to the filename to upscale it.
class MyView(discord.ui.View):
    def __init__(self, prompt, style, orientation, negative_prompt, seed, filename, image_id, seed1, filename1, image_id1, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompt
        self.style = style
        self.orientation = orientation
        self.negative_prompt = negative_prompt
        self.seed = seed
        self.filename = filename
        self.image_id = image_id
        self.seed1 = seed1
        self.filename1 = filename1
        self.image_id1 = image_id1

    @discord.ui.button(label="Upscale L", row=0, style=discord.ButtonStyle.primary, emoji="🖼️") 
    async def button_upscale(self, button, interaction):
        await interaction.response.send_message(f"Upscaling the image...", ephemeral=True, delete_after=4)
        upscaled_image = await upscale("GeneratedImages/" + self.image_id + ".png")
        with open(upscaled_image, 'rb') as f:
            image_bytes = f.read()
        message = await interaction.followup.send(f"Upscaled This Generation:", file=discord.File(io.BytesIO(image_bytes), f'{self.prompt}-{self.style}-upscaled.png'))
        
    @discord.ui.button(label="Upscale R", row=0, style=discord.ButtonStyle.primary, emoji="🖼️") 
    async def button_upscale2(self, button, interaction):
        await interaction.response.send_message(f"Upscaling the image...", ephemeral=True, delete_after=4)
        upscaled_image = await upscale("GeneratedImages/" + self.image_id1 + ".png")
        with open(upscaled_image, 'rb') as f:
            image_bytes = f.read()
        message = await interaction.followup.send(f"Upscaled This Generation:", file=discord.File(io.BytesIO(image_bytes), f'{self.prompt}-{self.style}-upscaled.png'))
        
    @discord.ui.button(label="Variation L", row=1, style=discord.ButtonStyle.primary, emoji="🌱") 
    async def button_variation(self, button, interaction):
        await interaction.response.send_message(f"Creating a variation of the image...", ephemeral=True, delete_after=4)  
        variation_image, image_id = await imagegen(self.prompt, self.style, self.orientation, self.negative_prompt, self.seed, variation=True)
        with open(variation_image, 'rb') as f:
            image_bytes = f.read()
        message = await interaction.followup.send(f"Varied This Generation:", file=discord.File(io.BytesIO(image_bytes), f'{self.prompt}-{self.style}-{image_id}-varied.png'), view=UpscaleOnlyView(f"GeneratedImages/{image_id}.png"))
        
    @discord.ui.button(label="Variation R", row=1, style=discord.ButtonStyle.primary, emoji="🌱") 
    async def button_variation2(self, button, interaction):
        await interaction.response.send_message(f"Creating a variation of the image...", ephemeral=True, delete_after=4)  
        variation_image, image_id = await imagegen(self.prompt, self.style, self.orientation, self.negative_prompt, self.seed1, variation=True)
        with open(variation_image, 'rb') as f:
            image_bytes = f.read()
        message = await interaction.followup.send(f"Varied This Generation:", file=discord.File(io.BytesIO(image_bytes), f'{self.prompt}-{self.style}-{image_id}-varied.png'), view=UpscaleOnlyView(f"GeneratedImages/{image_id}.png"))
        
    @discord.ui.button(label="Retry", row=2, style=discord.ButtonStyle.primary, emoji="🔄")
    async def button_retry(self, button, interaction):
        await interaction.response.send_message(f"Regenerating the image using the same settings...", ephemeral=True, delete_after=4)
        retried_image, image_id = await imagegen(self.prompt, self.style, self.orientation, self.negative_prompt, random.randint(0, 1000000000000))
        retried_image2, image_id2 = await imagegen(self.prompt, self.style, self.orientation, self.negative_prompt, random.randint(0, 1000000000000))
        retried_images = [
            discord.File(retried_image),
            discord.File(retried_image2),
        ]
        message = await interaction.followup.send(f"Retried These Generations:", files=retried_images, view=UpscaleOnlyView2(f"GeneratedImages/{image_id}.png", f"GeneratedImages/{image_id2}.png"))
        
# This is the function the generate the image and send the request to A1111.
async def imagegen(prompt, style, orientation, original_negativeprompt, seed, variation=False):
    global total_requests
    total_requests = total_requests + 1
    global webui_url
    global variation_strength
    currentTime = datetime.now()   
    width, height = make_orientation(orientation)
    prompt, negativeprompt = make_prompt(prompt, style, original_negativeprompt)
    if variation:
        variation_strength = variation_strength
    else:
        variation_strength = 0
    payload = {
        "prompt": prompt,
        'negative_prompt': negativeprompt,
        "steps": 20,
        'width': width,
        'height': height,
        'cfg_scale': 7,
        'sampler_name': 'Euler',
        'seed': seed,
        'tiling': False,
        'restore_faces': True,
        'subseed_strength': variation_strength
    }
    response = requests.post(url=f'{webui_url}/sdapi/v1/txt2img', json=payload)
    r = response.json()  
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{webui_url}/sdapi/v1/png-info', json=png_payload)
    
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        global characters
        image_id = ''.join(random.choice(characters) for i in range(24))
        file_path = f"GeneratedImages/{image_id}.png"
        image.save(file_path, pnginfo=pnginfo)
        print ("Generated Image:", file_path)
        print (total_requests)
        with open('current_requests.txt', 'w') as file:
            file.write(str(total_requests))
        return file_path, image_id

# Sends the upscale request to A1111
async def upscale(image):  
    global total_requests
    total_requests = total_requests + 1
    with open(image, 'rb') as image_file:
        image_b64 = base64.b64encode(image_file.read()).decode()
    upscale_payload = {
      "upscaling_resize": 4,
      "upscaling_crop": True,
      "gfpgan_visibility": 0.6,
      "codeformer_visibility": 0,
      "codeformer_weight": 0,
      "upscaler_1": "4x_NMKD-Siax_200k",
      "image": image_b64
    }
    response_upscaled = requests.post(url=f'{webui_url}/sdapi/v1/extra-single-image', json=upscale_payload)
    r_u = response_upscaled.json()
    image_bytes = base64.b64decode(r_u['image'])
    image_upscaled = Image.open(io.BytesIO(image_bytes))
    file_path = image
    file_path = file_path.replace('.png', '')
    file_path = f"{file_path}-upscaled.png"
    image_upscaled.save(file_path)
    print ("Upscaled Image:", file_path)
    print (total_requests)
    with open('current_requests.txt', 'w') as file:
        file.write(str(total_requests))
    return file_path
  
async def generate_prompt():
    # This generates a random prompt using a finetuned gpt 2. Uses the transformers library.
    prompt_beginnings = ["landscape of", "a beautiful", "digital concept art", "a", "abstract", "highly detailed", "landscape", "fantasy", "isometric", "Greg Rutkowski", "makoto shinkai", "undergrowth, lush", "volumetric lighting", "4k", "by", "dreamlike", "surreal", "lust city", "By Brad Rigney", "vivid colors"]
    prompt = random.choice(prompt_beginnings)  
    temperature = 0.9  
    top_k = 50              
    max_length = 50        
    repitition_penalty = 1.15
    num_return_sequences=1  
    input_ids = tokenizer(prompt, return_tensors='pt').input_ids
    output = model.generate(input_ids, do_sample=True, temperature=temperature, top_k=top_k, max_length=max_length, num_return_sequences=num_return_sequences, repetition_penalty=repitition_penalty, early_stopping=True)
    return str(tokenizer.decode(output[0], skip_special_tokens=True) + ", colorful, sharp focus")
    
# Command for the 2 random images
@bot.command(description="Generates 2 random images")
async def generate_random(
  ctx: discord.ApplicationContext,
  orientation: discord.Option(str, choices=['Square', 'Portrait', 'Landscape'], default='Square', description='In which orientation should the image be?'),
):
    if ctx.guild is None:
        await ctx.respond("This command cannot be used in direct messages.")
        return
    await ctx.respond("Generating 2 random images...", ephemeral=True, delete_after=4)  
    prompt = await generate_prompt()
    prompt2 = await generate_prompt()
    style = "No Style Preset"
    seed = random.randint(0, 1000000000000)
    seed2 = random.randint(0, 1000000000000)
    negative_prompt = "Default"
    title_prompt = prompt
    if len(title_prompt) > 150:
        title_prompt = title_prompt[:150] + "..."
    title_prompt2 = prompt2
    if len(title_prompt2) > 150:
        title_prompt2 = title_prompt2[:150] + "..."
    embed = discord.Embed(
            title="Generated 2 random images using these settings:",
            description=f"Prompt (Left): `{title_prompt}`\nPrompt (Right): `{title_prompt2}`\nOrientation: `{orientation}`\nSeed (Left): `{seed}`\nSeed (Right): `{seed2}`\nNegative Prompt: `{negative_prompt}`",
            color=discord.Colour.blurple(),
        )
    generated_image, image_id = await imagegen(prompt, style, orientation, negative_prompt, seed)
    generated_image2, image_id2 = await imagegen(prompt2, style, orientation, negative_prompt, seed2)
    generated_images = [
        discord.File(generated_image),
        discord.File(generated_image2),
    ]
    with open(generated_image, 'rb') as f:
        image_bytes = f.read()
    if len(prompt) > 100:
        prompt = prompt[:100]
    message = await ctx.respond(f"<@{ctx.author.id}>'s Random Generations:", files=generated_images, view=MyView(prompt, style, orientation, negative_prompt, seed, generated_image, image_id, seed2, generated_image2, image_id2), embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('👎')

# Command for the normal 2 image generation
@bot.command(description="Generates 2 image")
async def generate(
  ctx: discord.ApplicationContext,
  prompt: discord.Option(str, description='What do you want to generate?'),
  style: discord.Option(str, choices=['Cinematic', 'Low Poly', 'Anime', 'Oilpainting', 'Cute', 'Comic', 'Steampunk', 'Vintage', 'Natural', 'Cyberpunk', 'Watercolor', 'Apocalyptic', 'Fantasy', 'No Style Preset'], description='In which style should the image be?'),
  orientation: discord.Option(str, choices=['Square', 'Portrait', 'Landscape'], default='Square', description='In which orientation should the image be?'),
  negative_prompt: discord.Option(str, description='What do you want to avoid?', default='')
):
    if ctx.guild is None:
        await ctx.respond("This command cannot be used in direct messages.")
        return
    seed = random.randint(0, 1000000000000)
    seed2 = random.randint(0, 1000000000000)
    banned_words = ["nude", "naked", "nsfw", "porn"] # The most professional nsfw filter lol
    if not negative_prompt:
        negative_prompt = "Default"
    for word in banned_words:
        prompt = prompt.replace(word, "clothes :)")
    title_prompt = prompt
    if len(title_prompt) > 150:
        title_prompt = title_prompt[:150] + "..."
    embed = discord.Embed(
            title="Prompt: " + title_prompt,
            description=f"Style: `{style}`\nOrientation: `{orientation}`\nSeed (Left): `{seed}`\nSeed (Right): `{seed2}`\nNegative Prompt: `{negative_prompt}`",
            color=discord.Colour.blurple(),
        )
    await ctx.respond("Generating 2 images...", ephemeral=True, delete_after=3)  
    generated_image, image_id = await imagegen(prompt, style, orientation, negative_prompt, seed)
    generated_image2, image_id2 = await imagegen(prompt, style, orientation, negative_prompt, seed2)
    generated_images = [
        discord.File(generated_image),
        discord.File(generated_image2),
    ]
    if len(prompt) > 100:
        prompt = prompt[:100]
    message = await ctx.respond(f"<@{ctx.author.id}>'s Generations:", files=generated_images, view=MyView(prompt, style, orientation, negative_prompt, seed, generated_image, image_id, seed2, generated_image2, image_id2), embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('👎')

bot.run(discord_bot_key) 