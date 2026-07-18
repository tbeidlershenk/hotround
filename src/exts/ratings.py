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
from util.database import Database
from util.matching import course_name_contains_tokens, filter_duplicates
from util.helpers import dgscene_url_to_course_id

from discord.embeds import Embeds
from discord.ratings_view import RatingsView

plugin = disnake_plugins.Plugin()

@plugin.slash_command(description="Calculates ratings for a specified course and layout")
async def ratings(
    inter: disnake.CommandInteraction, 
    course_name: str = commands.Param(max_length=100, description="Name of course you played", default=None),
    dgscene_url: str = commands.Param(max_length=100, description="DiscGolfScene link of course you played", default=None), 
    score: int = commands.Param(description="Your score, relative to par", default=0)):

    if dgscene_url == None and course_name == None:
        await inter.response.send_message("Please supply either `course_name` or `dgscene_url` parameters")
        return

    # defer response to give IO time
    await inter.response.defer()
    bot: HotRoundBot = plugin.bot
    db: Database = bot.database
    matching_courses = []
    
    course_id = dgscene_url_to_course_id(dgscene_url)
    if course_id != -1:
        # get course by course id
        course = db.query_course(course_id)
        matching_courses = [course]
    else:
        # query and match courses to search
        courses = db.query_courses()
        courses = filter_duplicates(courses)

        # simple token match
        search_tokens = course_name.split(' ')
        matching_courses = [x for x in courses if course_name_contains_tokens(x, search_tokens)]
        
        # sort by number of tokens matched
        matching_courses.sort(key=lambda x: len(x.get_name_tokens()))

    # abort, no matches found
    if len(matching_courses) == 0:
        await inter.followup.send(embed=Embeds.no_matches(course_name))
        return

    # send the courses to a dropdown flow
    matching_courses_str = [x.to_json() for x in matching_courses]
    await inter.followup.send("", view=RatingsView(matching_courses_str, score))
    
    logger.info(f"User {inter.author.name} requested ratings for {course_name if dgscene_url is None else dgscene_url} with score {score}")

setup, teardown = plugin.create_extension_handlers()
