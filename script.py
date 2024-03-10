import asyncio
import aiohttp
import time
from asynciolimiter import Limiter

start_time = time.time()
data = []
errors = []

# async def main():
#     async with aiohttp.ClientSession() as session:
#         url = "http://localhost:5000/"
#         for num in range(1,1000):
#             params = {"num": num}
#             async with session.get(url, params=params) as resp:
#                 json_resp = await resp.json()
#                 data.append(json_resp)
#         print(data)

# asyncio.run(main())

# data = []

# semaphore = asyncio.Semaphore(1)

limiter =  Limiter(999/60)

async def get_data(session, params):
        await limiter.wait()
        url = "http://localhost:5000/"
        call_again = True
        count = 0
        while call_again == True:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    json_resp = await resp.json()
                    mapped_data = {
                        "message": json_resp['message'],
                        "calcs": json_resp['math']
                    }
                    call_again = False
                    return mapped_data
                else:
                    errors.append({"params": params, "status": resp.status})
                    count += 1
                    if count > 4:
                        call_again = False
                    else:
                         await asyncio.sleep(count)

async def main():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for num in range(1,2000):
                params = {"num": num}
                tasks.append(asyncio.ensure_future(get_data(session,params)))
            finished_data = await asyncio.gather(*tasks)
            finished_data = list(filter(None, finished_data))
            print(finished_data)
            print(finished_data[0])
            print(errors)
            print(len(errors))
            print(len(finished_data))
    
asyncio.run(main())
print(f"Requests processed in {(time.time() - start_time)} seconds")