# YTDV-YouTube Downloader

YTDV is a simple app for downloading videos from YouTube. 

**Features**:  

- Can downloading videos as mp3

- Has GUI and CLI 

- CLI has Ukrainian language support

- Dark and Light theme for GUI

[Download YTDV](https://github.com/latned/ytdv/releases)

## Usage

Run with `ytdv`. See `ytdv -h` or `ytdv --help` for help. 

`ytdv -l <link>`:  Downloading video with default settings.

Can specify video quality and path to save video using options `-q <quality>` and `-p <path>` respectively.

`ytdv config`: Change default app settings (quality and path). See `ytdv config -h` for help.

## Examples

`ytdv -l https://youtu.be/url_to_video` 

`ytdv -l https://youtu.be/url_to_video -q high -p /home/user/Downloads` 

For convenience add `alias yd="ytdv -l"` to ~/.bashrc and use:

`yd https://youtu.be/url_to_video` 
