# Dual-audio video maker

You can pass 2 playlists (or 2 lists with playlists), first for extracting audio (`audio-playlists`), second for resulting video (`video-playlists`), and get video with both audio tracks. For first playlists better use low-quality video.

## Dependencies

`ffmpeg` (work with media), `wget` (download) and `grep` utilities.

## CLI arguments

| Argument                | Action                                                                                               |
|:------------------------|:-----------------------------------------------------------------------------------------------------|
| `-d, --out-dir`         | Directory where place audio and video folders                                                        |
| `-a, --audio-playlists` | Path(s) to playlist(s) with videos from which extract audio                                          |
| `-v, --video-playlists` | Path(s) to playlist(s) with videos to add a second audio                                             |
| `--args`                | Pass shell arguments via file                                                                        |
| `--preserve-video`      | Preserving original videos from `video-playlists`                                                    |
| `--template`            | Path to template of playlist (if both audio and video playlists are the same format)                 |
| `--audio-template`      | Path to template of playlist with audio (videos to extract audio). Ignored if `--template` specified |
| `--video-template`      | Path to template of playlist with videos. Ignored if `--template` specified                          |
| `-h, --help`            | Show help message and exit                                                                           |

## How it works

1. Parse templates and playlists.
2. Download `audio-playlists`. For each playlist:
	- Download videos to `video-cache`.
	- Extract audio to `audio` folder and select extension (container) based on `ffprobe` (from `ffmpeg`) output:

```
Stream #0:0: Audio: aac (LC), 48000 Hz, stereo, fltp, 94 kb/s
```

3. For each playlist from `video-playlists` download videos to `video`.
4. Correlate audio and video file names (for example, `1x1.aac` will be added to `1x1.mp4`).
5. Join audios and videos and save to `video-result` folder.
6. If `--preserve-video` is not passed, move resulting videos to `video` folder.

## Playlists

For specifying how parse playlist, do folowing:

1. Copy from your playlist header and one entry.
2. Paste in new file and add line after header and paste `---`
3. Change places with title to `<title>` and with link to `<link>`

For example, this:

```
#EXTM3U
#EXTINF: 0,1x1 name
#EXTVLCOPT:http-user-agent=(here some user agent)
http://example.com/1x1.mp4
#EXTINF: 0,1x2 name
#EXTVLCOPT:http-user-agent=(here some user agent)
http://example.com/1x2.mp4
```

will change to this:

```
#EXTM3U
---
#EXTINF: 0,<title>
#EXTVLCOPT:http-user-agent=
<link>
```

*Note*. So far, it is assumed that part `#EXTINF: 0,` (for this example) will be the same for all entries. First argument in this line ...
