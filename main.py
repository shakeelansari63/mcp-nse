from fastmcp import FastMCP
from helper import get_market_state, get_all_market_pre_open, get_stock_details
from models import MarketStatusMcp, MarketPreOpenMcp, StockDetailResponse

mcp = FastMCP()


# Tool
@mcp.tool()
async def check_equity_market_status() -> str:
    """
    Check whether the Equity / Capital Market is up or not. Returns a string indicating the market status.
    """
    market_state: list[MarketStatusMcp] | None = get_market_state()

    if market_state is None:
        return "Unable to fetch Market Status from NSE"

    equity_market_state = list(
        filter(lambda x: x.market == "Capital Market", market_state)
    )[0]
    return equity_market_state.marketStatus


@mcp.tool()
def get_all_market_symbols() -> list[str | None] | str:
    """
    Returns the list of all symbols registered in NSE.
    """
    preopen_data: list[MarketPreOpenMcp] | None = get_all_market_pre_open()

    if preopen_data is None:
        return "Unable to fetch Symbols from NSE"

    return [d.symbol for d in preopen_data]


@mcp.tool()
def get_stock_closing_price(symbol: str) -> str:
    """
    Returns the closing price of the given stock symbol.

    :params
        symbol: Symbol / Code of Stock whose closing price is requested

    :resp
        Closing price of the stock from Market.
    """
    preopen_data: list[MarketPreOpenMcp] | None = get_all_market_pre_open()

    if preopen_data is None:
        return "Unable to fetch Symbols from NSE"

    price = None

    for d in preopen_data:
        if d.symbol == symbol:
            price = d.previousClose

    if price is None:
        return f"Symbol {symbol} not found in NSE Pre-Open Market Data"

    return f"Closing Price of {symbol} is INR {price}"


@mcp.tool()
def get_live_stock_price(symbol: str) -> str:
    """
    Returns the current live price of Stock registered in NSE.

    :params
        symbol: Symbol / Code of Stock whose price is requested

    :resp
        Current stock price from Market.
    """
    stock_detail: StockDetailResponse | None = get_stock_details(symbol)

    if stock_detail is None:
        return "Unable to fetch Stock Data from NSE"

    return f"Current Price of {symbol} is INR {stock_detail.priceInfo.lastPrice}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
