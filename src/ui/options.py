import datetime
import traceback
from disnake import ui, ButtonStyle, MessageInteraction
from disnake import ui, ButtonStyle, MessageInteraction
import disnake

NEWLINE = '\n'

class IncorrectButton(ui.Button):
    def __init__(self, disabled ):
        super().__init__(
            emoji="❓",
            style=ButtonStyle.grey,
            disabled=disabled,
            custom_id='incorrect'
        )

    async def callback(self, inter: MessageInteraction) -> None:
        view: CreateOptions = self.view
        try:
            await inter.response.defer()
            if view.author_id:
                if inter.author.id != view.author_id:
                    return await inter.send("You cannot interact with these buttons.", ephemeral=True)
            
            embed = disnake.Embed.from_dict({
                "title": f"Did you mean:",
                "color": 0xFF1B29,
                "timestamp": datetime.datetime.now().isoformat(),
                "author": {
                    "name": "HotRound",
                    "url": "https://hotround.site",
                    "icon_url": "https://uplaydiscgolf.org/cdn/shop/files/PDGA_4559f2a6-e3bc-4353-b8a7-1e7d8b2ed243.png?v=1678388512&width=1420",
                },
                "fields": [
                    {"name": "", "value": f"{NEWLINE.join(view.other_matches[:5])}", "inline": "false"},
                    {"name": "", "value": "Use `/ratings` with the correct name."}
                ]
            }) 
            await inter.edit_original_response(embed=embed, view=CreateOptions([embed], view.other_matches, disable_pagination=True, author_id=inter.author.id, timeout=600))
            
        except:
            traceback.print_exc()
            await inter.send('Unable to change the page.', ephemeral=True)


class PreviousButton(ui.Button):
    def __init__(self, disabled ):
        super().__init__(
            emoji="⬅️",
            style=ButtonStyle.grey,
            disabled=disabled,
            custom_id='previous'
        )

    async def callback(self, inter: MessageInteraction) -> None:
        view: CreateOptions = self.view
        try:
            if view.author_id:
                if inter.author.id != view.author_id:
                    return await inter.send("You cannot interact with these buttons.", ephemeral=True)
            if view.current_embed:
                await inter.response.edit_message(embed=view.embeds[view.current_embed-1])
                view.current_embed = view.current_embed - 1

                if view.current_embed == 0:
                    self.disabled = True
                for btn in view.children:
                    if btn.custom_id == "next":
                        btn.disabled = False
                await inter.edit_original_message(view=view)
                
        except:
            await inter.send('Unable to change the page.', ephemeral=True)

class NextButton(ui.Button):
    def __init__(self, disabled ):
        super().__init__(
            emoji="➡️",
            style=ButtonStyle.grey,
            disabled=disabled,
            custom_id='next'
        )

    async def callback(self, inter: MessageInteraction) -> None:
        view: CreateOptions = self.view
        try:
            if view.author_id:
                if inter.author.id != view.author_id:
                    return await inter.send("You cannot interact with these buttons.", ephemeral=True)

            await inter.response.edit_message(embed=view.embeds[view.current_embed+1])
            view.current_embed += 1

            if view.current_embed+1 == len(view.embeds):
                self.disabled = True
            for btn in view.children:
                if btn.custom_id == "previous":
                    btn.disabled = False
            await inter.edit_original_message(view=view)
            
        except:
            await inter.send('Unable to change the page.', ephemeral=True)


class CreateOptions(ui.View):
    def __init__(self, embeds: list[disnake.Embed], other_matches: list[str], disable_pagination: bool = False, author_id: int = None, timeout: float = None):
        
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.other_matches = other_matches
        self.author_id = author_id
        self.current_embed = 0

        self.add_item(PreviousButton(True))
        self.add_item(NextButton(disable_pagination or len(embeds) == 1))
        self.add_item(IncorrectButton(False))