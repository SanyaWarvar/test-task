from src.utils import get_rates, convert
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram import Router


router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer("Hello world!")


@router.message(Command("rates"))
async def rates_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    data = await get_rates()

    await message.answer(data)


@router.message(Command("exchange"))
async def exchange(
        message: Message,
        command: CommandObject
):
    try:
        args = command.args.split(" ", maxsplit=2)
        args[0] = float(args[0])
        data = await convert(*args)
    except ValueError:
        data = None

    if data is None:
        await message.answer(
            "Ошибка! Неверный ввод!\n"
            "Введите комманду в формате: /exchange Количество валюты Код первый валюты Код второй валюты.\n"
            "Например: /exchange 50 USD EUR\n"
            "Если вы не вводите код второй валюты, то она будет считаться Российским рублем.\n"
            "Например: /exchange 50 USD\n"
        )
        return

    await message.answer(data[1])
