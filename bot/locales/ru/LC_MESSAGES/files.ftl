### Тексты для диалога files.

## Окно scrollgroup.
file-info =  
    <b>Информация о файле:</b>
    - Название: { $name }
    - Путь: /{ $path }
    - Тип: { $symbol } { $type ->
        [folder] папка
        *[other] { $type }
    }
    - Избранное: { $favorite ->
        [True] ⭐
        [False] ❌
        *[other] ❔
    }
        
    <b>Свойства:</b>
    - Размер: { $size }
    - Последнее изменение: { $last_modified }
        
    <b>Информация о владельце:</b>
    - Пользователь: { $user }
    - Права доступа: { $permissions }
download-btn = ⬇️ Скачать
delete-btn = 🗑️ Удалить
create-btn = 🆕 Создать

## Окно multiselect
files-multiselect = 
    Выберите несколько файлов из:
    <i>{ $path }</i>
files-multidownload = 
    <i>Скачиваю файл: { $name }</i>
files-multidownload = 
    <i>Удаляю файл: { $name }</i>
multidownload-btn = ⬇️ Скачать выбранное
multedelete-btn = 🗑️ Удалить выбранное

## Окно Create.
create-file = 
    Выберите какой файл вы хотите создать в этой папке:
    <i>{ $path }</i>
folder-btn = 📁 Папка
upload-btn = ⬆️ Загрузить

## Окно Create folder.
create-folder = 
    Введите имя папки, чтобы создать папку по пути:
    <i>{ $path }/<имя-вашей-папки></i>
incorrect-folder-name=<i>Некорректное имя папки.</i>
folder-create-success=Папка <b>{ $name }</b> по пути <i>{ $path }</i> создана успешно.

## Окно Process documents.
upload-files-managment = 
    Отправьте файлы, которые вы хотите загрузить в Nextcloud в виде документа. 
    
    Нажмите на имя файла, которое вы хотите убрать из очереди загрузки. 
    
    Когда вы отправите все файлы, которые вы хотите загрузить, нажмите на кнопку "Загрузить".

## Upload Docuemnts window.
upload-files = <i>Загружаю { $name }</i>