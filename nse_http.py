from http.cookiejar import MozillaCookieJar
import httpx
from typing import Mapping, Any
import config as conf

nse_headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Connection": "keep-alive",
}


class NSEHttpClient:
    def __init__(self):
        # Create Cookie Jar Http Client
        cookiejar = MozillaCookieJar(filename="my-cookies.txt")
        try:
            cookiejar.load()
        except FileNotFoundError:
            pass

        # Create Http Client
        self.session = httpx.Client(
            cookies=cookiejar,
            headers=nse_headers,
        )

        # Initialize Cookies
        self.session.get(conf.BASE_URL)

    def get_data(self, url) -> Mapping[str, Any] | None:
        resp = self.session.get(url)
        if resp.status_code == 200:
            return resp.json()
        print(resp)
        return None
