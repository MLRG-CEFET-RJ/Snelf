from pydantic import BaseModel

class HttpResponse(BaseModel):
    texto: str
    status: int