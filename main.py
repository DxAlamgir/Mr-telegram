import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

# ==================== CONFIGURATION ====================
TOKEN = "8310808582:AAEeRHz1eJ8JYfBmiukIm8DGeliTNiON3hU"
ADMIN_ID = 5855176189
CHANNEL_USERNAME = "@hellobrotherjn"

# 🎯 ডেমো ভিডিওর ১৩টি আইডি
DEMO_POSTS_LIST = [13, 14, 15, 16, 17, 18, 19, 20, 3, 4, 5, 6, 7]

# 🎯 আপনার দেওয়া নতুন প্রিমিয়াম ভিডিওর আইডিগুলো এখানে বসানো হয়েছে
PREMIUM_POSTS_LIST = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

QR_IMAGE_URL = "https://i.supaimg.com/28c3b85a-08f9-4c19-8e50-0afa56fe2af3/89145c9a-a1dd-4dd8-abd6-58ba78e84586.png"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ==================== PROFESSIONAL DESIGN HELPERS ====================
def header(title: str) -> str:
    return f"✨ *{title}* ✨\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

def footer() -> str:
    return "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🔹 *Powered by VIP Hub* 🔹"

# ==================== START COMMAND ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome = (
        f"{header('Welcome to Premium Hub')}"
        f"👋 *Hello {user.first_name}*, glad to have you here!\n\n"
        f"🎬 *Exclusive Content*\n✔️ Ad-free HD videos\n✔️ Weekly updates\n\n"
        f"👇 *Check out free demo videos below* 👇"
        f"{footer()}"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")
    
    # Send all demo videos
    for post_id in DEMO_POSTS_LIST:
        try:
            await context.bot.copy_message(chat_id=user.id, from_chat_id=CHANNEL_USERNAME, message_id=post_id)
        except Exception as e:
            logging.error(f"Demo error: {e}")
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 UNLOCK PREMIUM 💎", callback_data='buy_full_video')],
        [InlineKeyboardButton("🔥 GET VIP ACCESS 🔥", callback_data='buy_full_video')]
    ])
    await update.message.reply_text(
        f"{header('📢 Loved the demos?')}"
        f"⚡ *Click below to unlock the full VIP pack*\n"
        f"💰 *Pay only 59 INR*\n"
        f"{footer()}",
        reply_markup=keyboard, parse_mode="Markdown"
    )

# ==================== PREMIUM BUTTON ====================
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'buy_full_video':
        msg = (
            f"{header('💳 Payment Gateway')}"
            f"💰 *Amount:* 59 INR\n\n"
            f"📌 *Steps:*\n"
            f"1️⃣ Scan the QR code below\n"
            f"2️⃣ Pay exactly 59 INR via PhonePe\n"
            f"3️⃣ Send the Transaction ID or screenshot here\n"
            f"4️⃣ Admin will verify and unlock your VIP pack within 5 minutes\n\n"
            f"⏳ *Send proof immediately after payment*"
            f"{footer()}"
        )
        try:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=QR_IMAGE_URL, caption=msg, parse_mode="Markdown")
        except:
            await query.edit_message_text(text=msg, parse_mode="Markdown")
        context.user_data['waiting_for_proof'] = True

