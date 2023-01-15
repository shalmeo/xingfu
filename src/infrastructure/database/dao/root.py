# from uuid import UUID
#
# from sqlalchemy import select, func, update, delete
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import joinedload, contains_eager, selectinload
#
# from src.domain.root import dto
# from src.domain.root.dto.group import Teacher
# from src.domain.root.interfaces.persistense import IRootDAO
# from src.application.common.exceptions.common import AlreadyExists, NotFound
# from src.domain.user.models.user import UserRole
# from src.infrastructure.database import models
# from src.infrastructure.database.dao.dao import SQLAlchemyDAO
#
#
# class RootDAO(SQLAlchemyDAO, IRootDAO):
#     async def add_user(self, user_create: dto.UserCreate) -> dto.User:
#         user = models.User(
#             telegram_id=user_create.telegram_id,
#             telegram_username=user_create.telegram_username,
#             name=user_create.name,
#             surname=user_create.surname,
#             patronymic=user_create.patronymic,
#             birthday=user_create.birthday,
#             email=user_create.email,
#             phone=user_create.phone,
#             timezone=user_create.timezone,
#             role=user_create.role,
#         )
#         try:
#             self.session.add(user)
#             await self.session.flush()
#             return dto.User(id=user.id)
#         except IntegrityError as err:
#             if "uq_users_email" in str(err):
#                 raise AlreadyExists(
#                     f"User with email={user_create.email} already exists"
#                 ) from err
#             if "uq_users_phone" in str(err):
#                 raise AlreadyExists(
#                     f"User with phone={user_create.phone} already exists"
#                 ) from err
#             if "uq_users_telegram_id" in str(err):
#                 raise AlreadyExists(
#                     f"User with telegram_id={user_create.telegram_id} already exists"
#                 )
#             if "uq_users_telegram_username" in str(err):
#                 raise AlreadyExists(
#                     f"User with telegram_username={user_create.telegram_username} already exists"
#                 )
#             if "uq_users_telegram_username" in str(err):
#                 raise AlreadyExists(
#                     f"User with telegram_username={user_create.telegram_username} already exists"
#                 )
#
#     async def update_user_role(self, user_id: int, role: UserRole) -> None:
#         await self.session.execute(
#             update(models.User).where(models.User.id == user_id).values(role=role)
#         )
#
#     async def get_paginate_admins(
#         self, offset: int, limit: int
#     ) -> list[dto.PaginateAdmin]:
#         admins = await self.session.scalars(
#             select(models.Admin)
#             .join(models.User)
#             .where(models.User.role == UserRole.ADMIN)
#             .order_by(models.Admin.created_at.desc())
#             .offset(offset)
#             .limit(limit)
#             .options(contains_eager(models.Admin.user))
#         )
#
#         return [
#             dto.PaginateAdmin(
#                 id=admin.id,
#                 name=admin.user.name,
#                 surname=admin.user.surname,
#             )
#             for admin in admins
#         ]
#
#     async def get_count_admins(self) -> int:
#         return await self.session.scalar(
#             select(func.count(models.Admin.id))
#             .join(models.User)
#             .where(models.User.role == UserRole.ADMIN)
#         )
#
#     async def get_admin(self, admin_id) -> dto.AdminInfo:
#         admin: models.Admin = await self.session.scalar(
#             select(models.Admin)
#             .where(models.Admin.id == admin_id)
#             .options(joinedload(models.Admin.user))
#         )
#
#         if admin is None:
#             raise NotFound(f"Admin with id={admin_id} not found in database")
#
#         return dto.AdminInfo(
#             id=admin.id,
#             user=dto.UserInfo(
#                 id=admin.user.id,
#                 name=admin.user.name,
#                 surname=admin.user.surname,
#                 patronymic=admin.user.patronymic,
#                 telegram_id=admin.user.telegram_id,
#                 telegram_username=admin.user.telegram_username,
#                 birthday=admin.user.birthday,
#                 email=admin.user.email,
#                 phone=admin.user.phone,
#                 timezone=admin.user.timezone,
#                 access_start=admin.user.access_start,
#                 access_end=admin.user.access_end,
#             ),
#             level=admin.level,
#             description=admin.description,
#             animal=admin.animal.name if admin.animal else None,
#             created_at=admin.created_at,
#         )
#
#     async def get_admins(self) -> list[dto.ExcelAdmin]:
#         admins = await self.session.scalars(
#             select(models.Admin)
#             .join(models.User)
#             .where(models.User.role == UserRole.ADMIN)
#             .order_by(models.Admin.created_at.asc())
#             .options(contains_eager(models.Admin.user))
#         )
#         return [
#             dto.ExcelAdmin(
#                 id=admin.id,
#                 user=dto.UserInfo(
#                     id=admin.user.id,
#                     name=admin.user.name,
#                     surname=admin.user.surname,
#                     patronymic=admin.user.patronymic,
#                     telegram_id=admin.user.telegram_id,
#                     telegram_username=admin.user.telegram_username,
#                     birthday=admin.user.birthday,
#                     email=admin.user.email,
#                     phone=admin.user.phone,
#                     timezone=admin.user.timezone,
#                     access_start=admin.user.access_start,
#                     access_end=admin.user.access_end,
#                 ),
#                 level=admin.level,
#                 description=admin.description,
#                 animal=admin.animal.name if admin.animal else None,
#                 created_at=admin.created_at,
#             )
#             for admin in admins
#         ]
#
#     async def add_admin(self, user_id: int, admin_create: dto.AdminCreate) -> dto.Admin:
#         admin = models.Admin(
#             user_id=user_id,
#             level=admin_create.level,
#             description=admin_create.description,
#         )
#         self.session.add(admin)
#         await self.session.flush()
#         return dto.Admin(id=admin.id)
#
#     async def delete_admin(self, admin_id: UUID) -> None:
#         admin: models.Admin = await self.session.get(
#             models.Admin, admin_id, options=[joinedload(models.Admin.user)]
#         )
#         admin.user.role = UserRole.UNCERTAIN
#         await self.session.delete(admin)
#         await self.session.flush()
#
#     async def update_admin(self, admin_update: dto.AdminUpdate):
#         admin: models.Admin = await self.session.get(
#             models.Admin, admin_update.id, options=[joinedload(models.Admin.user)]
#         )
#         if admin is None:
#             raise NotFound(f"Admin with id={admin_update.id} not found in database")
#
#         admin.level = admin_update.level
#         admin.description = admin_update.description
#
#         admin.user.name = admin_update.name
#         admin.user.surname = admin_update.surname
#         admin.user.patronymic = admin_update.patronymic
#         admin.user.telegram_id = admin_update.telegram_id
#         admin.user.telegram_username = admin_update.telegram_username
#         admin.user.email = admin_update.email
#         admin.user.phone = admin_update.phone
#         admin.user.timezone = admin_update.timezone
#         admin.user.birthday = admin_update.birthday
#         admin.user.access_start = admin_update.access_start
#         admin.user.access_end = admin_update.access_end
#
#         try:
#             await self.session.flush()
#         except IntegrityError as err:
#             if "uq_users_email" in str(err):
#                 raise AlreadyExists(
#                     f"User with email={admin_update.email} already exists"
#                 ) from err
#             if "uq_users_phone" in str(err):
#                 raise AlreadyExists(
#                     f"User with phone={admin_update.phone} already exists"
#                 ) from err
#             if "uq_users_telegram_id" in str(err):
#                 raise AlreadyExists(
#                     f"User with telegram_id={admin_update.telegram_id} already exists"
#                 )
#             if "uq_users_telegram_username" in str(err):
#                 raise AlreadyExists(
#                     f"User with telegram_username={admin_update.telegram_username} already exists"
#                 )
#
#     async def get_count_teachers(self) -> int:
#         return await self.session.scalar(select(func.count(models.Teacher.id)))
#
#     async def get_paginate_teachers(
#         self, offset: int, limit: int
#     ) -> list[dto.PaginateTeacher]:
#         teachers = await self.session.scalars(
#             select(models.Teacher)
#             .order_by(models.Teacher.created_at.desc())
#             .offset(offset)
#             .limit(limit)
#             .options(joinedload(models.Teacher.user))
#         )
#
#         return [
#             dto.PaginateTeacher(
#                 id=teacher.id,
#                 name=teacher.user.name,
#                 surname=teacher.user.surname,
#             )
#             for teacher in teachers
#         ]
#
#     async def get_teacher(self, teacher_id) -> dto.TeacherInfo:
#         teacher: models.Teacher = await self.session.scalar(
#             select(models.Teacher)
#             .where(models.Teacher.id == teacher_id)
#             .options(joinedload(models.Teacher.user))
#         )
#
#         if teacher is None:
#             raise NotFound(f"Teacher with id={teacher_id} not found in database")
#
#         return dto.TeacherInfo(
#             id=teacher.id,
#             user=dto.UserInfo(
#                 id=teacher.user.id,
#                 name=teacher.user.name,
#                 surname=teacher.user.surname,
#                 patronymic=teacher.user.patronymic,
#                 telegram_id=teacher.user.telegram_id,
#                 telegram_username=teacher.user.telegram_username,
#                 birthday=teacher.user.birthday,
#                 email=teacher.user.email,
#                 phone=teacher.user.phone,
#                 timezone=teacher.user.timezone,
#                 access_start=teacher.user.access_start,
#                 access_end=teacher.user.access_end,
#             ),
#             level=teacher.level,
#             description=teacher.description,
#             animal=teacher.animal.name if teacher.animal else None,
#             created_at=teacher.created_at,
#         )
#
#     async def get_teacher_by_user_id(self, user_id: int) -> dto.Teacher:
#         teacher = await self.session.scalar(
#             select(models.Teacher).join(models.User).where(models.User.id == user_id)
#         )
#
#         if teacher is None:
#             raise NotFound(f"Teacher with user_id={user_id} not found in database")
#
#         return dto.Teacher(id=teacher.id)
#
#     async def get_teachers(self) -> list[dto.TeacherInfo]:
#         teachers = await self.session.scalars(
#             select(models.Teacher)
#             .order_by(models.Teacher.created_at.desc())
#             .options(joinedload(models.Teacher.user))
#         )
#
#         return [
#             dto.TeacherInfo(
#                 id=teacher.id,
#                 user=dto.UserInfo(
#                     id=teacher.user.id,
#                     name=teacher.user.name,
#                     surname=teacher.user.surname,
#                     patronymic=teacher.user.patronymic,
#                     telegram_id=teacher.user.telegram_id,
#                     telegram_username=teacher.user.telegram_username,
#                     birthday=teacher.user.birthday,
#                     email=teacher.user.email,
#                     phone=teacher.user.phone,
#                     timezone=teacher.user.timezone,
#                     access_start=teacher.user.access_start,
#                     access_end=teacher.user.access_end,
#                 ),
#                 level=teacher.level,
#                 description=teacher.description,
#                 animal=teacher.animal.name if teacher.animal else None,
#                 created_at=teacher.created_at,
#             )
#             for teacher in teachers
#         ]
#
#     async def delete_teacher(self, teacher_id: UUID) -> None:
#         teacher: models.Teacher = await self.session.get(
#             models.Teacher, teacher_id, options=[joinedload(models.Teacher.user)]
#         )
#         teacher.user.role = UserRole.UNCERTAIN
#         await self.session.delete(teacher)
#         await self.session.flush()
#
#     async def get_excel_teachers(self) -> list[dto.ExcelTeacher]:
#         teachers = await self.session.scalars(
#             select(models.Teacher)
#             .order_by(models.Teacher.created_at.asc())
#             .options(
#                 joinedload(models.Teacher.user),
#                 joinedload(models.Teacher.animal),
#                 joinedload(models.Teacher.admin).joinedload(models.Admin.user),
#             )
#         )
#
#         return [
#             dto.ExcelTeacher(
#                 id=teacher.id,
#                 user=dto.UserInfo(
#                     id=teacher.user.id,
#                     name=teacher.user.name,
#                     surname=teacher.user.surname,
#                     patronymic=teacher.user.patronymic,
#                     telegram_id=teacher.user.telegram_id,
#                     telegram_username=teacher.user.telegram_username,
#                     birthday=teacher.user.birthday,
#                     email=teacher.user.email,
#                     phone=teacher.user.phone,
#                     timezone=teacher.user.timezone,
#                     access_start=teacher.user.access_start,
#                     access_end=teacher.user.access_end,
#                 ),
#                 level=teacher.level,
#                 description=teacher.description,
#                 animal=teacher.animal.name if teacher.animal else None,
#                 created_at=teacher.created_at,
#                 creator=dto.Creator(
#                     created_at=teacher.admin.created_at,
#                     user=dto.UserForUniqueCode(
#                         id=teacher.admin.user.id,
#                         telegram_id=teacher.admin.user.telegram_id,
#                         phone=teacher.admin.user.phone,
#                     ),
#                 ),
#             )
#             for teacher in teachers
#         ]
#
#     async def add_teacher(
#         self, user_id: int, teacher_create: dto.TeacherCreate
#     ) -> dto.Teacher:
#         teacher = models.Teacher(
#             user_id=user_id,
#             level=teacher_create.level,
#             description=teacher_create.description,
#         )
#         self.session.add(teacher)
#         await self.session.flush()
#         return dto.Teacher(id=teacher.id)
#
#     async def update_teacher(self, teacher_update: dto.TeacherUpdate) -> None:
#         teacher: models.Teacher = await self.session.get(
#             models.Teacher, teacher_update.id, options=[joinedload(models.Teacher.user)]
#         )
#         if teacher is None:
#             raise NotFound(f"Teacher with id={teacher_update.id} not found in database")
#
#         teacher.level = teacher_update.level
#         teacher.description = teacher_update.description
#
#         teacher.user.name = teacher_update.name
#         teacher.user.surname = teacher_update.surname
#         teacher.user.patronymic = teacher_update.patronymic
#         teacher.user.telegram_id = teacher_update.telegram_id
#         teacher.user.telegram_username = teacher_update.telegram_username
#         teacher.user.email = teacher_update.email
#         teacher.user.phone = teacher_update.phone
#         teacher.user.timezone = teacher_update.timezone
#         teacher.user.birthday = teacher_update.birthday
#         teacher.user.access_start = teacher_update.access_start
#         teacher.user.access_end = teacher_update.access_end
#
#         try:
#             await self.session.flush()
#         except IntegrityError as err:
#             if "uq_users_email" in str(err):
#                 raise AlreadyExists(
#                     f"User with email={teacher_update.email} already exists"
#                 ) from err
#             if "uq_users_phone" in str(err):
#                 raise AlreadyExists(
#                     f"User with phone={teacher_update.phone} already exists"
#                 ) from err
#             if "uq_users_telegram_id" in str(err):
#                 raise AlreadyExists(
#                     f"User with telegram_id={teacher_update.telegram_id} already exists"
#                 )
#             if "uq_users_telegram_username" in str(err):
#                 raise AlreadyExists(
#                     f"User with telegram_username={teacher_update.telegram_username} already exists"
#                 )
#
#     async def get_count_students(self) -> int:
#         return await self.session.scalar(select(func.count(models.Student.id)))
#
#     async def get_paginate_students(
#         self, offset: int, limit: int
#     ) -> list[dto.PaginateStudent]:
#         students = await self.session.scalars(
#             select(models.Student)
#             .order_by(models.Student.created_at.desc())
#             .offset(offset)
#             .limit(limit)
#             .options(joinedload(models.Student.user))
#         )
#
#         return [
#             dto.PaginateStudent(
#                 id=student.id,
#                 name=student.user.name,
#                 surname=student.user.surname,
#             )
#             for student in students
#         ]
#
#     async def get_student(self, student_id) -> dto.StudentInfo:
#         student: models.Student = await self.session.scalar(
#             select(models.Student)
#             .where(models.Student.id == student_id)
#             .options(joinedload(models.Student.user))
#         )
#
#         if student is None:
#             raise NotFound(f"Student with id={student_id} not found in database")
#
#         return dto.StudentInfo(
#             id=student.id,
#             user=dto.UserInfo(
#                 id=student.user.id,
#                 name=student.user.name,
#                 surname=student.user.surname,
#                 patronymic=student.user.patronymic,
#                 telegram_id=student.user.telegram_id,
#                 telegram_username=student.user.telegram_username,
#                 birthday=student.user.birthday,
#                 email=student.user.email,
#                 phone=student.user.phone,
#                 timezone=student.user.timezone,
#                 access_start=student.user.access_start,
#                 access_end=student.user.access_end,
#             ),
#             animal=student.animal.name if student.animal else None,
#             created_at=student.created_at,
#         )
#
#     async def get_student_by_user_id(self, user_id: int) -> dto.Student:
#         student = await self.session.scalar(
#             select(models.Student).join(models.User).where(models.User.id == user_id)
#         )
#
#         if student is None:
#             raise NotFound(f"Student with user_id={user_id} not found in database")
#
#         return dto.Student(id=student.id)
#
#     async def delete_student(self, student_id: UUID) -> None:
#         student: models.Student = await self.session.get(
#             models.Student, student_id, options=[joinedload(models.Student.user)]
#         )
#         student.user.role = UserRole.UNCERTAIN
#         await self.session.delete(student)
#         await self.session.flush()
#
#     async def get_students(self) -> list[dto.ExcelStudent]:
#         students = await self.session.scalars(
#             select(models.Student)
#             .order_by(models.Student.created_at.asc())
#             .options(
#                 joinedload(models.Student.user),
#                 joinedload(models.Student.animal),
#                 joinedload(models.Student.admin).joinedload(models.Admin.user),
#             )
#         )
#
#         return [
#             dto.ExcelStudent(
#                 id=student.id,
#                 user=dto.UserInfo(
#                     id=student.user.id,
#                     name=student.user.name,
#                     surname=student.user.surname,
#                     patronymic=student.user.patronymic,
#                     telegram_id=student.user.telegram_id,
#                     telegram_username=student.user.telegram_username,
#                     birthday=student.user.birthday,
#                     email=student.user.email,
#                     phone=student.user.phone,
#                     timezone=student.user.timezone,
#                     access_start=student.user.access_start,
#                     access_end=student.user.access_end,
#                 ),
#                 animal=student.animal.name if student.animal else None,
#                 created_at=student.created_at,
#                 creator=dto.Creator(
#                     created_at=student.admin.created_at,
#                     user=dto.UserForUniqueCode(
#                         id=student.admin.user.id,
#                         telegram_id=student.admin.user.telegram_id,
#                         phone=student.admin.user.phone,
#                     ),
#                 ),
#             )
#             for student in students
#         ]
#
#     async def add_student(
#         self, user_id: int, student_create: dto.StudentCreate
#     ) -> dto.Student:
#         student = models.Student(user_id=user_id)
#         self.session.add(student)
#         await self.session.flush()
#         return dto.Student(id=student.id)
#
#     async def update_student(self, student_update: dto.StudentUpdate) -> None:
#         student: models.Student = await self.session.get(
#             models.Student, student_update.id, options=[joinedload(models.Student.user)]
#         )
#         if student is None:
#             raise NotFound(f"Student with id={student_update.id} not found in database")
#
#         student.user.name = student_update.name
#         student.user.surname = student_update.surname
#         student.user.patronymic = student_update.patronymic
#         student.user.telegram_id = student_update.telegram_id
#         student.user.telegram_username = student_update.telegram_username
#         student.user.email = student_update.email
#         student.user.phone = student_update.phone
#         student.user.timezone = student_update.timezone
#         student.user.birthday = student_update.birthday
#         student.user.access_start = student_update.access_start
#         student.user.access_end = student_update.access_end
#
#         try:
#             await self.session.flush()
#         except IntegrityError as err:
#             if "uq_users_email" in str(err):
#                 raise AlreadyExists(
#                     f"User with email={student_update.email} already exists"
#                 ) from err
#             if "uq_users_phone" in str(err):
#                 raise AlreadyExists(
#                     f"User with phone={student_update.phone} already exists"
#                 ) from err
#             if "uq_users_telegram_id" in str(err):
#                 raise AlreadyExists(
#                     f"User with telegram_id={student_update.telegram_id} already exists"
#                 )
#             if "uq_users_telegram_username" in str(err):
#                 raise AlreadyExists(
#                     f"User with telegram_username={student_update.telegram_username} already exists"
#                 )
#
#     async def get_count_groups(self) -> int:
#         return await self.session.scalar(select(func.count(models.Group.id)))
#
#     async def get_paginate_groups(
#         self, offset: int, limit: int
#     ) -> list[dto.PaginateGroup]:
#         groups = await self.session.scalars(
#             select(models.Group)
#             .order_by(models.Group.created_at.desc(), models.Group.name.desc())
#             .offset(offset)
#             .limit(limit)
#         )
#
#         return [dto.PaginateGroup(id=group.id, name=group.name) for group in groups]
#
#     async def get_group(self, group_id: UUID) -> dto.GroupInfo:
#         group: models.Group = await self.session.get(
#             models.Group,
#             group_id,
#             options=[joinedload(models.Group.teacher).joinedload(models.Teacher.user)],
#         )
#         if group is None:
#             raise NotFound(f"Group with id={group_id} not found in database")
#
#         return dto.GroupInfo(
#             id=group.id,
#             name=group.name,
#             description=group.description,
#             teacher=Teacher(
#                 id=group.teacher.id,
#                 name=group.teacher.user.name,
#                 surname=group.teacher.user.surname,
#                 patronymic=group.teacher.user.patronymic,
#             )
#             if group.teacher
#             else None,
#         )
#
#     async def delete_group(self, group_id: UUID) -> None:
#         group: models.Group = await self.session.get(models.Group, group_id)
#         await self.session.delete(group)
#
#     async def get_count_tasks(self, group_id: UUID) -> int:
#         return await self.session.scalar(
#             select(func.count(models.Task.id)).where(models.Task.group_id == group_id)
#         )
#
#     async def get_paginate_tasks(
#         self, group_id: UUID, offset: int, limit: int
#     ) -> list[dto.PaginateTask]:
#         tasks = await self.session.scalars(
#             select(models.Task)
#             .where(models.Task.group_id == group_id)
#             .order_by(models.Task.created_at.desc())
#             .offset(offset)
#             .limit(limit)
#         )
#
#         return [dto.PaginateTask(id=task.id, title=task.title) for task in tasks]
#
#     async def get_task(self, task_id: UUID) -> dto.TaskInfo:
#         task = await self.session.get(
#             models.Task, task_id, options=[joinedload(models.Task.group)]
#         )
#
#         return dto.TaskInfo(
#             id=task.id,
#             title=task.title,
#             lesson_date=task.lesson_date,
#             deadline=task.deadline,
#             description=task.description,
#             group_id=task.group.id,
#         )
#
#     async def get_count_students_in_group(self, group_id: UUID) -> int:
#         return await self.session.scalar(
#             select(func.count(models.StudentGroupAssociation.id)).where(
#                 models.StudentGroupAssociation.group_id == group_id
#             )
#         )
#
#     async def get_paginate_students_in_group(
#         self, group_id: UUID, offset: int, limit: int
#     ) -> list[dto.PaginateStudentInGroup]:
#         students = await self.session.scalars(
#             select(models.Student)
#             .join(models.StudentGroupAssociation)
#             .where(models.StudentGroupAssociation.group_id == group_id)
#             .order_by(models.Student.created_at.desc())
#             .offset(offset)
#             .limit(limit)
#             .options(joinedload(models.Student.user))
#         )
#
#         return [
#             dto.PaginateStudentInGroup(
#                 id=student.id, name=student.user.name, surname=student.user.surname
#             )
#             for student in students
#         ]
#
#     async def add_group(self, group_create: dto.GroupCreate) -> dto.Group:
#         group = models.Group(
#             name=group_create.name,
#             description=group_create.description,
#             teacher_id=group_create.teacher_id,
#         )
#         try:
#             self.session.add(group)
#             await self.session.flush()
#             return dto.Group(id=group.id)
#         except IntegrityError as err:
#             if "fk_groups_teacher_id_teachers" in str(err):
#                 raise NotFound(
#                     f"Teacher with id={group_create.teacher_id} not found in database"
#                 )
#             if "uq_groups_name" in str(err):
#                 raise AlreadyExists(
#                     f"Group with name={group_create.name} already exists"
#                 )
#
#     async def update_group(self, group_update: dto.GroupUpdate) -> None:
#         group: models.Group = await self.session.get(models.Group, group_update.id)
#         if group is None:
#             raise NotFound(f"Group with id={group_update.id} not found in database")
#
#         group.name = group_update.name
#         group.description = group_update.description
#         group.teacher_id = group_update.teacher_id
#
#         try:
#             await self.session.flush()
#         except IntegrityError as err:
#             if "fk_groups_teacher_id_teachers" in str(err):
#                 raise NotFound(
#                     f"Teacher with id={group_update.teacher_id} not found in database"
#                 )
#             if "uq_groups_name" in str(err):
#                 raise AlreadyExists(
#                     f"Group with name={group_update.name} already exists"
#                 )
#
#     async def get_excel_groups(self) -> list[dto.ExcelGroup]:
#         groups = await self.session.scalars(
#             select(models.Group).options(
#                 joinedload(models.Group.admin).joinedload(models.Admin.user),
#                 joinedload(models.Group.teacher).joinedload(models.Teacher.user),
#                 selectinload(models.Group.students).joinedload(models.Student.user),
#             )
#         )
#
#         return [
#             dto.ExcelGroup(
#                 id=group.id,
#                 name=group.name,
#                 description=group.description,
#                 creator=dto.Creator(
#                     created_at=group.admin.created_at,
#                     user=dto.UserForUniqueCode(
#                         id=group.admin.user.id,
#                         telegram_id=group.admin.user.telegram_id,
#                         phone=group.admin.user.phone,
#                     ),
#                 ),
#                 teacher=dto.ExcelGroupTeacher(
#                     created_at=group.teacher.created_at,
#                     user=dto.UserForUniqueCode(
#                         id=group.teacher.user.id,
#                         telegram_id=group.teacher.user.telegram_id,
#                         phone=group.teacher.user.phone,
#                     ),
#                 )
#                 if group.teacher
#                 else None,
#                 students=[
#                     dto.ExcelGroupStudent(
#                         created_at=student.created_at,
#                         user=dto.UserForUniqueCode(
#                             id=student.user.id,
#                             telegram_id=student.user.telegram_id,
#                             phone=student.user.phone,
#                         ),
#                     )
#                     for student in group.students
#                 ],
#             )
#             for group in groups
#         ]
#
#     async def import_group(self, import_group: dto.ImportGroup) -> None:
#         students = []
#         for student_id in import_group.students:
#             student = await self.session.get(models.Student, student_id)
#             if student:
#                 students.append(student)
#
#         group = models.Group(
#             name=import_group.name,
#             description=import_group.description,
#             teacher_id=import_group.teacher_id,
#             students=students,
#         )
#
#         try:
#             self.session.add(group)
#             await self.session.flush()
#         except IntegrityError as err:
#             if "fk_groups_teacher_id_teachers" in str(err):
#                 raise NotFound(
#                     f"Teacher with id={import_group.teacher_id} not found in database"
#                 )
#             if "uq_groups_name" in str(err):
#                 raise AlreadyExists(
#                     f"Group with name={import_group.name} already exists"
#                 )
#
#     async def get_count_uncertains(self) -> int:
#         return await self.session.scalar(
#             select(func.count(models.User.id)).where(
#                 models.User.role == UserRole.UNCERTAIN
#             )
#         )
#
#     async def get_paginate_uncertains(
#         self, offset, limit
#     ) -> list[dto.PaginateUncertain]:
#         uncertains = await self.session.scalars(
#             select(models.User)
#             .where(models.User.role == UserRole.UNCERTAIN)
#             .order_by(models.User.created_at.desc())
#             .offset(offset)
#             .limit(limit)
#         )
#
#         return [
#             dto.PaginateUncertain(
#                 id=uncertain.id,
#                 name=uncertain.name,
#                 surname=uncertain.surname,
#             )
#             for uncertain in uncertains
#         ]
#
#     async def get_uncertain(self, uncertain_id: int) -> dto.UncertainInfo:
#         uncertain: models.User = await self.session.scalar(
#             select(models.User).where(models.User.id == uncertain_id)
#         )
#
#         if uncertain is None:
#             raise NotFound(f"Student with id={uncertain_id} not found in database")
#
#         return dto.UncertainInfo(
#             user=dto.UserInfo(
#                 id=uncertain.id,
#                 name=uncertain.name,
#                 surname=uncertain.surname,
#                 patronymic=uncertain.patronymic,
#                 telegram_id=uncertain.telegram_id,
#                 telegram_username=uncertain.telegram_username,
#                 birthday=uncertain.birthday,
#                 email=uncertain.email,
#                 phone=uncertain.phone,
#                 timezone=uncertain.timezone,
#                 access_start=uncertain.access_start,
#                 access_end=uncertain.access_end,
#             ),
#         )
#
#     async def delete_uncertain(self, uncertain_id: int) -> None:
#         await self.session.execute(
#             delete(models.User).where(models.User.id == uncertain_id)
#         )
