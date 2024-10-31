import contextvars
import difflib
import aiohttp
import disnake
import disnake_plugins
from disnake.ext import commands
from bot import CaddieBot
import numpy as np
from decimal import Decimal
from logger import logger

plugin = disnake_plugins.Plugin()

@plugin.slash_command(description="Calculates ratings for a specified course and layout.")
async def get_ratings(
    inter: disnake.CommandInteraction, 
    course_name: str = commands.Param(max_length=100, description="Name of course you played"), 
    layout_name: str = commands.Param(max_length=100, description="Name of course layout you played"),
    score: int = commands.Param(description="Your score, relative to par")):
    """
    Fetches ratings for a specified course and layout.
    Args:
        inter (disnake.CommandInteraction): The interaction object for the command.
        course_name (str, optional): The name of the course to get ratings for. Defaults to a maximum length of 100 characters.
        layout_name (str, optional): The name of the course layout to rate. Defaults to a maximum length of 100 characters.
    Returns:
        None
    """
    bot: CaddieBot = plugin.bot
    rounds = bot.database.query_all_course_rounds(course_name)
    if len(rounds) == 0:
        all_courses = [course.readable_course_name for course in bot.database.query_all_courses()]
        similar_course_names = difflib.get_close_matches(course_name, all_courses)
        await inter.response.send_message(f"No rounds found for {course_name}. Did you mean one of the following:\n{', '.join(similar_course_names)}?")
        return
    
    matching_rounds = [round for round in rounds if round.layout_name == layout_name]
    rounds_used = len(matching_rounds)
    if rounds_used == 0:
        all_layout_names = [round.layout_name for round in rounds]
        similar_layout_names = set(difflib.get_close_matches(layout_name, all_layout_names, n=100))
        await inter.response.send_message(f"No rounds found for {layout_name} at {course_name}. Did you mean one of the following:\n{', '.join(similar_layout_names)}?")
        return
    
    # par_ratings = np.array([round.par_rating for round in matching_rounds])
    # stroke_values = np.array([round.stroke_value for round in matching_rounds])

    # par_rating_mean = np.mean(par_ratings)
    # par_rating_std = np.std(par_ratings)
    # stroke_value_mean = np.mean(stroke_values)
    # stroke_value_std = np.std(stroke_values)

    # filtered_rounds = [
    #     round for round in matching_rounds 
    #     if abs(round.par_rating - par_rating_mean) <= 2 * par_rating_std and 
    #        abs(round.stroke_value - stroke_value_mean) <= 2 * stroke_value_std
    # ]

    # rounds_used = len(filtered_rounds)
    # if rounds_used == 0:
    #     await inter.response.send_message(f"All rounds for {layout_name} at {course_name} are considered outliers.")
    #     return

    average_par_rating = sum([round.par_rating for round in matching_rounds]) / rounds_used
    average_stroke_value = sum([round.stroke_value for round in matching_rounds if round.stroke_value > 0]) / rounds_used
    average_par_rating = Decimal(average_par_rating)
    average_stroke_value = Decimal(average_stroke_value)
    calculated_rating = int(average_par_rating - (Decimal(score) * average_stroke_value))
    
    await inter.response.send_message(f"Calculated rating: {calculated_rating} based on {rounds_used} rounds at {layout_name} on {course_name}")

setup, teardown = plugin.create_extension_handlers()
