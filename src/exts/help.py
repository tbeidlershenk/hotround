import disnake
import disnake_plugins
from disnake.ext.commands import Context

plugin = disnake_plugins.Plugin()

@plugin.slash_command(description='How to use the bot')
async def help(inter: disnake.CommandInteraction):
    message1 = "Use `/ratings` with one of `course_name` or `dgscene_url` to generate a PDGA round rating for a course."
    message2 = "You can supply your score (relative to par) using the `score` field. By default, HotRound will show the PDGA rating for E par."
    message3 = "Ratings are aggregated over multiple tournaments, giving a more accurate representation of course difficulty (irrespective of weather, exact pin locations, etc.)"
    await inter.response.send_message(message1 + '\n\n' + message2 + '\n\n' + message3)

setup, teardown = plugin.create_extension_handlers()