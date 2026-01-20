import subprocess
import sys
from pathlib import Path

# ---------------- CONFIG ----------------
WAN_DIR = Path("wan2gp")
PYTHON_BIN = WAN_DIR / "venv/bin/python"
INFER_SCRIPT = WAN_DIR / "infer.py"

SOURCE_DIR = Path("inputs/source_videos")
AVATAR_DIR = Path("inputs/avatars")
OUTPUT_ROOT = Path("outputs")

DEVICE = "cuda"  # auto-fallbacks to CPU if unavailable
# ---------------------------------------


def run(cmd):
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("Generation failed. Aborting.")
        sys.exit(1)


def main():
    if not SOURCE_DIR.exists() or not AVATAR_DIR.exists():
        raise RuntimeError("Input folders missing")

    source_videos = sorted(SOURCE_DIR.glob("*.mp4"))
    avatars = sorted(AVATAR_DIR.glob("*"))

    if not source_videos:
        raise RuntimeError("No source videos found")

    if not avatars:
        raise RuntimeError("No avatar images found")

    for avatar in avatars:
        avatar_name = avatar.stem
        avatar_output_dir = OUTPUT_ROOT / avatar_name
        avatar_output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n=== Generating videos for avatar: {avatar_name} ===")

        for video in source_videos:
            out_path = avatar_output_dir / video.name

            if out_path.exists():
                print(f"Skipping existing: {out_path}")
                continue

            cmd = [
                str(PYTHON_BIN),
                str(INFER_SCRIPT),
                "--source_video", str(video),
                "--reference_image", str(avatar),
                "--output", str(out_path),
                "--device", DEVICE
            ]

            run(cmd)

    print("\nAll video generations completed successfully.")


if __name__ == "__main__":
    main()
