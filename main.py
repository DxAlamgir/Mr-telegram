import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Configuration (Token is directly fixed here to prevent any Render errors)
TOKEN = "8310808582:AAEeRHz1eJ8JYfBmiukIm8DGeliTNiON3hU"
ADMIN_ID = 5855176189  # Your Telegram Chat ID

# 🎯 PASTE YOUR 5-6 DEMO VIDEO FILE IDs HERE
DEMO_VIDEOS_LIST = [
    "BAACAgUAAxkBAAMTahFw2X_7UMskukFpd2BaR7id3-UAAuseAALvjohUnx7U9pkg2FQ7BA",
    "BAACAgUAAxkBAAMUahFw2dopOI0MtnR3GCMlXQEPVVAAAuweAALvjohUzCbirEiL6VY7BA",
    "BAACAgUAAxkBAAMVahFw2UVzSdQNGbJ2sXmGo7UBy8sAAu0eAALvjohUt-iOhdaG0447BA",
    "BAACAgUAAxkBAAMWahFw2T-GzsTn9RIUWpNGch0w098AAvAeAALvjohUkyip_s7TT0s7BA",
    "BAACAgUAAxkBAAMXahFw2XsCid4JsS99dWE-4dhQScgAAu8eAALvjohUyYstoRyJzPc7BA"
]

# 🎯 PASTE YOUR 10-20 PREMIUM VIP VIDEO FILE IDs HERE
PREMIUM_VIDEOS_LIST = [
    "YOUR_PREMIUM_VIDEO_ID_1",
    "YOUR_PREMIUM_VIDEO_ID_2",
    "YOUR_PREMIUM_VIDEO_ID_3",
    "YOUR_PREMIUM_VIDEO_ID_4",
    "YOUR_PREMIUM_VIDEO_ID_5",
    "YOUR_PREMIUM_VIDEO_ID_6",
    "YOUR_PREMIUM_VIDEO_ID_7",
    "YOUR_PREMIUM_VIDEO_ID_8",
    "YOUR_PREMIUM_VIDEO_ID_9",
    "YOUR_PREMIUM_VIDEO_ID_10"
]

