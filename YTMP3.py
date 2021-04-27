from .. import loader, utils
import requests
from bs4 import BeautifulSoup as bs
import io

@loader.tds
class YTmp3Mod(loader.Module):
    """YouTube to .mp3 by @blazeftg"""
    strings = {"name": "ytmp3"}

    async def mp3cmd(self, message):
        """.mp3 <ссылка на видео> <опционально, качество аудиозаписи>
        Если не указать качество аудио, то оно автоматически будет выставлено на "1"
        Справка по качеству:
        1 - 320 kbps
        2 - 256 kbps
        3 - 192 kbps
        4 - 128 kbps
        Короче говоря, чем ниже - тем лучше.
        """
        await message.edit(f"<b>Скачиваю...</b>")
        all = utils.get_args_raw(message)
        is_mobile = False
        mobile_id = ''
        all1 = all.split(' ')
        link = all1[0]
        mobile = link.split('youtu.be/')
        try:
            mobile_id = mobile[1]
            is_mobile = True
        except IndexError:
            is_mobile = False
        try:
            quality = int(all1[1])
        except IndexError:
            quality = 1
        if quality < 1 or quality > 4:
            await message.edit(f"<b>[Ошибка] Качество аудио должно быть от 1 до 4.</b>")
        else:
            quality -= 1
            counter = 0
            filtered = link.split('v=')
            linkcheck = ''
            url_o = ''
            video_id = ''
            if is_mobile == False:
                try:
                    filtered = filtered[1].split('&ab_channel=')
                    filtered = filtered[0].split('&feature=')
                    video_id = filtered[0]
                except IndexError:
                    linkcheck = 'failed'
            else:
                pass
            if linkcheck == 'failed':
                await message.edit(f"<b>[Ошибка] Неправильный формат ссылки.</b>")
                return
            else:
                if mobile_id != '':
                    video_id = mobile_id
                else:
                    pass
                
                html = requests.get('https://www.yt-download.org/api/button/mp3/{id}'.format(id = video_id))
                soup = bs(html.text, 'html.parser')
                div = soup.find_all('a')
                for i in div:
                    if counter == quality:
                        url = i.get('href')
                        url_o = url
                    counter += 1
                dllink = url_o
                response = requests.get('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={id}'.format(id = video_id))
                try:
                    title = str(response.json()['title'])
                except:
                    await message.edit(f"<b>[Ошибка] Видео по такой ссылке не может быть найдено.</b>")
                    return
                try:
                    a = requests.get(dllink)
                except:
                    return
                mp3 = io.BytesIO(a.content)
                mp3.name = title + ".mp3"
                mp3.seek(0)
                await message.edit(f"<b>Загружаю в телегу...</b>")
                await message.client.send_file(message.to_id, mp3)
                await message.delete()