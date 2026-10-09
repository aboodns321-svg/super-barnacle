"""Build the replacement text block for the final slide."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

NAMES = ["فائزة البدراني", "هبه خشيم"]
# label+colon crops from the clean final frame: (y0, y1, x0, x1, baseline_y)
LABELS = [(490, 535, 226, 427, 519), (561, 612, 174, 479, 590)]
DY = -35          # move the two remaining lines up to re-center the block
CX = 287          # horizontal center of each line
GAP = 9           # name -> colon spacing (visible gap ~= original colon -> ؟؟؟)
ALEF_H = 23       # alef height in the original artwork (top -> baseline)
SS = 4            # supersampling for name rendering

def fit_size(font_path):
    lo, hi = 10, 80
    for size in range(lo, hi):
        f = ImageFont.truetype(font_path, size * SS)
        b = f.getbbox("ا", anchor="ls")
        if -b[1] / SS >= ALEF_H:
            return size
    return hi

def render_name(text, font_path, size):
    f = ImageFont.truetype(font_path, size * SS)
    l, t, r, b = f.getbbox(text, anchor="ls", direction="rtl")
    pad = 2 * SS
    W = r - l + 2 * pad; H = b - t + 2 * pad
    W += (-W) % SS; H += (-H) % SS
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).text((pad - l, pad - t), text, font=f, fill=255, anchor="ls", direction="rtl")
    im = im.resize((W // SS, H // SS), Image.LANCZOS)
    # baseline offset inside the downscaled image
    return im, (pad - t) / SS

def build(frame, font_path, size=None, scale_name=1.0):
    """Return (alpha L image of the whole 576x1024 text layer)."""
    size = size or fit_size(font_path)
    g = np.asarray(frame.convert("L")).astype(np.float32)
    layer = np.zeros(g.shape, np.float32)
    for (y0, y1, x0, x1, base), name in zip(LABELS, NAMES):
        lab = np.clip((252 - g[y0:y1, x0:x1]) / 252.0, 0, 1)
        nim, nbase = render_name(name, font_path, size)
        na = np.asarray(nim).astype(np.float32) / 255.0
        lw, nw = x1 - x0, na.shape[1]
        total = nw + GAP + lw
        left = int(round(CX - total / 2))
        # name on the left, label (with colon) on the right
        ny = int(round(base + DY - nbase))
        layer[ny:ny + na.shape[0], left:left + nw] = np.maximum(layer[ny:ny + na.shape[0], left:left + nw], na)
        lx = left + nw + GAP
        layer[y0 + DY:y1 + DY, lx:lx + lw] = np.maximum(layer[y0 + DY:y1 + DY, lx:lx + lw], lab)
    return Image.fromarray((layer * 255).astype(np.uint8)), size

def clean_bg(frame):
    a = np.asarray(frame.convert("RGB")).copy()
    a[395:640, 40:536] = 255
    return Image.fromarray(a)

def composite(bg, alpha_layer, color=(0, 0, 0)):
    a = np.asarray(bg.convert("RGB")).astype(np.float32)
    m = np.asarray(alpha_layer).astype(np.float32)[..., None] / 255.0
    out = a * (1 - m) + np.array(color, np.float32) * m
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8))
