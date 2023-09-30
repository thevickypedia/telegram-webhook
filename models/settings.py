from pydantic import BaseModel


class Message(BaseModel):
    """Base class for Message model."""

    date: int
    message_id: int

    class Chat(BaseModel):
        """Nested class for Chat model."""

        first_name: str
        last_name: str
        id: int
        type: str
        username: str
        is_bot: bool
        language_code: str

    # Below are the DataClass objects
    class Text(BaseModel):
        """Nested class for Text model."""

        text: str

    class PhotoFragment(BaseModel):
        """Nested class for PhotoFragment model."""

        file_id: str
        file_size: int
        file_unique_id: str
        height: int
        width: int

    class Audio(BaseModel):
        """Nested class for Audio model."""

        duration: int
        file_id: str
        file_name: str
        file_size: int
        file_unique_id: str
        mime_type: str

    class Voice(BaseModel):
        """Nested class for Voice model."""

        duration: int
        file_id: str
        file_size: int
        file_unique_id: str
        mime_type: str

    class Document(BaseModel):
        """Nested class for Document model."""

        file_id: str
        file_name: str
        file_size: int
        file_unique_id: str
        mime_type: str

    class Video(BaseModel):
        """Nested class for Video model."""

        duration: int
        file_id: str
        file_name: str
        file_size: int
        file_unique_id: str
        height: int
        mime_type: str
        width: int

        class Thumb(BaseModel):
            """Nested class for Thumb model."""

            file_id: str
            file_size: int
            file_unique_id: str
            height: int
            width: int

        class Thumbnail(BaseModel):
            """Nested class for Thumbnail model."""

            file_id: str
            file_size: int
            file_unique_id: str
            height: int
            width: int
