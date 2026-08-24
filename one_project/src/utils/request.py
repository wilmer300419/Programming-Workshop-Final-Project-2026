from fastapi import Request


async def get_request_json(request: Request):
    return await request.json()