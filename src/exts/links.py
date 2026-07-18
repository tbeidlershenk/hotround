import disnake
import disnake_plugins
from disnake.ext.commands import Context

plugin = disnake_plugins.Plugin()

@plugin.slash_command(description='About the HotRound project')
async def about(inter: disnake.CommandInteraction):
    message1 = "Check out the HotRound [web app](https://hotround.tbeidlershenk.dev)"
    message2 = "Give this project a ⭐ on [GitHub](https://github.com/tbeidlershenk/hotround)"
    message3 = "Report bugs/issues through [GitHub Issues](https://github.com/tbeidlershenk/hotround/issues)"
    await inter.response.send_message(message1 + '\n' + message2 + '\n' + message3, suppress_embeds=True)

setup, teardown = plugin.create_extension_handlers()