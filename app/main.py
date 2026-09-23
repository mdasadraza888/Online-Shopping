from fastapi import FastAPI
from app.core.exceptions import global_exception_handler


app = FastAPI(title="E-Commerce Backend", version='1.0.0')
app.add_exception_handler(Exception, global_exception_handler)

@app.get("/")
def root():
    return {"message": "E-commerce Api is running"}