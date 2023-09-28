from dotenv import dotenv_values

dot = dotenv_values()
TOKEN_API = dot["BRAWL_API"]
TOKEN_BOT = dot["BOT_API"]
URL_ROYALE = "https://bsproxy.royaleapi.dev/v1/"
URL_BRAWLAPI = "https://api.brawlapi.com/v1/"
