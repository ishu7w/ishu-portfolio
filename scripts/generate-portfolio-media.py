#!/usr/bin/env python3
"""Generate factual editorial portfolio artwork from verified repo descriptions and captured screenshots."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist/content/portfolio'
OUT.mkdir(parents=True,exist_ok=True)
FONT='/System/Library/Fonts/HelveticaNeue.ttc'
MONO='/System/Library/Fonts/Menlo.ttc'
def font(s,mono=False):return ImageFont.truetype(MONO if mono else FONT,s)
items=[
 ('parkwise','Parkwise','PARKING, WITH A PLAN.','React / TypeScript / Node / PostgreSQL',(171,225,199),'DRIVER + OWNER PLATFORM','01',True),
 ('credence','Credence','CREDENTIALS, VERIFIED.','React / Express / PostgreSQL',(145,207,245),'CERTIFICATE MANAGEMENT','02',True),
 ('scholarship-aid','Scholarship & Aid','OPPORTUNITY, ORGANIZED.','Java / Next.js / JDBC',(202,190,255),'SCHOLARSHIP MANAGEMENT','03',False),
 ('smarthealth','SmartHealth','SYSTEMS THAT CARE.','Java / Spring Boot / React',(151,229,221),'PATIENT PORTAL + PARALLEL PROCESSING','04',False),
 ('cinematic','CINEMATIC','DISCOVER YOUR NEXT FRAME.','Next.js / React Three Fiber / GSAP',(219,186,130),'MOVIE DISCOVERY EXPERIENCE','05',False),
 ('scholarai','ScholarAI','EXPLAIN EVERY MATCH.','Next.js / Supabase / TypeScript',(189,190,255),'EXPLAINABLE SCHOLARSHIP MATCHING','06',False),
 ('checkstyle','Checkstyle','SMALL FIX. SHARED IMPACT.','Dotted-directory extension parsing / PR #21518',(178,220,169),'MERGED CONTRIBUTION','07',False),
 ('gson','Gson','LESS COPYING. MORE CLARITY.','Efficient JsonArray.removeIf / PR #3115',(239,190,143),'MERGED CONTRIBUTION','08',False),
 ('java-pathfinder','Java Pathfinder','AT THE RIGHT BOUNDARY.','Buffer position clamping / PR #641',(159,198,242),'MERGED CONTRIBUTION','09',False),
]
def background(color):
 im=Image.new('RGB',(1280,720),(9,12,17));p=im.load()
 for y in range(720):
  for x in range(1280):
   v=max(0,1-math.hypot((x-1050)/1050,(y-250)/670))**2
   p[x,y]=tuple(int(9+v*c*.16) for c in color)
 return im

def title_art(slug,title,line,stack,color,label,num,screenshot):
 im=background(color); d=ImageDraw.Draw(im)
 if screenshot and (OUT/f'{slug}-source.png').exists():
  src=Image.open(OUT/f'{slug}-source.png').convert('RGB')
  src.thumbnail((1136,554))
  x=(1280-src.width)//2;y=28
  d.rounded_rectangle((x-1,y-1,x+src.width+1,y+src.height+1),radius=3,outline=(82,94,104),width=1)
  im.paste(src,(x,y)); d=ImageDraw.Draw(im)
  d.text((72,605),title,font=font(42),fill=(240,242,244))
  d.text((73,664),stack,font=font(16,True),fill=(151,162,176))
  d.text((1000,635),'LIVE PROJECT',font=font(15,True),fill=color)
 else:
  # Abstract engineering geometry is title artwork, never presented as an app interface.
  for r in [120,180,240,300]:
   d.ellipse((1020-r,290-r,1020+r,290+r),outline=tuple(int(c*.25) for c in color),width=1)
  for a in range(0,360,30):
   x=1020+240*math.cos(math.radians(a));y=290+240*math.sin(math.radians(a))
   d.ellipse((x-3,y-3,x+3,y+3),fill=color)
  d.text((72,58),label,font=font(17,True),fill=color)
  d.line((72,98,1208,98),fill=(53,62,73),width=1)
  d.text((72,208),title,font=font(84 if len(title)<18 else 65),fill=(240,242,244))
  d.text((77,328),line,font=font(21,True),fill=color)
  d.text((76,547),stack,font=font(18,True),fill=(173,184,198))
  d.text((76,587),'PROJECT TITLE ART' if label!='MERGED CONTRIBUTION' else 'OPEN SOURCE / VERIFIED MERGE',font=font(13,True),fill=(104,118,134))
  d.line((72,639,1208,639),fill=(53,62,73),width=1)
  d.text((73,664),'ISHU PATEL / ishu7w',font=font(15,True),fill=(164,175,189))
  d.text((1165,657),num,font=font(27,True),fill=color)
 im.save(OUT/f'{slug}.jpg',quality=93,subsampling=0)
 logo=Image.new('RGBA',(640,160),(0,0,0,0));ld=ImageDraw.Draw(logo)
 f=font(58 if len(title)<18 else 46); box=ld.textbbox((0,0),title,font=f);ld.text(((640-(box[2]-box[0]))/2,(160-(box[3]-box[1]))/2-box[1]),title,font=f,fill=(255,255,255,255))
 logo.save(OUT/f'{slug}-logo.png')
 return {'slug':slug,'title':title,'type':'actual screenshot on editorial background' if screenshot else 'editorial title art','source': {'parkwise':'https://parkwise-beta.vercel.app/','credence':'https://digital-certification-system-mu.vercel.app/'}.get(slug,'verified public repository README / merged pull request')}
manifest=[title_art(*item) for item in items]
im=background((160,189,245));d=ImageDraw.Draw(im)
d.text((70,55),'SOFTWARE / OPEN SOURCE / CREATIVE WEB',font=font(17,True),fill=(166,190,227))
d.text((66,235),'Ishu Patel',font=font(130),fill='white')
d.text((76,414),'Turning ideas into working systems.',font=font(32),fill=(173,185,204))
d.line((76,600,1205,600),fill=(60,72,91),width=1)
d.text((76,643),'SELECTED PROJECTS + MERGED CONTRIBUTIONS',font=font(19,True),fill=(166,190,227))
d.text((1060,643),'ishu7w',font=font(19,True),fill=(166,190,227))
im.save(OUT/'showreel.jpg',quality=94)
im.save(OUT/'social.jpg',quality=94)
lab=background((189,190,255));d=ImageDraw.Draw(lab);d.text((75,165),'Explore.',font=font(120),fill='white');d.text((75,300),'Build. Refine.',font=font(100),fill='white');d.text((81,518),'ISHU PATEL / PERSONAL PROJECT LAB',font=font(22,True),fill=(180,191,213));lab.save(OUT/'lab-mark.jpg',quality=93)
mark=Image.new('RGB',(512,512),(10,13,20));md=ImageDraw.Draw(mark);md.text((93,130),'ip',font=font(250),fill=(238,243,255));mark.save(OUT/'favicon.png');mark.save(OUT/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)]);mark.resize((180,180)).save(OUT/'apple-touch-icon.png')
(OUT/'media-sources.json').write_text(json.dumps({'created':'2026-10-15','identity':'Ishu Patel / ishu7w','media':manifest,'videoMethod':'Slow animated crop of the corresponding factual screenshot/title artwork; silent H.264 MP4 loops, not recorded application demos.'},indent=2))
print('Generated',len(manifest),'project artwork sets in',OUT)
