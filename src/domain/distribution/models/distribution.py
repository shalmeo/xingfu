from enum import Enum


class DistributionStatus(Enum):
    DURING = "DURING"
    FINISHED = "FINISHED"
    STOPPED = "STOPPED"


class DistributionRecordStatus(Enum):
    DURING = "DURING"
    DELIVERED = "DELIVERED"
    NOT_DELIVERED = "NOT_DELIVERED"


#
# bind = op.get_bind()
#     session = orm.Session(bind=bind)
#     settings = get_settings()
#
#     for i, admin_telegram_id in enumerate(settings.bot_admins, 1):
#         try:
#             user = models.User(
#                 name=f"Root{i}",
#                 surname=f"Administrator{i}",
#                 birthday=datetime.date.today(),
#                 telegram_id=admin_telegram_id,
#                 email=f"root{i}@email.com",
#                 role=UserRole.ROOT,
#             )
#             session.add(user)
#             session.flush()
#             admin = models.Admin(user_id=user.id)
#             session.add(admin)
#             session.flush()
#         except IntegrityError:
#             session.rollback()
#
#     session.commit()
