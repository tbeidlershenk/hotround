import datetime
import disnake
import disnake_plugins
from disnake.ext import commands
from bot import CaddieBot
from logger import logger
from fuzzywuzzy import fuzz, process
from Paginator import CreatePaginator
from models.round import group_comparable_rounds

plugin = disnake_plugins.Plugin()
NEWLINE = '\n'
COMMASPACE = ', '

@plugin.slash_command(description="Calculates ratings for a specified course and layout")
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
    all_course_names = [course.readable_course_name for course in bot.database.query_courses()]
    scored_course_names: tuple[str, int] = process.extractBests(course_name, all_course_names, scorer=fuzz.token_set_ratio, score_cutoff=0, limit=5)

    # ERR: No close course matches
    if len(scored_course_names) == 0 or scored_course_names[0][1] < 90:
        similar_course_names = [course for course, _ in scored_course_names]
        await inter.response.send_message(embed=disnake.Embed.from_dict({
            "title": f"{course_name}, {layout_name}: {score if score < 0 else '+' + str(score) if score > 0 else 'E'}",
            "description": f"No close matches for course '{course_name}'.",
            "color": 0x1491A0,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": "CaddieBot",
                "url": "https://www.pdga.com/",
                "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
            },
            "fields": [
                {"name": "Did you mean:", "value": f"{NEWLINE.join(similar_course_names[:5])}", "inline": "false"},
            ]
        }), ephemeral=False)
        return
    
    rounds = bot.database.query_rounds_for_course(course_name)
    all_layout_names = set([round.layout_name for round in rounds])
    scored_layouts: tuple[str, int] = process.extractBests(layout_name, all_layout_names, scorer=fuzz.partial_token_sort_ratio, score_cutoff=0, limit=10)

    # ERROR: No sanctioned rounds
    if len(scored_layouts) == 0:
        await inter.response.send_message(embed=disnake.Embed.from_dict({
            "title": f"{course_name}, {layout_name}: {score if score < 0 else '+' + str(score) if score > 0 else 'E'}",
            "description": f"No PDGA tournaments found for '{course_name}'.",
            "color": 0x1491A0,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": "CaddieBot",
                "url": "https://www.pdga.com/",
                "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
            }
        }), ephemeral=False)
        return
    
    # ERROR: No close layout matches
    if scored_layouts[0][1] < 75:
        similar_layout_names = [layout for layout, _ in scored_layouts]
        await inter.response.send_message(embed=disnake.Embed.from_dict({
            "title": f"{course_name}, {layout_name}: {score if score < 0 else '+' + str(score) if score > 0 else 'E'}",
            "description": f"No close matches for layout '{layout_name}'.",
            "color": 0x1491A0,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": "CaddieBot",
                "url": "https://www.pdga.com/",
                "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
            },
            "fields": [
                {"name": "Did you mean:", "value": f"{NEWLINE.join(similar_layout_names[:5])}", "inline": "false"},
            ]
        }), ephemeral=False)
        return

    matching_layout_names = [layout for layout, _ in process.extractBests(layout_name, all_layout_names, scorer=fuzz.partial_token_sort_ratio, score_cutoff=75, limit=100)]
    matching_rounds = [round for round in rounds if round.layout_name in matching_layout_names]
    grouped_layouts = group_comparable_rounds(matching_rounds)
    embeds = [
        disnake.Embed.from_dict({
            "title": f"{course_name}, {layout_name}: {score if score < 0 else '+' + str(score) if score > 0 else 'E'}",
            "description": f"Found {len(grouped_layouts)} results that might match your query.\nLayouts are matched using hole distances\n(pin positions) & total par.",
            "color": 0x1491A0,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": "CaddieBot",
                "url": "https://www.pdga.com/",
                "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
            },
            "fields": [
                {"name": "PDGALive layouts used", "value": f"{NEWLINE.join(layout.layout_names)}", "inline": "false"},
                {"name": "Layout information", "value": "", "inline": "false"},
                {"name": "", "value": f"{layout.hole_distances(3)[0]}", "inline": "true"},
                {"name": "", "value": f"{layout.hole_distances(3)[1]}", "inline": "true"},
                {"name": "", "value": f"{layout.hole_distances(3)[2]}", "inline": "true"},
                {"name": "", "value": f"{layout.course_metadata()}", "inline": "false"},
                {"name": "Calculated rating", "value": f"{layout.score_rating(score)}", "inline": "false"},
            ]
        })
        for layout in grouped_layouts
    ]

    author_id = inter.author.id 
    await inter.response.send_message(embed=embeds[0], view=CreatePaginator(embeds, author_id), ephemeral=False) 
    logger.info(f"User {author_id} requested ratings for {course_name}, {layout_name} with score {score}")

setup, teardown = plugin.create_extension_handlers()
