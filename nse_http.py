import httpx
from typing import Mapping, Any
import config as conf
import urllib.parse


class NSEHttpClient:
    def __init__(self):
        self._set_nse_cookies()

    def _set_nse_cookies(self):
        """
        This method is used to set the cookies required for NSE API requests.
        It initializes a session and fetches the cookies from the base URL.
        """
        client = httpx.Client()
        client.headers.update(conf.NSE_HEADER)
        client.get(conf.COOKIE_URL)
        self.cookies = client.cookies

    def _check_cookie_expired(self):
        """
        This method checks if the cookies have expired.
        If they have, it reinitializes the session and fetches new cookies.
        """
        if not self.cookies or not self.cookies.jar:
            self._set_nse_cookies()

        for cookie in self.cookies.jar:
            if cookie.is_expired():
                self._set_nse_cookies()
                break

    def _get_http_client(self):
        """
        This method returns the HTTP/2 client with the current cookies.
        It checks if the cookies are expired before returning the client.
        """
        self._check_cookie_expired()
        return httpx.Client(cookies=self.cookies, headers=conf.NSE_HEADER)

    def get_nse_data(self, url: str, params: Mapping[str, str] | None = None) -> Any:
        """
        This method fetches data from the given NSE URL.
        It returns the JSON response if successful, or None if there is an error.
        """
        if params is not None and len(params) > 0:
            url_params = urllib.parse.urlencode(params)
            url = f"{url}?{url_params}"
        try:
            client = self._get_http_client()
            response = client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
