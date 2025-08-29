from pydantic import BaseModel


class CommetBase(BaseModel):
    text: str
    task_id: int

class CommentCreateRequest(CommetBase):
    pass

class CommentCreateResponse(CommetBase):
    id: int
    author_id: int