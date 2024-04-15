"""This file represent startup bot routers."""
import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from src.bot.dispatcher import get_dispatcher
from src.configuration import conf


async def start_bot():
    """This function will start bot with polling mode."""
    bot = Bot(token=conf.token, default=DefaultBotProperties(parse_mode="HTML"))
    await bot.delete_webhook(drop_pending_updates=True)

    # ================================ Config notifications =============================
    conf.notify_manager.configurate(bot=bot, loger=conf.logger)
    conf.cameras_manager.configurate_notifier(notify_manager=conf.notify_manager, logger=conf.logger)
    conf.record_manager.configurate_notifier(notify_manager=conf.notify_manager, logger=conf.logger)

    watcher = asyncio.create_task(conf.record_manager.process_watcher())

    for admin in conf.configurator.admins.values():
        conf.notify_manager.subscribe(event_name=conf.record_manager.notify_name, tg_id=admin)
    # ===================================================================================

    # DP
    dp = get_dispatcher()
    await dp.start_polling(bot)
    try:
        watcher.cancel()
    except asyncio.CancelledError:
        pass

if __name__ == '__main__':
    asyncio.run(start_bot())