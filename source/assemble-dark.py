import base64,html,sys
sys.path.insert(0,'.')
def uri(p,m): return f'data:{m};base64,'+base64.b64encode(open(p,'rb').read()).decode()
ARROW='<svg viewBox="0 0 22 10" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 5h20M16 1l5 4-5 4"/></svg>'
objs=["Аэропорт Шереметьево","Стадион «Торпедо»","ТРЦ «Смоленский Пассаж»","АО «ВПК „НПО Машиностроения“»","Завод «СПГ Портовая»","Ермаковский ГОК","ЖК ЗИЛАРТ SPARK","ЖК Sky Garden","ЖК Ильинка 3/8","БЦ Dubinin’Sky","Депо «Южное»","Кинокластер «Кино №1»","Новосибирский металлургический завод","Больница ЦМСЧ № 141","Гольф-курорт «Шишкино»","Парк-отель «Бухта Коприно»","ЖК Одинбург","Супермаркет «Мираторг»","Московский эндокринный завод","Очистные сооружения, Геленджик"]
one=''.join(f'<span>{html.escape(o)}</span>' for o in objs)
two=''.join(f'<span aria-hidden="true">{html.escape(o)}</span>' for o in objs)

groups=[
 ("Жилые комплексы",["ЖК 1-й Нагатинский","ЖК 1-й Ясеневский (ГК ФСК)","ЖК EVO (DOGMA)","ЖК Sky Garden (ГК ФСК)","ЖК «Большая Семёрка»","ЖК «Глинки парк»","ЖК ЗИЛАРТ SPARK (Группа ЛСР)","ЖК «Ильинка 3/8» (Sminex)","Квартал «Белый мыс»","ЖК «Белый Grad»","ЖК «Ленинский»","ЖК «Новая Алексеевская роща» (ГК Гранель)","ЖК «Одинбург» (AFI Development)","ЖК «Шолохово»","МКД, пер. Мансуровский, 9"]),
 ("Промышленность и склады",["Завод «СПГ Портовая»","АО «ВПК „НПО Машиностроения“»","Ермаковский ГОК","Новосибирский металлургический завод им. Кузьмина","ФГУП «Московский эндокринный завод»","Склад металлоконструкций, Ступино","Склад производства ЩО, Мосводоканал","Склад «Рандеву», ул. Дубнинская","Логопарк, Софьино","Пневмокаркасное сооружение 18-33-9","Площадка выгрузки подкранового пути"]),
 ("Коммерческая недвижимость",["БЦ Dubinin’Sky","ТРЦ «Смоленский Пассаж»","Супермаркет «Мираторг»","Офис АО «БКИ СБ»","Конференц-зал, БЦ на ул. Двинцев","Учебный центр Matrinex, БЦ «Павловский»","Административное здание префектуры ЮАО"]),
 ("Транспорт и инфраструктура",["Аэропорт Шереметьево, ремонтная база","Депо «Южное» (АО «Мосинжпроект»)","Очистные сооружения, Геленджик","Зарядная станция для электромобилей, Новотушинский пр.","Паркинг, ул. Маршала Ерёменко","Воинская часть 3111"]),
 ("Гостиницы, спорт и культура",["Стадион «Торпедо» им. Э. Стрельцова","Парк-отель «Бухта Коприно»","Гольф-курорт «Шишкино»","Кинокластер «Кино №1»","Усадьба П. Ф. Митькова, объект культурного наследия","Резиденция, Сейшельские острова"]),
 ("Социальные объекты",["Больница ЦМСЧ № 141","Поликлиника на 750 посещений","Школа на 100 мест и детский сад на 170 мест","Школа № 12, Мытищи"]),
]
SPEC=''.join(f'<div class="spec-row" role="row"><div class="spec-cat" role="cell">{html.escape(g)}</div><div class="spec-n" role="cell">{len(l)}</div><ul class="spec-list" role="cell">'+''.join(f'<li>{html.escape(o)}</li>' for o in l)+'</ul></div>' for g,l in groups)
TOTAL=sum(len(l) for g,l in groups)

# stylized map
streets=[
 ('M-20,120 C200,140 420,90 860,150',14),('M-20,330 C240,300 520,360 860,320',18),
 ('M180,-20 C200,160 150,300 210,620',12),('M560,-20 C540,200 600,380 560,620',14),
 ('M-20,470 L860,420',10),('M380,-20 L420,620',9),('M700,-20 C690,200 720,400 760,620',8)]
m='<svg viewBox="0 0 840 520" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
m+='<rect width="840" height="520" fill="#0c1735"/>'
m+='<path d="M-10,560 C120,470 260,520 340,440 C420,360 520,430 620,380 C720,330 800,370 860,330 L860,560 Z" fill="#0f2148"/>'
m+='<rect x="430" y="160" width="110" height="140" rx="14" fill="#11263a"/><rect x="40" y="170" width="120" height="120" rx="14" fill="#11263a"/>'
import random; random.seed(3)
for gx in range(0,840,52):
  for gy in range(0,520,46):
    if random.random()<.55: m+=f'<rect x="{gx+8}" y="{gy+8}" width="{random.randint(18,34)}" height="{random.randint(16,28)}" rx="3" fill="#14224a"/>'
for d,w in streets:
  m+=f'<path d="{d}" stroke="#22346a" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
m+='<path d="M560,-20 C540,200 600,380 560,620" stroke="#f26a1b" stroke-opacity=".55" stroke-width="5" fill="none"/>'
m+='<text x="590" y="250" font-family="Jost,Manrope,sans-serif" font-size="14" font-weight="300" fill="#8f9cbc" transform="rotate(84 590 250)">ул. Советская</text>'
m+='<g transform="translate(548,214)"><circle r="46" fill="#f26a1b" opacity=".16"/><circle r="26" fill="#f26a1b" opacity=".22"/><path d="M0,0 C-16,-22 -20,-32 -20,-40 a20,20 0 1 1 40,0 c0,8 -4,18 -20,40z" fill="#f26a1b" stroke="#fff" stroke-width="3"/><circle cy="-40" r="7" fill="#fff"/></g>'
m+='</svg>'
t=open('template-dark.html').read()
for k,v in {'{{SCENE}}':uri('../assets/scene.webp','image/webp'),'{{LOGO}}':uri('../assets/logo-light.webp','image/webp'),'{{CAB_CLOSED}}':uri('../assets/cabinet-closed.webp','image/webp'),'{{CAB_OPEN}}':uri('../assets/cabinet-open.webp','image/webp'),'{{OBJECTS}}':one+two,'{{SPEC}}':SPEC,'{{TOTAL}}':str(TOTAL),'{{MAP}}':m,'{{ARROW}}':ARROW}.items():
  t=t.replace(k,v)
assert '{{' not in t
open('../amperazh-dark.html','w').write(t)
print(len(t))
