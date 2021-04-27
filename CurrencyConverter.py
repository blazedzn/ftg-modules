#by @blazedzn
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils
import asyncio
def register(cb):
    cb(CurrencyMod())
class CurrencyMod(loader.Module):
    """Конвертер валют от @blazeftg
    Работает с помощью бота @exchange_rates_vsk_bot
    """
    strings = {'name': 'CurrencyConverter'}
    async def currcmd(self, message):
        """.curr <кол-во> <валюта>
            Конвертирует валюты
            Пример: '.curr 5000 рублей/руб/rub/RUB'
        """
        state = utils.get_args_raw(message)
        await message.edit("<b>Получаем информацию...</b>")
        chat = '@exchange_rates_vsk_bot'
        async with message.client.conversation(chat) as conv:
            try:
                await message.edit("<b>Ожидаем ответ...</b>")
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=1210425892))
                bot_send_message = await message.client.send_message(chat, format(state))
                bot_response = response = await response
            except YouBlockedUserError:
                await message.edit('<b>Разблокируй</b> ' + chat)
                return
            await bot_send_message.delete()
            await message.edit(response.text)
            await bot_response.delete()