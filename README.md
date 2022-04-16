# Introduction

Firstly, be aware this bot uses the beta of the pycord library. So, errors can happens.
This project use `python3`.

# Installation

## Venv

Make sure to create a `venv` :

```bash
$ python3 -m venv <name of your venv>
```

Then switch to your venv

```bash
$ source ./venv/bin/activate
```

To quit the venv just make :

```bash
(venv) $ deactivate
```

## Install dependancies

To install the dependancies, make sure you're in your `venv` and then :

```bash
(venv) $ pip3 install -r requirement.txt
```

Make sure to be at the root of the project.

## Discord

### Create your bot

Go on [Discord Developer Portal](https://discord.com/developers/applications) and create a new application. Then go on "Bot" section and click "Add bot".

### Get your bot token

To get your bot token, go on "Bot" section in the [Discord Developer Portal](https://discord.com/developers/applications). You'll see a "Token" subsection. If you don't see your token, please click on "Reset Token". Then, you'll have access to your Discord Bot Token. Make sure to keep it safe.

### Add your bot to your server

To add your bot to your server, go on the "General" section, take your "application id" and replace it in this url :

```
https://discord.com/api/oauth2/authorize?client_id=<app_id>&permissions=395137001472&scope=applications.commands%20bot
```

## Environment variables

This project contains a Discord bot token. We saw on the previous section how to get your bot token. To keep it safe, we use `dotenv` which is a lib that allow you to store environment variables for your project.

To put it in the app, start to make a copy of the `.env.example` file and rename `.env`. Then, put your bot token and your server id in the `.env` file like this.

```
TOKEN=<your bot token>
GUILD_ID=<your discord server id>
```

Now, you are good to run the application

## Run the application

```
(venv) $ python3 main.py
```

# Guide

## Add a new event

To add new events, make sure to put them in the `data.json` file at the end of the `events` array. Put the correct attributes in it.

## Let all the servers run the bot commands

Replace this line in the `main.py`:

```Python
bot = discord.Bot(debug_guilds=[int(os.getenv('GUILD_ID'))])
```

by this line

```Python
bot = discord.Bot()
```

`/!\ Warning` : Your commands can take some time to be registered on all the servers

## Change the look of the embeds

To change the look of the embeds, you need to go on the `discord_helper.py` file and change the `get_embed_event_group()` and the `get_embeds_events_available()` methods. You can check the [Embed doc](https://docs.pycord.dev/en/master/api.html?highlight=embed#discord.Embed) of Pycord.
