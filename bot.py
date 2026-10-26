import os
import re
import aiohttp

HEALTH_URL = "https://cobolt-1-xmcq.gaur-alnilam.ts.net/api/health"
NERIMITY_TOKEN = os.environ.get("NERIMITY_TOKEN") # Note: This is used in the server, so there's a service with the token here, changing this will make the service fail and no bot will be up. 


async def check_status() -> bool:
    """Same logic as the workflow: 10s timeout, match "status" ... "ok"."""
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(HEALTH_URL) as resp:
                body = await resp.text()
    except Exception:
        return False
    return re.search(r'"status".*"ok"', body) is not None

def run_nerimity():
    from nerimity_sdk import Bot

    bot = Bot(token=NERIMITY_TOKEN)

    @bot.command("ping", description="Check whether the Cobolt server is up")
    async def ping(ctx):
        is_up = await check_status()
        await ctx.reply("🟢 Cobolt is **Up**" if is_up else "🔴 Cobolt is **Down**")
    bot.run()

if __name__ == "__main__":
    if not NERIMITY_TOKEN:
        raise SystemExit("Set NERIMITY_TOKEN")
    run_nerimity()
