"""This package is used for a bot routers implementation."""
from .commands import commands_router
from .admin_menu import admin_router
from .other_routers import other_routers
routers = (commands_router, admin_router, other_routers)
