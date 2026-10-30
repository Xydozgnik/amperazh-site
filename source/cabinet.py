# builds two aligned SVG layers of a 3-section switchboard
X=[22,216,410]; W=188; T=44; B=520
def defs():
    return '''<defs>
<linearGradient id="gDoor" x1="0" x2="1"><stop offset="0" stop-color="#d7dbe0"/><stop offset=".18" stop-color="#eef0f2"/><stop offset=".8" stop-color="#e4e7ea"/><stop offset="1" stop-color="#c9ced4"/></linearGradient>
<linearGradient id="gFrame" x1="0" x2="1"><stop offset="0" stop-color="#b9bfc6"/><stop offset=".5" stop-color="#dfe2e6"/><stop offset="1" stop-color="#aeb5bd"/></linearGradient>
<linearGradient id="gCu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd2a1"/><stop offset=".35" stop-color="#e8873f"/><stop offset=".7" stop-color="#b85a22"/><stop offset="1" stop-color="#e9935a"/></linearGradient>
<linearGradient id="gCuV" x1="0" x2="1"><stop offset="0" stop-color="#ffd2a1"/><stop offset=".35" stop-color="#e8873f"/><stop offset=".7" stop-color="#b85a22"/><stop offset="1" stop-color="#e9935a"/></linearGradient>
<linearGradient id="gInner" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3346"/><stop offset="1" stop-color="#1a2131"/></linearGradient>
<linearGradient id="gDev" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a5262"/><stop offset="1" stop-color="#2c323d"/></linearGradient>
<radialGradient id="gGlow" cx=".5" cy=".3" r=".7"><stop offset="0" stop-color="#ff8a3d" stop-opacity=".35"/><stop offset="1" stop-color="#ff8a3d" stop-opacity="0"/></radialGradient>
<symbol id="mcb" viewBox="0 0 12 34"><rect width="12" height="34" rx="1" fill="#eceef1"/><rect x="3" y="11" width="6" height="12" rx="1" fill="#2b3240"/><rect x="4" y="12" width="4" height="5" fill="#f26a1b"/><rect y="0" width="12" height="3" fill="#c3c8cf"/><rect y="31" width="12" height="3" fill="#c3c8cf"/></symbol>
<symbol id="mccb" viewBox="0 0 84 54"><rect width="84" height="54" rx="3" fill="url(#gDev)"/><rect x="6" y="6" width="72" height="10" rx="1" fill="#1b2029"/><rect x="34" y="21" width="16" height="22" rx="2" fill="#11151c"/><rect x="37" y="23" width="10" height="10" rx="1" fill="#f26a1b"/><circle cx="14" cy="38" r="3" fill="#9aa3b0"/><circle cx="70" cy="38" r="3" fill="#9aa3b0"/></symbol>
</defs>'''

def frame():
    s=f'<rect x="14" y="30" width="592" height="16" rx="3" fill="url(#gFrame)"/>'
    s+=f'<rect x="14" y="518" width="592" height="30" rx="2" fill="#5d6673"/><rect x="14" y="518" width="592" height="6" fill="#77808c"/>'
    for x in X:
        s+=f'<rect x="{x-6}" y="{T}" width="{W+12}" height="{B-T}" fill="#b4bac2"/>'
    return s

def closed():
    s=''
    for i,x in enumerate(X):
        dx,dy,dw,dh=x+2,T+6,W-4,B-T-12
        s+=f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="3" fill="url(#gDoor)" stroke="#a7aeb7"/>'
        s+=f'<rect x="{dx+8}" y="{dy+8}" width="{dw-16}" height="{dh-16}" rx="2" fill="none" stroke="#ffffff" stroke-opacity=".55"/>'
        # handle
        hx=dx+dw-22 if i!=1 else dx+12
        s+=f'<rect x="{hx}" y="{dy+200}" width="10" height="58" rx="3" fill="#3a404a"/><rect x="{hx+3}" y="{dy+214}" width="4" height="14" rx="1" fill="#8b939e"/>'
        # warning triangle
        s+=f'<path d="M{dx+22},{dy+40} l12,-21 l12,21 z" fill="#f4c430" stroke="#1c2230" stroke-width="1.5"/><path d="M{dx+35},{dy+25} l-3,7 h4 l-3,7" fill="none" stroke="#1c2230" stroke-width="1.6"/>'
        # nameplate
        s+=f'<rect x="{dx+dw/2-40}" y="{dy+66}" width="80" height="22" rx="2" fill="#ffffff" stroke="#9aa2ad"/><text x="{dx+dw/2}" y="{dy+81}" text-anchor="middle" font-family="IBM Plex Sans Condensed,Arial Narrow,sans-serif" font-size="10" fill="#1b2f6b">ГРЩ-1.{i+1}</text>'
        # louvres
        for k in range(5):
            s+=f'<rect x="{dx+dw/2-34}" y="{dy+dh-58+k*9}" width="68" height="4" rx="2" fill="#aab1ba"/>'
    # middle door instruments
    mx=X[1]+W/2
    for k,c in enumerate(['#f26a1b','#f6f7f9','#2a8a4a']):
        s+=f'<circle cx="{mx-28+k*28}" cy="{T+120}" r="8" fill="{c}" stroke="#4a5160" stroke-width="2"/>'
    for k in range(2):
        s+=f'<rect x="{mx-60+k*64}" y="{T+146}" width="56" height="40" rx="3" fill="#2d3442"/><rect x="{mx-54+k*64}" y="{T+152}" width="44" height="18" fill="#9fd3b0"/><text x="{mx-32+k*64}" y="{T+165}" text-anchor="middle" font-family="IBM Plex Sans Condensed,Arial Narrow,sans-serif" font-size="10" fill="#14321f">{["400 V","1250 A"][k]}</text>'
    return s

