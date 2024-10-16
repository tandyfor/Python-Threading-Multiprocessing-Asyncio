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
        self.time = 0

    def __str__(self):
        return f"{self.link} {self.status}"

    def get_row(self):
        # return self.link, self.status
        return self.link, self.status, round(self.time, 2)

class Downloader():
    def __init__(self, links_list: list[Link], path: str):
        self.links_list = links_list
        self.path = path
        self.n = 0
        self.viewer = Viewer(self.links_list)

    async def download(self, link: Link):
        print(self.viewer)
        async with aiohttp.ClientSession() as session:
            try:
                start = time.time()
                async with session.get(link.link) as responce:
                    if responce.ok:
                        f = await aiofiles.open(f'{self.path}/file_{self.n}.jpeg', mode='wb')
                        self.n += 1
                        await f.write(await responce.read())
                        await f.close()
                        link.status = SUCCESS
                        link.time = time.time() - start
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
        # self.table.field_names = ["Link", "Status"]
        self.table.field_names = ["Link", "Status", "Download time"]
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

async def async_input(links: list[Link], downloader: Downloader, loop: asyncio.new_event_loop):
    while True:
        link = await aioconsole.ainput("Input linl or press Enter to exit:\n")
        if not link: break
        link = Link(link)
        links.append(link)
        asyncio.create_task(downloader.download(link))
    n = 0
    while True:
        n += 1
        await asyncio.sleep(0.1)
        tasks = len(asyncio.all_tasks())
        print(f"{n} {tasks}")
        if tasks == 1:
            # loop.stop()
            return


def main():
    links = []
    d = Downloader(links, path_checker())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(async_input(links, d, loop))
    # loop.run_in_executor(async_input(links, d, loop))
    # loop.run_forever() # TODO: Добавить функционал для завершения.
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
# https://avatars.mds.yandex.net/i?id=1ce48e46d9be18457cc407e0fd3f84db-4969866-images-thumbs&n=13
# https://avatars.mds.yandex.net/i?id=e81d8ced97fc0b756754d3e698a63f38_l-5281441-images-thumbs&n=13
# https://avatars.mds.yandex.net/i?id=c35cfcea1dead6bb9760c7cc56fd5057_l-4234782-images-thumbs&n=13
# https://img.goodfon.com/wallpaper/nbig/d/9a/devushka-aziatka-vzgliad-110.webp
# https://yt3.ggpht.com/ytc/AKedOLQv3piyJBKo-KMp1UVlw7ameDW6-YTSZQSi4nli=s900-c-k-c0x00ffffff-no-rj
# https://avatars.mds.yandex.net/i?id=c20fcef0886895fe7a8495c2d1f4d781_l-4569757-images-thumbs&n=13
