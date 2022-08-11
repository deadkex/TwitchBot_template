import twitchio
from twitchio.ext import commands


class TBCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"{ctx.author.mention} Hi!")


def prepare(client: twitchio.Client):
    client.add_cog(TBCommands(client))
