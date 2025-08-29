from enum import Enum


class EventType(str, Enum):
    TASK = "task"
    MEETING = "meeting"
    OTHER = "other"