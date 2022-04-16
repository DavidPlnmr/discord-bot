"""
Author : CoachD
Discord : CoachD#4633
Date : 2022-04-16
Brief : This is the main file of the bot. It contains all the commands and the bot's main loop.
Description : Bot to help people to create raid groups.
"""
import discord
from discord.ext import commands
import os  # default module
from dotenv import load_dotenv
from discord_helper import DiscordHelper
import logging
import json

# Create log file
dir = "./log"
log_path = os.path.join(dir, "app.log")
if not os.path.isdir(dir):
    os.mkdir(dir)
if not os.path.isfile(log_path):
    f = open(log_path, "w")
    f.close()

logging.basicConfig(level=logging.INFO, filename='./log/app.log',
                    filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()  # load all the variables from the env file
logging.info("Loading variables from .env file")

# Loading data file with events
f = open("data.json", "r")
data = json.load(f)
events = data["events"]


# create a bot object
# debug guilds permits you to only use the bot in a specific guild.
# If you don't specify the guilds, the bot will be able to be used in all the guilds.
bot = discord.Bot(debug_guilds=[int(os.getenv('GUILD_ID'))])


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# Classic ping command
@bot.slash_command(name="ping", description="Ping the bot")
async def ping(ctx):
    await ctx.respond("Pong!")


async def respond_and_wait_msg_from_same_user(response: str, ctx: discord.ext.commands.Context):
    interact = await ctx.respond(response)
    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    return interact, response


async def edit_msg_and_wait_msg_from_same_user(msg: discord.Interaction, response: str, ctx: discord.ext.commands.Context):
    await msg.edit_original_message(content=response)
    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    return msg


@bot.slash_command(name="create_group", description="Crée un groupe avec les membres mentionnés")
# Role who can use this command
@commands.has_role("Organisation Events")
# Use any role if multiple roles are needed
# @commands.has_any_role(constants.ROLE_NAME)
async def create_group(ctx, event_id: int):
    logging.info(f"{ctx.author} asked to create a group for event {event_id}")
    # Get the event from the event id
    try:
        event = next(event for event in events if event["id"] == int(event_id))
    except StopIteration:
        # Saying at the user that
        await ctx.respond("Event non trouvé. `/events_available` pour voir la liste des évenements disponibles")
        logging.error(f"{ctx.author} specified an event that doesn't exist")
        return

    # Get the response of the user.
    # We keep the interact var because we want to edit the message later
    interact, response = await respond_and_wait_msg_from_same_user('Merci de spécifier une **date**', ctx)

    # Get the date from the response
    date = response.content
    await response.delete()

    response = await edit_msg_and_wait_msg_from_same_user(interact, 'Merci de spécifier les **joueur à ajouter au groupe**. \n**Exemple** : @<Joueur1> : <Classe>, @<Joueur2> : <Classe>, ...', ctx)

    # Get the players from the response
    players = response.content.split(', ')

    # Checking if the capacity has been passed
    if len(players) > event["capacity"]:
        await interact.edit_original_message(content="Vous ne pouvez pas ajouter plus de joueurs que la capacité du groupe")
        logging.error(
            f"{ctx.author} tried to add more players than the capacity. Input : {response.content}")
        return

    # Get players id
    players_id = []
    for player in players:
        players_id.append(DiscordHelper.getIdFromMentionedUser(player))

    # Checking if there is duplicate elements
    if len(players_id) != len(set(players_id)):
        await interact.edit_original_message(content="Vous avez spécifié des joueurs en double")
        logging.error(
            f"{ctx.author} specified duplicate players. Input : {response.content}")
        return

    # Get players object
    # Use to add them in the thread later
    try:
        players_object = await DiscordHelper.getUsersObjectsFromUsersIds(players_id, bot)
    except Exception as e:
        await interact.edit_original_message(content="Vous avez spécifié un joueur inconnu")
        logging.error(
            f"{ctx.author} specified an unknown player. Input : {response.content}")
        return

    await response.delete()

    embed = DiscordHelper.get_embed_event_group(
        event=event, players=players, date=date, author=ctx.author)

    await interact.edit_original_message(content="", embed=embed)

    # Getting the inital message that the bot sent to make a thread from it
    msg = await interact.original_message()
    # Thread creation
    thread = await ctx.channel.create_thread(name=event["tier"] + " : " + event["name"], message=msg, auto_archive_duration=1440)

    # Adding the players to the thread
    for user in players_object:
        await thread.add_user(user=user)
    logging.info(
        f"{ctx.author} created a group for event {event_id} with players {players}")


@bot.slash_command(name="events_available", description="Montre la liste des évenements disponibles")
async def events_available(ctx):
    embed = DiscordHelper.get_embed_events_available(
        events=events, author=ctx.author)
    await ctx.respond("", embed=embed)
    pass

bot.run(os.getenv('TOKEN'))  # run the bot with the token
