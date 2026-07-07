import disnake

from discord.embeds import Embeds
from discord.layout_dropdown import LayoutDropdownView

from bot import HotRoundBot
from models.course import Course

class CourseDropdownView(disnake.ui.View):
    def __init__(self, courses_str: list[str], score: int):
        super().__init__()
        self.add_item(CourseDropdown(courses_str, score))

class CourseDropdown(disnake.ui.StringSelect):
    # state variables
    score: int = 0
    courses: list[Course] = []

    missing_option = disnake.SelectOption(value="-1", label="???", description="My course is missing!")

    # Constructs the dropdown
    def __init__(self, courses_str: list[str], score: int):
        self.score = score
        self.courses = [Course.from_json(c) for c in courses_str]
        options = [disnake.SelectOption(value=str(c.course_id), label=c.get_name(), description=c.get_location()) for c in self.courses]
        options.append(self.missing_option)
        super().__init__(placeholder="Choose an course", min_values=1, max_values=1, options=options)

    # Callback when user selects an option
    async def callback(self, inter: disnake.MessageInteraction):
        bot: HotRoundBot = inter.bot
        await inter.response.defer()

        user_choice = self.values[0]
        if user_choice == self.missing_option.value:
            await inter.followup.send(embed=Embeds.course_missing())
        else:
            course = next(filter(lambda x: x.course_id == int(user_choice), self.courses), None)
            aggregate_layouts = bot.database.query_aggregate_layouts(course.course_id)
            aggregate_layouts.sort(key=lambda x: x.num_rounds, reverse=True)
            aggregate_layouts = aggregate_layouts[:10]
            aggregate_layouts_str = [l.to_json() for l in aggregate_layouts]
            await inter.followup.send("Select a layout:", view=LayoutDropdownView(course.to_json(), aggregate_layouts_str, self.score))