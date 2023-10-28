import discord


class GameSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(
            label="Valorant", value=1, emoji="<:valo:1160491417332895836>"
        ),
        discord.SelectOption(
            label="Call of Duty: Mobile", value=2, emoji="<:codm:1160491412027093092>"
        ),
        discord.SelectOption(
            label="Mobile Legends", value=3, emoji="<:ml:1160491413847429261>"
        ),
    ]

    @discord.ui.select(placeholder="Rate our service", options=options)
    async def menu_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        if select.values[0] == "1":
            game = "Valorant"
            role = "<@&1159724038055272531>"
        if select.values[0] == "2":
            game = "Call of Duty: Mobile"
            role = "<@&1159724038055272531>"
        if select.values[0] == "3":
            game = "Mobile Legends"
            role = "<@&1159724038055272531>"
