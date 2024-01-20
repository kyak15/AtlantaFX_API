
from fastapi import FastAPI,Request
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
import random
import json



with open('data.json', "r") as file:
    data = json.load(file)

seasons_data = data["seasons"]
cast_data = data["cast"]
quote_data = data['quotes']
print(quote_data)

templates = Jinja2Templates(directory="templates")
app = FastAPI()


@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/api/seasons/')
async def get_seasons():
    return seasons_data


@app.get('/api/seasons/{season_number}/')
async def get_season_by_number(season_number: int):
    for season in seasons_data:
        if season['season_number'] == season_number:
            return season
    raise HTTPException(status_code=404, detail="Season not found")


@app.get('/api/seasons/{season_number}/episodes/')
async def get_episodes_from_season(season_number: int):
    for season in seasons_data:
        if season['season_number'] == season_number:
            return season['episodes']
    raise HTTPException(status_code=404, detail="Season not found")


@app.get('/api/seasons/{season_number}/episodes/{episode_number}/')
async def get_episode_by_season_number(season_number: int, episode_number: int):
    for season in seasons_data:
        if season['season_number'] == season_number:
            for episode in season['episodes']:
                if episode['episode_number'] == episode_number:
                    return episode
    raise HTTPException(status_code=404, detail='Episode not found')


@app.get('/api/cast/')
async def get_cast():
    return cast_data


@app.get('/api/quotes/')
async def get_quotes():
    return quote_data



@app.post('/api/quotes/')
async def add_quote(character: str, quote_text: str):
    for item in quote_data:
        if quote_text == item['character']:
            raise HTTPException(status_code=301, detail="Quote Already in API")
    quote_data.append({character: quote_text})

@app.get('/api/quotes/randomquote')
async def get_random_quote():
    rand_int = random.randint(0, len(quote_data))
    print(quote_data[rand_int])
    return quote_data[rand_int]

@app.delete('/api/quotes')
async def delete_quote(character: str, quote_text: str):
    for item in quote_data:
        if quote_text == item['character']:
            quote_data.remove({character: quote_text})
