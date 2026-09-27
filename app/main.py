from fastapi import FastAPI
from app.api.v1.endpoints.auth import router


app = FastAPI(title="E-Commerce Backend", version='1.0.0')

app.include_router(router=router, prefix="/Auth", tags=['auth'])

@app.get("/")
def root():
    return {"message": "E-commerce Api is running"}