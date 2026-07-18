import disnake

async def send_message(inter: disnake.MessageInteraction, view: disnake.ui.View, embed: disnake.Embed) -> None:
    if view.ratings_response == None:
        view.ratings_response = await inter.followup.send(embed=embed, wait=True)
    else:
        await view.ratings_response.edit(embed=embed)


