import datetime
from typing import Tuple, Dict
from aiohttp import ClientSession
import xml.etree.ElementTree as ET
from config import CURRENCY_API, DATE_FORMAT


async def get_data(url=CURRENCY_API) -> str | None:
    """
    Запрос к апи для получения xml документца.
    :param url: Адрес апи
    :return: xml документ строкой, если статус код 200. Иначе None
    """
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                xml_data = await response.text()
                return xml_data
            else:
                return None


async def get_currency() -> Tuple[Dict, datetime] | None:
    """
    Вызывает функцию get_data и обрабатывает полученный документ для последующей записи.

    :return: Кортеж с данными и датой.
    """
    data = await get_data()

    if data is None:
        return

    root = ET.fromstring(data)

    date = root.attrib["Date"].split(".")
    date = datetime.date(day=int(date[0]), month=int(date[1]), year=int(date[2])).strftime(DATE_FORMAT)

    currency_data = dict()

    for currency in root:
        char_code = currency.find("CharCode").text
        name = currency.find("Name").text
        vunit_rate = currency.find("VunitRate").text  # курс к рублю
        vunit_rate = vunit_rate.replace(",", ".")

        currency_data[char_code] = (float(vunit_rate), name)

    return currency_data, date
