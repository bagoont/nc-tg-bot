### Текстовые сообщения и кнопки меню управления корзиной.

## Корзина.
trashbin =
    В корзине 
    { $count ->
        [one] находится <b>{ $count }</b> файл.
        [few] находятся <b>{ $count }</b> файла.
        *[other] находятся <b>{ $count }</b> файлов.
    }
    Корзина занимает <b>{ $size }</b>.

    <i><u>Выберите файл, чтобы удалить или восстановить его:</u></i>
trashbin-item = 🔹 <i>{ $path }</i>
trashbin-empty = Корзина пуста

## Очистка корзины.
trashbin-cleanup-button = Очистить корзину
trashbin-cleanup-start = Вы уверены, что хотите очистить корзину?

## Действия с файлом внутри корзины.
trashbin-fsnode = Выберите действие.
trashbin-delete-button = ❌ Удалить 
trashbin-restore-button = 🔃 Восстановить
trashbin-delete-alert = Файл удален.
trashbin-restore-alert = Файл восстановлен.