# Your PhonePe QR Code Image URL
QR_IMAGE_URL = "YOUR_QR_IMAGE_URL" 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 1. Start Command: Automatically sends all Demo Videos as an Album
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    welcome_text = (
        f"👋 *Welcome {user.first_name} to the Premium Video Hub!*\n\n"
        "✨ We offer high-quality, exclusive premium content.\n"
        "👇 Below are your free teaser/demo videos. Enjoy!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")
    
    # Send Demo Videos as an Album
    try:
        media_group = [InputMediaVideo(video_id) for video_id in DEMO_VIDEOS_LIST]
        media_group[0].caption = "🎬 *Watch the Free Teaser Videos Now!*"
        media_group[0].parse_mode = "Markdown"
        await context.bot.send_media_group(chat_id=user.id, media=media_group)
    except Exception as e:
        logging.error(f"Demo video album error: {e}")
        await update.message.reply_text("Error loading demo videos. Please contact the administrator.")

    # Premium Unique Layout Button Design
    keyboard = [
        [InlineKeyboardButton("💎 ── UNLOCK ALL PREMIUM VIDEOS ── 💎", callback_data='buy_full_video')],
        [InlineKeyboardButton("🚀 Get Instant VIP Access", callback_data='buy_full_video')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚡ *Loved the teasers? Don't miss out on the full VIP experience!*\n"
        "Click the button below to unlock all premium videos instantly 👇", 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 2. Premium Button Click: Displays PhonePe QR, 59 Taka Price and English instructions
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'buy_full_video':
        payment_instructions = (
            "🎯 *VIP PREMIUM ACCESS GATEWAY* 🎯\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "💰 *Amount to Pay:* 59 INR Only\n\n"
            "📌 *FOLLOW THESE EASY STEPS:* \n"
            "1️⃣ Scan the *PhonePe QR Code* shown above.\n"
            "2️⃣ Pay exactly *59 INR* securely.\n"
            "3️⃣ Copy the *Transaction ID / Payment ID* or take a *Screenshot*.\n"
            "4️⃣ Send the ID text or Screenshot directly in this chat! 📥\n\n"
            "⚠️ *Note:* Admin will manually verify your 59 INR payment and unlock the full VIP video pack within 5 minutes! ⏳"
        )
        
        try:
            await context.bot.send_photo(
                chat_id=query.message.chat_id, 
                photo=QR_IMAGE_URL, 
                caption=payment_instructions,
                parse_mode="Markdown"
            )
        except Exception as e:
            logging.error(f"QR Image error: {e}")
            await query.edit_message_text(text=payment_instructions, parse_mode="Markdown")
            
        context.user_data['waiting_for_proof'] = True

# 3. Handle Payment Proof: Forwards text/photo to Admin
async def handle_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    if context.user_data.get('waiting_for_proof'):
        context.user_data['waiting_for_proof'] = False
        
        await update.message.reply_text(
            "⏳ *Submission Received!*\n"
            "Your payment proof has been forwarded to the admin. Verification in progress... 🔐",
            parse_mode="Markdown"
        )
        
        admin_keyboard = [[InlineKeyboardButton("Approve & Send VIP Pack ✅", callback_data=f"approve_{user.id}"),
                           InlineKeyboardButton("Reject ❌", callback_data=f"reject_{user.id}")]]
        admin_markup = InlineKeyboardMarkup(admin_keyboard)
        
        admin_msg = (
            f"🔔 *NEW VIP PAYMENT ALERT (59 INR)!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 *User Name:* {user.first_name}\n"
            f"🆔 *User ID:* `{user.id}`\n"
            f"🔗 *Username:* @{user.username if user.username else 'None'}\n\n"
        )
        
        if update.message.text:
            admin_msg += f"💬 *Sent Payment ID:* `{update.message.text}`"
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg, reply_markup=admin_markup, parse_mode="Markdown")
        elif update.message.photo:
            caption = admin_msg + "🖼 *User uploaded a Payment Screenshot below.*"
            await context.bot.send_photo(chat_id=ADMIN_ID, photo=update.message.photo[-1].file_id, caption=caption, reply_markup=admin_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Please click the *Unlock All Premium Videos* button first to make a purchase.", parse_mode="Markdown")

# 4. Admin Panel: Splits up to 20 videos into clean 10-video albums
async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split("_")
    action = data[0]
    target_user_id = int(data[1])
    
    if action == "approve":
        success_text = (
            "🎉 *PAYMENT VERIFIED SUCCESSFULLY!* 🎉\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Thank you for your purchase of 59 INR! Your VIP premium pack is completely unlocked.\n"
            "🍿 *Enjoy all your premium videos below:* "
        )
        await context.bot.send_message(chat_id=target_user_id, text=success_text, parse_mode="Markdown")
        
        try:
            for i in range(0, len(PREMIUM_VIDEOS_LIST), 10):
                chunk = PREMIUM_VIDEOS_LIST[i:i+10]
                premium_media = [InputMediaVideo(video_id) for video_id in chunk]
                premium_media[0].caption = f"🔥 *Premium VIP Video Pack (Part {i//10 + 1})* 🔥"
                premium_media[0].parse_mode = "Markdown"
                await context.bot.send_media_group(chat_id=target_user_id, media=premium_media)
        except Exception as e:
            logging.error(f"Error sending premium album: {e}")
            await context.bot.send_message(chat_id=target_user_id, text="Error sending premium files. Please contact support.")
        
        status_msg = f"🟢 *Approved!* All premium VIP videos sent to user `{target_user_id}`."
        await query.edit_message_caption(caption=status_msg, parse_mode="Markdown") if query.message.photo else await query.edit_message_text(text=status_msg, parse_mode="Markdown")
        
    elif action == "reject":
        fail_text = (
            "❌ *PAYMENT VERIFICATION FAILED* ❌\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "The Transaction ID or screenshot you sent could not be verified.\n"
            "Please check your bank statement and submit the valid proof again."
        )
        await context.bot.send_message(chat_id=target_user_id, text=fail_text, parse_mode="Markdown")
        
        status_msg = f"🔴 *Rejected!* Request from user `{target_user_id}` was turned down."
        await query.edit_message_caption(caption=status_msg, parse_mode="Markdown") if query.message.photo else await query.edit_message_text(text=status_msg, parse_mode="Markdown")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click, pattern='^buy_full_video$'))
    application.add_handler(CallbackQueryHandler(admin_action, pattern='^(approve|reject)_'))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_proof))

    print("Premium VIP Bot is operating smoothly in English...")
    application.run_polling()

if __name__ == '__main__':
    main()
