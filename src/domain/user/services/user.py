from src.domain.user.models.user import User


def create_user(
    email: str,
    phone: int,
    timezone: str,
    role,
    telegram_id: int,
    telegram_username: str,
) -> User:
    return User(
        email=email,
        phone=phone,
        timezone=timezone,
        role=role,
        telegram_id=telegram_id,
        telegram_username=telegram_username,
    )


def update_user(
    user: User,
    email: str,
    phone: int,
    timezone: str,
    role,
    telegram_id: int,
    telegram_username: str,
) -> User:
    user.email = email
    user.phone = phone
    user.timezone = timezone
    user.role = role
    user.telegram_id = telegram_id
    user.telegram_username = telegram_username

    return user
