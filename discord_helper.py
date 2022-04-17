"""
Author : CoachD
Discord : CoachD#4633
Date : 2022-04-16
Brief : This file contains all the methods that helps to manage mentionned users and the embeds.
Description : Bot to help people to create raid groups.
"""
import re
import discord


class DiscordGroupHelper():
    def getIdFromMentionedUser(user_mentionned: str):
        """
        Get the user id from the user mentionned string
        :param user_mentionned_string: user mentionned
        """
        return " ".join(re.findall("[0-9]+", user_mentionned))

    async def getUsersObjectsFromUsersIds(users_ids: list, bot: discord.Bot):
        """
        Get the users object from the users id
        :param users_ids: list of users id
        :param bot: bot object
        """
        users_objects = []
        for user_id in users_ids:
            user_object = await bot.get_or_fetch_user(int(user_id))
            users_objects.append(user_object)
        return users_objects
        pass

    def get_embed_event_group(event: object, color: int = discord.Colour.blurple(), players: list = None, date: str = None, author: discord.Member = None):
        """
        Get the embed object
        """

        ilvl_text = f":dagger: **Niveau minimum requis** : { event['ilvl'] }"

        date_text = f":date: **Date de disponibles** : {date}"

        players_text = ":mage: **Membres**\n"
        for i in range(event["capacity"]):
            player = "- "
            if i < len(players):
                player += f"<@{players[i].id}>"
            players_text += player + "\n"

        guides_urls_md = "**Guides**\n"
        for i in range(len(event["guides_url"])):
            guides_urls_md += "[Guide " + \
                str(i+1) + "](" + event["guides_url"][i] + "); "

        embed = discord.Embed(
            title=f"{event['tier']} : {event['type']} - {event['name']}",
            description=f"{ilvl_text} \n {date_text} \n\n {players_text} \n\n {guides_urls_md}",
            # Pycord provides a class with default colors you can choose from
            color=color,
        )

        # Set the author of the embed
        #embed.set_author(name=author, icon_url=author.avatar)
        embed.set_image(url=event["image_url"])
        return embed

    def get_embed_events_available(events: list, author: discord.Member = None):
        embed = discord.Embed(
            title="Liste des événements disponibles",
            # Pycord provides a class with default colors you can choose from
            color=discord.Colour.blurple(),
        )

        for event in events:
            embed.add_field(
                name=f"ID : {event['id']}", value=f"{event['name']} - {event['tier']}", inline=False)

        embed.set_author(name=author, icon_url=author.avatar)
        return embed

    async def create_embed_thread_and_add_players(event: object, players: list, date: str, ctx: discord.ext.commands.Context, interact: discord.Interaction):
        embed = DiscordGroupHelper.get_embed_event_group(
            event=event, players=players, date=date, author=ctx.author)

        await interact.edit_original_message(content="", embed=embed)

        # Getting the inital message that the bot sent to make a thread from it
        msg = await interact.original_message()
        # Thread creation
        thread = await ctx.channel.create_thread(name=event["tier"] + " : " + event["name"], message=msg, auto_archive_duration=1440)

        # Adding the players to the thread
        for user in players:
            await thread.add_user(user=user)
