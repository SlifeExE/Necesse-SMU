import sys
from PIL import Image


def main():
    if len(sys.argv) < 3:
        print("Usage: png_to_ico.py <input.png> <output.ico>")
        return 1
    src = sys.argv[1]
    dst = sys.argv[2]
    img = Image.open(src).convert("RGBA")
    # Save ICO with common sizes
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(dst, sizes=sizes)
    print(f"Wrote {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

