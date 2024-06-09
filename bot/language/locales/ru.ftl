# Сообщения и кнопки бота на русском языке.

## Обычные сообщения

start = Добро пожаловать!
    Я бот для взаимодействия с облаком Nextcloud, находящемуся по адресу:
    { $url }

    Для начала работы вам необходимо пройти авторизацию.
    Чтобы начать авторизацию введите /auth.
help = Помощь

## Сообщения для процесса авторизации в Nextcloud.

auth-init = Чтобы авторизироваться вам необходимо перейти по ссылке, перейдя по ссылке, предоставьте боту доступ к вашей учетной записи.

    { $url }

    К сожалению, время ограничено и для выполнения авторизации выделяется лишь { $timeout } минут.
auth-timeout = Вышло время для авторизации.
auth-success = Авторизация прошла успешно.
auth-welcome = Добро пожаловать.
not-authorized = Вы не авторизованы.
already-authorized = Вы уже авторизованы.

## Сообщения для выхода из Nextcloud.

logout = Вы уверены, что хотите выйти?
logout-confirm = Вы успешно вышли.
logout-cancel = Выход отменен.

## Сообщения для работы с файлами.

file = Файл { $name }
file_root = Вы находитесь в корневом файле.
file-not-found = Файл не надйен.
file-url = Ссылка на файл { $url }
file-delete = Удалить файл?
file-delete-success = Файл был удален.
file-delete-pop-up = Файл был удален.

file-mkdir-start = Отправьте название папки, чтобы ее создать.
file-mkdir-success = Папка успешно создана.
file-mkdir-incorrectly = Папка не может быть так названа.

file-upload-start = Отправьте файлы в виде документа, чтобы его загрузить.
file-upload-success = Файл загружен успешно.
file-upload-incorrectly = Файл должен быть в виде документа.

file-cancel = Операция отменена.

## Кнопки основного меню.

files-menu-button = 🗃️ Файлы

## Кнопки подветрждения и отмены.

confirm-button = ✅ Да
deny-button = ❌ Нет
cancel-button = 🚫 Отменить

## Инлайн кнопки файлового меню.

file-delete-button = ❌ Удалить
file-download-button = ⬇️ Скачать
file-upload-button = ⬆️ Загрузить
file-mkdir-button = 🆕 Создать папку
file-back-button = ⏮️ Вернуться
file-update-button = 🔄️ Обновить
file-pag-back-button = ⬅️
file-pag-next-button = ➡️

## Ошибки
msg_user_not_found = Автор сообщения не надйен.