from pydantic import BaseModel, Field



#schema for blog posts
class PostSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    id:int=Field(...)

    class Config:
        schema_extra = {
            "example": {

                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }
