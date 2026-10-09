import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S="/tmp/claude-0/-home-user-super-barnacle/35d16e81-df7f-5220-b9cf-59e4fb6d0b72/scratchpad"
F=f"{S}/fonts2/Cairo_wght_700.ttf"
TEAL=(14,124,134); DARK=(30,41,59); K=1.875
CUT={1:650,2:640,3:703,4:708,5:708,6:750,7:740,8:645,9:680,10:722,11:730,12:650,13:650,14:650}
AR="٠١٢٣٤٥٦٧٨٩"; ORD=["","الأولى","الثانية","الثالثة","الرابعة","الخامسة","السادسة","السابعة","الثامنة","التاسعة","العاشرة"]
CAP={2:"ندخل من أي متصفح",3:"نبحث عن منصة مدرستي ونختار الخيار الثاني",4:"نضغط على تسجيل الدخول",
5:"نختار الدخول بحساب مايكروسوفت",6:"ندخل البريد الإلكتروني وكلمة المرور",7:"بعدها يتم تسجيل الدخول إلى منصة مدرستي",
8:"إذا كان حساب ابنتك محفوظًا نختاره، وإذا لم يكن موجودًا نكتبه في خانة تسجيل الدخول",
9:"نكتب كلمة المرور مع الانتباه للحروف الكبيرة والصغيرة، والصفر دائمًا رقم صفر",
10:"نضغط على أيقونة «نعم»",11:"تفتح الصفحة الخاصة بالطالبة"}
def font(sz): 
    f=ImageFont.truetype(F,sz); return f
def wrap(d,text,f,w):
    words=text.split(); lines=[]; cur=""
    for wd in words:
        t=(cur+" "+wd).strip()
        if d.textlength(t,font=f,direction="rtl",features=["-liga"] if False else None)<=w: cur=t
        else: lines.append(cur); cur=wd
    lines.append(cur); return lines
def card(im,box,label,text,badge=None,size=60):
    x0,y0,x1,y1=box
    sh=Image.new("RGBA",im.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((x0,y0+12,x1,y1+12),44,fill=(15,40,60,70))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
    d=ImageDraw.Draw(im); d.rounded_rectangle(box,44,fill=(255,255,255,255),outline=(14,124,134,255),width=5)
    right=x1-48
    if badge:
        cx,cy=x1-48-70,(y0+y1)//2
        d.ellipse((cx-70,cy-70,cx+70,cy+70),fill=TEAL); f=font(84 if len(badge)==1 else 62)
        d.text((cx,cy+6),badge,font=f,fill="white",anchor="mm",direction="rtl")
        right=cx-70-36
    f=font(size); lines=wrap(d,text,f,right-(x0+48)); fl=font(int(size*0.68))
    lh=int(size*1.55); th=lh*len(lines)+(int(size*1.2) if label else 0)
    y=(y0+y1)//2-th//2
    if label: d.text((right,y),label,font=fl,fill=TEAL,anchor="ra",direction="rtl"); y+=int(size*1.2)
    for ln in lines: d.text((right,y),ln,font=f,fill=DARK,anchor="ra",direction="rtl"); y+=lh
LOGO=Image.open(f"{S}/clean/c_02.png").convert("RGB").crop((340,52,542,168))
def mockup(im):
    sh=Image.new("RGBA",im.size,(0,0,0,0)); sd=ImageDraw.Draw(sh)
    sd.rounded_rectangle((170,940,910,1400),40,fill=(15,40,60,90)); sd.rounded_rectangle((720,1290,930,1700),48,fill=(15,40,60,90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)))
    d=ImageDraw.Draw(im)
    # laptop
    d.rounded_rectangle((190,900,890,1330),34,fill=(38,48,62)); d.rounded_rectangle((214,924,866,1306),14,fill=(255,255,255))
    d.rectangle((214,924,866,968),fill=(14,124,134)); 
    for i,cx in enumerate((236,262,288)): d.ellipse((cx-8,938,cx+8,954),fill=(255,255,255,200))
    lg=LOGO.resize((430,int(430*LOGO.height/LOGO.width)),Image.LANCZOS); im.paste(lg,(540-215,1000))
    d.rounded_rectangle((300,1230,560,1262),16,fill=(225,242,243)); d.rounded_rectangle((300,1270,480,1290),10,fill=(235,240,244))
    d.polygon([(130,1330),(950,1330),(920,1374),(160,1374)],fill=(205,212,220)); d.rounded_rectangle((440,1334,640,1352),9,fill=(170,178,188))
    # phone
    d.rounded_rectangle((730,1290,920,1690),44,fill=(38,48,62)); d.rounded_rectangle((744,1304,906,1676),32,fill=(255,255,255))
    d.rounded_rectangle((790,1316,860,1328),6,fill=(38,48,62))
    lp=LOGO.resize((140,int(140*LOGO.height/LOGO.width)),Image.LANCZOS); im.paste(lp,(755,1400))
    d.rounded_rectangle((770,1560,880,1600),20,fill=(14,124,134)); d.rounded_rectangle((770,1612,880,1630),9,fill=(225,235,240))
