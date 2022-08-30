try:
    from src.artifact import *
    from src.settings import *
except:
    from diohod_bot.src.artifact import *
    from diohod_bot.src.settings import *

base = Artifact('База', os.path.join(ARTIFACTS_IMG, 'base.png'), 'base')
dino = Artifact('Динозавр', os.path.join(ARTIFACTS_IMG, 'dino.png'), 'dino')
cosmos = Artifact('Тьма неопознанная', os.path.join(ARTIFACTS_IMG, 'cosmos.png'), 'cosmos')
volcano = Artifact('Вулкан', os.path.join(ARTIFACTS_IMG, 'volcano.png'), 'volcano')
empty = Artifact('Пустота', os.path.join(ARTIFACTS_IMG, 'empty.png'), 'empty')
camera_roll = Artifact('Пленка кончилась', os.path.join(ARTIFACTS_IMG, 'camera_roll.png'), 'camera_roll')
idol = Artifact('Истукан прямо, как на острове Пасхи', os.path.join(ARTIFACTS_IMG, 'idol.png'), 'idol')

ufo_01 = Artifact('НЛО-1', os.path.join(ARTIFACTS_IMG, 'ufo_01.png'), 'ufo_01')
ufo_02 = Artifact('НЛО-2', os.path.join(ARTIFACTS_IMG, 'ufo_02.png'), 'ufo_02')
ufo_03 = Artifact('НЛО-3', os.path.join(ARTIFACTS_IMG, 'ufo_03.png'), 'ufo_03')
key = Artifact('Ключ', os.path.join(ARTIFACTS_IMG, 'key.png'), 'key')
gold = Artifact('Золотишко', os.path.join(ARTIFACTS_IMG, 'gold.png'), 'gold')

mammoth = Artifact('Мамонт', os.path.join(ARTIFACTS_IMG, 'mammoth.png'), 'mammoth')
goose = Artifact('Гусь', os.path.join(ARTIFACTS_IMG, 'goose.png'), 'goose')
orangutan = Artifact('Орангутан', os.path.join(ARTIFACTS_IMG, 'orangutan.png'), 'orangutan')
unicorn = Artifact('Орангутан', os.path.join(ARTIFACTS_IMG, 'unicorn.png'), 'unicorn')

shard = Artifact('Т', os.path.join(ARTIFACTS_IMG, 'shard.png'), 'shard')
letter_p = Artifact('П', os.path.join(ARTIFACTS_IMG, 'letter_p.png'), 'letter_p')
letter_o = Artifact('О', os.path.join(ARTIFACTS_IMG, 'letter_o.png'), 'letter_o')
letter_l = Artifact('Л', os.path.join(ARTIFACTS_IMG, 'letter_l.png'), 'letter_l')
letter_e = Artifact('Е', os.path.join(ARTIFACTS_IMG, 'letter_e.png'), 'letter_e')
letter_t = Artifact('Т', os.path.join(ARTIFACTS_IMG, 'letter_t.png'), 'letter_t')

lenin = Artifact('Памятник Ленину', os.path.join(ARTIFACTS_IMG, 'lenin.png'), 'lenin')
pyramid = Artifact('Пирамида', os.path.join(ARTIFACTS_IMG, 'pyramid.png'), 'pyramid')
