from typing import Dict, Tuple, List, Awaitable
from datetime import datetime
import redis

from src.config import DATE_FORMAT, REDIS_PORT, REDIS_HOST, TIMEZONE


class Cache:
    """
    Менеджер для работы с кэшем (Redis)
    """
    __slots__ = ["client"]

    def __init__(self, host="localhost", port=6379):
        self.client = redis.Redis(host, port, charset="utf-8", decode_responses=True)

    def get_currency(self, char_code: str) -> Awaitable[list] | list:
        """
        Получение конкректной валюты по ее коду

        :param char_code: Код валюты. Например EUR
        :return: Кортеж, который содержит курс валюты к рублю и ее полное название
        """
        return self.client.lrange(char_code, 0, -1)

    def update_currency(self, data: Tuple[Dict, str]):
        """
        Обновление данных о валютах. Перезаписывает курс валют и дату последнего обновления.
        :param data: Кортеж с данными о валютах и актуальной датой этого курса
        """
        self.client.set("Date", data[1])
        for name, value in data[0].items():
            self.client.lpop(name, 2)
            self.client.rpush(name, *value)

    def update_rates(self, data: str):
        """
        Обновить курс валют (именно сообщение с общим списком)
        :param data: Список с курсом валют (строкой)
        """
        self.client.set("rates", data)

    def get_rates(self) -> str:
        """
        Получить список с курсом всех валют (заранее созданная строка)
        :return: Список с курсом всех валют
        """
        return self.client.get("rates")

    def is_valid_data(self) -> bool:
        """
        Проверка являются ли данные о валютах актуальными. Данные являются актуальными, если они были обновлены сегодня.
        :return: Булевое значение актуальности данных
        """
        date_str: str = self.client.get("Date")
        if date_str is None:
            return False

        try:
            date = datetime.strptime(date_str, DATE_FORMAT).date()
        except ValueError:
            return False

        if date > (datetime.now(TIMEZONE).date()):
            return False
        return True


cache_manager = Cache(REDIS_HOST, REDIS_PORT)
