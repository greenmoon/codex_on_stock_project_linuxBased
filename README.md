# codex_on_stock_project_linuxBased

Stock monitoring GUI project based on `jb_A411B_stock_AI_v36b.py`, with a browser version in `index.html` for GitHub Pages.

The original app is a PyQt5 desktop tool for browsing selected Taiwan stock symbols and viewing market-derived indicators. The web version ports the main stock list, TWSE/TPEX loading path, Bollinger bands, RSI, MACD, and BUY/SELL/WAIT decision display into plain HTML, CSS, and JavaScript.

## Main File

- `jb_A411B_stock_AI_v36b.py`
- `index.html`

## Browser / Worldwide URL

GitHub Pages serves `index.html` directly. After the repository is pushed and Pages is enabled, open:

```text
https://greenmoon.github.io/codex_on_stock_project_linuxBased/
```

The browser version can run on a worldwide URL because it does not require Python or PyQt5 in the visitor's browser.

TWSE data is fetched directly from the official TWSE JSON endpoint, which currently exposes `access-control-allow-origin: *`. TPEX support is included, but the tested TPEX endpoint did not expose an allow-origin header for `https://greenmoon.github.io`, so TPEX browser loading may require a small proxy/backend if the endpoint blocks GitHub Pages.

## Requirements

These are only needed for the desktop Python version:

Install dependencies with:

```bash
python3 -m pip install -r requirements.txt
```

## Run

Desktop Python version:

```bash
python3 jb_A411B_stock_AI_v36b.py
```

The app fetches market data from TWSE and TPEX network endpoints, so an internet connection is required.
