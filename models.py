from pydantic import BaseModel


class MarketState(BaseModel):
    market: str
    marketStatus: str
    tradeDate: str
    index: str
    last: float | str
    variation: float | str
    percentChange: float | str
    marketStatusMessage: str


class MarketStatusApiResp(BaseModel):
    marketState: list[MarketState]


class MarketStatusMcp(BaseModel):
    market: str
    marketStatus: str
    tradeDate: str
    marketStatusMessage: str
