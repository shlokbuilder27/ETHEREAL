import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FFMPEG_PATH = r"C:\Users\hp\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
OUTPUT_DIR = r"F:\DEV\ethereal-desktop\assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)
MP4_OUTPUT = os.path.join(OUTPUT_DIR, "ethereal-showcase-30s.mp4")
GIF_OUTPUT = os.path.join(OUTPUT_DIR, "ethereal-promo.gif")

WIDTH, HEIGHT = 1280, 720
FPS = 30
TOTAL_DURATION = 30.0
TOTAL_FRAMES = int(TOTAL_DURATION * FPS) # 900 frames

# Fonts
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG_PATH = r"C:\Windows\Fonts\segoeui.ttf"
FONT_MONO_PATH = r"C:\Windows\Fonts\consola.ttf"

font_title_large = ImageFont.truetype(FONT_BOLD_PATH, 54)
font_title_med = ImageFont.truetype(FONT_BOLD_PATH, 38)
font_subtitle = ImageFont.truetype(FONT_REG_PATH, 22)
font_badge = ImageFont.truetype(FONT_BOLD_PATH, 16)
font_mono = ImageFont.truetype(FONT_MONO_PATH, 18)

# Load Images
icon_path = r"F:\DEV\ethereal-desktop\build\icon.png"
icon_img = Image.open(icon_path).convert("RGBA") if os.path.exists(icon_path) else None

screens_dir = os.path.join(OUTPUT_DIR, "screenshots")
screens = {
    "dashboard": Image.open(os.path.join(screens_dir, "01_hero_dashboard.png")).convert("RGBA"),
    "radar": Image.open(os.path.join(screens_dir, "02_radar_biometrics.png")).convert("RGBA"),
    "focus": Image.open(os.path.join(screens_dir, "03_focus_protocol.png")).convert("RGBA"),
    "calendar": Image.open(os.path.join(screens_dir, "04_calendar_schedule.png")).convert("RGBA"),
    "nutrition": Image.open(os.path.join(screens_dir, "05_nutrition_matrix.png")).convert("RGBA"),
    "ai": Image.open(os.path.join(screens_dir, "06_ai_coach.png")).convert("RGBA"),
    "profile": Image.open(os.path.join(screens_dir, "07_profile_biometrics.png")).convert("RGBA"),
}

def draw_hud_badge(draw, text, x, y, bg_color=(16, 185, 129, 210), border_color=(52, 211, 153, 255)):
    bbox = draw.textbbox((0, 0), text, font=font_badge)
    w = bbox[2] - bbox[0] + 28
    h = bbox[3] - bbox[1] + 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=bg_color, outline=border_color, width=1)
    draw.text((x + 14, y + 6), text, font=font_badge, fill=(255, 255, 255, 255))
    return w, h

