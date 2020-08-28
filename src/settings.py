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
ROTATE_HAT_PATTERN = '(rotate\()(|north|east|west|south|)(\))'

MEMORY_LIMIT = 30
TIME_LIMIT = 1000