# ==================== PAYMENT PROOF + SUPPORT ====================
async def handle_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    # Ignore admin messages
    if user_id == ADMIN_ID:
        return

    user_link = f"[{user.first_name}](tg://user?id={user_id})"

    # Case: waiting for payment proof
    if context.user_data.get('waiting_for_proof'):
        context.user_data['waiting_for_proof'] = False
        await update.message.reply_text(
            f"{header('✅ Submission Received')}"
            f"Your payment proof has been forwarded to admin. You will receive your VIP content shortly.\n"
            f"Thank you! {footer()}",
            parse_mode="Markdown"
        )
        admin_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Approve & Send VIP", callback_data=f"approve_{user_id}"),
             InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")]
        ])
        admin_txt = (
            f"🔔 *NEW PAYMENT REQUEST* 🔔\n"
            f"👤 User: {user_link}\n"
            f"🆔 `{user_id}`\n"
        )
        if update.message.photo:
            admin_txt += f"🖼 *Screenshot attached below*"
            await context.bot.send_photo(ADMIN_ID, update.message.photo[-1].file_id, caption=admin_txt, reply_markup=admin_kb, parse_mode="Markdown")
        elif update.message.text:
            admin_txt += f"💬 *Transaction ID:* `{update.message.text}`"
            await context.bot.send_message(ADMIN_ID, admin_txt, reply_markup=admin_kb, parse_mode="Markdown")
        return
    
    # General support message (not payment proof)
    await update.message.reply_text(
        f"{header('📬 Support Center')}"
        f"Your message has been forwarded to admin. You will receive a reply here soon.\n"
        f"⏳ Please wait.\n{footer()}",
        parse_mode="Markdown"
    )
    support_kb = InlineKeyboardMarkup([[InlineKeyboardButton("💬 Reply to User", callback_data=f"reply_user_{user_id}")]])
    info = (
        f"📩 *NEW SUPPORT MESSAGE*\n"
        f"👤 User: {user_link}\n🆔 `{user_id}`\n"
    )
    if update.message.text:
        await context.bot.send_message(ADMIN_ID, info + f"📝 *Message:*\n{update.message.text}", reply_markup=support_kb, parse_mode="Markdown")
    elif update.message.photo:
        await context.bot.send_photo(ADMIN_ID, update.message.photo[-1].file_id, caption=info + "🖼 Photo attached", reply_markup=support_kb, parse_mode="Markdown")
    else:
        await context.bot.send_message(ADMIN_ID, info + "📎 Media/File Sent", reply_markup=support_kb, parse_mode="Markdown")

# ==================== ADMIN ACTIONS ====================
async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("reply_user_"):
        uid = int(data.split("_")[2])
        await context.bot.send_message(
            ADMIN_ID,
            f"✏️ *To reply to user `{uid}`*, use:\n`/reply {uid} your message`\nExample: `/reply {uid} Your issue has been resolved.`",
            parse_mode="Markdown"
        )
        await query.edit_message_reply_markup(reply_markup=None)
        return
        
    parts = data.split("_")
    action, uid = parts[0], int(parts[1])
    if action == "approve":
        try:
            await context.bot.send_message(
                uid,
                f"{header('🎉 Payment Verified!')}"
                f"Thank you for your purchase. Your full VIP pack has been unlocked.\n"
                f"🍿 Enjoy your premium content below:\n{footer()}",
                parse_mode="Markdown"
            )
            for pid in PREMIUM_POSTS_LIST:
                try:
                    await context.bot.copy_message(chat_id=uid, from_chat_id=CHANNEL_USERNAME, message_id=pid)
                except Exception as e:
                    logging.error(f"Premium copy error: {e}")
            await query.edit_message_text(text=f"✅ Approved! All premium videos sent to user {uid}.")
        except TelegramError:
            await query.edit_message_text(text=f"❌ Approval Failed: User blocked the bot.")
            
    elif action == "reject":
        try:
            await context.bot.send_message(
                uid,
                f"{header('❌ Payment Rejected')}"
                f"The transaction ID or screenshot you provided could not be verified.\n"
                f"Please send the correct proof again.\n{footer()}",
                parse_mode="Markdown"
            )
            await query.edit_message_text(text=f"❌ Rejected. User {uid} has been notified.")
        except TelegramError:
            await query.edit_message_text(text=f"🔴 Rejected! (User has blocked the bot)")

# ==================== ADMIN REPLY COMMAND ====================
async def admin_reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Unauthorized.")
        return
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: `/reply user_id message`", parse_mode="Markdown")
        return
    uid = int(context.args[0])
    text = " ".join(context.args[1:])
    try:
        await context.bot.send_message(uid, f"📩 *Admin Reply:*\n{text}\n━━━━━━━━━━━━━━━━\nThank you for contacting us.", parse_mode="Markdown")
        await update.message.reply_text(f"✅ Reply sent to user {uid}.")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed: {e}")

# ==================== MAIN ====================
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", admin_reply_command))
    app.add_handler(CallbackQueryHandler(button_click, pattern='^buy_full_video$'))
    app.add_handler(CallbackQueryHandler(admin_action, pattern='^(approve|reject|reply_user_)'))
    app.add_handler(MessageHandler(filters.ALL, handle_proof))
    print("✅ Bot is running perfectly with new Premium slots...")
    app.run_polling()

if __name__ == '__main__':
    main()
