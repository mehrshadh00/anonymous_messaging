import os
from telegram import Update, Message
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID"))  # آیدی شخصی شما
conversation_map = {}  # پیام فوروارد شده ← چت آیدی هنرجو

async def handle_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg: Message = update.message
    forwarded = await context.bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=user_msg.chat_id,
        message_id=user_msg.message_id
    )
    conversation_map[forwarded.message_id] = user_msg.chat_id

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_msg: Message = update.message
    if reply_msg.reply_to_message and reply_msg.chat_id == ADMIN_CHAT_ID:
        original_msg_id = reply_msg.reply_to_message.message_id
        if original_msg_id in conversation_map:
            target_user_id = conversation_map[original_msg_id]
            await context.bot.send_message(
                chat_id=target_user_id,
                text=reply_msg.text
            )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, handle_user))
app.add_handler(MessageHandler(filters.Chat(ADMIN_CHAT_ID) & filters.REPLY & filters.TEXT, handle_reply))

if __name__ == "__main__":
    app.run_polling()
