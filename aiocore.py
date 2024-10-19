import sys
import time
import base64
import aiohttp
import asyncio
import traceback
from urllib.parse import urljoin
from urllib.parse import urlparse

async def requests_async_function_(tasks, URL=True, STATUS_CODE=True, TEXT_LENGTH=True, HEADERS=True, TEXT=True, CONTENT=False, semaphore=2048, timeout=300):

    media_type = ["image/","video/","audio/","application/zip","application/x-rar-compressed","application/x-tar","application/gzip","application/x-7z-compressed","application/pdf","application/msword","application/vnd.ms-excel","application/vnd.ms-powerpoint","application/font"]

    async with aiohttp.ClientSession( timeout=aiohttp.ClientTimeout(total=timeout), connector=aiohttp.TCPConnector(ssl=False, limit=semaphore) ) as session:
        _semaphore = asyncio.Semaphore(semaphore) if semaphore else asyncio.Semaphore()

        async def async_request(task):
            if not task: return dict()
            if type(task)==str: task = { "url" : task }
            try:
                async with _semaphore:
                    start_time=time.time()
                    async with session.request(
                            method = "GET" if not task.get( "data" ) else "POST",
                            timeout = aiohttp.ClientTimeout( total=timeout ),
                            url = urljoin( task.get( "webroot" ),task.get("path") ) if not task.get("url") else task.get("url"),
                            headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0"},
                            params = task.get( "params" ),
                            data = task.get( "data" )
                            ) as response:

                        if response is not None:
                            print(f"[{response.status}] {response.url}")

                            if TEXT_LENGTH==True and TEXT==True:
                                response.text = await response.text(errors="replace")
                                response.text_length = len( response.text )

                            elif TEXT_LENGTH==True and TEXT==False:
                                response.text = await response.text(errors="replace")
                                response.text_length = len( response.text )
                                response.text = str()

                            else:
                                response.text = await response.text(errors="replace") if TEXT else str()

                            response.content = await response.read() if CONTENT else str()
                            content_type = response.headers.get("Content-Type")

                            for _type in media_type:
                                if content_type and _type in content_type:
                                    response.text=str()

                        return {
                                "url" : str(response.url) if URL else str(),
                                "status_code" : response.status if STATUS_CODE else int(),
                                "text-length" : response.text_length if TEXT_LENGTH else int(),
                                "headers" : dict(response.headers) if HEADERS else dict(), 
                                "text" : str(response.text) if TEXT else str(), 
                                "content" : responses.content if CONTENT else bytes()
                                }

            except Exception as e:
                # print(f"\033[91m[!] {urljoin( task.get('webroot'), task.get('path')) }  Exception:{e}\033[0m")
                # print(f"[!] Exception:{traceback.format_exc()}")
                return dict()

        tasks = [asyncio.create_task(async_request(task)) for task in tasks]
        responses = await asyncio.gather(*tasks)
    return responses

def requests_responses(tasks, semaphore=2048, timeout=300) -> list():
    responses = asyncio.run(requests_async_function_(tasks))
    return responses
