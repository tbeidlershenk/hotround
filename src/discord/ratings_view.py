import disnake
from discord.course_dropdown import CourseDropdown
from discord.layout_dropdown import LayoutDropdown

class RatingsView(disnake.ui.View):
    def __init__(self, courses_str: list[str], score: int):
        super().__init__()

        self.score = score
        self.course = None
        self.layout = None

        self.course_dropdown = CourseDropdown(courses_str)
        self.layout_dropdown = LayoutDropdown()
        self.ratings_response = None

        self.add_item(self.course_dropdown)
        self.add_item(self.layout_dropdown)
        