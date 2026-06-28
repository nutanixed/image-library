# Image Library

A lightweight Flask web UI for browsing files under a mounted storage path and generating copyable download links.

## Features

- Recursively scans files under `/data`
- Search by filename/path
- Optional "show hidden files" mode
- Groups files by extension in the UI
- Copy-friendly links that can point to a dedicated download host
- Logout redirect endpoint for integrations behind auth proxies

## Project Structure

- `app.py`: Flask app and file-index logic
- `templates/index.html`: UI template
- `static/`: static assets
- `restart.sh`: helper to restart the Docker service from a host compose project

## Requirements

- Python 3.9+
- `pip`

Python packages:
- `flask`
- `python-dotenv`

Install:

```bash
pip install flask python-dotenv
```

## Configuration

Create a `.env` file (do not commit it) with optional values:

```env
DOWNLOAD_URL=https://downloads.example.com
LOGOUT_REDIRECT_URL=/
```

Environment variables:

- `DOWNLOAD_URL`: Base URL used when generating file links in the UI. If unset, the app uses the current request host.
- `LOGOUT_REDIRECT_URL`: Redirect target for `/logout`. Default is `/`.

## Run Locally

```bash
python app.py
```

The app listens on `0.0.0.0:5000`.

## How It Works

- The app walks `STORAGE_PATH` (currently `/data`).
- The `logs` directory is excluded from traversal.
- Hidden files/directories are excluded by default unless `show_all=true` is set in the query string.
- Results are sorted and grouped by extension for display.

## Example URLs

- Main view: `http://localhost:5000/`
- Search: `http://localhost:5000/?search=ubuntu`
- Show hidden files: `http://localhost:5000/?show_all=true`

## Docker Restart Helper

`restart.sh` runs:

```bash
docker compose up -d nutanix-images-ui
```

from `/home/nutanix/plex-docker`.

## Security Notes

- `.env`, logs, and Python cache files should stay untracked (see `.gitignore`).
- Rotate any secrets that were previously committed by mistake.
