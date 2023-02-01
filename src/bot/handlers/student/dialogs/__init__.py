from aiogram_dialog import DialogRegistry


from src.bot.handlers.student.dialogs import profile


def setup(registry: DialogRegistry):
    registry.register(profile.dialog)
