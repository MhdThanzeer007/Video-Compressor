#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | @AbirHasan2005


from bot.database import Database
from bot.localisation import Localisation
from bot import (
    UPDATES_CHANNEL,
    DATABASE_URL,
    SESSION_NAME
)
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

db = Database(DATABASE_URL, SESSION_NAME)
CURRENT_PROCESSES = {}
CHAT_FLOOD = {}
broadcast_ids = {}

async def new_join_f(client, message):
    # delete all other messages, except for AUTH_USERS
    await message.delete(revoke=True)
    # reply the correct CHAT ID,
    # and LEAVE the chat
    chat_type = message.chat.type
    if chat_type != "private":
        await message.reply_text(
            Localisation.WRONG_MESSAGE.format(
                CHAT_ID=message.chat.id
            )
        )
        # leave chat
        await message.chat.leave()


async def help_message_f(client, message):
    if not await db.is_user_exist(message.chat.id):
        await db.add_user(message.chat.id)
    ## Force Sub ##
    if UPDATES_CHANNEL is not None:
        try:
            user = await client.get_chat_member(UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
               await message.reply_text(
                   text="Sorry Sir, You are Banned to use me. Contact Onwer[👨‍💻 𝗢𝗡𝗪𝗘𝗥 👨‍💻](https://t.me/mhd_thanzeer).",
                   parse_mode="markdown",
                   disable_web_page_preview=True
               )
               return
        except UserNotParticipant:
            await message.reply_text(
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Join Updates Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await message.reply_text(
                text="Something went Wrong. Contact my [𝗠𝗛𝗗 𝗧𝗛𝗔𝗡𝗭𝗘𝗘𝗥](https://t.me/mhd_thanzeer).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    ## Force Sub ##
    await message.reply_text(
        Localisation.HELP_MESSAGE,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝗠𝗼𝘃𝗶𝗲𝘀', url='https://t.me/wolfpackmedia'),
                    InlineKeyboardButton('𝗢𝗡𝗪𝗘𝗥', url='https://t.me/mhd_thanzeer'),
                    InlineKeyboardButton('𝐖𝐄𝐁 𝐒𝐄𝐑𝐈𝐄𝐒', url='https://t.me/joinchat/ttmNCbSNSyM2NWU1')
                ],
                [
                    InlineKeyboardButton('❌️ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗖𝗢𝗗𝗘 ❌️', url='https://telegra.ph/file/057ec425d174e8129826e.jpg')
                ]
            ]
        ),
        quote=True
    )
