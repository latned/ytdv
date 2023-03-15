#!/usr/bin/python3

import locale
locale.setlocale(locale.LC_ALL, "")
mes_lang = locale.getlocale(locale.LC_MESSAGES)[0]


en_main = '''usage: ytdv [-h] [-q QUALITY] [-p PATH] link {config} ...

Downloads youtube video

positional arguments:
    config              Change default settings.

optional arguments:
  -h, --help            Show this help message and exit.
  -l, LINK              URL to youtube video that should download.
  -q QUALITY            Specify the quality in what should download video. 
                        Available options: {high, mid, music}
  -p PATH               Specify the path to save video.

examples:
    ytdv -l https://youtu.be/url_to_video
    ytdv -l https://youtu.be/url_to_video -q high
    ytdv -l https://youtu.be/url_to_video -q high -p /home/user/Downloads
    ytdv config
    ytdv config -h'''

en_config = '''usage: ytdv config [-h] [-dq DEFAULT_QUALITY] [-dp DEFAULT_PATH]

Customize app settings 

optional arguments:
  -h, --help                Show this help message and exit.
  -dq DEFAULT_QUALITY       Specify the quality in what should download video by default.
                            All videos will be downloaded with this quality, you won't need 
                            to additionally specify the quality for each download.
                            Available options:
                                high   Highest video resolution posible
                                mid    Video with 720p
                                music  Convert video to mp3 file 
                            "high" by default.
  -dp DEFAULT_PATH          Specify the path to save video by default. 
                            "current working directory" by default

examples:
    ytdv config -dp high 
    ytdv config -dp /home/user/Videos'''

ua_main = '''використання: ytdv [-h] [-q QUALITY] [-p PATH] link {config} ...

Завантажує відео з youtube

позиційні аргументи:   
    config              Змінити налаштування за замовчуванням.

необов'язкові аргументи:
  -h, --help            Показати це довідкове повідомлення та вийти.
  -link LINK            URL-адреса посилання на відео YouTube, яке потрібно завантажити. 
  -q QUALITY            Вкажіть якість, в якому потрібно завантажити відео.
                        Доступні параметри: {high, mid, music}
  -p PATH               Вкажіть шлях для збереження відео.

приклади:
    ytdv -l https://youtu.be/url_to_video
    ytdv -l https://youtu.be/url_to_video -q high
    ytdv -l https://youtu.be/url_to_video -q high -p /home/user/Downloads
    ytdv config
    ytdv config -h'''

ua_config = '''використання: ytdv config [-h] [-dq DEFAULT_QUALITY] [-dp DEFAULT_PATH]

Налаштувати параметри програми

позиційні аргументи:
  -h, --help                Показати це довідкове повідомлення та вийти.
  -dq DEFAULT_QUALITY       Вкажіть якість, у якому має завантажуватися відео за замовчуванням.
                            Усі відео будуть завантажуватися з такою якістю, вам не потрібно буде 
                            додатково вказувати якість для кожного завантаження.
                            Доступні параметри: 
                                "high" Найвища можлива роздільна здатність відео 
                                "mid" Відео у якості 720p 
                                "music" Перетворення відео у файл mp3 з музикою
                            "high" за замовчуванням.

  -dp DEFAULT_PATH          Вкажіть шлях який використовувати для збереження відео за замовчуванням.
                            "поточний робочий каталог" за замовчуванням.

приклади:
    ytdv config -dp high 
    ytdv config -dp /home/user/Videos'''


if mes_lang[:2] == 'uk':
    HELP_MAIN = ua_main
    HELP_CONFIG = ua_config
else:
    HELP_MAIN = en_main
    HELP_CONFIG = en_config

