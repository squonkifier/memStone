# shellStone
https://github.com/user-attachments/assets/eb19355a-4f71-44d7-9754-3d293f066560

tiny terminal UI for fancy presentation of pre-commented shell scripts stored locally. Geared towards system maintenance. In the spirit of [eos-welcome](https://github.com/endeavouros-team/welcome); Good for helping new users, good for one-off black book tricks whose purpose you'd forget. A Memory rock of shell ideas

## Benefits
- Simple interface and metadata rules
- Extensible; drop in your Py & Bash scripts
- Unnecessarily parallaxed starfield effects
- ~50kb

## Requirements
- Python 3.10+ (`curses`, `subprocess`, `pathlib`, `json`)

## Usage
Run `python3 shellstone.py`.

Categories are auto-populated with .sh and .py scripts when placed in their respective folders

Descriptions and Names are stored inside the .sh/.py themselves as metadata tags. Program "HELP" has more information on the format, or look at the sample scripts to see an example.

## AI Disclosure
This README.md hand-written. Code was generated with Tencent HY3 Preview on  a Pareto vibecurve; 80% code generation, 20% time inspecting source files and manually checking behavior. 
