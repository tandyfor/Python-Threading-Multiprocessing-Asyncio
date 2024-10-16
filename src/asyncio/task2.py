import asyncio
import os

import aioconsole
import aiofiles
import aiohttp
import prettytable


SUCCESS = "Успех"
FAIL = "Ошибка"
IN_PROCESS = "В процессе"


class Link(): 
    def __init__(self, link: str):
        self.link = link
        self.status = IN_PROCESS
        self.file_extension = self.get_file_extension()

    def __str__(self):
        return f"{self.link} {self.status}"

    def get_row(self):
        return self.link, self.status
    
    def get_file_extension(self):
        return  self.link.split('.')[-1] if self.link.split('.')[-1] in ['png', 'jpg', 'jpeg', 'gif'] else 'jpeg'


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
                async with session.get(link.link) as responce:
                    if responce.ok:
                        f = await aiofiles.open(f'{self.path}/file_{self.n}.{link.get_file_extension()}', mode='wb')
                        self.n += 1
                        await f.write(await responce.read())
                        await f.close()
                        link.status = SUCCESS
                    else:
                        print(responce.status)
            except:
                link.status = FAIL
        print(self.viewer)


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
        return self.table.get_string() + "\nInput link or press Enter to exit:"

def path_checker():
    path = ""
    while not os.path.isdir(path) or not os.access(path, os.W_OK):
        path = input("Введите путь для сохранения файлов: ")
    return path

async def async_input(links: list[Link], downloader: Downloader):
    while True:
        link = await aioconsole.ainput("Input link or press Enter to exit:\n")
        if not link: break
        link = Link(link)
        links.append(link)
        asyncio.create_task(downloader.download(link))
    while True:
        await asyncio.sleep(0.1)
        if len(asyncio.all_tasks()) == 1: break


def main():
    links = []
    d = Downloader(links, path_checker())
    asyncio.run(async_input(links, d))


if __name__ == "__main__":
    main()


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
