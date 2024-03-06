import json

import aiohttp
import re
from .utils import shakikoo


class ForumClient(object):
    url = "https://atelier801.com/"

    def __init__(self, username: str, password: str, debug: bool = False):
        self.username = username
        self.password = password
        self.session = aiohttp.ClientSession(headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 6.1) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/68.0.3440.106 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9"
        })

    async def close(self):
        """Closes the client."""
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def get_page(self, page: str):
        """Gets a page from the forum."""
        return await self.session.get(self.url + page)

    async def _get_csrf_token(self, page: str = None):
        """Gets csrf keys from a page to perform an action."""
        response = await self.get_page(page or "index")
        html = await response.read()

        search = re.search(rb'<input type="hidden" name="(.+?)" value="(.+?)">', html)
        if search is not None:
            token_name, token_value = search.group(1, 2)
            return token_name.decode(), token_value.decode()

    async def post_action(self, data: dir, page: str, referer=None):
        """Performs a POST action on the forum."""
        token_name, token_value = await self._get_csrf_token(referer)

        data[token_name] = token_value

        headers = None
        if referer is not None:
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Referer": self.url + referer
            }

        return await self.session.post(self.url + page, data=data, headers=headers)

    async def get_action(self, data: dir, page: str):
        """Performs a GET action on the forum."""

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        return await self.session.get(self.url + page, data=data, headers=headers)

    async def login(self):
        """Logs in the forum."""
        response = await self.post_action({
            "rester_connecte": "on",  # "Stay connected" in French
            "id": self.username,
            "pass": shakikoo.shakikoo(self.password).decode(),
            "redirect": self.url[:-1]
        }, "identification", "login")
        data = json.loads(await response.read())

        if "supprime" in data:
            print("Login successful.")
            return True

        print("Login failed.")
        return False

    async def reply_to_thread(self, message: str, f: str, t: str):
        response = await self.post_action({
            "t": t,
            "f": f,
            "message_reponse": message
        }, "answer-topic", f"topic?f={f}&t={t}")
        data = json.loads(await response.read())

        if "supprime" in data:
            print("Reply successful.")
            return True

        print("Reply failed.")
        return False



    async def get_message(self, f: str, t: str, id: str):
        page = int(id) // 20 + 1

        response = await self.get_action({
            "f": f,
            "t": t,
            "p": page
        }, f"topic?f={f}&t={t}&p={page}")
        print(await response.text())


