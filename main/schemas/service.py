from pydantic import BaseModel, Field

class ServiceRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5)
    importance: int = Field(gt=0, lt=11)
