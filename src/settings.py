import os

PHOTOS = True

LAUNCH_BUTTON_TEXT = "запустить виртуальную ракету"
PUBLISH_BUTTON_TEXT = "дать новость"
HELP_BUTTON_TEXT = "помощь"
SETTINGS_BUTTON_TEXT = "регистрация"

ANONYMOUS_USER = 'Анонимный пользователь'
DB_DIR = os.path.join(os.curdir, 'db')

ARTIFACTS_IMG = os.path.join(os.curdir, 'img', 'artifacts')
MISSIONS_IMG = os.path.join(os.curdir, 'img', 'missions')

CYCLE_HAT_PATTERN = 'repeat\(\d*\)\ {0,1}\{{0,1}'
STATEMENT_HAT_PATTERN = 'if last is \w*\ {0,1}\{{0,1}'
ELSE_HAT_PATTERN = 'else\ {0,1}\{{0,1}'
ROTATE_HAT_PATTERN = '(rotate\()(|north|east|west|south||)(\))'

MEMORY_LIMIT = 30
TIME_LIMIT = 3500

HELP_TEXT = """
- Планета разбита на клетки. В каждой клетке не более одного объекта
- Начальное положение диохода: база, направление - север
- В конце каждой миссии диоход отправляет нам все сделанные фотографии
- `move()` сдвинуться на одну клетку в направлении головы
- `rotate()` повернуться на 90 градусов по часовой стрелке
- `rotate(WEST)` повернуться на запад
- `photo()` сделать фотографию
- `pop()` удалить последнюю фотографию
- Повторить 4 раза:
```
repeat(4)
{
    <ДЕЙСТВИЯ ДЛЯ ПОВТОРЕНИЯ>
}
```
- Если на последней фотографии ВУЛКАН:
```
if last is VOLCANO
{
    <Что делать, если условие выполнено?>
}
else
{
    <Что делать, если условие не выполнено?>
}
```
- В условии else необязателен
+ Вместо `VOLCANO`= \"Вулкан\" может быть много чего
+ `EMPTY` = \"Пустота\" 
+ `DINO` = \"Динозавр\" 
+ `COSMOS` = \"Космос\"
+ `BASE` = \"База\" 
"""