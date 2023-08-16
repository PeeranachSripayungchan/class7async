# https://flask.palletsprojects.com/en/2.3.x/
# https://www.python-httpx.org/async/
# https://flask.palletsprojects.com/en/2.3.x/quickstart/#rendering-templates

import asyncio
import time
from random import randint
import httpx
from flask import Flask, render_template

app = Flask(__name__)

# function converted to coroutine
async def get_xkcd_image(session): # dont wait for the response of API
    random = randint(0, 1000)
    result = await session.get(f'https://xkcd.com/{random}/info.0.json')
    return result.json()['img']

# function converted to coroutine
async def get_multiple_images(number): 
    async with httpx.AsyncClient() as session:
        tasks = [get_xkcd_image(session) for _ in range(number)]
        result = await asyncio.gather(*tasks, return_exceptions=True)
    return result

@app.get('/comic')
async def hello(): 
    start = time.perf_counter()
    url = await get_multiple_images(10)
    end = time.perf_counter()
    return render_template('index.html', end=end, start=start, urls=urls)

if __name__ == '__main__':
    app.run(debug=True, port=5555)