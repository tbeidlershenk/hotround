import contextvars
import aiohttp
import disnake
import disnake_plugins
from disnake.ext.commands import Context

plugin = disnake_plugins.Plugin()

@plugin.slash_command(description='Get status of bot')
async def status(inter: disnake.CommandInteraction):
    await inter.response.send_message('https://tenor.com/view/calvin-heimburg-cheimborg-disc-golf-paul-mcbeth-jomez-gif-17295086880136338920')

setup, teardown = plugin.create_extension_handlers()