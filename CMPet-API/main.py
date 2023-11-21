import os
from urllib.request import Request

from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

import os

from db import database

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_keys = os.environ.get('VALID_API_KEYS')

VALID_API_KEYS = api_keys


# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Custom middleware for API key validation
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("api-key")
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    response = await call_next(request)
    return response


@app.get('/')
async def root():
    return {'eg': ' this is an example', 'data': 0}


@app.get("/get_data")
async def get_data():
    try:
        query = "SELECT * FROM ingredients_table;"
        results = await database.fetch_all(query)

        serialized_results = [dict(result) for result in results]
        return JSONResponse(content=serialized_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_data/{pet}")
async def get_pet(pet):
    try:
        query = f"SELECT id, name, description, {pet}, {pet}_description FROM ingredients_table WHERE {pet} = 0 OR {pet} = 1 OR {pet} = 2 OR {pet} = 3;"
        results = await database.fetch_all(query)

        serialized_results = [dict(result) for result in results]
        return JSONResponse(content=serialized_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search_by_name/{name}")
async def search_by_name(name: str):
    try:
        query = "SELECT * FROM ingredients_table WHERE name LIKE :name;"
        values = {"name": f"%{name}%"}
        results = await database.fetch_all(query=query, values=values)

        serialized_results = [dict(result) for result in results]
        return JSONResponse(content=serialized_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search_by_names/{names}")
async def search_by_names(names: str):
    try:
        names_list = names.split(',')
        query = "SELECT * FROM ingredients_table WHERE name IN :names;"
        values = {"names": tuple(names_list)}
        results = await database.fetch_all(query=query, values=values)

        serialized_results = [dict(result) for result in results]
        return JSONResponse(content=serialized_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Get the port number from the PORT environment variable
port = int(os.environ.get('PORT', 8000))  # Use a default port if not provided


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
