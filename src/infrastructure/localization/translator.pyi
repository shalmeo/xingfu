from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    start: Start
    attached: Attached
    sticker: Sticker
    root: Root
    web: Web
    excel: Excel
    undefined: Undefined

    @staticmethod
    def back() -> Literal["""Назад"""]: ...

    @staticmethod
    def change() -> Literal["""Изменить"""]: ...

    @staticmethod
    def delete() -> Literal["""Удалить"""]: ...

    @staticmethod
    def upload() -> Literal["""Загрузить"""]: ...

    @staticmethod
    def accept() -> Literal["""Принять"""]: ...

    @staticmethod
    def reject() -> Literal["""Отколонить"""]: ...

    @staticmethod
    def teacher() -> Literal["""Учитель"""]: ...

    @staticmethod
    def student() -> Literal["""Ученик"""]: ...


class Start:
    @staticmethod
    def welcome() -> Literal["""Добро пожаловать"""]: ...


class Attached:
    @staticmethod
    def files() -> Literal["""Прикрепленные файлы"""]: ...


class Sticker:
    @staticmethod
    def welcome() -> Literal["""CAACAgIAAxkBAAEFdNli6oLvpMhSOdgE_Np34piuMhiy1QACaBkAAk5sEEtWX12hX9vgyikE"""]: ...


class Root:
    profile: RootProfile


class RootProfile:
    registry: RootProfileRegistry
    distriburions: RootProfileDistriburions

    @staticmethod
    def button() -> Literal["""Профиль"""]: ...

    @staticmethod
    def text() -> Literal["""Профиль супер-администратора"""]: ...


class RootProfileRegistry:
    admins: RootProfileRegistryAdmins
    admin: RootProfileRegistryAdmin
    teachers: RootProfileRegistryTeachers
    teacher: RootProfileRegistryTeacher
    students: RootProfileRegistryStudents
    student: RootProfileRegistryStudent
    groups: RootProfileRegistryGroups
    group: RootProfileRegistryGroup
    undefineds: RootProfileRegistryUndefineds
    undefined: RootProfileRegistryUndefined
    user: RootProfileRegistryUser


class RootProfileRegistryAdmins:
    @staticmethod
    def button() -> Literal["""Реестр администраторов"""]: ...

    @staticmethod
    def text() -> Literal["""Реестр администраторов"""]: ...


class RootProfileRegistryAdmin:
    @staticmethod
    def button(*, surname, name) -> Literal["""{ $surname } { $name }"""]: ...

    @staticmethod
    def info(*, surname, name, patronymic, phone, email, telegram_id, username, birthday, level, description, access_start, access_end, timezone) -> Literal["""&lt;b&gt;Администратор&lt;/b&gt;

&lt;b&gt;Фамилия:&lt;/b&gt; &lt;code&gt;{ $surname }&lt;/code&gt;
&lt;b&gt;Имя:&lt;/b&gt; &lt;code&gt;{ $name }&lt;/code&gt;
&lt;b&gt;Отчество:&lt;/b&gt; &lt;code&gt;{ $patronymic }&lt;/code&gt;
&lt;b&gt;Телефон:&lt;/b&gt; &lt;code&gt;{ $phone }&lt;/code&gt;
&lt;b&gt;Почта:&lt;/b&gt; &lt;code&gt;{ $email }&lt;/code&gt;
&lt;b&gt;Телеграм ID:&lt;/b&gt; &lt;code&gt;{ $telegram_id }&lt;/code&gt;
&lt;b&gt;Имя пользователя:&lt;/b&gt; &lt;code&gt;{ $username }&lt;/code&gt;
&lt;b&gt;Дата рождения:&lt;/b&gt; &lt;code&gt;{ $birthday }&lt;/code&gt;

&lt;b&gt;Уровень подготовки:&lt;/b&gt; &lt;code&gt;{ $level }&lt;/code&gt;
&lt;b&gt;Дополнительное описание:&lt;/b&gt;
&lt;code&gt;{ $description }&lt;/code&gt;

&lt;b&gt;Запись активна с:&lt;/b&gt; &lt;code&gt;{ $access_start }&lt;/code&gt;
&lt;b&gt;Запись пассивна с:&lt;/b&gt; &lt;code&gt;{ $access_end }&lt;/code&gt;
&lt;b&gt;Часовой пояс:&lt;/b&gt; &lt;code&gt;{ $timezone }&lt;/code&gt;"""]: ...


class RootProfileRegistryTeachers:
    @staticmethod
    def button() -> Literal["""Реестр учителей"""]: ...

    @staticmethod
    def text() -> Literal["""Реестр учителей"""]: ...


