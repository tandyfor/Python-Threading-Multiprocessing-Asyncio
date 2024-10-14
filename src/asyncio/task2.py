import asyncio
import os
import curses
import multiprocessing.dummy

import aiohttp
import aiofiles
import prettytable


class Link():
    def __init__(self, link: str):
        self.link = link
        self.status = None


class Downloader():
    def __init__(self, links_list: list[Link], path: str):
        self.links_list = links_list
        self.path = path
        self.n = 0

    async def download(self, link: Link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link.link) as responce:
                print(f"Responce {responce.status}")
                # html = await responce.text()
                # print(f"Body: {html}")
                f = await aiofiles.open(f'{self.path}/file_{self.n}.jpeg', mode='wb')
                self.n += 1
                await f.write(await responce.read())
                await f.close()

    def download_all(self):
        return [self.download(link) for link in self.links_list]


class Viewer():
    def __init__(self, links_list: list[Link]):
        self.table =  prettytable.PrettyTable()
        self.table.field_names = ["Link", "Status"]
        self.links = links_list

    def update_links(self):
        pass


def path_checker():
    path = ""
    while not os.path.isdir(path) or not os.access(path, os.W_OK): # TODO: Добавить функционал создания директории и проверки прав как в примере в документации.
        path = input("Введите путь для сохранения файлов: ")
    return path

def main():
    links = [
        Link("https://i.pinimg.com/originals/36/75/27/367527aa5f6f0fd80d86858ae25bb089.jpg"),
        Link("https://mir-s3-cdn-cf.behance.net/projects/original/4a627163531171.Y3JvcCwxMDI3NCw4MDQyLDk2NCww.jpg"),
        Link("https://www.ixpap.com/images/2022/02/Blade-Runner-Wallpaper-13.jpg"),
        Link("https://i.pinimg.com/originals/2d/a2/5a/2da25a2b249359f26f0335fc164d58c5.jpg")
        ]
    d = Downloader(links, path_checker())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(*d.download_all()))
    loop.close()

if __name__ == "__main__":
    main()
