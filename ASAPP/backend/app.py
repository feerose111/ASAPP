from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Starting ASAPP...")

@app.get("/menu")
async def get_menu():
    return None