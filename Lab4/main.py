from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import router, load_barbershop_state

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_event_handler("startup", load_barbershop_state)

app.include_router(router)
