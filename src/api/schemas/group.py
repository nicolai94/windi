from src.core.config import BaseSchema


class GroupCreateInput(BaseSchema):
    name: str
    owner_id: int
    members: list[int]


class GroupCreateOutput(GroupCreateInput):
    id: int
