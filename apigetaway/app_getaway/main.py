import uvicorn
from fastapi import FastAPI,Request
from httpx import AsyncClient



app = FastAPI()

client = AsyncClient()


@app.post("/{path:path}")
async def forward_auth_request(path: str, request: Request):
    url = f'http://0.0.0.0:8000/auth/{path}'
    print(url)
    payload = await request.body()
    print(payload)
    headers = request.headers
    print(headers)
    response = await client.post(url, data=payload, headers=headers)
    return response.json()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8002)