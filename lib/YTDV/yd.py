#!/usr/bin/python3

from pytube import YouTube
import pytube
import youtube_dl
import os


class Downloader:

    def __init__(self, quality, link, path):
        """
        Initializes a Downloader object that can handle downloading process
        :param quality: (str) the quality in which user want to download the video
        :param link: (str) the link to youtube video to download
        :param path: (str) the path to save the video
        """
        self.quality = quality
        self.link = link
        self.path = path

    def download_video(self):
        if self.quality == '-HIGH-':
            yd = self.yt.streams.get_highest_resolution()
            yd.download(output_path=self.path)
        elif self.quality == '-MID-':
            yd = self.yt.streams.get_by_resolution('720p')
            yd.download(output_path=self.path)
        else:
            self.mp3_only()

    def mp3_only(self):
        yd = self.yt.streams.get_audio_only()
        out_file = yd.download(output_path=self.path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

    def check_link(self):
        try:
            self.yt = YouTube(self.link)
        except pytube.exceptions.RegexMatchError:
            return 1
        except pytube.exceptions.PytubeError:
            return 2
        else:
            self.download_video()
            return 0

