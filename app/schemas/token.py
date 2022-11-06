from pydantic import BaseModel


# TODO: Add an extra field so we can invalidate tokens
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: str | None = None
