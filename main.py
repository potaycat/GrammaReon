import os
import discord
from discord.ext.commands import Bot
from gingerit.gingerit import GingerIt
from dotenv import load_dotenv
import utils

load_dotenv()
TOKEN = os.getenv("DISCORD_CLENT_SECRET")
DEBUG_WEBHOOK_URL = os.getenv("DEBUG_WEBHOOK_URL")
WHITELIST = {
    "im": "I'm",
    "Im": "I'm",
    "isnt": "isn't",
}


class GrammaReon(Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            command_prefix="??",
            intents=intents,
        )
        self.startup_extensions = []
        self.parser = GingerIt()

    async def setup_hook(self):
        print(self.user.name, "is setting up...")
        for ext in self.startup_extensions:
            await self.load_extension(ext)
            print("Loaded:", ext)
        self.debug_webhook = discord.SyncWebhook.from_url(DEBUG_WEBHOOK_URL)

    async def on_ready(self):
        print("READY")

    @utils.Async.alt_thread
    def detect_grammar(self, text):
        return self.parser.parse(text)

    @utils.Async.alt_thread
    def log_error(self, e):
        self.debug_webhook.send(e)

    async def on_message(self, message):
        if message.author.bot:
            return
        if "Reon" in message.author.name:
            return
        try:
            text = message.content
            for word, replacement in WHITELIST.items():
                text = text.replace(word, replacement)
            res = await self.detect_grammar(text)
            if res["corrections"].__len__():
                await message.author.send(
                    f"```ORIGINAL: {message.content}\n\nCORRECTED: {res['result']}```"
                )
        except Exception as e:
            await self.log_error(e)


if __name__ == "__main__":
    bot = GrammaReon()
    bot.run(TOKEN)
