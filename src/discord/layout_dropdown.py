import disnake

from discord.embeds import Embeds

from models.course import Course
from models.layout import AggregateLayout

MISSING_LABEL = "???"

class LayoutDropdown(disnake.ui.StringSelect):
    layouts: list[AggregateLayout] = []
    
    missing_option = disnake.SelectOption(value="-1", label="???", description="My layout is missing!")
    default_option = disnake.SelectOption(value="placeholder", label="placeholder", description="Select a course first")

    # Constructs the dropdown
    def __init__(self):
        super().__init__(placeholder=f"Select a course first", options=[self.default_option], disabled=True)

    # Callback when user selects an option
    async def callback(self, inter: disnake.MessageInteraction):
        view = self.view
        await inter.response.defer()
        embed = None

        user_choice = self.values[0]
        if user_choice == self.missing_option.value:
            embed = Embeds.layout_missing()
        else:
            layout = next(l for l in self.layouts if l.get_unique_identifier() == self.values[0])
            view.layout = layout
            embed = Embeds.success(view.course, view.layout, view.score)

        if view.ratings_response is None:
            view.ratings_response = await inter.followup.send(embed=embed, wait=True)
        else:
            await view.ratings_response.edit(embed=embed)
