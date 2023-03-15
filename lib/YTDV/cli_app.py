#!/usr/bin/python3

from importlib.machinery import SourceFileLoader
import argparse
import json
import sys
import os

# imports the module from the given path
lang = SourceFileLoader("lang","/usr/lib/YTDV/lang.py").load_module()
yd = SourceFileLoader("yd","/usr/lib/YTDV/yd.py").load_module()

path = os.path.expanduser('~')

class CliApp:

    def __init__(self):
        self.check_args()

    def check_args(self):
        # check if should display help message in terminal for user
        help_lst = ('-h', '--help')
        if len(sys.argv) == 1 or sys.argv[1] in help_lst:
            print(lang.HELP_MAIN)
            return 1

        if len(sys.argv) == 2 and sys.argv[1] == 'config':
            print(lang.HELP_CONFIG)
            return 1

        if len(sys.argv) > 2 and sys.argv[2] in help_lst:
            print(lang.HELP_CONFIG)
            return 1

        self.run_argparse()


    def run_argparse(self):
        """
        Parse passed arguments and if parser doesn't find errors
        pass args to next function
        """
        parser = argparse.ArgumentParser(
                            prog = 'ytdv',
                            description = 'Downloads youtube video',
                            formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument('-l', '--link', help='URL to youtube video that should download')
        parser.add_argument('-q', '--quality', help='Specify the quality in what should download video')
        parser.add_argument('-p', '--path', help='Specify the path to save video')

        subparsers = parser.add_subparsers(dest='command')
        config = subparsers.add_parser('config', help='Change default settings')
        config.add_argument('-dq', '--default_quality', help='Change default downloading quality', dest='def_quality')
        config.add_argument('-dp', '--default_path', help='Change default saving path', dest='def_path')

        args = parser.parse_args()
        self.choose_action(args)

    def choose_action(self, args):
 
        with open(f'{path}/.YTDV/settings.json') as f:
            self.settings = json.load(f)

        map_gui2cli = {
                '-HIGH-': 'high',
                '-MID-': 'mid',
                '-MUSIC-': 'music'
                }

        map_cli2gui = {
                'high': '-HIGH-',
                'mid': '-MID-',
                'music': '-MUSIC-'
                }

        self.quality = self.settings['quality']
        self.path = self.settings['path']

        if args.link:
            self.link = args.link
            if args.quality:
                self.quality = map_cli2gui[args.quality]
                if args.path:
                    self.path = args.path
            self.download_video_cli()

        elif args.command:
            if args.def_quality:
                self.settings['quality'] = map_cli2gui[args.def_quality]
                if args.def_path:
                    self.settings['path'] = args.def_path
            self.save_user_settings_cli()


    def download_video_cli(self):
        print('Downloading video, it can take a while...')

        downloader = yd.Downloader(self.quality, self.link, self.path)
        res = downloader.check_link()

        if res == 0:
            print('Video successfully downloaded')
        elif res == 1:
            print('Please enter proper link')
        elif res == 2:
            print('Video not available')

    def save_user_settings_cli(self):
        with open(f'{path}/.YTDV/settings.json', 'w') as f:
            json.dump(self.settings, f)
        print('Settings saved')


