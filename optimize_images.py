from __future__ import annotations

from pathlib import Path

from PIL import Image


QUALITY = 80
METHOD = 6


def find_assets_dir(script_dir: Path) -> Path:
    candidates = [
        script_dir / "WEB" / "assets",
        script_dir / "assets",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("Could not find an assets/ directory to scan.")


def convert_png_to_webp(png_path: Path, quality: int = QUALITY, method: int = METHOD) -> Path:
    webp_path = png_path.with_suffix(".webp")
    if webp_path.exists() and webp_path.stat().st_mtime >= png_path.stat().st_mtime:
        return webp_path

    with Image.open(png_path) as img:
        img.save(webp_path, "WEBP", quality=quality, method=method)

    return webp_path


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    assets_dir = find_assets_dir(script_dir)

    png_files = sorted(assets_dir.rglob("*.png"))
    if not png_files:
        print(f"No PNG files found in {assets_dir}")
        return

    converted = 0
    for png_path in png_files:
        try:
            convert_png_to_webp(png_path)
            converted += 1
        except Exception as exc:  # pragma: no cover - best effort conversion
            print(f"Failed to convert {png_path.name}: {exc}")

    print(f"Converted {converted} PNG file(s) in {assets_dir}")


if __name__ == "__main__":
    main()
