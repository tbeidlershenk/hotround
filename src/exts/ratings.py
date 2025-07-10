import datetime
import disnake
import disnake_plugins
from disnake.ext import commands
from fuzzywuzzy import fuzz, process
from logger import logger
from ui.options import CreateOptions
from bot import HotRoundBot
from models.layout import AggregateLayout
import disnake
from disnake.ext import commands

plugin = disnake_plugins.Plugin()
NEWLINE = '\n'
COMMASPACE = ', '

def layout_to_str(layout: AggregateLayout, num_results = 3) -> str:
    return "\n".join([f"H{x+1} • Par {layout.pars[x]} • **{layout.distances[x]}**'" for x in range(min(layout.num_holes, num_results))])

@plugin.slash_command(description="Calculates ratings for a specified course and layout")
async def ratings(
    inter: disnake.CommandInteraction, 
    course_name: str = commands.Param(max_length=100, description="Name of course you played"), 
    # TODO find a better solution for UX purposes
    layout_keywords: str = commands.Param(max_length=200, default="", description="Comma separated keywords (ex. 'Gold, Long, MPO' )"), 
    score: int = commands.Param(description="Your score, relative to par")):

    await inter.response.defer()
    bot: HotRoundBot = plugin.bot

    all_course_names = [course.readable_course_name for course in bot.database.query_courses()]
    scored_course_names: tuple[str, int] = process.extractBests(course_name, all_course_names, scorer=fuzz.token_set_ratio, score_cutoff=0, limit=5)
    similar_course_names = [course for course, _ in scored_course_names]
    chosen_course_name = similar_course_names[0] if similar_course_names else course_name
    aggregate_layouts = bot.database.query_aggregate_layouts(chosen_course_name)
    num_results = len(aggregate_layouts)

    # ERROR: No sanctioned rounds
    if num_results == 0:
        embeds=[disnake.Embed.from_dict({
            "title": f"{chosen_course_name}: {score if score < 0 else '+' + str(score) if score > 0 else 'E'}",
            "description": f"No PDGA tournaments found for '{chosen_course_name}'.\n\n*Wrong course? Click ❓*",
            "color": 0xFF1B29,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": "HotRound",
                "url": "https://hotround.site",
                "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
            },
        })]
        await inter.followup.send(embed=embeds[0], view=CreateOptions(embeds, similar_course_names, disable_pagination=True, author_id=inter.author.id, timeout=600))
        return
    
    layout_keywords = layout_keywords.replace(' ', '').split(',')
    aggregate_layouts.sort(key=lambda x: x.score_layout_tokens(layout_keywords), reverse=True)
    embeds = [
        disnake.Embed.from_dict({
            "title": f"{score if score < 0 else '+' + str(score) if score > 0 else 'E'} is **{layout.score_rating(score)} rated**",
            "color": 0x008E6F,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": "HotRound",
                "url": "https://hotround.site",
                "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
            },
            "description": f"""
                **__{chosen_course_name}__**\n*{layout.descriptive_name}*\n**{layout.total_distance}'**, par **{layout.total_par}**\n{layout_to_str(layout, num_results=3)}...\n\nCalculated from **{layout.num_layouts}** rounds\nEvents: **{COMMASPACE.join(layout.layout_links()[:5])}**\n\n*Wrong layout? Click ➡️\nWrong course? Click ❓*""",
            "footer": {
                "text": f"Result {i+1} of {num_results}"
            }
        }) 
        for i, layout in enumerate(aggregate_layouts)]

    logger.info(f"User {inter.author.name} requested ratings for {chosen_course_name} with score {score}")
    await inter.followup.send(embed=embeds[0], view=CreateOptions(embeds, similar_course_names, author_id=inter.author.id, timeout=600)) 

setup, teardown = plugin.create_extension_handlers()
