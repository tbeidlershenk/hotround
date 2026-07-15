import disnake
from disnake.embeds import Embed
from datetime import datetime

from models.course import Course
from models.layout import AggregateLayout

author = {
    "name": "HotRound",
    "url": "https://hotround.tbeidlershenk.dev",
    "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
}

def layout_to_str(layout: AggregateLayout, num_results = 3) -> str:
    return "\n".join([f"H{x+1} • Par {layout.pars[x]} • **{layout.distances[x]}**'" for x in range(min(layout.num_holes, num_results))])

class Embeds:
    def no_matches(searched_name: str) -> Embed:
        description = f"""
            HotRound did not find any courses matching the name {searched_name}.
            
            **Some things to try:**
            1. Use this command with `discgolfscene_url` parameter\n2. Try **[browsing the dataset](https://hotround.tbeidlershenk.dev/courses.txt)**

            If we missed your course,
            **[submit a missing course report](https://forms.google.com)**
        """
        return disnake.Embed.from_dict({
            "title": "No matches found",
            "description": description,
            "color": 0xFF1B29,
            "timestamp": datetime.now().isoformat(),
            "author": author
        })
    
    def course_missing() -> Embed:
        description = """
            The HotRound database may not be complete. Courses
            and events are updated on the **1st of each month.**
            
            **Some things to try:**
            1. Use this command with `discgolfscene_url` parameter\n2. Try **[browsing the dataset](https://hotround.tbeidlershenk.dev/courses.txt)**

            If we missed your course,
            **[submit a missing course report](https://forms.google.com)**
        """
        return disnake.Embed.from_dict({
            "title": f"Don't see your course?",
            "description": description,
            "color": 0xFF1B29,
            "timestamp": datetime.now().isoformat(),
            "author": author
        })
    
    def layout_missing() -> Embed:
        description = """
            The HotRound database may not be complete. Courses
            and events are updated on the **1st of each month.**
            
            Some layouts may not have hosted tournaments.
            If the layout is new, please try again later.

            If we missed your layout,
            **[submit a missing layout report](https://forms.google.com)**
        """
        return disnake.Embed.from_dict({
            "title": f"Don't see your layout?",
            "description": description,
            "color": 0xFF1B29,
            "timestamp": datetime.now().isoformat(),
            "author": author
        })

    def success(course: Course, layout: AggregateLayout, score: int) -> Embed:
        description = f"""
            **__{course.get_name()}__**
            *{layout.descriptive_name}*
            **{layout.total_distance}'**, par **{layout.total_par}**
            {layout_to_str(layout, num_results=3)}...
            
            Calculated from **{layout.num_layouts}** rounds
            Events: **{', '.join(layout.layout_links()[:5])}**
        """
        return disnake.Embed.from_dict({
            "title": f"{score if score < 0 else '+' + str(score) if score > 0 else 'E'} is **{layout.score_rating(score)} rated**",
            "color": 0x008E6F,
            "timestamp": datetime.now().isoformat(),
            "author": author,
            "description": description
        })
