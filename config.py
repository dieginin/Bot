from dotenv import dotenv_values


dot = dotenv_values()
TOKEN_API = dot["BRAWL_API"]
TOKEN_BOT = dot["BOT_API"]
ROYALE_API = "https://bsproxy.royaleapi.dev/v1/"

COGS = ["commands.extras"]
