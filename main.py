from fastmcp import FastMCP
from thefuzz import fuzz
from helper import (
    get_market_state,
    get_all_market_pre_open,
    get_stock_details,
    get_stock_running_52week_low,
    get_stock_running_52week_high,
    get_weekly_volume_gainers,
    get_nse_companies_list_from_wikipedia,
)
from models import (
    MarketStatusMcp,
    MarketPreOpenMcp,
    StockDetailResponse,
    Stock52weekAnalysis,
    StockWeeklyVolumeGainers,
    NSECompanyListWithMatchScore,
)

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


@mcp.tool()
def get_stock_running_at_52week_high() -> list[str] | str:
    """
    Returns the list of stock symbols that are currently running at their 52-week high.

    :resp
        List of stock symbols running at 52-week high.
    """
    data: list[Stock52weekAnalysis] | None = get_stock_running_52week_high()
    if data is None:
        return "Unable to fetch 52-week high data from NSE"

    return [item.symbol for item in data]


@mcp.tool()
def get_stock_running_at_52week_low() -> list[str] | str:
    """
    Returns the list of stock symbols that are currently running at their 52-week low.

    :resp
        List of stock symbols running at 52-week low.
    """
    data: list[Stock52weekAnalysis] | None = get_stock_running_52week_low()
    if data is None:
        return "Unable to fetch 52-week low data from NSE"

    return [item.symbol for item in data]


@mcp.tool()
def weekly_volume_gainer_stocks() -> list[str] | str:
    """
    Returns the list of stock symbols that are weekly volume gainers.

    :resp
        List of stock symbols that are weekly volume gainers.
    """
    data: list[StockWeeklyVolumeGainers] | None = get_weekly_volume_gainers()
    if data is None:
        return "Unable to fetch weekly volume gainers from NSE"

    return [item.symbol for item in data]


@mcp.tool()
def search_nse_companies(search_key: str) -> list[dict[str, str]] | str:
    """
    Returns a list of NSE companies that match the search key.
    The search key can be a part of the company name or symbol.

    :params
        search_key: The key to search for in the NSE companies list.

    :resp
        A list containing mapping object/dictionary where key is company symbol and value is company name.

    Example Output:
        [
            {"TCS" : "Tata Consultancy Services Limited"},
            {"INFY" : "Infosys Limited"}
        ]
    """
    companies_list = get_nse_companies_list_from_wikipedia()

    if companies_list is None:
        return "Unable to fetch NSE companies list from Wikipedia"

    companies_score = sorted(
        [
            NSECompanyListWithMatchScore(
                symbol=company.symbol,
                companyName=company.companyName,
                score=fuzz.ratio(search_key.lower(), company.companyName.lower()),
            )
            for company in companies_list
        ],
        key=lambda x: x.score,
        reverse=True,
    )

    top_3_matches = [
        {company.symbol: company.companyName} for company in companies_score
    ][:3]

    return top_3_matches


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
