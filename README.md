# osu!vision
An external cheat for osu!

## Notes/Bugs
- No further updates will be made.

- Only supports stable.
- A few bugs with note generation.

- A decently fleshed out SDK for further feature development (I don't know why you'd want to work on this.)
- A lot of the SDK is in a rough state, I never really cleaned it up.

## Features
### TaikoMania
- Note Style: `Circle, Rectangle`
- Playstyle: `KDDK, DKKD, KKDD, DDKK, KDKD, DKDK`
- 2K Finisher: `[ ]` Splits finishers into two notes, using both keys instead of one
- Alternate BPM: `0-500`
- Scroll Speed: `0.1-3.0`
- Stage Spacing: `5-30`
- Offset: `-100-100`
- Don Color
- Katsu Color

### Mania
- Note Style: `Circle, Rectangle`
- Scroll Speed: `0.1-3.0`
- Stage Spacing: `5-30`
- Offset: `-100-100`
- Note Color
- LN Head Color
- LN Body Color
- LN Tail: `[ ]` Enable/Disable LN Tail
- LN Tail Color

## Why release it?
- I plan on rewriting the entire project in C++.
- Further development in Python is just a major pain in the ass for what I want to do.
- So others can learn too.

## Is it detected?
- As far as I'm concerned, no.
- Reads memory the same way tosu does.
- If status changes I will make it known.

## Requirements
- `Python 3.13.7`
- [requirements.txt](https://github.com/yo-ru/osu-vision/blob/main/requirements.txt)

## Installation
1. Install `Python 3.13.7`
2. Clone this repo.
3. Install requirements: `python3.13 -m pip install -r requirements.txt`


## Usage
1. Open osu!
2. Run `python3.13 main.py`
3. Profit?
