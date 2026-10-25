import os
from resvg_py import svg_to_bytes
from PIL import Image
import io

svg_path = r"F:\DEV\ethereal-desktop\build\icon.svg"
png_path = r"F:\DEV\ethereal-desktop\build\icon.png"
ico_path = r"F:\DEV\ethereal-desktop\build\icon.ico"

with open(svg_path, "r", encoding="utf-8") as f:
    svg_str = f.read()

# Render 512x512 PNG bytes using resvg
png_bytes = svg_to_bytes(svg_str, width=512, height=512)

with open(png_path, "wb") as f:
    f.write(png_bytes)

print(f"Saved {png_path} ({len(png_bytes)} bytes)")

# Open with Pillow to create multi-resolution Windows ICO
img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")

# Standard Windows icon sizes
icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
img.save(ico_path, format="ICO", sizes=icon_sizes)

print(f"Saved {ico_path} with sizes: {icon_sizes}")
