import numpy as np
import json

class OrderbookData:

    def __init__(self, path: str):
        self.__path = path
        with open(path, 'r') as f:
            ob_data = json.load(f)

        self.__bids = np.array([[np.float64(bid) for bid in mes['bids']] for mes in ob_data])
        self.__asks = np.array([[np.float64(ask) for ask in mes['asks']] for mes in ob_data])

        self.__bid_fairs = self.__compute_side_fair_price(True)
        self.__ask_fairs = self.__compute_side_fair_price(False)
        self.__fair_prices = self.__compute_fair_price()

        self.__mid_spread_prices = self.__compute_mid_spread_price()
        self.__best_bids = self.__get_best_side_price(True)
        self.__best_asks = self.__get_best_side_price(False)
        self.__tick_amt = self.__best_bids.shape[0]

    def __compute_side_fair_price(self, bids: bool) -> np.array:
        data = self.__bids if bids else self.__asks
        return np.sum(data[:, :, 0] * data[:, :, 1], axis=1) / np.sum(data[:, :, 1], axis=1)

    def __compute_fair_price(self) -> np.array:
        bids_cap = np.sum(self.__bids[:, :, 0] * self.__bids[:, :, 1], axis=1)
        asks_cap = np.sum(self.__asks[:, :, 0] * self.__asks[:, :, 1], axis=1)
        bids_volume = np.sum(self.__bids[:, :, 1], axis=1)
        asks_volume = np.sum(self.__asks[:, :, 1], axis=1)
        return (bids_cap + asks_cap) / (bids_volume + asks_volume)

    def __compute_mid_spread_price(self) -> np.array:
        return (self.__bids[:, 0, 0] + self.__asks[:, 0, 0]) / 2

    def __get_best_side_price(self, bids: bool) -> np.array:
        data = self.__bids if bids else self.__asks
        return data[:, 0, 0]

    @property
    def bids(self) -> np.array:
        return self.__bids

    @property
    def asks(self) -> np.array:
        return self.__asks

    @property
    def bid_fairs(self) -> np.array:
        return self.__bid_fairs

    @property
    def ask_fairs(self) -> np.array:
        return self.__ask_fairs
    
    @property
    def fair_prices(self) -> np.array:
        return self.__fair_prices
    
    @property
    def mid_spread_prices(self) -> np.array:
        return self.__mid_spread_prices

    @property
    def best_bids(self) -> np.array:
        return self.__best_bids

    @property
    def best_asks(self) -> np.array:
        return self.__best_asks
    
    @property
    def nticks(self) -> int:
        return self.__tick_amt
