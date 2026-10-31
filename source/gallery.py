# Блок «Галерея»: 4 стеклянные папки, внутри — фото.
# Порт компонента Glass Folder Cards на чистый HTML/CSS/JS.
#
# Как добавить реальные фото: положить файлы в assets/gallery/ и вписать путь
# вместо None, например ("Сборка ГРЩ", "gallery/sborka-1.jpg").
# Пока фото нет, показывается заглушка: фрагмент рендера шкафа.
# kind="doc" рисует лист документа; href — ссылка, которая откроется по клику.
import base64
import html
import mimetypes
import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
CERT = ('https://s3.reg.solutions/9671136a-65d2-4fae-b5e7-1a49fdd57bac/files/484757ef-da1c-4a05-b23d-bb9264df1064-'
        '%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82_%D0%B0%D0%BC%D0%BF%D0%B5%D1%80%D0%B0%D0%B6_'
        '%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE__2_.pdf')

FOLDERS = [
    {'label': 'Производство', 'meta': 'Цех в Королёве', 'art': 'ember', 'files': [
        {'name': 'Сборка ГРЩ', 'image': None},
        {'name': 'Монтаж шин', 'image': None},
        {'name': 'Испытания', 'image': None},
    ]},
    {'label': 'Готовые щиты', 'meta': 'ГРЩ, ВРУ, АВР', 'art': 'steel', 'files': [
        {'name': 'ГРЩ 0,4 кВ', 'image': None},
        {'name': 'ВРУ', 'image': None},
        {'name': 'Шкаф АВР', 'image': None},
    ]},
    {'label': 'На объектах', 'meta': 'Москва и регионы', 'art': 'dusk', 'files': [
        {'name': 'ЖК', 'image': None},
        {'name': 'Завод', 'image': None},
        {'name': 'ЦОД', 'image': None},
    ]},
    {'label': 'Документы', 'meta': 'Сертификат и паспорта', 'art': 'night', 'files': [
        {'name': 'Паспорт щита', 'kind': 'doc', 'meta': 'PDF'},
        {'name': 'Схемы', 'kind': 'doc', 'meta': 'PDF'},
        {'name': 'Сертификат', 'kind': 'doc', 'meta': 'PDF', 'href': CERT},
    ]},
]

W, H, HEADROOM = 340, 272, 54
FRONT_TOP = 74
FRONT_H = H - FRONT_TOP
BACK_PATH = ('M0 56A22 22 0 0 1 22 34L146 34C170 34 172 0 198 0L318 0A22 22 0 0 1 340 22L340 250'
             'A22 22 0 0 1 318 272L22 272A22 22 0 0 1 0 250Z')
FRONT_PATH = (f'M0 22A22 22 0 0 1 22 0L118 0C144 0 146 32 172 32L318 32A22 22 0 0 1 340 54L340 {FRONT_H - 22}'
              f'A22 22 0 0 1 318 {FRONT_H}L22 {FRONT_H}A22 22 0 0 1 0 {FRONT_H - 22}Z')

# где на рендере шкафа брать фрагмент для заглушки (background-position)
CROPS = ['18% 40%', '42% 55%', '70% 35%', '88% 60%', '30% 70%', '58% 30%', '12% 62%', '50% 48%', '80% 45%']


def _uri(rel):
    path = os.path.join(ASSETS, rel)
    mime = mimetypes.guess_type(path)[0] or 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def _sheet(f, i, n, crop):
    e = html.escape
    slot = 0 if n <= 1 else i / (n - 1) * 2 - 1
    depth = n - 1 - i
    jx = ((i * 37 + len(f['name']) * 13) % 11 - 5) * 0.9
    jr = ((i * 53 + len(f['name']) * 7) % 9 - 4) * 0.35
    style = f'--gf-slot:{slot:.3f};--gf-depth:{depth};--gf-jx:{jx:.1f}px;--gf-jr:{jr:.2f}deg;z-index:{i + 1}'
    meta = f'<span class="gf-sheet-meta">{e(f["meta"])}</span>' if f.get('meta') else ''
    head = f'<span class="gf-sheet-head"><span class="gf-sheet-name">{e(f["name"])}</span>{meta}</span>'
    if f.get('kind') == 'doc':
        body = '<span class="gf-lines" aria-hidden="true"><i style="width:70%"></i><i style="width:92%"></i><i style="width:84%"></i><i style="width:60%"></i><i style="width:88%"></i><i style="width:40%"></i></span>'
        cls = 'gf-sheet gf-sheet--doc'
    elif f.get('image'):
        body = f'<img class="gf-sheet-art" src="{_uri(f["image"])}" alt="{e(f["name"])}" loading="lazy" draggable="false">'
        cls = 'gf-sheet gf-sheet--art'
    else:
        body = f'<span class="gf-sheet-art gf-ph" style="background-position:{crop}" role="img" aria-label="{e(f["name"])}, фото появится позже"></span>'
        cls = 'gf-sheet gf-sheet--art'
    if f.get('href'):
        return f'<a class="{cls}" style="{style}" href="{e(f["href"])}" target="_blank" rel="noopener" role="listitem">{body}{head}</a>'
    return f'<button class="{cls}" style="{style}" type="button" data-name="{e(f["name"])}" role="listitem">{body}{head}</button>'


def build():
    e = html.escape
    out, k = [], 0
    for fi, fd in enumerate(FOLDERS):
        files = fd['files'][-4:]
        sheets = []
        for i, f in enumerate(files):
            sheets.append(_sheet(f, i, len(files), CROPS[k % len(CROPS)]))
            k += 1
        out.append(f'''<div class="gf-root rv" style="--i:{fi}" data-art="{fd['art']}">
  <div class="gf-stage">
    <div class="gf-tilt">
      <div class="gf-shadow" aria-hidden="true"></div>
      <div class="gf-back" style="clip-path:path('{BACK_PATH}')" aria-hidden="true"><div class="gf-art"></div><div class="gf-back-sheen"></div></div>
      <svg class="gf-rim gf-back-rim" viewBox="0 0 {W} {H}" aria-hidden="true"><path d="{BACK_PATH}"/></svg>
      <div class="gf-front" style="clip-path:path('{FRONT_PATH}')">
        <div class="gf-tint" aria-hidden="true"></div>
        <div class="gf-spec" aria-hidden="true"></div>
        <svg class="gf-rim gf-front-rim" viewBox="0 0 {W} {FRONT_H}" aria-hidden="true"><path d="{FRONT_PATH}"/></svg>
        <button type="button" class="gf-hit" aria-expanded="false" aria-label="Открыть папку «{e(fd['label'])}», файлов: {len(fd['files'])}"></button>
        <div class="gf-label"><span class="gf-title">{e(fd['label'])}</span><span class="gf-meta">{e(fd['meta'])}</span></div>
      </div>
      <div class="gf-files" role="list" aria-label="{e(fd['label'])}" inert>{''.join(sheets)}</div>
      <span class="gf-key" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg></span>
    </div>
  </div>
</div>''')
    return '\n'.join(out)


GALLERY = build()
