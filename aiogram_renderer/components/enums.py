from enum import Enum


class RenderMode(str, Enum):
    EDIT = "edit"
    DELETE_AND_SEND = "delete_and_send"
    ANSWER = "answer"
    REPLY = "reply"
    EDIT_OR_ANSWER = "edit_or_answer"
