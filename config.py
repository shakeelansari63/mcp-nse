BASE_URL = "https://www.nseindia.com"
COOKIE_URL = f"{BASE_URL}/get-quotes/equity?symbol=TCS"
MARKET_STATUS_URL = f"{BASE_URL}/api/marketStatus"
STOCK_QUOTE_URL = f"{BASE_URL}/api/quote-equity"
MARKET_PRE_OPEN_URL = f"{BASE_URL}/api/market-data-pre-open?key=ALL"

NSE_HEADER: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Accept": "*/*",
    "Origin": BASE_URL,
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Connection": "keep-alive",
}
