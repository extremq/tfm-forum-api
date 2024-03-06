import os

from tforum.client import ForumClient
import asyncio
from dotenv import load_dotenv


async def main():
    client = ForumClient(os.getenv("username"), os.getenv("password"), True)
    await client.login()
    await client.get_message(f="877874", t="945086", id="1")
    await client.close()

load_dotenv()
asyncio.run(main())
