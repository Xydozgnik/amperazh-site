# Вырезает фото шкафа из белого фона: два совпадающих кадра (закрытый и открытый) -> webp с прозрачностью.
# В открытом кадре белый фон, видный сквозь проёмы, заменяется тёмной глубиной шкафа.
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

SRC = '../assets/'
X0, X1, Y0, Y1 = 92, 1910, 288, 1572   # кадр вокруг шкафа (исходник 2000x2000)
W_OUT = 1400
DEEP = np.array([9, 15, 34], float)     # цвет глубины шкафа

def load(n):
    return np.asarray(Image.open(SRC + n).convert('RGB')).astype(float)

op, cl = load('cabinet-open-src.webp'), load('cabinet-closed-src.webp')

# силуэт по закрытому кадру: всё, что не белое, плюс заливка дыр
m = cl.min(2) < 236
m[Y1 - 3:, :] = False
m = ndimage.binary_closing(m, iterations=3)
m = ndimage.binary_fill_holes(m)
lab, n = ndimage.label(m)
m = lab == (np.bincount(lab.ravel())[1:].argmax() + 1)
alpha = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))

# открытый: белый фон в проёмах -> тёмная глубина (мягкий переход)
mn = op.min(2); sat = op.max(2) - mn
t = np.clip((mn - 214) / 30, 0, 1) * np.clip(1 - sat / 40, 0, 1)
t = ndimage.gaussian_filter(t, 1.0)[..., None]
inner = op * (1 - t) + DEEP * t

def save(arr, name):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')
    im.putalpha(alpha)
    im = im.crop((X0, Y0, X1, Y1))
    im = im.resize((W_OUT, round(W_OUT * (Y1 - Y0) / (X1 - X0))), Image.LANCZOS)
    im.save(SRC + name, 'WEBP', quality=86, method=6)
    print(name, im.size)

save(cl, 'cabinet-closed.webp')
save(inner, 'cabinet-open.webp')