class RootProfileRegistryTeacher:
    @staticmethod
    def button(*, surname, name) -> Literal["""{ $surname } { $name }"""]: ...

    @staticmethod
    def info(*, surname, name, patronymic, phone, email, telegram_id, username, birthday, level, description, access_start, access_end, timezone) -> Literal["""&lt;b&gt;Учитель&lt;/b&gt;

&lt;b&gt;Фамилия:&lt;/b&gt; &lt;code&gt;{ $surname }&lt;/code&gt;
&lt;b&gt;Имя:&lt;/b&gt; &lt;code&gt;{ $name }&lt;/code&gt;
&lt;b&gt;Отчество:&lt;/b&gt; &lt;code&gt;{ $patronymic }&lt;/code&gt;
&lt;b&gt;Телефон:&lt;/b&gt; &lt;code&gt;{ $phone }&lt;/code&gt;
&lt;b&gt;Почта:&lt;/b&gt; &lt;code&gt;{ $email }&lt;/code&gt;
&lt;b&gt;Телеграм ID:&lt;/b&gt; &lt;code&gt;{ $telegram_id }&lt;/code&gt;
&lt;b&gt;Имя пользователя:&lt;/b&gt; &lt;code&gt;{ $username }&lt;/code&gt;
&lt;b&gt;Дата рождения:&lt;/b&gt; &lt;code&gt;{ $birthday }&lt;/code&gt;

&lt;b&gt;Уровень подготовки:&lt;/b&gt; &lt;code&gt;{ $level }&lt;/code&gt;
&lt;b&gt;Дополнительное описание:&lt;/b&gt;
&lt;code&gt;{ $description }&lt;/code&gt;

&lt;b&gt;Запись активна с:&lt;/b&gt; &lt;code&gt;{ $access_start }&lt;/code&gt;
&lt;b&gt;Запись пассивна с:&lt;/b&gt; &lt;code&gt;{ $access_end }&lt;/code&gt;
&lt;b&gt;Часовой пояс:&lt;/b&gt; &lt;code&gt;{ $timezone }&lt;/code&gt;"""]: ...


class RootProfileRegistryStudents:
    @staticmethod
    def button() -> Literal["""Реестр учеников"""]: ...

    @staticmethod
    def text() -> Literal["""Реестр учеников"""]: ...


class RootProfileRegistryStudent:
    @staticmethod
    def button(*, surname, name) -> Literal["""{ $surname } { $name }"""]: ...

    @staticmethod
    def info(*, surname, name, patronymic, phone, email, telegram_id, username, birthday, access_start, access_end, timezone) -> Literal["""&lt;b&gt;Ученик&lt;/b&gt;

&lt;b&gt;Фамилия:&lt;/b&gt; &lt;code&gt;{ $surname }&lt;/code&gt;
&lt;b&gt;Имя:&lt;/b&gt; &lt;code&gt;{ $name }&lt;/code&gt;
&lt;b&gt;Отчество:&lt;/b&gt; &lt;code&gt;{ $patronymic }&lt;/code&gt;
&lt;b&gt;Телефон:&lt;/b&gt; &lt;code&gt;{ $phone }&lt;/code&gt;
&lt;b&gt;Почта:&lt;/b&gt; &lt;code&gt;{ $email }&lt;/code&gt;
&lt;b&gt;Телеграм ID:&lt;/b&gt; &lt;code&gt;{ $telegram_id }&lt;/code&gt;
&lt;b&gt;Имя пользователя:&lt;/b&gt; &lt;code&gt;{ $username }&lt;/code&gt;
&lt;b&gt;Дата рождения:&lt;/b&gt; &lt;code&gt;{ $birthday }&lt;/code&gt;

&lt;b&gt;Запись активна с:&lt;/b&gt; &lt;code&gt;{ $access_start }&lt;/code&gt;
&lt;b&gt;Запись пассивна с:&lt;/b&gt; &lt;code&gt;{ $access_end }&lt;/code&gt;
&lt;b&gt;Часовой пояс:&lt;/b&gt; &lt;code&gt;{ $timezone }&lt;/code&gt;"""]: ...


class RootProfileRegistryGroups:
    @staticmethod
    def button() -> Literal["""Реестр групп"""]: ...

    @staticmethod
    def text() -> Literal["""Реестр групп"""]: ...


class RootProfileRegistryGroup:
    tasks: RootProfileRegistryGroupTasks
    task: RootProfileRegistryGroupTask
    select: RootProfileRegistryGroupSelect
    successfully: RootProfileRegistryGroupSuccessfully

    @staticmethod
    def button(*, name) -> Literal["""{ $name }"""]: ...

    @staticmethod
    def info(*, name, teacher, description) -> Literal["""&lt;b&gt;Группа:&lt;/b&gt; &lt;code&gt;{ $name }&lt;/code&gt;

&lt;b&gt;Учитель:&lt;/b&gt; &lt;code&gt;{ $teacher }&lt;/code&gt;

&lt;b&gt;Описание:&lt;/b&gt;
&lt;code&gt;{ $description }&lt;/code&gt;"""]: ...


