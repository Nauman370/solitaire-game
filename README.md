# Solitaire

A Klondike Solitaire game.

## Features

- Classic Klondike rules: 7 tableau piles, stock and waste, 4 foundations, moving runs of cards
- Click a card to select it, then click where it should go
- Undo (each undo adds a 10 second penalty)
- Save and load your game
- Timer, move counter and a top-10 leaderboard with names and dates
- Easy mode: only Hearts and Spades, with its own separate leaderboard
- 7 color themes that are remembered between launches
- Fullscreen support

## Controls

| Key | Action |
|-----|--------|
| Click | Select a card, then click a destination |
| Click the stock | Draw a card |
| Z | Undo (+10 s penalty) |
| N | New game |
| S | Save game |
| L | Load game |
| B | Show or hide the leaderboard |
| M | Switch between Normal and Easy mode |
| T | Change theme |
| H | Hide or show the controls bar |

All of these also have buttons in the bar at the bottom.

## Run it

You need Python 3 and pygame-ce:

```
pip install pygame-ce
python solitaire.py
```

## Build the .exe (Windows)

```
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name Solitaire solitaire.py
```

The exe appears in the `dist` folder.

## Saved files

The game stores these in your home folder:

- `solitaire-save.json` (saved game)
- `solitaire-scores.json` and `solitaire-scores-easy.json` (leaderboards)
- `solitaire-settings.json` (chosen theme)

Delete them to reset everything.

