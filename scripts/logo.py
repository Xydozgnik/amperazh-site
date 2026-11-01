# Пересобирает светлую версию логотипа из оригинала (тёмно-синий + оранжевый на светлом фоне):
# фон -> прозрачный, тёмно-синее -> белое, оранжевое остаётся оранжевым. Края без ореолов.
# Запуск из корня репозитория: python3 scripts/logo.py
import os
import numpy as np
from PIL import Image, ImageFilter

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
src = Image.open(os.path.join(A, 'logo-original.jfif')).convert('RGB')
SCALE = 3                                   # рисуем крупнее, чтобы края были гладкими
big = src.resize((src.width * SCALE, src.height * SCALE), Image.LANCZOS)
p = np.asarray(big).astype(float)

# цвет фона — медиана по краям картинки
edge = np.concatenate([p[:20].reshape(-1, 3), p[-20:].reshape(-1, 3)])
bg = np.median(edge, 0)

# «color to alpha»: насколько пиксель отличается от фона
diff = bg - p                               # фон светлый, всё нарисованное темнее
alpha = np.clip(diff.max(2) / bg.max(), 0, 1)
alpha = np.clip((alpha - 0.10) / 0.55, 0, 1)  # срезаем шум JPEG и усиливаем

r, g, b = p[..., 0], p[..., 1], p[..., 2]
orange = (r - b > 70) & (r > 150)
# мягкая маска оранжевого, чтобы не было ступенек на границе цветов
om = np.asarray(Image.fromarray((orange * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(float)[..., None] / 255
ORANGE = np.array([250, 84, 14], float)
WHITE = np.array([246, 248, 252], float)
rgb = WHITE * (1 - om) + ORANGE * om
# у оранжевого альфа всегда полная (внутри букв нет полупрозрачности)
alpha = np.maximum(alpha, om[..., 0])

# тонкие светлые дорожки внутри молнии: всё светлое внутри контура молнии делаем белым и непрозрачным
from scipy import ndimage
lab, n = ndimage.label(orange)
sizes = ndimage.sum(orange, lab, range(1, n + 1))
bolt = lab == (int(np.argmax(sizes)) + 1)            # самая большая оранжевая область — молния
inside = ndimage.binary_fill_holes(ndimage.binary_closing(bolt, iterations=6 * SCALE)) & ~bolt
region = ndimage.binary_fill_holes(ndimage.binary_closing(bolt, iterations=6 * SCALE))
light = region & (g > 120) & (r > 200)
lm = np.asarray(Image.fromarray((light * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(float)[..., None] / 255
rgb = rgb * (1 - lm) + np.array([255, 196, 160], float) * lm
alpha = np.maximum(alpha, inside.astype(float))

out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
im = Image.fromarray(out, 'RGBA')
bbox = im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox()
pad = 6 * SCALE
im = im.crop((bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad))
im.save(os.path.join(A, 'logo-light-big.png'))                              # крупная версия для печати и соцсетей
im = im.resize((round(im.width * 260 / im.height), 260), Image.LANCZOS)  # на сайте логотип до ~60px высотой: запас под 4×
im.save(os.path.join(A, 'logo-light.webp'), 'WEBP', quality=92, alpha_quality=100, method=6)
im.save(os.path.join(A, 'logo-light.png'))
print('logo-light', im.size, os.path.getsize(os.path.join(A, 'logo-light.webp')) // 1024, 'KB')
