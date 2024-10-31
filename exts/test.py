import contextvars
import aiohttp
import disnake
import disnake_plugins
from disnake.ext.commands import Context
from bot import CaddieBot

plugin = disnake_plugins.Plugin()

@plugin.slash_command()
async def test_command(inter: disnake.CommandInteraction):
    await inter.response.send_message("Success")

setup, teardown = plugin.create_extension_handlers()