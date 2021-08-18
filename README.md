# Dual-audio video maker

You can pass 2 playlists (or 2 lists with playlists), first for extracting audio (`audio-playlists`), second for resulting video (`video-playlists`), and get video with both audio tracks. For the first playlists it is better to use low quality video.

## Dependencies

You need installed in system `ffmpeg` (work with media), `wget` (download) and `grep` utilities.

## Install

```bash
pip install dual-audio
```

## Usage example

Extract audios from video files from `audio-playlist.m3u` and add to related videos from `video-playlist.m3u` (for example, `1x1.aac` will be added to `1x1.mp4`).

```bash
dual-audio --out-dir . -a audio-playlist.m3u -v video-playlist.m3u
```

Number of entries in both audio and video playlists should be equal.

## CLI arguments

| Argument                | Action                                                      |
|:------------------------|:------------------------------------------------------------|
| `-d, --out-dir`         | Directory where place audio and video folders               |
| `-a, --audio-playlists` | Path(s) to playlist(s) with videos from which extract audio |
| `-v, --video-playlists` | Path(s) to playlist(s) with videos to add a second audio    |
| `--args`                | Pass shell arguments via file                               |
| `--preserve-video`      | Preserving original videos from `video-playlists`           |
| `-h, --help`            | Show help message and exit                                  |

## Shortened M3U playlist syntax

You can write playlists manually by this template:

```
#EXTM3U
#EXTINF: <duration>,<title>
#EXTVLCOPT:
<link>
```

- `#EXTM3U` is the required header for the file,
- duration can be zero,
- the title must not contain commas,
- the link should be on a separate line,
- other lines and directives are ignored and can be omitted.

*For example*:

```
#EXTM3U
#EXTINF: 0,Your show - episode 1
http://example.com/1x1.mp4
#EXTINF: 0,Your show - episode 2
http://example.com/1x2.mp4
```

These videos will be saved as `Your show - episode 1.mp4` and `Your show - episode 2.mp4`.

## How it works

1. Parse playlists.
2. Download `audio-playlists`. For each playlist:
	- Download videos to `video-cache` folder,
	- Extract audio to `audio` folder and select extension based on `ffprobe` (from `ffmpeg`) output,

	For example, from the `Stream #0:0: Audio: aac (LC), 48000 Hz, stereo, fltp, 94 kb/s` line will be taken `aac`.
3. For each playlist from `video-playlists` download videos to `video/` folder.
4. Correlate audio and video file names (for example, `1x1.aac` will be added to `1x1.mp4`).
5. Join audios and videos and save to `video-result` folder.
6. If `--preserve-video` is not passed, move resulting videos to `video` folder.
