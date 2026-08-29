import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

PRODUCTS = {
    "bala": {"name": "BALA MODS", "price": 100},
    "abcd": {"name": "ABCD PANNEL", "price": 99},
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Products", callback_data="products")],
        [InlineKeyboardButton("📦 My Orders", callback_data="orders")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("📞 Support", callback_data="support")],
    ]

    await update.message.reply_text(
        "🔥 *WELCOME TO WANTED STORE* 🔥\n\n"
        "Choose an option below:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
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
            [
                InlineKeyboardButton(
                    f"💳 Buy — ₹{product['price']}",
                    callback_data=f"buy_{query.data}",
                )
            ],
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
            "💳 Payment system will be connected in the next step.",
            parse_mode="Markdown",
        )

    elif query.data == "orders":
        await query.edit_message_text(
            "📦 *My Orders*\n\nNo orders yet.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
            ),
        )

    elif query.data == "balance":
        await query.edit_message_text(
            "💰 *Balance*\n\nYour balance: ₹0",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
            ),
        )

    elif query.data == "support":
        await query.edit_message_text(
            "📞 *Support*\n\nContact the WANTED STORE administrator.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
            ),
        )

    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("🛒 Products", callback_data="products")],
            [InlineKeyboardButton("📦 My Orders", callback_data="orders")],
            [InlineKeyboardButton("💰 Balance", callback_data="balance")],
            [InlineKeyboardButton("📞 Support", callback_data="support")],
        ]

        await query.edit_message_text(
            "🔥 *WELCOME TO WANTED STORE* 🔥\n\nChoose an option:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("WANTED STORE bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
