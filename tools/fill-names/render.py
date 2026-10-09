"""Re-render the video with the names filled in on the final slide."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image
import anim, block

src, ref_png, font, out = sys.argv[1:5]
W, H, START, SETTLE = 576, 1024, 2472, 2500
ref = Image.open(ref_png).convert("RGB")
layer, size = block.build(ref, font)
mf = anim.moments(np.asarray(ref))
print("font size", size, "final center", mf["cx"], mf["cy"], file=sys.stderr)

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf",
    "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"],
    stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
    "-i", src, "-map", "0:v", "-map", "1:a", "-c:a", "copy",
    "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
    "-movflags", "+faststart", out], stdin=subprocess.PIPE)

n = 0
fsz = W * H * 3
while True:
    buf = dec.stdout.read(fsz)
    if len(buf) < fsz:
        break
    if n >= START:
        frame = Image.frombuffer("RGB", (W, H), buf)
        bg = block.clean_bg(frame)
        if n >= SETTLE:
            lay = layer
        else:
            p = anim.params(anim.moments(np.asarray(frame)), mf)
            if p is None:
                lay = None
            else:
                s = p["s"]
                # inverse map: frame coords -> final-state coords
                a, b, c = 1 / s, 0, mf["cx"] - p["cx"] / s
                d, e, f = 0, 1 / s, mf["cy"] - p["cy"] / s
                lay = layer.transform((W, H), Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC)
                lay = lay.point(lambda v, al=p["alpha"]: int(v * al + 0.5))
        out_im = bg if lay is None else block.composite(bg, lay)
        buf = out_im.tobytes()
    enc.stdin.write(buf)
    n += 1
enc.stdin.close()
dec.wait(); enc.wait()
print("frames", n, file=sys.stderr)
sys.exit(enc.returncode)
