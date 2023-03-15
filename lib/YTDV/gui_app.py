#!/usr/bin/python3

from importlib.machinery import SourceFileLoader
 
import PySimpleGUI as sg
import threading
import json
import os

# imports the module from the given path
yd = SourceFileLoader("yd","/usr/lib/YTDV/yd.py").load_module()
icons = SourceFileLoader("icons","/usr/lib/YTDV/icons.py").load_module()

path = os.path.expanduser('~')

class App:

    # lists of keys
    def __init__(self):
        self.quality_btns = ('-HIGH-', '-MID-', '-MUSIC-')
        self.theme_btns = ('-LIGHT-', '-DARK-')
        self.start_right_theme()
        self.set_global_settings()
        self.create_main_window()

    def set_global_settings(self):
        # sets global settings (for all windows)
        sg.set_options(
                font='Inter 11',
                border_width=0,
                text_element_background_color=self.bg_clr,
                )

    def save_settings(self, q, t, p):
        """
        Save user settings to json
        Gets quality, theme, and path that have been selected in Settings window
        checks if value not None and writes them to settings.json file
        :param q: (str) default quality 
        :param t: (str) theme of the app
        :param p: (str) default path to save media
        """

        settings = self.read_settings()
        
        if q != '':
            settings['quality'] = q
        if t != '':
            settings['theme'] = t
        if p != '':
            settings['path'] = p

        with open(f'{path}/.YTDV/settings.json', 'w') as f:
            json.dump(settings, f)


    def read_settings(self):
        with open(f'{path}/.YTDV/settings.json') as f:
            user_settings = json.load(f)

        return user_settings


    def update_buttons_state(self, state):
        """
        Change buttons state for all buttons in main window
        when second window active state = disabled
        when second window closed return active state
        :param state: (bool) state of the button if True button will be disabled and reverse for False
        """
        for i in self.button_keys:
            self.window[i].update(disabled=state)


    def update_btn_clrs(self, wind, buttons, btn):
        """
        Change buttons color:
            if button was pressed -> change background color to more saturated
            for other buttons -> return background color to default
        :param wind: (obj) pysimplegui window object
        :param buttons: (list) list of buttons that color need to be changed
        :param btn: (str) button that should update color to look like selected 
        """
        for i in buttons:
            if i == btn:
                wind[btn].update(button_color=self.btn_prs_clr)
            else:
                wind[i].update(button_color=self.btn_clr)


    def update_window_with_settings(self, wind):
        """
        Reads user settings from json and updates buttons and input element 
        with default values 
        :param wind: (obj) pysimplegui window object
        """
        settings = self.read_settings()

        wind[settings['quality']].update(button_color=self.btn_prs_clr)
        
        if '-DARK-' in wind.AllKeysDict:
            wind[settings['theme']].update(button_color=self.btn_prs_clr)
            if wind['-PATH-'] != '':
                wind['-PATH-'].update(value=settings['path'])


    def download_yt_video(self, q, l, w):
        """
        Perform long_operation for downloading youtube video 
        Read output path from settings if empty save to current working directory
        Send params to Downloader object to handle downloading 
        :param q: (str) quality of video
        :param l: (str) link to youtube video
        :param w: (queue.Queue) Queue to communicate back to GUI that task is completed
        """
        def_path = self.read_settings()['path']

        if def_path.strip() == '':
            def_path = os.getcwd()

        downloader = yd.Downloader(q, l, def_path)
        res = downloader.check_link()

        if res == 0:
            w.write_event_value('-THREAD-', 0)
        elif res == 1:
            w.write_event_value('-THREAD-', 1)
        elif res == 2:
            w.write_event_value('-THREAD-', 2)


    def start_right_theme(self):
        # read settings to choose what theme to load
        theme = self.read_settings()['theme']
        if theme == '-LIGHT-':
            # light theme
            self.btn_clr = '#7c73e6'
            self.btn_prs_clr = '#5b50e5'
            self.bg_clr = '#fafafa'
            self.txt_clr = '#352ba3'
            self.inp_clr = '#ffe9e3'
            self.err_clr = '#cb3747'
            self.suc_clr = '#7cbd1e'
            self.settings_icon = icons.SETTINGS_LIGHT
            self.folder_icon = icons.FOLDER_LIGHT
        else:
            # dark theme
            self.btn_clr = '#c24d2c'
            self.btn_prs_clr = '#cd2d00'
            self.bg_clr = '#2e3233'
            self.txt_clr = '#d9dbd0'
            self.inp_clr = '#323b4e'
            self.err_clr = '#fc3c3c'
            self.suc_clr = '#8dc828'
            self.settings_icon = icons.SETTINGS_DARK
            self.folder_icon = icons.FOLDER_DARK

    def output_res_of_thread(self, values):
        if values['-THREAD-'] == 0:
            self.window['-RES-'].update('Successfully downloaded', text_color=self.suc_clr)
        elif values['-THREAD-'] == 1:
            self.window['-RES-'].update('Please enter proper link', text_color=self.err_clr)
        elif values['-THREAD-'] == 2:
            self.window['-RES-'].update('Video not available', text_color=self.err_clr)
        self.window['-DOWNLOAD-'].update(disabled=False)

    def create_button(self, name, key):
        return sg.B(
                name,
                button_color=self.btn_clr,
                p=0,
                k=key,
                mouseover_colors=(self.bg_clr, self.txt_clr)
                )


    def create_text(self, text, p=16):
        if text.startswith('Choose'):
            exp = True
            pad = 130
        else:
            exp = False
            pad = 0
        
        return sg.T(
                text,
                text_color=self.txt_clr,
                p=((pad,0),(p,9)),
                expand_x=exp,
                )


    def create_input(self, key):
        return sg.I(
                focus=True,
                p=((0,0),(0,5)),
                background_color=self.inp_clr,
                text_color=self.txt_clr,
                k=key,
                )


    def create_column(self, column, pad=0):
        return sg.Column(
                column,
                background_color=self.bg_clr,
                element_justification='c',
                justification='c',
                p=((0,pad),0),
                vertical_alignment='c',
                )


    def create_main_window(self):
        # creating widgets for main window
        layout = [
                [
                    self.create_text('Choose video quality'),
                    # settings button
                    sg.B(
                        tooltip='Manage your settings',
                        image_data=self.settings_icon,
                        button_color=self.bg_clr,
                        k='-SETTINGS-',
                        mouseover_colors=self.bg_clr,
                        p=((0,0),(8,0)),
                        )
                ],

                # quality buttons
                [
                    self.create_button('Highest', '-HIGH-'),
                    self.create_button('720p', '-MID-'),
                    self.create_button('Music', '-MUSIC-')
                ],

                [
                    self.create_text('Paste video link', p=20)
                ],

                [
                    self.create_input('-LINK-')
                ],

                [
                    # output result or error
                    sg.T(
                        '',
                        k='-RES-',
                        font='Inter 10',
                        text_color=self.txt_clr,
                        p=(0,(4,0))
                        )
                ],
                [
                    sg.B(
                        'Download',
                        button_color=self.btn_clr,
                        p=(0,(10,16)),
                        key='-DOWNLOAD-',
                        mouseover_colors=(self.bg_clr, self.txt_clr)
                        )
                ]
            ]

        # main window
        self.window = sg.Window(
                'YTDV',
                layout,
                background_color=self.bg_clr,
                element_justification='c',
                icon=icons.APP_ICON,
                finalize=True
                )

        # set pointer cursor for buttons
        self.button_keys = ('-HIGH-', '-MID-', '-MUSIC-', '-DOWNLOAD-', '-SETTINGS-')

        for i in self.button_keys:
            self.window[i].Widget.config(cursor='hand2')


        # setup main window before launch
        self.update_window_with_settings(self.window)
        def_quality = self.read_settings()['quality']

        # run main window
        while True:
            event, values = self.window.read() 
            print(event, values)
            if event == sg.WIN_CLOSED:
                break
            elif event == '-SETTINGS-':
                self.update_buttons_state(True)
                self.run_settings_window()
                self.update_buttons_state(False)
            elif event in self.quality_btns:
                self.update_btn_clrs(self.window, self.quality_btns, event)
                def_quality = event
            elif event == '-DOWNLOAD-':
                self.window['-RES-'].update(value='Downloading video, it can take a while', text_color=self.txt_clr)
                self.window['-DOWNLOAD-'].update(disabled=True)
                threading.Thread(target=self.download_yt_video, args=(def_quality, values['-LINK-'], self.window,), daemon=True).start()
            elif event == '-THREAD-':
                self.output_res_of_thread(values)

        self.window.close()


    def run_settings_window(self):
        # creating second "Settings" window
        qualities = ('Highest', '720p', 'Music')
        def_val = 'Highest'

        col = [
                [
                    self.create_text('Default quality')
                ],

                [
                    self.create_button('Highest', '-HIGH-'),
                    self.create_button('720p', '-MID-'),
                    self.create_button('Music', '-MUSIC-')
                ],
            ]

        col_2 = [
                [
                    self.create_text('Change Theme')
                ],

                [
                    self.create_button('Light', '-LIGHT-'),
                    self.create_button('Dark', '-DARK-'),
                ],
            ]

        layout2 = [
                [
                    self.create_column(col, pad=90),
                    self.create_column(col_2)
                ],

                [
                    self.create_text('Default path') 
                ],

                [
                    self.create_input('-PATH-'),
                    sg.B(
                        k='-BB-',
                        target='-PATH-',
                        border_width=0, 
                        button_type=1, 
                        image_data=self.folder_icon,
                        button_color=self.bg_clr,
                        mouseover_colors=self.bg_clr,
                        p=((5,0),(0,7)),
                        )
                ],

                [
                    sg.B(
                        'Save',
                        button_color=self.btn_clr,
                        mouseover_colors=(self.bg_clr, self.txt_clr),
                        k='-SAVE-',
                        p=(0,5),
                        )
                ],
            ]

        # Settings window (2)
        window2 = sg.Window(
                'Settings',
                layout2,
                background_color=self.bg_clr,
                use_default_focus=False,
                element_justification='c',
                finalize=True,
                )

        # temporary variables to store settings 
        set_quality = ''
        set_theme = ''

        # set pointer cursor for buttons
        button_keys2 = ('-HIGH-', '-MID-', '-MUSIC-', '-BB-', '-SAVE-', '-LIGHT-', '-DARK-')

        for i in button_keys2:
            window2[i].Widget.config(cursor='hand2')


        # update Settings window before launch
        self.update_window_with_settings(window2)

        # run "Settings" window
        while True:
            event, values = window2.read()
            print(event, values)
            if event == sg.WIN_CLOSED:
                break
            elif event == '-SAVE-':
                self.save_settings(set_quality, set_theme, values['-PATH-'])
                break
            elif event in self.quality_btns:
                set_quality = event
                self.update_btn_clrs(window2, self.quality_btns, event)
            elif event in self.theme_btns:
                set_theme = event
                self.update_btn_clrs(window2, self.theme_btns, event)

        window2.close()


