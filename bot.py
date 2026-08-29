import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", "10000"))
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

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
            [InlineKeyboardButton("BALA MODS — ₹100", callback_data="bala")],
            [InlineKeyboardButton("ABCD PANNEL — ₹99", callback_data="abcd")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")],
        ]

        await query.edit_message_text(
            "🛒 *WANTED STORE PRODUCTS*\n\nSelect a product:",
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
            [InlineKeyboardButton("🔙 Products", callback_data="products")],
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

        await query.edit_message_text(
            f"🧾 *ORDER DETAILS*\n\n"
            f"📦 Product: {product['name']}\n"
            f"💰 Amount: ₹{product['price']}\n\n"
            "💳 Payment system will be connected next.",
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
            "📞 *Support*\n\nContact the WANTED STORE administrator.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ]),
        )

    elif query.data == "back":
        await query.edit_message_text(
            "🔥 *WELCOME TO WANTED STORE* 🔥\n\nChoose an option:",
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing.")

    if not RENDER_URL:
        raise RuntimeError("RENDER_EXTERNAL_URL is missing.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

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