EMB=Image.open(f"{S}/design/d1_ref.png").convert("RGB").crop((368,45,548,168))
def render(n):
    img=cv2.imread(f"{S}/clean/c_{n:02d}.png")
    if n==2:
        ic=img[590:780].copy(); img[330:790]=255; img[400:590]=ic
    ARW={4:(-33,-34),5:(0,-115)}
    if n in ARW:
        x0,y0,x1,y1=372,620,505,680; dx,dy=ARW[n]; pt=img[y0:y1,x0:x1].copy(); img[y0:y1,x0:x1]=255
        dst=img[y0+dy:y1+dy,x0+dx:x1+dx]; img[y0+dy:y1+dy,x0+dx:x1+dx]=np.minimum(dst,pt)
    big=cv2.resize(img,(1080,1920),interpolation=cv2.INTER_LANCZOS4)
    bl=cv2.GaussianBlur(big,(0,0),1.2); big=cv2.addWeighted(big,1.5,bl,-0.5,0)
    if n==1:
        mk=np.zeros(big.shape[:2],np.uint8); mk[36:240,630:1060]=255; mk[164:218,296:610]=255; mk[40:166,356:560]=255
        big=cv2.inpaint(big,mk,12,cv2.INPAINT_TELEA)
    im=Image.fromarray(cv2.cvtColor(big,cv2.COLOR_BGR2RGB)).convert("RGBA")
    if n==1:
        hd=ImageDraw.Draw(im); fh=font(38)
        hd.text((468,66),"الابتدائية",font=fh,fill=DARK,anchor="mt",direction="rtl")
        hd.text((468,120),"التاسعة والأربعون",font=fh,fill=TEAL,anchor="mt",direction="rtl")
        lg=LOGO.resize((400,int(400*LOGO.height/LOGO.width)),Image.LANCZOS).convert("RGBA")
        mm=Image.new("L",lg.size,0); ImageDraw.Draw(mm).rectangle((14,14,lg.width-14,lg.height-14),fill=255)
        im.paste(lg,(650,50),mm.filter(ImageFilter.GaussianBlur(9)))
    # laptop removal
    cy=int(CUT[n]*K); m=Image.new("L",im.size,0); ImageDraw.Draw(m).rectangle((0,cy,1080,1920),fill=255)
    im.paste(Image.new("RGBA",im.size,(255,255,255,255)),(0,0),m.filter(ImageFilter.GaussianBlur(3)))
    d=ImageDraw.Draw(im)
    bd=ImageDraw.Draw(im); bd.rectangle((0,int(158*K),int(300*K),int(309*K)),fill=(255,255,255,255)); bd.rectangle((0,int(172*K),1080,int(309*K)),fill=(255,255,255,255))
    if n==1: mockup(im)
    else:
        hd=ImageDraw.Draw(im); fh=font(38)
        hd.text((468,66),"الابتدائية",font=fh,fill=DARK,anchor="mt",direction="rtl")
        hd.text((468,120),"التاسعة والأربعون",font=fh,fill=TEAL,anchor="mt",direction="rtl")
    top=max(cy+50,1330) if n in CAP else 0
    if n in CAP:
        label=f"الخطوة {ORD[n-1]}"; f=font(58); dd=ImageDraw.Draw(im)
        nl=len(wrap(dd,CAP[n],f,960-96-140-36)); h=int(58*1.55)*nl+int(58*1.2)+110; h=max(h,300)
        top=max(min(top,1870-h),cy+30); card(im,(60,top,1020,top+h),label,CAP[n],badge="".join(AR[int(c)] for c in str(n-1)),size=58)
    elif n==1: card(im,(60,360,1020,780),None,"طريقة دخول ولي الأمر إلى منصة مدرستي وتفعيلها",size=76)
    elif n==12: card(im,(60,640,1020,1280),"دخول ولي الأمر","باستخدام اسم المستخدم المرسل عبر توكلنا، ثم إدخال كلمة المرور الخاصة بالحساب",size=62)
    elif n==13: card(im,(60,600,1020,1380),"ملاحظة","من لم يفهم الخطوات يزورنا في المدرسة، وعلى الرحب والسعة. والأهم أن يحضر الجوال الذي تصل إليه الرسائل النصية.",size=58)
    elif n==14:
        card(im,(60,640,1020,900),"مديرة المدرسة","فائزة البدراني",size=80)
        card(im,(60,980,1020,1240),"مسؤولة منصة مدرستي","هبة خشيم",size=80)
    im.convert("RGB").save(f"{S}/design/d_{n:02d}.png")
for n in range(1,15): render(n)
