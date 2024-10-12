import asyncio
import os
import curses
import multiprocessing.dummy

import aiohttp
import aiofiles
import prettytable

def main():
    print(path_checker())

def path_checker():
    path = ""
    while not os.path.isdir(path):
        path = input("Введите путь для сохранения файлов: ")
    return path

class Downloader():
    pass

async def downloader(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open('/some/file.img', mode='wb')
                await f.write(await resp.read())
                await f.close()
            else:
                print(resp.status)

class Link():
    def __init__(self, link):
        self.link = link
        self.status = None

class Viewer():
    def __init__(self, links_list):
        self.table =  prettytable.PrettyTable()
        self.table.field_names = ["Link", "Status"]
        self.links = links_list

    def update_links(self):
        pass

if __name__ == "__main__":
    main()