class RootProfileRegistryGroupTasks:
    @staticmethod
    def button() -> Literal["""Реестр Д/З"""]: ...


class RootProfileRegistryGroupTask:
    student: RootProfileRegistryGroupTaskStudent

    @staticmethod
    def button(*, title) -> Literal["""{ $title }"""]: ...

    @staticmethod
    def info(*, title, lesson_date, deadline, description) -> Literal["""&lt;b&gt;Домашнее задание&lt;/b&gt;: &lt;code&gt;{ $title }&lt;/code&gt;

&lt;b&gt;Дата проведенного урока:&lt;/b&gt; &lt;code&gt;{ $lesson_date }&lt;/code&gt;
&lt;b&gt;Крайняя дата сдачи Д/З:&lt;/b&gt; &lt;code&gt;{ $deadline }&lt;/code&gt;

&lt;b&gt;Описание по Д/З:&lt;/b&gt;
&lt;code&gt;{ $description }&lt;/code&gt;"""]: ...


class RootProfileRegistryGroupTaskStudent:
    @staticmethod
    def button(*, surname, name) -> Literal["""{ $surname } { $name }"""]: ...


class RootProfileRegistryGroupSelect:
    @staticmethod
    def task() -> Literal["""&lt;b&gt;Выберите задание&lt;/b&gt;"""]: ...

    @staticmethod
    def student() -> Literal["""&lt;b&gt;Выберите ученика&lt;/b&gt;"""]: ...


class RootProfileRegistryUndefineds:
    @staticmethod
    def button() -> Literal["""Неопределенные пользователи"""]: ...

    @staticmethod
    def text() -> Literal["""Реестр неопределенных пользователи"""]: ...


class RootProfileRegistryUndefined:
    select: RootProfileRegistryUndefinedSelect
    successfully: RootProfileRegistryUndefinedSuccessfully

    @staticmethod
    def button(*, surname, name) -> Literal["""{ $surname } { $name }"""]: ...

    @staticmethod
    def info(*, surname, name, patronymic, phone, email, telegram_id, username, birthday, timezone) -> Literal["""&lt;b&gt;Неопределенный пользователь&lt;/b&gt;

&lt;b&gt;Фамилия:&lt;/b&gt; &lt;code&gt;{ $surname }&lt;/code&gt;
&lt;b&gt;Имя:&lt;/b&gt; &lt;code&gt;{ $name }&lt;/code&gt;
&lt;b&gt;Отчество:&lt;/b&gt; &lt;code&gt;{ $patronymic }&lt;/code&gt;
&lt;b&gt;Телефон:&lt;/b&gt; &lt;code&gt;{ $phone }&lt;/code&gt;
&lt;b&gt;Почта:&lt;/b&gt; &lt;code&gt;{ $email }&lt;/code&gt;
&lt;b&gt;Телеграм ID:&lt;/b&gt; &lt;code&gt;{ $telegram_id }&lt;/code&gt;
&lt;b&gt;Имя пользователя:&lt;/b&gt; &lt;code&gt;{ $username }&lt;/code&gt;
&lt;b&gt;Дата рождения:&lt;/b&gt; &lt;code&gt;{ $birthday }&lt;/code&gt;

&lt;b&gt;Часовой пояс:&lt;/b&gt; &lt;code&gt;{ $timezone }&lt;/code&gt;"""]: ...


class RootProfileRegistryUndefinedSelect:
    @staticmethod
    def role() -> Literal["""&lt;b&gt;Выберите роль&lt;/b&gt;"""]: ...


class RootProfileDistriburions:
    @staticmethod
    def button() -> Literal["""Рассылки"""]: ...


class RootProfileRegistryUser:
    successfully: RootProfileRegistryUserSuccessfully


class RootProfileRegistryUserSuccessfully:
    @staticmethod
    def deleted() -> Literal["""Пользователь успешно удален и перемещен в реестр неопределенных пользователей"""]: ...


class RootProfileRegistryGroupSuccessfully:
    @staticmethod
    def deleted() -> Literal["""Группа успешна удалена"""]: ...


class RootProfileRegistryUndefinedSuccessfully:
    @staticmethod
    def added() -> Literal["""Пользователь успешно добавлен"""]: ...

    @staticmethod
    def rejected() -> Literal["""Пользователь успешно отклонен"""]: ...


class Web:
    create: WebCreate
    admin: WebAdmin
    teacher: WebTeacher
    student: WebStudent
    group: WebGroup
    undefined: WebUndefined


class WebCreate:
    record: WebCreateRecord


class WebCreateRecord:
    @staticmethod
    def button() -> Literal["""Создать запись"""]: ...


