from pydantic import BaseModel

class QueryResponse(BaseModel):
    result:dict=None