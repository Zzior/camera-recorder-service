"""This file represent startup bot routers."""
import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from src.bot.dispatcher import get_dispatcher
from src.configuration import conf
from src.const.logs_strings import TASK_ERROR_LOG


async def start_bot():
    """This function will start bot with polling mode."""
    bot = Bot(token=conf.token, default=DefaultBotProperties(parse_mode="HTML"))
    await bot.delete_webhook(drop_pending_updates=True)

    # ================================ Config notifications =============================
    conf.notify_manager.configurate(bot=bot, loger=conf.logger)
    conf.cameras_manager.configurate_notifier(notify_manager=conf.notify_manager, logger=conf.logger)
    conf.record_manager.configurate_notifier(notify_manager=conf.notify_manager, logger=conf.logger)
    conf.file_manager.configurate_notifier(notify_manager=conf.notify_manager, logger=conf.logger)

    record_watcher = asyncio.create_task(conf.record_manager.process_watcher())
    camera_watcher = asyncio.create_task(conf.cameras_manager.status_checker())
    schedule_task = asyncio.create_task(conf.schedule_manager.schedule_task())
    file_manager = asyncio.create_task(conf.file_manager.file_task())

    for admin in conf.configurator.admins.values():
        for event_name in conf.notify_manager.events.keys():
            conf.notify_manager.subscribe(event_name=event_name, tg_id=admin)
    # ===================================================================================

    # DP
    dp = get_dispatcher()
    await dp.start_polling(bot)
    for task in (record_watcher, camera_watcher, schedule_task, file_manager):
        try:
            task.cancel()
        except Exception as e:
            conf.logger.error(TASK_ERROR_LOG.format(e=e))

if __name__ == '__main__':
    asyncio.run(start_bot())
