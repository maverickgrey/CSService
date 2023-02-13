from fastapi import APIRouter

wrouter = APIRouter(
    prefix="/intro",
    tags=['intro'])

@wrouter.get("/")
def hello():
    return {"message":"hello! to use the code search function, you should.....and we offer...."}
