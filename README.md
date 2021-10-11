![](public/synthesia.png)

[![GitHub Issues](https://img.shields.io/github/issues/SoloSteve/copycat)](https://github.com/SoloSteve/magic-search/issues)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)]()
# copycat
**Synthesia Video Converter**

Download a video of a Synthesia song, run it through the program, and receive the sheet music!

### Basic Tutorial
> This program is in its early stages so don't expect very high quality output at this time

> If the beat doesn't sound quite right, remove all occurrences of 'z/8' and it might sound better

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

### Example
Here is an example of a song with the correct parameters running in debug mode (`--debug`)

`main.py --file /tmp/taylor_swift.mp4 --first-key D2 --debug`

![](public/debug_example.png)

##### Explained
1. The orange line is the detection line. It is where the key detection actually happens. Make sure no *special effects* are seen at this line.
2. The purple key text has been placed above the respective key.

If everything looks good you can run without the `--debug` flag

Example output:
```text
T: 
C: 
Q: 120
[B,1] [D1] [A1] [G1] [A1] [G1] [D1] [G1] [B,1]  %
[D1] [A1] [G1] [A1] [G1] [D1] [G1] [A,1] [D1] [A1]  %
[G1] [A1] [G1] [D1] [G1] [A,1] [D1] [A1] [G1] [A1]  %
[G1] [D1] [G1] [B,1] [E1] [A1] [G1] [A1] [G1] [E1]  %
[G1] [B,1] [E1] [A1] [G1] [A1] [G1] [E1] [G1] [C1]  %
[D1] [A1] [G1] [A1] [G1] [D1] [G1] [C1] [D1] [A1]  %
[G1] [A1] [G1] [D1] [G1] [^F1] [G1] [G2] [G3]  %
[G1] [^F1] [G2] [A2] [G2] [G1] [^F1] [G2]  %
[G3] [G1] [G1] [^F1] [G2] [A2] [G1] [^F1]  %
[G1] [E8] z2 [G1] [G1] [G1] [^F1] [^F1] [D1]  %
```

Take the output string when the program finishes and paste it into your favorite
[abc notation editor](https://www.abcjs.net/abcjs-editor.html)