import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Configuration (Token and Admin ID are fully fixed)
TOKEN = "8310808582:AAEeRHz1eJ8JYfBmiukIm8DGeliTNiON3hU"
ADMIN_ID = 5855176189  # Your Telegram Chat ID

CHANNEL_USERNAME = "@hellobrotherjn"

# 🎯 এখানে আপনার ৬টি ডেমো ভিডিওর পোস্ট আইডি বসাবেন (আপাতত আপনার ২ নম্বর পোস্টটি দেওয়া আছে)
DEMO_POSTS_LIST = [
    3,  # ১ম ডেমো ভিডিওর পোস্ট আইডি
    4,  # ২য় ডেমো ভিডিওর পোস্ট আইডি
    5,  # ৩য় ডেমো ভিডিওর পোস্ট আইডি
    6,  # ৪র্থ ডেমো ভিডিওর পোস্ট আইডি
    7,  # ৫মি ডেমো ভিডিওর পোস্ট আইডি
    2   # ৬ষ্ঠ ডেমো ভিডিওর পোস্ট আইডি
]

# 🎯 এখানে আপনার ২০টি প্রিমিয়াম VIP ভিডিওর পোস্ট আইডি বসাবেন (আপাতত ২ নম্বর পোস্ট দেওয়া আছে)
PREMIUM_POSTS_LIST = [
    2,  # ১ম প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ২য় প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ৩য় প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ৪র্থ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ৫ম প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ৬ষ্ঠ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ৭ম প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ৮ম প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ৯ম প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১০ম প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১১শ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১২শ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১৩শ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১৪শ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১৫শ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১৬শ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১৭শ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১৮শ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2,  # ১৯শ প্রিমিয়াম ভিডিওর পোস্ট আইডি
    2   # ২০ম প্রিমিয়াম ভিডিওর পোস্ট আইডি
]

# Your PhonePe QR Code Image URL
QR_IMAGE_URL = "https://i.supaimg.com/28c3b85a-08f9-4c19-8e50-0afa56fe2af3/89145c9a-a1dd-4dd8-abd6-58ba78e84586.png" 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 1. Start Command: Automatically copies all 6 Demo Videos one by one (No Forward Tag)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    welcome_text = (
        f"👋 *Welcome {user.first_name} to the Premium Video Hub!*\n\n"
        "✨ We offer high-quality, exclusive premium content.\n"
        "👇 Below are your free teaser/demo videos. Enjoy!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")
    
    # Copies all 6 demo videos seamlessly
    for post_id in DEMO_POSTS_LIST:
        try:
            await context.bot.copy_message(
                chat_id=user.id,
                from_chat_id=CHANNEL_USERNAME,
                message_id=post_id
            )
        except Exception as e:
            logging.error(f"Demo copy error for post {post_id}: {e}")

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

# 4. Admin Panel: Copies all 20 Premium videos directly (No Forward Tag)
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
            "🍿 *Enjoy your premium content below:* "
        )
        await context.bot.send_message(chat_id=target_user_id, text=success_text, parse_mode="Markdown")
        
        # Copies all 20 premium videos one by one cleanly
        for post_id in PREMIUM_POSTS_LIST:
            try:
                await context.bot.copy_message(
                    chat_id=target_user_id,
                    from_chat_id=CHANNEL_USERNAME,
                    message_id=post_id
                )
            except Exception as e:
                logging.error(f"Premium copy error for post {post_id}: {e}")
        
        status_msg = f"🟢 *Approved!* All 20 premium videos copied to user `{target_user_id}`."
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

    print("Premium VIP Bot is operating securely with Custom 6 Demo & 20 Premium slots...")
    application.run_polling()

if __name__ == '__main__':
    main()
