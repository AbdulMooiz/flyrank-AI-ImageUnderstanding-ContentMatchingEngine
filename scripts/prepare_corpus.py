from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlretrieve

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "data" / "corpus"
MANIFEST_PATH = CORPUS_DIR / "manifest.json"


def ensure_manifest() -> list[dict]:
    if not MANIFEST_PATH.exists():
        examples = [
            {"id": "fox-01", "filename": "fox-01.jpg", "category": "animal", "subject": "red fox", "source_url": "https://images.unsplash.com/photo-1474511320723-9a56873867b5?auto=format&fit=crop&w=1200&q=80"},
            {"id": "fox-02", "filename": "fox-02.jpg", "category": "animal", "subject": "red fox", "source_url": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?auto=format&fit=crop&w=1200&q=80"},
            {"id": "wolf-01", "filename": "wolf-01.jpg", "category": "animal", "subject": "wolf", "source_url": "https://images.unsplash.com/photo-1474511320723-9a56873867b5?auto=format&fit=crop&w=1200&q=80"},
            {"id": "dog-01", "filename": "dog-01.jpg", "category": "animal", "subject": "dog", "source_url": "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=1200&q=80"},
            {"id": "bear-01", "filename": "bear-01.jpg", "category": "animal", "subject": "bear", "source_url": "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=1200&q=80"},
            {"id": "deer-01", "filename": "deer-01.jpg", "category": "animal", "subject": "deer", "source_url": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?auto=format&fit=crop&w=1200&q=80"},
        ]
        CORPUS_DIR.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(json.dumps(examples, indent=2), encoding="utf-8")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def download_images() -> list[Path]:
    manifest = ensure_manifest()
    images_dir = CORPUS_DIR / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    for item in manifest:
        target = images_dir / item["filename"]
        if not target.exists() and item.get("source_url"):
            urlretrieve(item["source_url"], target)
        downloaded.append(target)
    return downloaded


if __name__ == "__main__":
    records = download_images()
    print(f"Downloaded {len(records)} corpus files to {CORPUS_DIR / 'images'}")
