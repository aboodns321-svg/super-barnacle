import cv2, numpy as np, sys
S = "/tmp/claude-0/-home-user-super-barnacle/35d16e81-df7f-5220-b9cf-59e4fb6d0b72/scratchpad"
plate = cv2.imread(f"{S}/slides/plate.png")
# title ghosts: steps 1-6/10/11 all have a (mostly hidden) title in the same spot, so the median keeps it;
# slide 14 has nothing above y=415, use it for the top part
plate[:400] = cv2.imread(f"{S}/slides/src_14.png")[:400]

# (slide, mode, x0, y0, x1, y1)  -- local coords in the 576x1024 frame
ROIS = {
 1:  [("plate", 55, 340, 530, 630)],
 2:  [("plate", 170, 258, 500, 335), ("plate", 140, 345, 510, 435)],
 3:  [("plate", 170, 258, 500, 335), ("plate", 330, 500, 545, 555)],
 4:  [("plate", 170, 258, 500, 335), ("plate", 355, 500, 520, 600)],
 5:  [("plate", 170, 258, 500, 335), ("plate", 330, 500, 548, 600)],
 6:  [("plate", 170, 258, 500, 335), ("plate", 325, 350, 520, 505)],
 7:  [("plate", 170, 258, 500, 335), ("plate", 395, 455, 570, 620)],
 8:  [("plate", 160, 320, 450, 394),
      ("white", 200, 402, 336, 471), ("white", 350, 468, 545, 503), ("thick", 316, 508, 545, 549)],
 9:  [("plate", 170, 320, 450, 405),
      ("white", 255, 422, 420, 446), ("white", 316, 466, 560, 548), ("white", 200, 548, 560, 660)],
 10: [("plate", 190, 258, 500, 345), ("inpaint", 186, 668, 450, 712)],
 11: [("plate", 170, 258, 560, 315), ("plate", 340, 450, 540, 640)],
 12: [("plate", 70, 330, 560, 655)],
 13: [("plate", 30, 305, 560, 360), ("plate", 30, 395, 560, 660)],
 14: [("plate", 70, 415, 500, 610)],
}

def smooth(m, r=1.4):
    return cv2.GaussianBlur(m.astype(np.float32), (0, 0), r)

def run(n):
    img = cv2.imread(f"{S}/slides/src_{n:02d}.png")
    out = img.astype(np.float32)
    pl = plate.astype(np.float32)
    for mode, x0, y0, x1, y1 in ROIS[n]:
        roi = np.zeros(img.shape[:2], bool); roi[y0:y1, x0:x1] = True
        K = lambda k: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
        if mode == "plate":
            d = np.abs(img.astype(int) - plate.astype(int)).max(2)
            m = ((d > 26) & roi).astype(np.uint8)
            m = cv2.dilate(m, K(9)) & roi
            a = smooth(m)[..., None]; a = np.clip(a * 1.6, 0, 1) * roi[..., None]
            out = out * (1 - a) + pl * a
        elif mode == "white":
            d = (255 - img.astype(int)).max(2)
            m = ((d > 24) & roi).astype(np.uint8)
            m = cv2.dilate(m, K(9)) & roi
            a = smooth(m)[..., None]; a = np.clip(a * 1.6, 0, 1) * roi[..., None]
            out = out * (1 - a) + 255.0 * a
        elif mode in ("inpaint", "thick"):
            g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if mode == "thick":
                m = ((g < 175) & roi).astype(np.uint8)
            else:
                mn = img.min(2)
                m = (((mn < 215) | ((img.max(2).astype(int) - mn) > 45)) & roi).astype(np.uint8)
            m = cv2.dilate(m, K(9)) & roi
            tmp = cv2.inpaint(np.clip(out, 0, 255).astype(np.uint8), (m * 255).astype(np.uint8), 5, cv2.INPAINT_TELEA).astype(np.float32)
            a = smooth(m)[..., None]; a = np.clip(a * 1.6, 0, 1)
            out = out * (1 - a) + tmp * a
    return np.clip(out + 0.5, 0, 255).astype(np.uint8)

if __name__ == "__main__":
    for n in (int(x) for x in sys.argv[1:]) or range(1, 15):
        cv2.imwrite(f"{S}/clean/c_{n:02d}.png", run(n))
