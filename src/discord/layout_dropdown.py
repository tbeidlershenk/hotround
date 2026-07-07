import disnake

from discord.embeds import Embeds

from models.course import Course
from models.layout import AggregateLayout

MISSING_LABEL = "???"

class LayoutDropdownView(disnake.ui.View):
    def __init__(self, course_str: str, layouts_str: list[str], score: int):
        super().__init__()
        self.add_item(LayoutDropdown(course_str, layouts_str, score))

class LayoutDropdown(disnake.ui.StringSelect):
    # state variables
    course: Course = None
    layouts: list[AggregateLayout] = []
    score: int = 0
    
    missing_option = disnake.SelectOption(value="-1", label="???", description="My layout is missing!")

    # Constructs the dropdown
    def __init__(self, course_str: str, layouts_str: list[str], score: int):
        self.course = Course.from_json(course_str)
        self.layouts = [AggregateLayout.from_json(l) for l in layouts_str]
        self.score = score
        options = [disnake.SelectOption(value=l.get_descriptive_name(), label=l.get_descriptive_name(), description=l.total_distance) for l in self.layouts]
        options.append(self.missing_option)
        super().__init__(placeholder="Choose an layout", min_values=1, max_values=1, options=options)

    # Callback when user selects an option
    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.defer()
        user_choice = self.values[0]
        if user_choice == self.missing_option.value:
            await inter.followup.send(embed=Embeds.layout_missing())
        else:     
            layout: AggregateLayout = next(filter(lambda x: x.get_descriptive_name() == user_choice, self.layouts), None)
            await inter.followup.send(embed=Embeds.success(self.course, layout, self.score))