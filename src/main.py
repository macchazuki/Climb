from fastapi import FastAPI

from .routers import status, admin

app = FastAPI()

app.include_router(status.router)
app.include_router(admin.router, prefix='/admin')


@app.get("/")
def root():
    return {"message": "Welcome to Climb!"}
