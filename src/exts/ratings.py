import datetime
import disnake
import disnake_plugins
from disnake.ext import commands
from fuzzywuzzy import fuzz, process
from itertools import groupby
from logger import logger
from ui.options import CreateOptions
from bot import HotRoundBot
from models.layout import AggregateLayout
import disnake
from disnake.ext import commands
from util.matching import course_name_contains_tokens, filter_duplicates

from discord.embeds import Embeds
from discord.ratings_view import RatingsView

plugin = disnake_plugins.Plugin()

@plugin.slash_command(description="Calculates ratings for a specified course and layout")
async def ratings(
    inter: disnake.CommandInteraction, 
    course: str = commands.Param(max_length=100, description="Name of course you played"), 
    score: int = commands.Param(description="Your score, relative to par", default=0)):

    # defer response to give IO time
    await inter.response.defer()
    bot: HotRoundBot = plugin.bot

    # query and match courses to search
    courses = bot.database.query_courses()

    # filter out duplicates
    courses = filter_duplicates(courses)
    
    # simple token match
    search_tokens = course.split(' ')
    matching_courses = [x for x in courses if course_name_contains_tokens(x, search_tokens)]

    # abort, no matches found
    if len(matching_courses) == 0:
        await inter.followup.send(embed=Embeds.no_matches(course))
        return

    # send the courses to a dropdown flow
    matching_courses.sort(key=lambda x: len(x.get_name_tokens()))
    matching_courses_str = [x.to_json() for x in matching_courses]
    await inter.followup.send("", view=RatingsView(matching_courses_str, score))

    logger.info(f"User {inter.author.name} requested ratings for {course} with score {score}")

setup, teardown = plugin.create_extension_handlers()
