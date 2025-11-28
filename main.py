from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.api_route("/", methods=["GET", "POST", "OPTIONS"])
async def http_entry(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=204)
    name = "world"
    if request.query_params.get("name"):
        name = request.query_params["name"]
    else:
        if request.method == "POST":
            try:
                body = await request.json()
            except Exception:
                body = {}
            if isinstance(body, dict) and body.get("name"):
                name = body["name"]

    return {
        "hello": name,
        "runtime": "python",
        "my test env": os.getenv("TEST_ENV", "unknown"),
    }
