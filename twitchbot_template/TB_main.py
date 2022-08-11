from datetime import datetime

from twitchio import Message
from twitchio.ext import commands, pubsub

from TB_defines import init_channels, ChannelIDs, debug, client_data

client_data.read_config()


client = commands.Bot(
    token=client_data.user_access_token,
    prefix="?",
    initial_channels=init_channels
)


@client.event()
async def event_ready():
    topics = [
        pubsub.channel_points(client_data.user_access_token)[ChannelIDs.main]
    ]
    await client.pubsub.subscribe_topics(topics)
    text = f"* {'-' * 40}\n" \
           f"* [{datetime.now().replace(microsecond=0)}]\n" \
           f"* {client.nick} ready\n" \
           + (f"* Debug: {debug}\n" if debug else f"") \
           + f"* {'-' * 40}"
    print(text)


@client.event()
async def event_message(message: Message):
    if message.echo:  # ignore bot's own message
        return
    print(f"[{message.channel.name}] -> [{message.author.name}]: {message.content}")


@client.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    print(f"{event.user.name} | {event.status} | {event.reward.title}")


client.load_module("TB_modules.TB_commands")


client.pubsub = pubsub.PubSubPool(client)
client.run()
