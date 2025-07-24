from fastmcp import FastMCP
import config as conf
from nse_http import NSEHttpClient
from models import MarketStatusApiResp, MarketStatusMcp
from typing import Mapping, Any

mcp = FastMCP()


nse_client = NSEHttpClient()


# Tool
@mcp.tool()
async def check_market_status() -> list[MarketStatusMcp] | str:
    """
    Check whether the Market is up or not. Returns a Json value indicating market status for various markets like
    Capital/Equity
    Currency
    Commodity
    Debt
    Currency Future
    """
    data = nse_client.get_data(conf.MARKET_STATUS_URL)
    if data is None:
        return "Unable to get Data from NSE API"

    market_state = MarketStatusApiResp.model_validate(data)

    resp_market_state = [
        MarketStatusMcp(
            market=status.market,
            marketStatus=status.marketStatus,
            tradeDate=status.tradeDate,
            marketStatusMessage=status.marketStatusMessage,
        )
        for status in market_state.marketState
    ]

    return resp_market_state


@mcp.tool()
def get_live_stock_price(symbol: str):
    """
    Returns the current live price of Stock registered in NSE.

    :params
        symbol: Symbolk / Code of Stock whose price is requested

    :resp
        Current stock price from Market. This will return the closing price if Market is close
    """
    data = nse_client.get_data(f"{conf.STOCK_QUOTE_URL}?symbol={symbol.upper()}")
    print(data)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
