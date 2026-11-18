import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

rounds = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "WELCOME TO DIBIA AVIATOR 5X SIGNALS!\n\n"
        "Commands:\n"
        "/record 5.20 - Record a multiplier\n"
        "/stats - View statistics\n"
        "/last - View last recorded rounds\n"
        "/help - Show commands\n\n"
        "Note: These are statistical observations, "
        "not predictions of future rounds."
    )

async def record(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])

        if value < 1:
            raise ValueError

        rounds.append(value)

        message = f"Recorded multiplier: {value:.2f}x"

        if value >= 5:
            message += "\nThis round reached 5x or above!"

        await update.message.reply_text(message)

    except (IndexError, ValueError):
        await update.message.reply_text(
            "Use this format: /record 5.20"
        )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not rounds:
        await update.message.reply_text("No rounds recorded yet.")
        return

    total = len(rounds)
    five = sum(x >= 5 for x in rounds)
    percentage = five / total * 100

    await update.message.reply_text(
        f"AVIATOR STATISTICS\n\n"
        f"Rounds recorded: {total}\n"
        f"Rounds reaching 5x+: {five}\n"
        f"Observed 5x frequency: {percentage:.1f}%\n\n"
        "Past results do not predict future rounds."
    )

async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not rounds:
        await update.message.reply_text("No rounds recorded.")
        return

    recent = rounds[-10:]
    result = "\n".join(f"{x:.2f}x" for x in reversed(recent))

    await update.message.reply_text(
        "LAST RECORDED ROUNDS:\n\n" + result
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

def main():
    if not TOKEN:
        raise RuntimeError("Telegram token is missing.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("record", record))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("last", last))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling()

if __name__ == "__main__":
    main()
