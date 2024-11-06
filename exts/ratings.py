import datetime
import disnake
import disnake_plugins
from disnake.ext import commands
from bot import CaddieBot
from fuzzywuzzy import fuzz, process
import logging
from models.round import group_comparable_rounds
from Paginator import CreatePaginator

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
    # await inter.response.defer()
    bot: CaddieBot = plugin.bot
    all_course_names = [course.readable_course_name for course in bot.database.query_all_courses()]
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
    
    course_name = scored_course_names[0][0]
    rounds = bot.database.query_all_course_rounds(course_name)
    all_layout_names = set([round.layout_name for round in rounds])
    scored_layouts: tuple[str, int] = process.extractBests(layout_name, all_layout_names, scorer=fuzz.token_set_ratio, score_cutoff=0, limit=10)

    # ERR: No sanctioned rounds
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
    
    # ERR: No close layout matches
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

    matching_layout_names = [layout for layout, _ in process.extractBests(layout_name, all_layout_names, scorer=fuzz.token_set_ratio, score_cutoff=75, limit=100)]
    matching_rounds = [round for round in rounds if round.layout_name in matching_layout_names]
    grouped_layouts = group_comparable_rounds(matching_rounds, threshold=0.5)
    grouped_layouts.sort(key=lambda x: sum(s for (_, s) in process.extractBests(layout_name, x.layout_names)), reverse=True)
    embeds = [
        disnake.Embed.from_dict({
            "title": f"{course_name}, {layout_name}: {score if score < 0 else '+' + str(score) if score > 0 else 'E'}",
            "description": f"Found {len(grouped_layouts)} results that might match your query.\nLayouts matched with total par, merging pin positions.",
            "color": 0x1491A0,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": "CaddieBot",
                "url": "https://www.pdga.com/",
                "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
            },
            "fields": [
                {"name": "Layouts used", "value": "", "inline": "false"},
                {"name": "", "value": f"{NEWLINE.join(layout.layouts_used()[:5])}", "inline": "false"},
                {"name": "", "value": f"{layout.course_metadata()}", "inline": "false"},
                {"name": "", "value": f"{layout.hole_distances(3)[0]}", "inline": "true"},
                {"name": "", "value": f"{layout.hole_distances(3)[1]}", "inline": "true"},
                {"name": "", "value": f"{layout.hole_distances(3)[2]}", "inline": "true"},
                {"name": "", "value": f"Calculated rating: **{layout.score_rating(score)['rating']}**", "inline": "false"},
            ],
            "footer": {
                "text": f"From {len(layout.layouts_used())} tournament(s), {len(layout.rounds_used)} round",
            }
        })
        for layout in grouped_layouts
    ]
    bot.logger.info(f"User {inter.author.name} requested ratings for {course_name}, {layout_name} with score {score}")
    await inter.response.send_message(embed=embeds[0], view=CreatePaginator(embeds, author_id=inter.author.id, timeout=600)) 

setup, teardown = plugin.create_extension_handlers()
