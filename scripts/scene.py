# Ночная сцена первого экрана, разложенная на слои для параллакса:
#   layer-sky.webp   — небо, звёзды, свечение у горизонта (непрозрачный)
#   layer-far.webp   — дальний хребет (прозрачный выше гребня)
#   layer-near.webp  — ближний хребет (прозрачный выше гребня)
#   layer-water.webp — вода с отражением (прозрачная выше горизонта)
# Все слои одного размера и при наложении дают исходную картинку.
# Запуск из корня репозитория: python3 scripts/scene.py
import os
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
W, H = 2400, 1350
HZ = int(H * 0.56)
OUT_W = 1920
rng = np.random.default_rng(21)
x = np.linspace(0, 1, W)
yy = np.arange(H)[:, None]


def c(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def fbm(n, octaves=7, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros(n)
    for o in range(octaves):
        k = 2 ** o
        pts = r.normal(0, 1, k + 2)
        out += np.interp(np.linspace(0, k, n), np.arange(k + 2), pts) / (1.9 ** o)
    return out


def ridge(seed, peak_l, peak_r, base, amp, valley=0.36):
    """Хребет с V-образной долиной в центре; возвращает y гребня для каждого x."""
    n = fbm(W, 11, seed)
    shape = np.where(x < 0.5,
                     peak_l * np.clip(1 - x / valley, 0, 1) ** 1.25,
                     peak_r * np.clip(1 - (1 - x) / valley, 0, 1) ** 1.25)
    return base - np.maximum(shape + n * amp * np.maximum(shape, 0.03)
                             + fbm(W, 11, seed + 50) * 0.012 * (shape > 0.01), 0)


far = ridge(3, 0.30, 0.26, HZ / H - 0.005, 0.16, 0.46) * H
near = ridge(7, 0.50, 0.44, HZ / H + 0.002, 0.22, 0.33) * H

# --- небо
sky = np.zeros((H, W, 3))
t = (yy / HZ).clip(0, 1)
for i in range(3):
    sky[..., i] = (c('#070d1f')[i] * (1 - t) + c('#22355f')[i] * t)[:, 0][:, None]
glow = np.exp(-(((x[None, :] - 0.5) / 0.22) ** 2) - (((yy - HZ) / (H * 0.18)) ** 2))
sky += glow[..., None] * c('#3b4f80') * 0.45
stars = rng.random((H, W)) > 0.9993
sky[stars & (yy < HZ * 0.7)] = [200, 210, 235]
sky = gaussian_filter(sky, (0.6, 0.6, 0))
sky += np.exp(-((yy - HZ) / (H * 0.05)) ** 2)[..., None] * c('#2a3d6b') * 0.25


def paint(rid, col_dark, col_lit, snow_amt, seed):
    """Склон хребта со снегом; ниже горизонта продолжается тёмным, чтобы при сдвиге не было щели."""
    sm = gaussian_filter(rid, 2)
    lit = np.clip(np.abs(np.gradient(sm)) * 0.55 + 0.1, 0, 1)
    r = np.random.default_rng(seed)
    g1 = gaussian_filter(r.normal(0, 1, (H, W)), (14, 1.6))
    g2 = gaussian_filter(r.normal(0, 1, (H, W)), (4, 4))
    depth = np.clip((yy - rid[None, :]) / 260, 0, 1)
    snow = np.clip(lit[None, :] * 1.1 + g1 * 0.9 + g2 * 0.25 - 0.35 - depth * 0.9, 0, 1) ** 1.4 * snow_amt
    mask = (yy >= rid[None, :]).astype(float)
    rim = np.exp(-((yy - rid[None, :]) / 3.0) ** 2) * mask * np.clip(lit[None, :] + 0.2, 0, 1)
    col = col_dark[None, None, :] * (1 - snow[..., None]) + col_lit[None, None, :] * snow[..., None]
    col = col + rim[..., None] * col_lit * 0.6
    col += np.exp(-((yy - HZ) / (H * 0.05)) ** 2)[..., None] * c('#2a3d6b') * 0.25  # дымка у горизонта
    alpha = gaussian_filter(mask, 0.7)
    return col, alpha


far_col, far_a = paint(far, c('#121d3a'), c('#4a5f8e'), 0.55, 11)
near_col, near_a = paint(near, c('#0a1124'), c('#8ea3cc'), 0.9, 12)

# --- сводная картинка выше горизонта (для отражения в воде)
comp = sky.copy()
for col, a in ((far_col, far_a), (near_col, near_a)):
    comp = comp * (1 - a[..., None]) + col * a[..., None]

# --- вода: отражение верхней части с рябью
rh = H - HZ
refl = comp[:HZ][::-1][:rh]
ry = np.arange(rh)[:, None]
wob = gaussian_filter(rng.normal(0, 1, (rh, W // 6)), (1.2, 10))
wob = np.array(Image.fromarray(wob.astype(np.float32)).resize((W, rh), Image.BICUBIC))
dx = wob * (4 + ry * 0.06)
dy = np.abs(wob) * (1 + ry * 0.02)
Y, X = np.mgrid[0:rh, 0:W].astype(float)
out = np.stack([map_coordinates(refl[..., k], [np.clip(Y + dy, 0, rh - 1), np.clip(X + dx, 0, W - 1)], order=1)
                for k in range(3)], -1)
out = gaussian_filter(out, (1.5, 4, 0))
fade = np.exp(-ry / (rh * 0.9))
water = out * (0.55 * fade[..., None] + 0.12) + c('#08112a') * (1 - fade[..., None]) * 0.9
lines = gaussian_filter(rng.normal(0, 1, (rh, W // 10)), (0.6, 25))
lines = np.array(Image.fromarray(lines.astype(np.float32)).resize((W, rh), Image.BICUBIC))
water += np.clip(lines, 0, None)[..., None] * c('#3c5486') * 0.35 * fade[..., None]
streak = np.exp(-(((x[None, :] - 0.5) / 0.05) ** 2)) * np.exp(-ry / (rh * 0.55))
water += (streak * (0.6 + 0.4 * np.clip(lines * 1.5 + 0.5, 0, 1)))[..., None] * c('#ff8a3d') * 0.42

water_full = np.zeros((H, W, 3))
water_full[HZ:] = water
water_full += np.exp(-((yy - HZ) / 2.5) ** 2)[..., None] * c('#6f86b8') * 0.35  # светлая линия горизонта
water_a = np.clip((yy - (HZ - 3)) / 4, 0, 1) * np.ones((1, W))

# --- лёгкий шум, чтобы не было полос на градиентах
def grain(a):
    return a + rng.normal(0, 1.2, a.shape)


def save(rgb, alpha, name, q=80):
    rgb = np.clip(grain(rgb), 0, 255).astype(np.uint8)
    if alpha is None:
        im = Image.fromarray(rgb)
    else:
        im = Image.fromarray(np.dstack([rgb, (np.clip(alpha, 0, 1) * 255).astype(np.uint8)]), 'RGBA')
    im = im.resize((OUT_W, round(OUT_W * H / W)), Image.LANCZOS)
    im.save(os.path.join(OUT, name), 'WEBP', quality=q, method=6)
    print(name, os.path.getsize(os.path.join(OUT, name)) // 1024, 'KB')


save(sky, None, 'layer-sky.webp')
save(far_col, far_a, 'layer-far.webp')
save(near_col, near_a, 'layer-near.webp')
save(water_full, water_a, 'layer-water.webp')
print('horizon fraction', HZ / H)
