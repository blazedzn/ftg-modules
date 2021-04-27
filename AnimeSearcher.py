from .. import loader, utils
import requests
import os
import datetime

@loader.tds
class AnimeSearcherrMod(loader.Module):
    """Ищет аниме по картинке by @blazeftg"""
    strings = {"name": "AnimeSearcher"}

    async def findanimecmd(self, message):
        """ .findanime <в ответ на картинку>
        Ищет аниме, по картинке
        """
        await message.edit("<b>Ищу...</b>")
        reply = await message.get_reply_message()
        if not reply:
          await message.edit("Нужен реплай на пикчу")
          return
        file = await reply.download_media()
        files = {'image' : open(file, 'rb')}
        response = requests.post('https://trace.moe/api/search', files = files)
        seconds = round(response.json()['docs'][0]['at'])
        time = str(datetime.timedelta(seconds=seconds))
        id = response.json()['docs'][0]['anilist_id']
        similarity = float(response.json()['docs'][0]['similarity']) * 100
        is_hentai = str(response.json()['docs'][0]['is_adult'])
        link = "https://anilist.co/anime/{anilist_id}".format(anilist_id = str(response.json()['docs'][0]['anilist_id']))
        if is_hentai == 'False':
            is_hentai = 'нет'
        else:
            is_hentai = 'да'
        await message.edit("Вероятность совпадения: " + f"<code>{str(round(similarity,1)) + '%'}</code>" + "\nНа этой фотографии обнаружено аниме: " + f"<code>{str(response.json()['docs'][0]['title_english'])}</code>" +"\nЭпизод №" + f"<code>{str(response.json()['docs'][0]['episode'])}</code>" + " на таймкоде " + f"<code>{str(time)}</code>" + "\nЯвляется хентаем? " + f"<code>{is_hentai}</code>" +"\n" + f"<a href={link}"">Страница этого аниме на Anilist.co</a>")
        os.remove(file)