import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import os
import json
import urllib.request
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashCommand, SlashContext
 

with open("config.json") as f:
    config = json.load(f) 
 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["comando"], description="ayuda bot") #Comando
bot.remove_command("help") # Borra el comando por defecto !help
slash = SlashCommand(bot, sync_commands=True)
@slash.slash(
    name="Noticias", description="Noticias Habbo Hotel",
    options=[
                
                 create_option(
                  name="hotel",
                  description="Elige él hotel",
                  option_type=3,
                  required=True,
                  choices=[
                      create_choice(
                          name="ES - Hotel España",
                          value="es"
                      ),
                      create_choice(
                          name="BR - Hotel Brasil",
                          value="com.br"
                      ),
                      create_choice(
                          name="COM - Hotel Estados unidos",
                          value="com"
                      ),
                      create_choice(
                          name="DE - Hotel Aleman",
                          value="de"
                      ),
                      create_choice(
                          name="FR - Hotel Frances",
                          value="fr"
                      ),
                      create_choice(
                          name="FI - Hotel Finalandia",
                          value="fi"
                      ),
                      create_choice(
                          name="IT - Hotel Italiano",
                          value="it"
                      ),
                      create_choice(
                          name="TR - Hotel Turquia",
                          value="com.tr"
                      ),
                      create_choice(
                          name="NL - Hotel Holandés",
                          value="nl"
                      )
                  ]
                
               
                  
                )
             ])
             
            
             

    


async def _noticias(ctx:SlashContext, hotel:str):
    await ctx.defer()

    bandera_dict = {
    "es": "https://i.imgur.com/IplIfNP.png",
    "com.br":  "https://i.imgur.com/YGQlPor.png",
    "nl":"https://i.imgur.com/fC8eIvR.png",
    "de":"https://i.imgur.com/vUgY11U.png",
    "fr":"https://i.imgur.com/CoLWbjf.png",
    "it":"https://i.imgur.com/va1X4j6.png",
    "com":"https://i.imgur.com/D6vwN9n.png",
    "com.tr":"https://i.imgur.com/wtiow4R.png",
    "fi":"https://i.imgur.com/BpQCpVi.png"
    }
    bandera = bandera_dict[str(hotel)]
    ####
    HotelNoticia_dict = {
    "es": "es",
    "com.br":  "pt",
    "nl":"nl",
    "de":"de",
    "fr":"fr",
    "it":"it",
    "com":"en",
    "com.tr":"tr",
    "fi":"fi"
    }
    HotelNoticia = HotelNoticia_dict[str(hotel)]
    HotelNoticia=f"{HotelNoticia}" ## es -> en -> it -> de-> fr -> fi -> fi -> tr -> nl -> pt 
    url = f"https://images.habbo.com/habbo-web-news/{HotelNoticia}/production/front.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    hotel=f"{hotel}" ## es -> com ->it -> de -> fr -> com.tr ->nl -> com.br

    titulo = soup.find_all('h2', class_='news-header__title')[1].text

    imagen = soup.find_all('img')[2]
    imagenPeque = soup.find_all('img')[3]

    urlNoticia = soup.find_all('a', class_="news-header__link news-header__banner")[1]

    descripcion = soup.find_all('p', class_='news-header__wrapper news-header__summary')[1].text 
    #####

    embed = discord.Embed(title=f"{titulo}", description=f"{descripcion}" f"\n\n\n[Ver Noticia en Habbo.{hotel}]"+"("+ f"https://habbo.{hotel}"+urlNoticia['href']+ ")", color=discord.Colour.random())
    embed.set_image(url=f"{imagen['src']}" )
    embed.set_author(name=f"Habbo [{HotelNoticia}]",  icon_url=f"{bandera}")
    embed.set_footer(text=f"habbo [{HotelNoticia}]", icon_url="https://i.imgur.com/6ePWlHz.png")

    embed.set_thumbnail(url=f"{imagenPeque['src']}" )
    await ctx.send(embed=embed)
   
 
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send('El comando no existe 🤷🏼‍♂️🔍')
  

@bot.event
async def on_ready():
    print("BOT listo!")





bot.run(config["token_discord"])