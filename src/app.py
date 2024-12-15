from fastapi import FastAPI

from queues.router import router as router_queues

from results.router import router as router_results
from exceptions.error_handler import add_exception_handler
from startup.create_exchange import create_queues_and_exchanges

app = FastAPI(title="RestAPIForHigh-loadQueries")


app.include_router(router_queues)
app.include_router(router_results)

add_exception_handler(app)


@app.on_event("startup")
async def on_startup():
    await create_queues_and_exchanges()


@app.get("/")
async def root():
    return
