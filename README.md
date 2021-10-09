![](public/synthesia.png)

[![GitHub Issues](https://img.shields.io/github/issues/SoloSteve/copycat)](https://github.com/SoloSteve/magic-search/issues)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)]()
# copycat
**Synthesia Video Converter**

Download a video of a Synthesia song, run it through the program, and receive the sheet music!

### Basic Tutorial
> This program is in its early stages so don't expect very high quality output at this time

Program Arguments
```text
(venv) >python -m copycat.main --help

usage: main.py [-h] -f PATH [-k NOTE] [-t TEMPO] [--skip-frames SKIP_FRAMES] [--debug] {manual} ...

positional arguments:
  {manual}

optional arguments:
  -h, --help            show this help message and exit
  -f PATH, --file PATH  The path of the mp4 synthesia video
  -k NOTE, --first-key NOTE
                        The first white key in the bounds.
  -t TEMPO, --tempo TEMPO
                        The tempo of the piece in BPM
  --skip-frames SKIP_FRAMES
                        How many frame to skip in case there is an introduction
  --debug               Show debugged version
```

If there are issues with part of the detection process, you can add manual arguments

```text
(venv) >python -m copycat.main manual --help
usage: main.py manual [-h] [--bounds X Y WIDTH HEIGHT] [--detector-line-offset DETECTOR_LINE_OFFSET] [--min-speed MIN_SPEED]

optional arguments:
  -h, --help            show this help message and exit
  --bounds X Y WIDTH HEIGHT
                        The boundaries around the piano keys space separated
  --detector-line-offset DETECTOR_LINE_OFFSET
                        Number of pixels from the top of the boundary to offset the detector line
  --min-speed MIN_SPEED
                        Defines a minimum note duration
```

### Example
Here is an example of a song with the correct parameters running in debug mode (`--debug`)

`main.py --file /tmp/taylor_swift.mp4 --first-key D2 --debug`

![](public/debug_example.png)

##### Explained
1. The orange line is the detection line. It is where the key detection actually happens. Make sure no *special effects* are seen at this line.
2. The purple key text has been placed above the respective key.

If everything looks good you can run without the `--debug` flag

Take the output string when the program finishes and paste it into your favorite
[abc notation editor](https://www.abcjs.net/abcjs-editor.html)