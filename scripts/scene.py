import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates
W,H=2400,1350; HZ=int(H*0.56)
rng=np.random.default_rng(21)
def fbm(n,oct=7,seed=0):
    r=np.random.default_rng(seed); out=np.zeros(n)
    for o in range(oct):
        k=2**o; pts=r.normal(0,1,k+2)
        xs=np.linspace(0,k,n); out+=np.interp(xs,np.arange(k+2),pts)/(1.9**o)
    return out
x=np.linspace(0,1,W)
# mountain ridges: V-shaped valley opening in the centre
def ridge(seed,peakL,peakR,base,amp,valley=0.36):
    n=fbm(W,11,seed)
    shape=np.where(x<0.5, peakL*np.clip(1-(x/valley),0,1)**1.25, peakR*np.clip(1-((1-x)/valley),0,1)**1.25)
    return base-np.maximum(shape+n*amp*np.maximum(shape,0.03)+fbm(W,11,seed+50)*0.012*(shape>0.01),0)
far=ridge(3,0.30,0.26,HZ/H-0.005,0.16,0.46)*H
near=ridge(7,0.50,0.44,HZ/H+0.002,0.22,0.33)*H
yy=np.arange(H)[:,None]
img=np.zeros((H,W,3))
def c(h): return np.array([int(h[i:i+2],16) for i in (1,3,5)],float)
# sky
t=(yy/HZ).clip(0,1)
sky=c('#070d1f')*(1-t)+c('#1c2d55')*t
glow=np.exp(-(((x[None,:]-0.5)/0.22)**2)-(((yy-HZ)/(H*0.18))**2))
sky=sky[:, :, None] if sky.ndim==2 else sky
img[:]=c('#070d1f')
for i in range(3): img[...,i]=(c('#070d1f')[i]*(1-t)+c('#22355f')[i]*t)[:,0][:,None]
img+= (glow[...,None]*c('#3b4f80')*0.45)
# stars
s=rng.random((H,W))>0.9993
img[s & (yy<HZ*0.7)]=[200,210,235]
img=gaussian_filter(img,(0.6,0.6,0))
def paint(rid,col_dark,col_lit,snow_amt,seed):
    mask=yy>=rid[None,:]
    sm=gaussian_filter(rid,2)
    slope=np.gradient(sm)
    lit=np.clip(np.abs(slope)*0.55+0.1,0,1)
    r=np.random.default_rng(seed)
    g1=gaussian_filter(r.normal(0,1,(H,W)),(14,1.6))
    g2=gaussian_filter(r.normal(0,1,(H,W)),(4,4))
    # gullies follow the slope direction: shear the streak texture by slope
    sh=(np.arange(H)[:,None]*0+0)
    depth=np.clip((yy-rid[None,:])/260,0,1)
    snow=np.clip(lit[None,:]*1.1+g1*0.9+g2*0.25-0.35-depth*0.9,0,1)**1.4*snow_amt
    rim=np.exp(-((yy-rid[None,:])/3.0)**2)*mask*np.clip(lit[None,:]+0.2,0,1)
    col=col_dark[None,None,:]*(1-snow[...,None])+col_lit[None,None,:]*snow[...,None]
    col=col+rim[...,None]*col_lit*0.6
    img[mask]=col[mask]
paint(far,c('#121d3a'),c('#4a5f8e'),0.55,11)
paint(near,c('#0a1124'),c('#8ea3cc'),0.9,12)
# atmospheric haze near horizon
haze=np.exp(-((yy-HZ)/(H*0.05))**2)
img+=haze[...,None]*c('#2a3d6b')*0.25
img[HZ:]=0
# water = reflection of top part with ripples
top=img[:HZ].copy()
refl=top[::-1]
rh=H-HZ
refl=refl[:rh]
ry=np.arange(rh)[:,None]
wob=gaussian_filter(rng.normal(0,1,(rh,W//6)),(1.2,10))
wob=np.array(Image.fromarray(wob.astype(np.float32)).resize((W,rh),Image.BICUBIC))
dx=wob*(4+ry*0.06); dy=np.abs(wob)*(1+ry*0.02)
Y,X=np.mgrid[0:rh,0:W].astype(float)
out=np.stack([map_coordinates(refl[...,k],[np.clip(Y+dy,0,rh-1),np.clip(X+dx,0,W-1)],order=1) for k in range(3)],-1)
out=gaussian_filter(out,(1.5,4,0))
fade=np.exp(-ry/(rh*0.9))
water=out*(0.55*fade[...,None]+0.12)+c('#08112a')*(1-fade[...,None])*0.9
# ripple highlights
lines=gaussian_filter(rng.normal(0,1,(rh,W//10)),(0.6,25))
lines=np.array(Image.fromarray(lines.astype(np.float32)).resize((W,rh),Image.BICUBIC))
water+=np.clip(lines,0,None)[...,None]*c('#3c5486')*0.35*fade[...,None]
# warm reflection streak under the cabinet (cabinet itself is a separate layer)
cx=0.5
streak=np.exp(-(((x[None,:]-cx)/0.05)**2))*np.exp(-ry/(rh*0.55))
streakmod=0.6+0.4*np.clip(lines*1.5+0.5,0,1)
water+=(streak*streakmod)[...,None]*c('#ff8a3d')*0.42
img[HZ:]=water
# horizon line glow
img+=np.exp(-((yy-HZ)/2.5)**2)[...,None]*c('#6f86b8')*0.35
# vignette
vx=(x[None,:]-0.5)/0.7; vy=(yy/H-0.5)/0.75
img*= (1-0.55*np.clip(vx**2+vy**2,0,1))[...,None]
img+=rng.normal(0,1.2,img.shape)
im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
im.save('/home/claude/amperazh/v2/scene.jpg',quality=88)
im.resize((1920,1080),Image.LANCZOS).save('/home/claude/amperazh/v2/scene.webp',quality=80)
im.resize((1200,675)).save('/home/claude/amperazh/v2/scene-preview.jpg',quality=80)
print('HZ frac',HZ/H)
