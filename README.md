# shellStone
tiny terminal UI for fancy presentation of pre-commented shell scripts stored locally. In the spirit of [eos-welcome](https://github.com/endeavouros-team/welcome); Good for helping new users, good for one-off black book tricks whose purpose you'd forget. A Memory rock of shell ideas

## Benefits
- Simple interface and metadata rules
- Extensible; drop in your Py & Bash scripts
- Unnecessarily parallaxed starfield effects
- ~50kb

## Requirements
- Python 3.10+ (`curses`, `subprocess`, `pathlib`)
- python3 on PATH (only when running `.py` scripts — soft error if missing)

## Usage
Run `python3 shellstone.py`.

Categories are auto-populated with .sh and .py scripts when placed in their respective folders

Descriptions and Names are stored inside the .sh/.py themselves as metadata tags. Program "HELP" has more information on the format, or look at the sample scripts to see an example.

## AI DISCLOSURE
This README.md hand-written.
Generated with Tencent HY3 Preview roughly following a Pareto Vibe; 80% time AI driven code generation, 20% time inspecting source files and manually checking behavior. 
