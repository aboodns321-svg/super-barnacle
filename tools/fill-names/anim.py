"""Estimate per-frame scale/center/opacity of the original text block."""
import numpy as np
R = (395, 640, 40, 536)

def moments(rgb):
    a = rgb[R[0]:R[1], R[2]:R[3]].astype(np.float32)
    y = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    d = np.clip(250 - y, 0, None)
    tot = d.sum()
    if tot < 500:
        return None
    yy, xx = np.mgrid[R[0]:R[1], R[2]:R[3]]
    cy = (d * yy).sum() / tot; cx = (d * xx).sum() / tot
    sy = np.sqrt((d * (yy - cy) ** 2).sum() / tot); sx = np.sqrt((d * (xx - cx) ** 2).sum() / tot)
    return dict(tot=tot, cx=cx, cy=cy, sx=sx, sy=sy)

def params(m, mf):
    """Transform mapping final-state coords to frame coords: p' = c + s (p - cf)."""
    if m is None:
        return None
    s = 0.5 * (m["sx"] / mf["sx"] + m["sy"] / mf["sy"])
    alpha = min(1.0, m["tot"] / (s * s * mf["tot"]))
    return dict(s=s, alpha=alpha, cx=m["cx"], cy=m["cy"])