def zoom_and_crop(img, scale, center_x_pct=0.5, center_y_pct=0.5):
    # Scale and crop to WIDTH x HEIGHT
    orig_w, orig_h = img.size
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    resized = img.resize((new_w, new_h), Image.Resampling.BILINEAR)

    cx = int(new_w * center_x_pct)
    cy = int(new_h * center_y_pct)

    left = max(0, min(cx - WIDTH // 2, new_w - WIDTH))
    top = max(0, min(cy - HEIGHT // 2, new_h - HEIGHT))
    right = left + WIDTH
    bottom = top + HEIGHT

    return resized.crop((left, top, right, bottom))

print(f"Starting 30s motion graphics generation: {TOTAL_FRAMES} frames @ {FPS}fps...")

ffmpeg_cmd = [
    FFMPEG_PATH,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgba",
    "-r", str(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "veryfast",
    "-crf", "19",
    MP4_OUTPUT
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

gif_frames = []

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / FPS
    frame = Image.new("RGBA", (WIDTH, HEIGHT), (4, 9, 7, 255))
    draw = ImageDraw.Draw(frame)

    # SCENE 1: Intro (0.0s - 4.5s)
    if t < 4.5:
        p = t / 4.5
        # Background subtle ambient glow
        glow_size = int(200 + p * 150)
        draw.ellipse([WIDTH//2 - glow_size, HEIGHT//2 - glow_size, WIDTH//2 + glow_size, HEIGHT//2 + glow_size],
                     fill=(16, 185, 129, int(35 + 15 * math.sin(p * math.pi))))

        # Animated Icon Zoom in
        icon_scale = min(1.0, 0.4 + p * 0.7)
        if icon_img:
            ic_size = int(220 * icon_scale)
            ic_resized = icon_img.resize((ic_size, ic_size), Image.Resampling.BILINEAR)
            frame.paste(ic_resized, (WIDTH//2 - ic_size//2, HEIGHT//2 - ic_size//2 - 60), ic_resized)

        # Title Fade & Slide
        alpha = min(255, int(p * 350))
        title_y = int(HEIGHT//2 + 90 - (1 - min(1.0, p*1.5)) * 30)
        draw.text((WIDTH//2 - 130, title_y), "ETHEREAL", font=font_title_large, fill=(255, 255, 255, alpha))

        sub_text = "THE ULTIMATE SLEEPER BUILD PROTOCOL"
        bbox_sub = draw.textbbox((0, 0), sub_text, font=font_subtitle)
        draw.text((WIDTH//2 - (bbox_sub[2]-bbox_sub[0])//2, title_y + 65), sub_text, font=font_subtitle, fill=(167, 243, 208, alpha))

        draw_hud_badge(draw, "⚡ DESKTOP PROTOCOL ENGINE", 50, 45)
        draw_hud_badge(draw, "🌿 NATURE x BIOMECHANICS", WIDTH - 270, 45)

    # SCENE 2: Liquid Glass Dashboard & Alpine Biome (4.5s - 9.0s)
    elif t < 9.0:
        p = (t - 4.5) / 4.5
        # Zoom In from 1.05 to 1.35 into workout tracker
        scale = 1.05 + (p * 0.30)
        cx = 0.5 + p * 0.08
        cy = 0.45 + p * 0.05
        bg = zoom_and_crop(screens["dashboard"], scale, cx, cy)
        frame.paste(bg, (0, 0))

        # Bottom HUD overlay
        overlay = Image.new("RGBA", (WIDTH, 140), (7, 19, 14, 210))
        frame.paste(overlay, (0, HEIGHT - 140), overlay)
        d_hud = ImageDraw.Draw(frame)

        draw_hud_badge(d_hud, "FEATURE 01 // PURE LIQUID GLASS", 50, HEIGHT - 118)
        d_hud.text((50, HEIGHT - 76), "Alpine Meadow Backdrops & Sleeper Volume Matrix", font=font_title_med, fill=(255, 255, 255))
        d_hud.text((WIDTH - 380, HEIGHT - 90), "• Zero Solid Boxy Cards\n• Full Transparency Dynamics\n• Real-Time Workout Heatmap", font=font_mono, fill=(167, 243, 208))

    # SCENE 3: Biomechanical Radar & Mist Peaks (9.0s - 13.5s)
    elif t < 13.5:
        p = (t - 9.0) / 4.5
        # Zoom Out from 1.30 to 1.05 centered on radar
        scale = 1.30 - (p * 0.25)
        cx = 0.55 - p * 0.05
        cy = 0.50
        bg = zoom_and_crop(screens["radar"], scale, cx, cy)
        frame.paste(bg, (0, 0))

        overlay = Image.new("RGBA", (WIDTH, 140), (7, 19, 14, 210))
        frame.paste(overlay, (0, HEIGHT - 140), overlay)
        d_hud = ImageDraw.Draw(frame)

        draw_hud_badge(d_hud, "FEATURE 02 // MULTI-AXIS RADAR", 50, HEIGHT - 118)
        d_hud.text((50, HEIGHT - 76), "Biomechanical Symmetry & Sleeper Score", font=font_title_med, fill=(255, 255, 255))
        d_hud.text((WIDTH - 380, HEIGHT - 90), "• Upper / Lower / Core / Cardio\n• Real-Time Radar Polygon\n• Granite Mist Dynamic Scene", font=font_mono, fill=(167, 243, 208))

    # SCENE 4: Ambient Audio & Deep Focus (13.5s - 18.0s)
    elif t < 18.0:
        p = (t - 13.5) / 4.5
        # Zoom in on Focus Pomodoro & Audio synthesizer
        scale = 1.08 + (p * 0.28)
        cx = 0.50 + p * 0.05
        cy = 0.48 + p * 0.06
        bg = zoom_and_crop(screens["focus"], scale, cx, cy)
        frame.paste(bg, (0, 0))

        overlay = Image.new("RGBA", (WIDTH, 140), (7, 19, 14, 210))
        frame.paste(overlay, (0, HEIGHT - 140), overlay)
        d_hud = ImageDraw.Draw(frame)

        draw_hud_badge(d_hud, "FEATURE 03 // BINAURAL SYNTHESIZER", 50, HEIGHT - 118)
        d_hud.text((50, HEIGHT - 76), "Nature Soundscapes & Deep Focus Pomodoro", font=font_title_med, fill=(255, 255, 255))
        d_hud.text((WIDTH - 380, HEIGHT - 90), "• Alpine Wind & Forest Rain\n• High-State Alpha Brainwaves\n• Floating Cursor Air Breeze", font=font_mono, fill=(167, 243, 208))

    # SCENE 5: Precision Bio-Fuel & AI Protocol Coach (18.0s - 22.5s)
    elif t < 22.5:
        p = (t - 18.0) / 4.5
        if p < 0.5:
            scale = 1.10 + p * 0.25
            bg = zoom_and_crop(screens["nutrition"], scale, 0.48, 0.45)
        else:
            scale = 1.25 - (p - 0.5) * 0.25
            bg = zoom_and_crop(screens["ai"], scale, 0.52, 0.48)
        frame.paste(bg, (0, 0))

        overlay = Image.new("RGBA", (WIDTH, 140), (7, 19, 14, 210))
        frame.paste(overlay, (0, HEIGHT - 140), overlay)
        d_hud = ImageDraw.Draw(frame)

        draw_hud_badge(d_hud, "FEATURE 04 // BIO-FUEL & AI COACH", 50, HEIGHT - 118)
        d_hud.text((50, HEIGHT - 76), "Precision Macro Calculator & Adaptive Advisor", font=font_title_med, fill=(255, 255, 255))
        d_hud.text((WIDTH - 380, HEIGHT - 90), "• Surplus/Deficit Optimization\n• High Mountain Spring Biome\n• Starry Ridge AI Intelligence", font=font_mono, fill=(167, 243, 208))

    # SCENE 6: Desktop Power & Keep-Awake Engine (22.5s - 26.5s)
    elif t < 26.5:
        p = (t - 22.5) / 4.0
        scale = 1.12 + p * 0.18
        bg = zoom_and_crop(screens["profile"], scale, 0.50, 0.48)
        frame.paste(bg, (0, 0))

        # Windows Native Desktop Badge
        draw_hud_badge(draw, "⚡ WINDOWS ELECTRON ~200MB APP", 50, 50, bg_color=(4, 120, 87, 230))

        overlay = Image.new("RGBA", (WIDTH, 140), (7, 19, 14, 210))
        frame.paste(overlay, (0, HEIGHT - 140), overlay)
        d_hud = ImageDraw.Draw(frame)

        draw_hud_badge(d_hud, "FEATURE 05 // ALWAYS-ON POWER ENGINE", 50, HEIGHT - 118)
        d_hud.text((50, HEIGHT - 76), "Native Keep-Awake Lock // Zero Screen Sleep", font=font_title_med, fill=(255, 255, 255))
        d_hud.text((WIDTH - 380, HEIGHT - 90), "• prevent-display-sleep Enabled\n• 100% Offline & Private\n• Zero Background Throttling", font=font_mono, fill=(167, 243, 208))

    # SCENE 7: Outro & Call To Action (26.5s - 30.0s)
    else:
        p = (t - 26.5) / 3.5
        # Graceful dark fade with pulsing emblem
        fade_val = min(1.0, p * 1.5)
        glow_size = int(180 + math.sin(p * math.pi * 2) * 20)
        draw.ellipse([WIDTH//2 - glow_size, HEIGHT//2 - glow_size - 40, WIDTH//2 + glow_size, HEIGHT//2 + glow_size - 40],
                     fill=(16, 185, 129, int(45 * (1 - p*0.4))))

        if icon_img:
            ic_size = 200
            ic_resized = icon_img.resize((ic_size, ic_size), Image.Resampling.BILINEAR)
            frame.paste(ic_resized, (WIDTH//2 - ic_size//2, HEIGHT//2 - ic_size//2 - 60), ic_resized)

        draw.text((WIDTH//2 - 130, HEIGHT//2 + 90), "ETHEREAL", font=font_title_large, fill=(255, 255, 255))
        tag = "THE SLEEPER BUILD STANDARD // GITHUB REPOSITORY"
        bbox_t = draw.textbbox((0, 0), tag, font=font_subtitle)
        draw.text((WIDTH//2 - (bbox_t[2]-bbox_t[0])//2, HEIGHT//2 + 155), tag, font=font_subtitle, fill=(52, 211, 153))

        draw_hud_badge(draw, "★ STAR ON GITHUB // CLONE & BUILD TODAY", WIDTH//2 - 170, HEIGHT//2 + 200)

    # Convert to bytes and write to ffmpeg
    raw_bytes = frame.tobytes()
    proc.stdin.write(raw_bytes)

    # Sample frames for animated preview GIF (every 10 frames = 3 fps, 90 frames total)
    if frame_idx % 10 == 0:
        gif_thumb = frame.resize((640, 360), Image.Resampling.BILINEAR).convert("RGB")
        gif_frames.append(gif_thumb)

    if frame_idx % 90 == 0 or frame_idx == TOTAL_FRAMES - 1:
        print(f"Rendered frame {frame_idx + 1}/{TOTAL_FRAMES} ({(frame_idx+1)/TOTAL_FRAMES*100:.1f}%)")

proc.stdin.close()
proc.wait()
print(f"MP4 Video successfully generated: {MP4_OUTPUT}")

# Save GIF preview
if gif_frames:
    print(f"Saving animated preview GIF ({len(gif_frames)} frames)...")
    gif_frames[0].save(
        GIF_OUTPUT,
        save_all=True,
        append_images=gif_frames[1:],
        duration=333, # ~3 fps
        loop=0,
        optimize=True
    )
    print(f"GIF Preview successfully generated: {GIF_OUTPUT}")
