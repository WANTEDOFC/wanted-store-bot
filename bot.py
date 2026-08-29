import os
from urllib.parse import quote

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", "10000"))
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

UPI_ID = os.environ.get("UPI_ID")
UPI_NAME = os.environ.get("UPI_NAME", "WANTED STORE")

PRODUCTS = {
    "bala": {"name": "BALA MODS", "price": 100},
    "abcd": {"name": "ABCD PANNEL", "price": 99},
}


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Products", callback_data="products")],
        [InlineKeyboardButton("📦 My Orders", callback_data="orders")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("📞 Support", callback_data="support")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 *WELCOME TO WANTED STORE* 🔥\n\n"
        "Choose an option below:",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "products":
        keyboard = [
            [InlineKeyboardButton(
                "BALA MODS — ₹100",
                callback_data="bala"
            )],
            [InlineKeyboardButton(
                "ABCD PANNEL — ₹99",
                callback_data="abcd"
            )],
            [InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )],
        ]

        await query.edit_message_text(
            "🛒 *WANTED STORE PRODUCTS*\n\n"
            "Select a product:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data in PRODUCTS:
        product = PRODUCTS[query.data]

        keyboard = [
            [InlineKeyboardButton(
                f"💳 Buy — ₹{product['price']}",
                callback_data=f"buy_{query.data}"
            )],
            [InlineKeyboardButton(
                "🔙 Products",
                callback_data="products"
            )],
        ]

        await query.edit_message_text(
            f"📦 *{product['name']}*\n\n"
            f"💰 Price: ₹{product['price']}\n\n"
            "Press the button below to continue.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data.startswith("buy_"):
        product_id = query.data.replace("buy_", "")
        product = PRODUCTS[product_id]

        upi_link = (
            f"upi://pay?"
            f"pa={quote(UPI_ID)}&"
            f"pn={quote(UPI_NAME)}&"
            f"am={product['price']}&"
            f"cu=INR"
        )

        keyboard = [
            [InlineKeyboardButton(
                f"💳 Pay ₹{product['price']} via UPI",
                url=upi_link
            )],
            [InlineKeyboardButton(
                "✅ I've Paid",
                callback_data=f"paid_{product_id}"
            )],
            [InlineKeyboardButton(
                "🔙 Products",
                callback_data="products"
            )],
        ]

        await query.edit_message_text(
            f"🧾 *ORDER DETAILS*\n\n"
            f"📦 Product: {product['name']}\n"
            f"💰 Amount: ₹{product['price']}\n\n"
            "1️⃣ Tap *Pay via UPI*\n"
            "2️⃣ Complete the payment\n"
            "3️⃣ Tap *I've Paid*\n\n"
            "⚠️ Your payment will be manually verified.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data.startswith("paid_"):
        product_id = query.data.replace("paid_", "")
        product = PRODUCTS[product_id]

        context.user_data["pending_product"] = product_id

        await query.edit_message_text(
            f"✅ *Payment submitted for {product['name']}*\n\n"
            "Please send your UPI transaction/reference number (UTR).\n\n"
            "Example: `123456789012`",
            parse_mode="Markdown",
        )

    elif query.data == "orders":
        await query.edit_message_text(
            "📦 *My Orders*\n\nNo orders yet.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ]),
        )

    elif query.data == "balance":
        await query.edit_message_text(
            "💰 *Balance*\n\nYour balance: ₹0",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ]),
        )

    elif query.data == "support":
        await query.edit_message_text(
            "📞 *Support*\n\n"
            "Contact the WANTED STORE administrator.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ]),
        )

    elif query.data == "back":
        await query.edit_message_text(
            "🔥 *WELCOME TO WANTED STORE* 🔥\n\n"
            "Choose an option:",
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )


async def receive_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "pending_product" not in context.user_data:
        return

    product_id = context.user_data["pending_product"]
    product = PRODUCTS[product_id]
    utr = update.message.text.strip()

    await update.message.reply_text(
        "⏳ *Payment submitted for verification.*\n\n"
        f"📦 Product: {product['name']}\n"
        f"💰 Amount: ₹{product['price']}\n"
        f"🧾 UTR: `{utr}`\n\n"
        "Please wait while the payment is verified.",
        parse_mode="Markdown",
    )

    # The UTR is currently only collected.
    # You will manually verify the payment before delivering the key.
    context.user_data.pop("pending_product", None)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing.")

    if not RENDER_URL:
        raise RuntimeError("RENDER_EXTERNAL_URL is missing.")

    if not UPI_ID:
        raise RuntimeError("UPI_ID is missing.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receive_utr)
    )

    webhook_url = f"{RENDER_URL}/telegram"

    print(f"Starting WANTED STORE on port {PORT}")
    print(f"Webhook: {webhook_url}")

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=webhook_url,
    )


if __name__ == "__main__":
    main()
