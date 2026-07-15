import disnake

from discord.embeds import Embeds
from discord.layout_dropdown import LayoutDropdown

from bot import HotRoundBot
from models.course import Course

class CourseDropdown(disnake.ui.StringSelect):
    # state variables
    courses: list[Course] = []

    missing_option = disnake.SelectOption(value="-1", label="???", description="My course is missing!")

    # Constructs the dropdown
    def __init__(self, courses_str: list[str]):
        self.courses = [Course.from_json(c) for c in courses_str]
        options = [disnake.SelectOption(value=str(c.course_id), label=c.get_name(), description=c.get_location()) for c in self.courses]
        options.append(self.missing_option)
        placeholder_text = f"Choose a course ({len(courses_str)} options)" if len(courses_str) > 1 else "Choose a course (1 option)"
        super().__init__(placeholder=placeholder_text, min_values=1, max_values=1, options=options)

    # Callback when user selects an option
    async def callback(self, inter: disnake.MessageInteraction):
        view: disnake.ui.View = self.view
        await inter.response.defer()
        bot: HotRoundBot = inter.bot
        user_choice = self.values[0]

        if user_choice == self.missing_option.value:
            if view.ratings_response == None:
                view.ratings_response = await inter.followup.send(embed=Embeds.course_missing(), wait=True)
                view.course_dropdown.placeholder = "???"
                view.layout_dropdown.placeholder = "???"
                view.layout_dropdown.disabled = True
            else:
                await view.ratings_response.edit(embed=Embeds.course_missing())
                view.course_dropdown.placeholder = "???"
                view.layout_dropdown.placeholder = "???"
                view.layout_dropdown.disabled = True
        else:
            # pull course with course_id
            course = next(c for c in self.courses if c.course_id == int(user_choice))

            # retrieve layouts for selected course
            layouts = bot.database.query_aggregate_layouts(course.course_id)
            layouts.sort(key=lambda x: x.num_rounds, reverse=True)
            layouts = layouts[:10]

            view.course = course
            view.course_dropdown.placeholder = course.get_name()

            view.layout_dropdown.layouts = layouts
            view.layout_dropdown.disabled = False
            view.layout_dropdown.placeholder = f"Choose a layout ({len(layouts)} options)" if len(layouts) > 1 else f"Choose a layout ({len(layouts)} option)"
            view.layout_dropdown.options = [disnake.SelectOption(value=l.get_unique_identifier(), label=l.get_descriptive_name(), description=f"Par {l.total_par}, {l.total_distance} ft)") for l in layouts]
            view.layout_dropdown.options.append(view.layout_dropdown.missing_option)

        await inter.edit_original_response(view=view)
