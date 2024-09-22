import asyncio
import random

async def async_hello():
    await asyncio.sleep(random.random())
    print("Hello, async Python!")

async def print_number(number):
    await asyncio.sleep(random.random())
    print(number)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(
        asyncio.gather(*[print_number(number) for number in range(10)], async_hello())
    )

    loop.close()