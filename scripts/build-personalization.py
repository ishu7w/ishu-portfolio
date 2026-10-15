#!/usr/bin/env python3
"""Generate Ishu's portfolio without changing the retained animation engine."""
import html
import json
import re
import subprocess
import sys
import shutil
from pathlib import Path
from branding_geometry import write_personal_geometry

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT/'dist'
REFERENCE = ROOT/'reference'
VERSION = '1780406240914'
profile = json.loads((ROOT/'content/portfolio.json').read_text())
subprocess.run([sys.executable,str(ROOT/'scripts/localize.py')],check=True)
patches=[]

def patch(text, old, new, expected=None):
    count=text.count(old)
    if not count or (expected is not None and count != expected):
        raise ValueError(f'Content patch no longer matches ({count}): {old[:90]}')
    patches.append({'old':old,'new':new,'count':count})
    return text.replace(old,new)

def quoted(value):
    return json.dumps(value,ensure_ascii=False)

def save_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

projects=[]
write_personal_geometry(DIST)
personal_images=DIST/'assets/images/personal'
personal_images.mkdir(parents=True,exist_ok=True)
for filename in ['github.png','linkedin.png','leetcode.png','lab-mark.png','lab-map.png','showreel.jpg']:
    shutil.copyfile(DIST/'content/portfolio'/filename,personal_images/filename)
for index, project in enumerate(profile['projects']):
    slug=project['slug']
    for suffix in ['.jpg','-logo.png']:
        shutil.copyfile(DIST/'content/portfolio'/f'{slug}{suffix}',personal_images/f'{slug}{suffix}')
    projects.append({
        'id':f'ishu-{slug}', 'name':project['name'], 'slug':slug,
        'description':project['description'], 'clientName':project['stack'],
        'period':project['kind'], 'completionDate':'2026-01-01T00:00:00.000Z',
        'projectLogo':{'url':f'assets/images/personal/{slug}-logo.png'},
        'video':{'url':f'/content/portfolio/{slug}.mp4','thumbnail':f'assets/images/personal/{slug}.jpg'},
        'uiColor':project['color'], 'tags':project['tags'], 'priority':index+1,
        'caseStudyURL':project['source'], 'projectURL':project['demo']
    })
save_json(DIST/'content/cms/projects-dev.json',projects)
save_json(DIST/'content/cms/metadata-dev.json',{'title':profile['title'],'description':profile['description'],'ogImage':{'url':'/content/portfolio/social.jpg'}})
save_json(DIST/'content/cms/contact-dev.json',{'links':[{'title':k.title(),'url':v} for k,v in profile['links'].items()]})
save_json(DIST/'content/portfolio/profile.json',profile)

scene=json.loads((REFERENCE/f'assets/data/uil.{VERSION}.json').read_text())
scene_updates={
 'INPUT_Element_4_Home_text3d_text':profile['homeText'],
 'INPUT_Element_3_About_text3d_text':profile['aboutHeading'],
 'INPUT_Element_4_About_text3d_text':profile['aboutText'],
 'INPUT_Element_15_CleanRoom_text3d_text':profile['labHeading'],
 'INPUT_Element_20_CleanRoom_text3d_text':profile['labText'],
 'INPUT_Element_5_WorkDetailContent_text3d_text':projects[0]['name'],
 'INPUT_Element_8_WorkDetailContent_text3d_text':projects[0]['period']+'\n'+projects[0]['clientName']
}
scene.update(scene_updates)
for key,value in list(scene.items()):
    if isinstance(value,dict) and value.get('src') in ['assets/geometry/logo/AT_logo.bin','assets/geometry/particles/at_logo.bin']:
        scene[key]={**value,'filename':'ishu-logo.json','relative':'assets/geometry/personal','src':'assets/geometry/personal/ishu-logo.json'}
    elif isinstance(value,dict) and value.get('src') == 'assets/geometry/home/logo.json':
        scene[key]={**value,'filename':'ishu-logo-large.json','relative':'assets/geometry/personal','src':'assets/geometry/personal/ishu-logo-large.json'}
    elif isinstance(value,dict) and value.get('src') == 'assets/images/ui/at-labrds.jpg':
        scene[key]={**value,'filename':'lab-mark.png','relative':'assets/images/personal','src':'assets/images/personal/lab-mark.png'}
    elif isinstance(value,dict) and value.get('src') == 'assets/images/lab.jpg':
        scene[key]={**value,'filename':'lab-map.png','relative':'assets/images/personal','src':'assets/images/personal/lab-map.png'}
save_json(DIST/f'assets/data/uil.{VERSION}.json',scene)

