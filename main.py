from fastapi import FastAPI

app = FastAPI()


@app.get("/welcome")
def welcome_func():
    return {
        "message":"Hello World"
    }