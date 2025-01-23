from typing import Optional

from pydantic import BaseModel


# id = Column(Integer, primary_key=True, index=True)
# name = Column(String, nullable=False)
# description = Column(String, nullable=True)


class ResourceCreate(BaseModel):
    name: str
    description: str | None = ""
    # тут буде цікава помилка


class ResourceDetail(BaseModel):
    id: int
    name: str
    description: Optional[str]
