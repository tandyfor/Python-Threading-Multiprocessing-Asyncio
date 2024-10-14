import asyncio
import os
import curses
import multiprocessing.dummy

import aiohttp
import aiofiles
import aioconsole
import prettytable

import time

SUCCESS = "Успех"
FAIL = "Ошибка"
IN_PROCESS = "В процессе"

class Link(): 
    def __init__(self, link: str):
        self.link = link # TODO: Добавить поиск расширения файла для корректного сохранения.
        self.status = IN_PROCESS

    def __str__(self):
        return f"{self.link} {self.status}"

    def get_row(self):
        return self.link, self.status

class Downloader():
    def __init__(self, links_list: list[Link], path: str):
        self.links_list = links_list
        self.path = path
        self.n = 0
        self.viewer = Viewer(self.links_list)

    async def download(self, link: Link):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link.link) as responce:
                    if responce.ok:
                        f = await aiofiles.open(f'{self.path}/file_{self.n}.jpeg', mode='wb')
                        self.n += 1
                        await f.write(await responce.read())
                        await f.close()
                        link.status = SUCCESS
                    else:
                        print(responce.status)
            except:
                link.status = FAIL
        print(self.viewer)

    def download_all(self):
        return [self.download(link) for link in self.links_list if link.status == IN_PROCESS]


class Viewer():
    def __init__(self, links_list: list[Link]):
        self.table =  prettytable.PrettyTable()
        self.table.field_names = ["Link", "Status"]
        self.links = links_list

    def update_links(self):
        self.table.clear_rows()
        for link in self.links:
            self.table.add_row(link.get_row())

    def __str__(self):
        self.update_links()
        print("\033c")
        return self.table.get_string()

def path_checker():
    path = ""
    while not os.path.isdir(path) or not os.access(path, os.W_OK): # TODO: Добавить функционал создания директории и проверки прав как в примере в документации.
        path = input("Введите путь для сохранения файлов: ")
    return path

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    links = [
        Link("https://i.pinimg.com/originals/36/75/27/367527aa5f6f0fd80d86858ae25bb089.jpg"),
        Link("https://mir-s3-cdn-cf.behance.net/projects/original/4a627163531171.Y3JvcCwxMDI3NCw4MDQyLDk2NCww.jpg"),
        Link("https://www.ixpap.com/images/2022/02/Blade-Runner-Wallpaper-13.jpg"),
        Link("https://i.pinimg.com/originals/2d/a2/5a/2da25a2b249359f26f0335fc164d58c5.jpg"),
        Link("https://i.pinimg.com/originals/51/3c/86/513c863cee2dfbbd7e61b3f5f2fbeb00.png"),
        Link("dwa")
        ]
    d = Downloader(links, path_checker())
    loop.run_until_complete(asyncio.gather(*d.download_all()))
    loop.close()


if __name__ == "__main__":
    s = time.time()
    main()
    print(time.time() - s)



# https://i.pinimg.com/originals/36/75/27/367527aa5f6f0fd80d86858ae25bb089.jpg
# https://mir-s3-cdn-cf.behance.net/projects/original/4a627163531171.Y3JvcCwxMDI3NCw4MDQyLDk2NCww.jpg
# https://www.ixpap.com/images/2022/02/Blade-Runner-Wallpaper-13.jpg
# https://i.pinimg.com/originals/2d/a2/5a/2da25a2b249359f26f0335fc164d58c5.jpg
# https://i.pinimg.com/originals/51/3c/86/513c863cee2dfbbd7e61b3f5f2fbeb00.png
# dwa