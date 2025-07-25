from pydantic import BaseModel, ConfigDict
from typing import Any


class FlexibleBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class MarketState(FlexibleBaseModel):
    market: str
    marketStatus: str
    tradeDate: str
    index: str
    last: float | str
    variation: float | str
    percentChange: float | str
    marketStatusMessage: str


class MarketStatusApiResp(FlexibleBaseModel):
    marketState: list[MarketState]


class MarketStatusMcp(FlexibleBaseModel):
    market: str
    marketStatus: str
    tradeDate: str
    marketStatusMessage: str


class MarketPreOpenApiResponseMetadata(FlexibleBaseModel):
    symbol: str | None
    identifier: str | None
    purpose: Any
    lastPrice: float | None
    change: float | None
    pChange: float | None
    previousClose: float | None
    finalQuantity: float | None
    totalTurnover: float | None
    marketCap: Any
    yearHigh: float | None
    yearLow: float | None
    iep: float | None
    chartTodayPath: Any


class MarketPreOpenApiResponseData(FlexibleBaseModel):
    metadata: MarketPreOpenApiResponseMetadata
    detail: Any


class MarketPreOpenApiResponse(FlexibleBaseModel):
    declines: int | None
    unchanged: float | None
    data: list[MarketPreOpenApiResponseData]
    advances: float | None
    timestamp: str | None
    totalTradedValue: float | None
    totalmarketcap: float | None
    totalTradedVolume: float | None


class MarketPreOpenMcp(FlexibleBaseModel):
    symbol: str | None
    identifier: str | None
    lastPrice: float | None
    change: float | None
    pChange: float | None
    previousClose: float | None
    finalQuantity: float | None
    totalTurnover: float | None
    yearHigh: float | None
    yearLow: float | None