app_path=DIST/f'assets/js/app.{VERSION}.js'
app=app_path.read_text()
for old,new in [
 ('Active Theory · Creative Digital Experiences',profile['title']),
 (' · Active Theory',' · '+profile['name']),
 ('HELLO@ACTIVETHEORY.NET',profile['email'].upper()),
 ('Email us at hello@activetheory.net','Email '+profile['name']+' at '+profile['email']),
 ('mailto:hello@activetheory.net','mailto:'+profile['email']),
 ('https://mailchi.mp/activetheory/newsletter',profile['links']['repositories']),
 ('https://activetheory.notion.site/privacy',profile['links']['github']),
 ('https://jobs.lever.co/activetheory',profile['links']['contributions']),
 ('https://www.instagram.com/activetheory',profile['links']['github']),
 ('https://www.linkedin.com/company/active-theory/',profile['links']['linkedin']),
 ('https://twitter.com/active_theory',profile['links']['leetcode']),
 ('https://atlab.io',profile['links']['repositories']),
 ('assets/images/ui/ig.png','assets/images/personal/github.png'),
 ('assets/images/ui/in.png','assets/images/personal/linkedin.png'),
 ('assets/images/ui/tw.png','assets/images/personal/leetcode.png'),
 ('assets/video/reel.mp4','/content/portfolio/showreel.mp4'),
 ('assets/video/reel-frame.jpg','/content/portfolio/showreel.jpg'),
 ('assets/images/lab.gif','assets/images/personal/showreel.jpg'),
 ('Newsletter Signup','All repositories'),
 ('Privacy Notice','GitHub profile'),
 ('Careers','Contributions'),
 ('CONTACT US',"LET'S BUILD"),
 ('[ MOBILE SYNC ]','[ GITHUB PROFILE ]'),
 ('Ask me anything...','Ask about my work...'),
 ('What are you looking for?','Explore my work'),
 ('Im trained on 112 projects',f"{len(projects)} projects & contributions"),
 ('Medium Case Study','View source on GitHub'),
 ('Project Link','Open live project'),
 ('Our site uses essential cookies and, with your consent, analytics cookies. Details in ', 'This portfolio stores viewing preferences in your browser. No analytics cookies. Explore my work on '),
 ('Privacy Policy.','GitHub profile.'),
 ('Accept Cookies','Keep preferences'),
 ('Reject Cookies','Dismiss')
]:
    app=patch(app,old,new)
for old,new in [('LAX','JAVA'),('NYC','WEB'),('SYD','WEB'),('AMS','AI'),('Instagram','GitHub'),('Linked in','LinkedIn'),('Twitter','LeetCode')]:
    app=patch(app,quoted(old),quoted(new))
for old,new in [('Los Angeles','Java'),('New York City','Web development'),('Amsterdam','Applied AI'),('Contact Us',"Contact Ishu Patel")]:
    app=patch(app,quoted(old),quoted(new))
for key,url,label in [
    ('email','mailto:'+profile['email'],'Email '+profile['name']),
    ('subscribe',profile['links']['repositories'],'All repositories'),
    ('privacy',profile['links']['github'],'GitHub profile'),
    ('careers',profile['links']['contributions'],'Contribution history')
]:
    target=f'_this.{key}.interact(hover,(_=>window.open({quoted(url)}'+('' if key=='email' else ',"_blank"')+')),"#")'
    app=patch(app,target,target[:-1]+','+quoted(label)+')',1)
app=patch(app,'_this.onFullscreenClick=_=>{_this.modal.css({display:"flex",zIndex:"9999"}),_this.video.play()}',
    '_this.onFullscreenClick=_=>{_this.video.src=Assets.getPath(_this.get("Work/project",!0)?.videoURL||"/content/portfolio/showreel.mp4"),_this.modal.css({display:"flex",zIndex:"9999"}),_this.video.play()}',1)

old_filters='_this.addFilter("-> websites","Website",!0,100),_this.addFilter("-> installations","Installation",!0,200),_this.addFilter("-> XR / VR / AI","XR",!0,300),_this.addFilter("-> multiplayer","Multiplayer",!0,400),_this.addFilter("-> games","Game",!0,500)'
new_filters=','.join(f'_this.addFilter({quoted("-> "+c["label"])},{quoted(c["tag"])},!0,{(i+1)*100})' for i,c in enumerate(profile['categories']))
app=patch(app,old_filters,new_filters,1)
app=patch(app,'${new Date(data.completionDate).getFullYear()}\\n${data.clientName}\\n${data.tags.toLowerCase()}','${data.period||"Personal project"}\\n${data.clientName}\\n${data.tags.toLowerCase()}',1)

# QR keeps its original visual treatment and points to the verified public profile.
qr_start='let url=location.href;url=url.split("#")[0],url+=url.includes("?")?"&":"?",url+=`roomqr=${encodeURIComponent(_params.key)}`;const items=await _this.get("WorkItems/items"),ids=[];items.toJSON().forEach((item=>ids.push(item.index))),url+=`&workids=${encodeURIComponent(ids.join(","))}`,console.log("url ",url);'
app=patch(app,qr_start,'let url='+quoted(profile['links']['github'])+';',1)

