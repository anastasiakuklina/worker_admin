from pydantic import BaseModel, PositiveInt, Field


class CreateEmployeeData(BaseModel):
    name: str = Field(min_length=1)
    age: PositiveInt = Field(ge=18, le=100)
    position: str
    salary: float = Field(gt=0)


class UpdateEmployeeData(BaseModel):
    name: str | None = Field(None, min_length=1)
    age: PositiveInt | None = Field(None, ge=18, le=100)
    position: str | None = None
    salary: float | None = Field(None, gt=0)