def inner():
    s=''
    for i,x in enumerate(X):
        s+=f'<rect x="{x}" y="{T}" width="{W}" height="{B-T}" fill="url(#gInner)"/>'
        s+=f'<rect x="{x}" y="{T}" width="{W}" height="{B-T}" fill="url(#gGlow)"/>'
        # perforated rails
        for rx in (x+6,x+W-12):
            s+=f'<rect x="{rx}" y="{T+4}" width="6" height="{B-T-8}" fill="#8e97a4"/>'
            s+=f'<line x1="{rx+3}" y1="{T+8}" x2="{rx+3}" y2="{B-8}" stroke="#2a3346" stroke-width="2.4" stroke-dasharray="3 6"/>'
    # main horizontal busbars across all sections
    for k,y in enumerate([64,80,96,112]):
        s+=f'<rect x="{X[0]+10}" y="{y}" width="{X[2]+W-X[0]-20}" height="9" rx="1.5" fill="url(#gCu)"/>'
        if k==3: s+=f'<rect x="{X[0]+10}" y="{y+3}" width="{X[2]+W-X[0]-20}" height="3" fill="#2f6fd1" opacity=".9"/>'
    # insulators
    for x in [X[0]+40,X[1]+40,X[1]+W-40,X[2]+W-40]:
        s+=f'<rect x="{x-5}" y="58" width="10" height="70" rx="2" fill="#c9442a" opacity=".85"/>'
    # section 1: drops to ACB
    x=X[0]
    for k in range(3):
        bx=x+56+k*28
        s+=f'<rect x="{bx}" y="64" width="10" height="150" fill="url(#gCuV)"/>'
    s+=f'<rect x="{x+28}" y="210" width="132" height="128" rx="5" fill="url(#gDev)" stroke="#11151c" stroke-width="2"/>'
    s+=f'<rect x="{x+40}" y="222" width="108" height="34" rx="2" fill="#11151c"/><rect x="{x+48}" y="230" width="36" height="18" fill="#f26a1b"/><rect x="{x+92}" y="230" width="48" height="18" fill="#2b3240"/>'
    s+=f'<circle cx="{x+62}" cy="{290}" r="12" fill="#2a8a4a"/><circle cx="{x+126}" cy="{290}" r="12" fill="#c9302c"/><text x="{x+94}" y="{326}" text-anchor="middle" font-family="IBM Plex Sans Condensed,Arial Narrow,sans-serif" font-size="10" fill="#c6ccd5">ACB 1600A</text>'
    for k in range(3):
        bx=x+56+k*28
        s+=f'<rect x="{bx}" y="338" width="10" height="120" fill="url(#gCuV)"/>'
        s+=f'<path d="M{bx+5},458 C{bx+5},490 {bx-10+k*6},500 {bx-10+k*6},520" stroke="#0d0f14" stroke-width="12" fill="none" stroke-linecap="round"/>'
    # section 2: ATS + DIN rows
    x=X[1]
    for k in range(3):
        bx=x+60+k*24
        s+=f'<rect x="{bx}" y="64" width="8" height="70" fill="url(#gCuV)"/>'
    for k in range(2):
        cx=x+30+k*70
        s+=f'<rect x="{cx}" y="140" width="58" height="74" rx="4" fill="url(#gDev)" stroke="#11151c"/><rect x="{cx+10}" y="152" width="38" height="12" fill="#11151c"/><rect x="{cx+22}" y="176" width="14" height="26" rx="2" fill="#f26a1b"/>'
    s+=f'<text x="{x+W/2}" y="232" text-anchor="middle" font-family="IBM Plex Sans Condensed,Arial Narrow,sans-serif" font-size="10" fill="#c6ccd5">АВР</text>'
    for r,y in enumerate([252,318,384]):
        s+=f'<rect x="{x+16}" y="{y+14}" width="{W-32}" height="6" fill="#aab3c0"/>'
        for k in range(11):
            s+=f'<use href="#mcb" x="{x+20+k*13.6}" y="{y}" width="12" height="34"/>'
        # wiring comb
        s+=f'<path d="M{x+22},{y+38} H{x+W-22}" stroke="#2f6fd1" stroke-width="2"/>'
    for k in range(6):
        s+=f'<path d="M{x+30+k*26},420 C{x+30+k*26},470 {x+60+k*12},480 {x+60+k*12},520" stroke="{["#0d0f14","#2f6fd1","#0d0f14","#c9a227","#0d0f14","#2f6fd1"][k]}" stroke-width="5" fill="none"/>'
    # section 3: riser + MCCBs
    x=X[2]
    for k in range(3):
        bx=x+22+k*14
        s+=f'<rect x="{bx}" y="64" width="9" height="420" fill="url(#gCuV)"/>'
    for k in range(6):
        y=140+k*60
        s+=f'<use href="#mccb" x="{x+76}" y="{y}" width="84" height="54"/>'
        s+=f'<rect x="{x+60}" y="{y+22}" width="18" height="6" fill="url(#gCu)"/>'
        s+=f'<path d="M{x+160},{y+27} C{x+176},{y+27} {x+172},{y+40} {x+172},{y+60}" stroke="#0d0f14" stroke-width="6" fill="none"/>'
    s+=f'<path d="M{x+172},470 V520" stroke="#0d0f14" stroke-width="14"/>'
    return s

def svg(content,cls):
    return f'<svg class="{cls}" viewBox="0 0 620 560" role="img" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">{content}</svg>'

D=defs()
CLOSED=svg(D+frame()+closed(),'cab cab-closed')
INNER=svg(frame()+inner(),'cab cab-inner')
REFLECT=f'<svg class="cab-refl" viewBox="0 0 620 560" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">{frame()}{closed()}</svg>'
