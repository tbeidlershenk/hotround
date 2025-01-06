import datetime
import disnake
import disnake_plugins
from disnake.ext import commands
from fuzzywuzzy import fuzz, process
from logger import logger
from Paginator import CreatePaginator
from bot import CaddieBot
from models.layout import AggregateLayout
import disnake
from disnake.ext import commands

plugin = disnake_plugins.Plugin()
NEWLINE = '\n'
COMMASPACE = ', '

def layout_to_markdown_table(layout: AggregateLayout, row_size = 6) -> str:
    rows = []
    for i in range(layout.num_holes // row_size):
        start = i * row_size
        end = (i + 1) * row_size
        holes = [f"H{x}".ljust(5) for x in range(start + 1, end + 1)]
        pars = [str(x).ljust(5) for x in layout.pars[start:end]]
        distances = [str(x).ljust(5) for x in layout.distances[start:end]]
        row = ""+"".join(holes) + "\n"
        row += ""+"".join(pars) + "\n"
        row += "" +"".join(distances) + "\n"
        rows.append(row)
    return ("----------------------------" + "\n").join(rows)

def layout_to_str(layout: AggregateLayout, num_results = 3) -> str:
    return "\n".join([f"H{x+1} • Par {layout.pars[x]} • **{layout.distances[x]}**'" for x in range(min(layout.num_holes, num_results))])

@plugin.slash_command(description="Calculates ratings for a specified course and layout")
async def ratings(
    inter: disnake.CommandInteraction, 
    course_name: str = commands.Param(max_length=100, description="Name of course you played"), 
    # TODO find a better solution for UX purposes
    layout_keywords: str = commands.Param(max_length=200, default="", description="Comma separated keywords (ex. 'Gold, Long, MPO' )"), 
    score: int = commands.Param(description="Your score, relative to par")):
    """
    Fetches ratings for a specified course and layout.
    Args:
        inter (disnake.CommandInteraction): The interaction object for the command.
        course_name (str, required): The name of the course to get ratings for. Defaults to a maximum length of 100 characters.
        score (int, required): the sscore to use to calculate ratings
    Returns:
        None
    """
    bot: CaddieBot = plugin.bot
    all_course_names = [course.readable_course_name for course in bot.database.query_courses()]
    scored_course_names: tuple[str, int] = process.extractBests(course_name, all_course_names, scorer=fuzz.token_set_ratio, score_cutoff=0, limit=5)
    
    # ERROR: No close course matches
    if course_name not in [course for course, _ in scored_course_names]:
        similar_course_names = [course for course, _ in scored_course_names]
        await inter.response.send_message(embed=disnake.Embed.from_dict({
            "title": f"{course_name}: {score if score < 0 else '+' + str(score) if score > 0 else 'E'}",
            "description": f"No matches for course '{course_name}'.",
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
    
    aggregate_layouts = bot.database.query_aggregate_layouts(course_name)
    num_results = len(aggregate_layouts)

    # ERROR: No sanctioned rounds
    if num_results == 0:
        await inter.response.send_message(embed=disnake.Embed.from_dict({
            "title": f"{course_name}: {score if score < 0 else '+' + str(score) if score > 0 else 'E'}",
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
    
    layout_keywords = layout_keywords.replace(' ', '').split(',')
    aggregate_layouts.sort(key=lambda x: x.score_layout_tokens(layout_keywords), reverse=True)
    embeds = [
        disnake.Embed.from_dict({
            "title": f"{score if score < 0 else '+' + str(score) if score > 0 else 'E'} is **{layout.score_rating(score)} rated**",
            "color": 0x008E6F,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": "CaddieBot",
                "url": "https://www.pdga.com/",
                "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
            },
            "description": f"""
                **__{course_name}__**\n*{layout.descriptive_name}*\n**{layout.total_distance}'**, par **{layout.total_par}**\n{layout_to_str(layout, num_results=3)}...\n\nCalculated from **{layout.num_layouts}** rounds\nEvents: **{COMMASPACE.join(layout.layout_links()[:5])}**\n\n*Wrong layout? Click below :)*""",
            "footer": {
                "text": f"Result {i+1} of {num_results}"
            }
        }) 
        for i, layout in enumerate(aggregate_layouts)]

    logger.info(f"User {inter.author.name} requested ratings for {course_name} with score {score}")
    await inter.response.send_message(embed=embeds[0], view=CreatePaginator(embeds, author_id=inter.author.id, timeout=600)) 

setup, teardown = plugin.create_extension_handlers()