class WebAdmin:
    create: WebAdminCreate
    update: WebAdminUpdate


class WebAdminCreate:
    @staticmethod
    def url(*, base_url) -> Literal["""https://{ $base_url }/admin/create"""]: ...


class WebAdminUpdate:
    @staticmethod
    def url(*, base_url, id) -> Literal["""https://{ $base_url }/admin/update/{ $id }"""]: ...


class WebTeacher:
    create: WebTeacherCreate
    update: WebTeacherUpdate


class WebTeacherCreate:
    @staticmethod
    def url(*, base_url) -> Literal["""https://{ $base_url }/teacher/create"""]: ...


class WebTeacherUpdate:
    @staticmethod
    def url(*, base_url, id) -> Literal["""https://{ $base_url }/teacher/update/{ $id }"""]: ...


class WebStudent:
    create: WebStudentCreate
    update: WebStudentUpdate


class WebStudentCreate:
    @staticmethod
    def url(*, base_url) -> Literal["""https://{ $base_url }/student/create"""]: ...


class WebStudentUpdate:
    @staticmethod
    def url(*, base_url, id) -> Literal["""https://{ $base_url }/student/update/{ $id }"""]: ...


class WebGroup:
    create: WebGroupCreate
    update: WebGroupUpdate


class WebGroupCreate:
    @staticmethod
    def url(*, base_url) -> Literal["""https://{ $base_url }/group/create"""]: ...


class WebGroupUpdate:
    @staticmethod
    def url(*, base_url, id) -> Literal["""https://{ $base_url }/group/update/{ $id }"""]: ...


class WebUndefined:
    sign: WebUndefinedSign


class WebUndefinedSign:
    up: WebUndefinedSignUp


class WebUndefinedSignUp:
    @staticmethod
    def url(*, base_url, telegram_id, telegram_username) -> Literal["""https://{ $base_url }/undefined/sign-up?telegram_id={ $telegram_id }&amp;telegram_username={ $telegram_username }"""]: ...


class Excel:
    export: ExcelExport
    impor: ExcelImpor


class ExcelExport:
    @staticmethod
    def button() -> Literal["""Экспорт EXCEL"""]: ...


class ExcelImpor:
    detected: ExcelImporDetected
    upload: ExcelImporUpload

    @staticmethod
    def button() -> Literal["""Загрузить из EXCEL"""]: ...

    @staticmethod
    def text() -> Literal["""Пришлите сюда файл &lt;code&gt;*.excel&lt;/code&gt;"""]: ...


class ExcelImporDetected:
    records: ExcelImporDetectedRecords


class ExcelImporDetectedRecords:
    @staticmethod
    def text(*, count) -> Literal["""Обнаружено записей: &lt;code&gt;{ $count }&lt;/code&gt;
Если записей нехватает, пересмотрите файл, заполните недостающие ячейки и пришлите обратно отредактированный файл"""]: ...


class ExcelImporUpload:
    records: ExcelImporUploadRecords


class ExcelImporUploadRecords:
    @staticmethod
    def text(*, count) -> Literal["""Всего добавлено записей: &lt;code&gt;{ $count }&lt;/code&gt;
Если число обнаруженных записей отличается от всего добавленных записей, проверьте что в файле нет записей которые есть в базе"""]: ...


class Undefined:
    start: UndefinedStart


class UndefinedStart:
    review: UndefinedStartReview
    games: UndefinedStartGames
    open: UndefinedStartOpen
    invite: UndefinedStartInvite
    request: UndefinedStartRequest

    @staticmethod
    def text() -> Literal["""你好 или привет!
Добро пожаловать в школу китайского языка Xingfu."""]: ...


class UndefinedStartReview:
    @staticmethod
    def button() -> Literal["""Отзывы и результаты"""]: ...


class UndefinedStartGames:
    @staticmethod
    def button() -> Literal["""Игры на развитие"""]: ...


class UndefinedStartOpen:
    day: UndefinedStartOpenDay


class UndefinedStartOpenDay:
    @staticmethod
    def button() -> Literal["""День открытых дверей"""]: ...


class UndefinedStartInvite:
    parent: UndefinedStartInviteParent
    student: UndefinedStartInviteStudent


class UndefinedStartInviteParent:
    @staticmethod
    def button() -> Literal["""Пригласить родителя"""]: ...


class UndefinedStartInviteStudent:
    @staticmethod
    def button() -> Literal["""Пригласить ученика"""]: ...


class UndefinedStartRequest:
    trial: UndefinedStartRequestTrial


class UndefinedStartRequestTrial:
    lesson: UndefinedStartRequestTrialLesson


class UndefinedStartRequestTrialLesson:
    @staticmethod
    def button() -> Literal["""Заявка на
пробное занятие"""]: ...

