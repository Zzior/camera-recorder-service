from aiogram import Dispatcher

from .routers import routers
from .middlewares.check_permission import AdminChecker

from configuration import conf


def get_dispatcher() -> Dispatcher:
    """This function set up dispatcher with routers, filters and middlewares."""
    dp = Dispatcher()
    for router in routers:
        dp.include_router(router)

    # Register middlewares
    dp.message.middleware(AdminChecker(conf.configurator.admins.values()))

    return dp
