# Фон для телефона: из широкой картинки города вырезается пустая середина,
# левая и правая части города сдвигаются друг к другу (стык прячется за шкафом).
# Запуск из корня репозитория: python3 scripts/city_mobile.py
import os
import numpy as np
from PIL import Image

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
src = np.asarray(Image.open(os.path.join(A, 'bg-city-src.webp')).convert('RGB')).astype(float)
H, W, _ = src.shape
cut0, cut1, b = int(W * 0.36), int(W * 0.64), 60
t = np.linspace(0, 1, b)[None, :, None]
seam = src[:, cut0:cut0 + b] * (1 - t) + src[:, cut1 - b:cut1] * t
out = np.concatenate([src[:, :cut0], seam, src[:, cut1:]], axis=1)
img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
img = img.resize((1100, round(1100 * img.height / img.width)), Image.LANCZOS)
img.save(os.path.join(A, 'bg-city-mobile.webp'), quality=82, method=6)
print('bg-city-mobile', img.size, os.path.getsize(os.path.join(A, 'bg-city-mobile.webp')) // 1024, 'KB', 'aspect', round(img.width / img.height, 3))
