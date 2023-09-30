import os
from typing import Dict, Tuple, Union

from models.settings import Chat, Video, Text, Voice, Audio, Document, PhotoFragment


def serialize(payload: Dict[str, Union[str, int, dict]]) -> Tuple[str, int]:
    chat = Chat(**{**payload, **payload['chat'], **payload['from']})
    if payload.get('video'):
        return process_video(chat, Video(**payload['video']))
    if payload.get('text'):
        return process_text(chat, Text(**payload))
    if payload.get('voice'):
        return process_voice(chat, Voice(**payload['voice']))
    if payload.get('audio'):
        return process_audio(chat, Audio(**payload['audio']))
    if payload.get('document'):
        return process_document(chat, Document(**payload['document']))
    if payload.get('photo'):
        # Matches for compressed images
        return process_photo(chat, [PhotoFragment(**d) for d in payload['photo']])
    raise ValueError("Payload type is not allowed.")


def process_video(chat, data) -> Tuple[str, int]:
    return "Received a video", chat.id


def process_text(chat: Chat, data: Text) -> Tuple[str, int]:
    if 'stop' in data.text or 'exit' in data.text or 'kill' in data.text:
        response = "Stopping webhook server"
        os.kill(os.getpid(), 15)  # Send a terminate signal for the current process ID triggering shutdown event
    else:
        response = f"Received {data.text}"
    return response, chat.id


def process_voice(chat, data) -> Tuple[str, int]:
    return "Received a voice memo", chat.id


def process_audio(chat, data) -> Tuple[str, int]:
    return "Received an audio file", chat.id


def process_document(chat, data) -> Tuple[str, int]:
    return "Received a document", chat.id


def process_photo(chat, data) -> Tuple[str, int]:
    return "Received a photo", chat.id
