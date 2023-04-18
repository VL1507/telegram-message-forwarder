from pyrogram import types, filters
from pyrogram.client import Client
from pyrogram.types import InputMediaAudio, InputMediaVideo
from pyrogram.types import InputMediaDocument, InputMediaPhoto


api_id = ...
api_hash = ...


FROM_CHATS_ID = [..., ..., ...]
TO_CHAT_ID = ...


app = Client(name='UserBot', api_id=api_id, api_hash=api_hash)

input_media1 = []   # костыль, чтобы нормально отправлялись media_group


@app.on_message(filters.chat(FROM_CHATS_ID))
def my_handler(client: Client, msg: types.Message):
    global input_media1

    if msg.media_group_id is None:
        app.copy_message(chat_id=TO_CHAT_ID,
                         from_chat_id=msg.chat.id,
                         message_id=msg.id)
    else:
        media_group = app.get_media_group(chat_id=msg.chat.id,
                                          message_id=msg.id)

        input_media = []
        for media in media_group:
            if media.photo is not None:
                input_media.append(InputMediaPhoto(media.photo.file_id,
                                                   media.caption))
            elif media.document is not None:
                input_media.append(InputMediaDocument(media.document.file_id,
                                                      media.caption))
            elif media.video is not None:
                input_media.append(InputMediaVideo(media.video.file_id,
                                                   media.caption))
            elif media.audio is not None:
                input_media.append(InputMediaAudio(media.audio.file_id,
                                                   media.caption))
            else:
                print('что-то не то\n', media)

        if input_media1 != input_media:
            input_media1 = input_media.copy()
            app.send_media_group(chat_id=TO_CHAT_ID, media=input_media1)


if __name__ == '__main__':
    print("===== user-bot online =====")
    app.run()
