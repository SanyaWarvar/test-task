from src.currency_api import get_currency
from src.redis_crud import cache_manager


async def update_cache(force: bool = False):
    """
    Обновление данных в кеше, если данные невалидны (последнее обновление было не сегодня).

    :param force: Если истина, то обновление произойдет вне зависимоти от того, актуальны ли сохраненные данные
    """
    if cache_manager.is_valid_data() and force is False:
        return

    data = await get_currency()
    cache_manager.update_currency(data)

    rates = await generate_rates(data)
    cache_manager.update_rates(rates)


async def convert(amount: float, first: str, second: str = None, ndigits=2) -> tuple[float, str]:
    """
    Конвертация одной валюты в другую.

    :param amount: Количество первой валюты
    :param first: Буквенный код первой валюты. Например USD.
    :param second: Буквенный код второй валюты. Например EUR. По умолчанию - RUB
    :param ndigits: Количество чисел после запятой при округлении результатов
    :return: Кортеж с числом, которое получилось при конвертации и поясняющим сообщением.
    """
    if not cache_manager.is_valid_data():
        await update_cache()


    rate1 = (1, "Российский Рубль") if first == "RUB" else cache_manager.get_currency(first)
    rate2 = (1, "Российский Рубль") if (second == "RUB" or second is None) else cache_manager.get_currency(second)

    if rate1 == [] or rate2 == [] or amount < 0:
        raise ValueError

    answer = amount * float(rate1[0]) / float(rate2[0])
    return round(answer, ndigits), f"{amount} {rate1[1]} = {round(answer, ndigits)} {rate2[1]}"


async def generate_rates(data: tuple[dict, str] = None) -> str:
    """
    Генерируется текст сообщения со списком всех валют и их курсом.
    :param data: Кортеж с датой данных и данными о валютах. Если не указан, то будет делаться запрос к апи.
    :return: Строка с курсом всех валют
    """
    if data is None:
        data = await get_currency()

    answer_text = f"Курс валют ({data[1]}):\n"
    for name, value in data[0].items():
        answer_text += f"{value[1]} ({name}) = {value[0]}\u20bd\n"

    return answer_text



async def get_rates() -> str:
    """
    Проверяет актуальность записанной информации и обновляет ее при необходимости. Далее читает курс валют из кэша.
    :return: Строка с курсом валют
    """
    if not cache_manager.is_valid_data():
        await update_cache()

    data = cache_manager.get_rates()

    return data
