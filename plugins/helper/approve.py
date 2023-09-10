import os
import asyncio
from Script import script
from pyrogram import Client, filters
from pyrogram.types import Message, User, ChatJoinRequest
from database.users_chats_db import db
from info import CHAT_ID, TEXT, APPROVED, LOG_CHANNEL


@Client.on_chat_join_request((filters.group | filters.channel) & filters.chat(CHAT_ID) if CHAT_ID else (filters.group | filters.channel))
async def autoapprove(client, message: ChatJoinRequest):
    chat=message.chat 
    user=message.from_user 
    print(f"{user.first_name} Joined (Approved)") 
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVED == "on":
        await client.send_message(chat_id=user.id, text=TEXT.format(mention=user.mention, title=chat.title))
        if not await db.is_user_exist(user.id):
            await db.add_user(user.id, user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))