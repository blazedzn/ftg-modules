#by @blazedzn
from .. import loader, utils
import requests
import datetime
import asyncio

@loader.tds
class BestPriceGamesFinderMod(loader.Module):
    """Поиск игр by @blazeftg"""
    strings = {"name": "GameFinder"}

    async def gamecmd(self, message):
        """ .game <Название игры>,<*опционально* лимит на вывод игр>
        Обязательно через запятую если хочешь сделать лимит
        Ищет игры по заданому названию
        """
        await message.edit(f"<b>Поиск...</b>")
        limit = ''
        all = utils.get_args_raw(message)
        filtered = all.split(',')
        name = filtered[0]
        try:
            limit = filtered[1]
        except IndexError:
            limit = 20
        output_mess = ''
        response = requests.get('https://www.cheapshark.com/api/1.0/games?title={name}&limit={limit}'.format(name = name, limit = limit))
        if response.json() == []:
            if output_mess == '':
                output_mess += "<b>[Ошибка] Игры с таким название не найдено.</b>"
            else:
                pass
        else:
            for i in range(len(response.json())):
                cheapest_link = "https://www.cheapshark.com/redirect?dealID={dealid}".format(dealid = response.json()[i]['cheapestDealID'])
                try:
                    int(response.json()[i]['steamAppID'])
                    steam_link = "https://store.steampowered.com/app/{gameid}".format(gameid = response.json()[i]['steamAppID'])
                except:
                    steam_link = "Этой игры нету в Steam"
                if steam_link == "Этой игры нету в Steam":
                    output_mess += "\nНазвание игры: " + f"<code>{str(response.json()[i]['external'])}</code>" + "\n    ID игры: " + f"<code>{str(response.json()[i]['gameID'])}</code>" + "\n    Страница игры в Стиме: " + f"<code>{str(steam_link)}</code>" + "\n    Самая низкая цена на данный момент: " + f"<code>{str(response.json()[i]['cheapest'])}</code>" + "$" + f"<a href={cheapest_link}"">\n    Магазин с самой низкой ценой</a>" + "\n"
                else:
                    output_mess += "\nНазвание игры: " + f"<code>{str(response.json()[i]['external'])}</code>" +"\n    ID игры: " + f"<code>{str(response.json()[i]['gameID'])}</code>" + f"<a href={steam_link}"">\n    Страница игры в Стиме</a>" + "\n    Самая низкая цена на данный момент: " + f"<code>{str(response.json()[i]['cheapest'])}</code>" + "$" + f"<a href={cheapest_link}"">\n    Магазин с самой низкой ценой</a>" + "\n"
        await utils.answer(message, output_mess)
    async def detailgamecmd(self, message):
        """ .detailgame <ID игры>
        Показывает детальную информацию об игре
        """
        game_id = utils.get_args_raw(message)
        output_mess = ''
        response = requests.get('https://www.cheapshark.com/api/1.0/games?id={gameid}'.format(gameid=game_id))
        try:
            cheapest_time = datetime.datetime.fromtimestamp(int(response.json()['cheapestPriceEver']['date']))
            stores = requests.get('https://www.cheapshark.com/api/1.0/stores')
            where_to_buy = []
            price = []
            link = []
            retail_price = []
            savings = []
            rounded_savings = []
            cutted = str(cheapest_time).split(' ')
            cheapest_time_s = cutted[0]
            cutted2 = cheapest_time_s.split('-')
            cheapest_time_f = cutted2[2] + "." +cutted2[1] + "." + cutted2[0]
            try:
                output_mess += "Информация о " + f"<code>{str(response.json()['info']['title'])}</code>" + ":" + "\n    Самая низкая цена на эту игру была: " + f"<code>{str(response.json()['cheapestPriceEver']['price'])}</code>" + "$" + "\n    Дата, когда эта цена была зафиксирована: " + f"<code>{str(cheapest_time_f)}</code>" + "\n    Эту игру можно купить: "
            except TypeError:
                output_mess += "<b>[Ошибка] Игры с таким ID не найдено. Проверьте правильность его написания.</b>"
            for i in range(len(response.json()['deals'])):
                storeid = int(response.json()['deals'][i]['storeID'])
                price.append(str(response.json()['deals'][i]['price']))
                where_to_buy.append(str(stores.json()[storeid - 1]['storeName']))
                link.append("https://www.cheapshark.com/redirect?dealID=" + str(response.json()['deals'][i]['dealID']))
                retail_price.append(str(response.json()['deals'][i]['retailPrice']))
                savings.append(response.json()['deals'][i]['savings'])
                rounded_savings.append(round(float(savings[i])))
                if rounded_savings[i] == 0:
                    output_mess += "\n    " + f"<a href={link[i]}"">Тут</a>" + " (" + where_to_buy[i] + ")" + " за " + f"<code>{price[i]}</code>" + "$."
                else:
                    output_mess += "\n    " + f"<a href={link[i]}"">Тут</a>" + " (" + where_to_buy[i] + ")" + " за " + f"<code>{price[i]}</code>" + "$." + " Обычная цена игры: " + f"<code>{retail_price[i]}</code>" + "$" + " экономия составит " + f"<code>{str(rounded_savings[i])}</code>" + "%"
        except KeyError:
            output_mess += "[Ошибка] ID должно быть целым числом."
        await message.edit(output_mess)