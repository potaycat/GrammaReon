import asyncio
from concurrent.futures import ThreadPoolExecutor


class Async:
    executor = ThreadPoolExecutor()

    async def run_blockings(*blockings):
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(Async.executor, *fun) for fun in blockings]
        results = await asyncio.gather(*tasks)
        return results

    async def run_blocking(blocking):
        (result,) = await Async.run_blockings(blocking)
        return result

    def alt_thread(fun):
        async def wrapper(*args):
            return await Async.run_blocking((fun, *args))

        return wrapper