# Replace the page's declared context with factual personal information.
strings=list(re.finditer(r'"(?:[^"\\]|\\.)*"',app))
for match in reversed(strings):
    literal=match.group(0)
    try: value=json.loads(literal)
    except json.JSONDecodeError: continue
    new=None
    if value.startswith('Active Theory is a creative digital production studio'):
        new=profile['name']+' is a '+profile['role']+'. '+profile['aboutText'].replace('\n',' ')+' Skills: '+', '.join(profile['skills'])+'. Profile: '+profile['links']['github']
    elif value.startswith('Get more information about Active Theory'):
        new="Read Ishu Patel's verified biography, skills, public projects and open-source contributions."
    elif value.startswith('Open the contact modal for Active Theory'):
        new="Open Ishu Patel's contact panel and verified public profile links."
    if new is not None:
        app=app[:match.start()]+quoted(new)+app[match.end():]
app=patch(app,'get_more_agency_info','get_portfolio_info',1)

# The same animated conversation UI uses one stateless request on Vercel.
assistant_start = app.index('InteractAI.Class((function Assistant(_props)')
assistant_end = app.index('InteractAI.Class((function GPT(_props)', assistant_start)
app = app[:assistant_start] + 'InteractAI.Class((function Assistant(_props){Inherit(this,Component);const _this=this;var _project="";AppState.set("InteractAIAssistant/isThinking",!1);AppState.bind("Work/project",(data=>{_project=data?data.perma:""}));this.once=async function(message){await _this.wait((_=>!AppState.get("InteractAIAssistant/isThinking")));AppState.set("InteractAIAssistant/isThinking",!0);try{if(_project)message=`I\'m looking at ${_project}. `+message;const response=await fetch("/api/search",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:message})});if(!response.ok)throw Error("Search unavailable");const result=await response.json();if(result.slug)AppState.set("CMSData/slug",{slug:result.slug,message:result.text},!0);return result.text}catch(error){return "Search is temporarily unavailable. Explore Work or use the links in Contact."}finally{AppState.set("InteractAIAssistant/isThinking",!1)}}})),' + app[assistant_end:]

app_path.write_text(app)

page=(DIST/'index.html').read_text()
page=page.replace('Active Theory · Creative Digital Experiences',html.escape(profile['title'],quote=True))
page=page.replace('Founded in 2012. We blend story, art & technology as an in-house team of passionate makers. Our industry-leading web toolset consistently delivers award-winning work through quality & performance. ',html.escape(profile['description'],quote=True))
page=page.replace('content="Active Theory"','content="'+profile['name']+'"')
page=page.replace('https://activetheory.net','https://github.com/ishu7w')
page=page.replace('/content/media/social.jpg','/content/portfolio/social.jpg')
page=re.sub(r'<link[^>]+(?:favicon-|apple-touch-icon|safari-pinned-tab)[^>]*>', '', page)
page=page.replace('</head>','<link rel="icon" type="image/svg+xml" href="/content/portfolio/favicon.svg">\n</head>')
structured={'@context':'https://schema.org','@type':'Person','name':profile['name'],'description':profile['description'],'sameAs':[profile['links'][k] for k in ['github','linkedin','leetcode']]}
page=page.replace('</head>','<script type="application/ld+json">'+json.dumps(structured).replace('<','\\u003c')+'</script>\n</head>')
(DIST/'index.html').write_text(page)
save_json(DIST/'assets/meta/manifest.json',{'name':profile['name']+' Portfolio','short_name':profile['name'],'start_url':'/','display':'standalone','background_color':'#000000','theme_color':'#000000'})
(DIST/'content/portfolio/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#090e13"/><circle cx="32" cy="32" r="25" fill="none" stroke="#9ed3e4" stroke-width="2"/><text x="32" y="42" font-family="monospace" font-size="28" text-anchor="middle" fill="#e0f0f6">IP</text></svg>')
save_json(ROOT/'docs/personalization-patches.json',{'profile':profile['name'],'bundle_replacements':patches,'scene_content_keys':list(scene_updates),'preserved':'All shaders, camera paths, scene transforms and animation values; only content and identity asset references change.'})
save_json(ROOT/'docs/local-changes.json',{
    'profile':profile['name'], 'version':VERSION,
    'changes':['Personal biography, project/contribution CMS, metadata and contact destinations','IP identity meshes and logo textures','Personal project previews, motion presentations and profile QR','Local factual portfolio search','Analytics removed; local India region fixture'],
    'preserved':['Shader collection','Camera paths','Scene transforms','Animation parameters','Typography','Particles and transitions'],
    'content_source':'content/portfolio.json'
})
print(f'Built {profile["name"]} portfolio: {len(projects)} projects/contributions, {len(patches)} content replacements.')
