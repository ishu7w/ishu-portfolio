"""Small, checked fixes to the retained runtime; shaders and scenes stay intact."""
import html


def apply_runtime_patches(app, patch):
    # Keep render targets and the final canvas on the same pixel budget. The
    # original renderer supersampled low-DPI displays and ignored World.DPR.
    start = app.index('_this.getDPR=_=>', app.index('function Tests()'))
    end = app.index(',_this.capFPS=', start)
    original = app[start:end]
    quality = original.split('=_=>', 1)[1]
    app = patch(app, original,
        '_this.getDPR=_=>Math.min((' + quality + '),Device.pixelRatio,1.5,'
        'Math.max(.75,Math.sqrt((Device.mobile?1e6:2e6)/(Stage.width*Stage.height))))', 1)
    start = app.index('function getDPR(){', app.index('function RenderManager()'))
    end = app.index('function directRenderCallback', start)
    app = patch(app, app[start:end],
        'function getDPR(){return window.AURA?Device.pixelRatio:World.DPR||Math.min(Device.pixelRatio,1.5)}', 1)

    # The refraction object is stable; only its texture contents change. Avoid
    # an async lookup and new promise for every work-card shader, every frame.
    app = patch(app,
        '_this.startRender((async _=>{let refraction=await _this.get("Work/refraction");_this.shader.set("tRefraction",refraction),_this.shader.set("uPhone",Device.mobile&&Stage.height>Stage.width?1:0)}))',
        'Promise.resolve(_this.get("Work/refraction")).then(refraction=>_this.shader.set("tRefraction",refraction));'
        'const updatePhone=_=>_this.shader.set("uPhone",Device.mobile&&Stage.height>Stage.width?1:0);'
        'updatePhone(),_this.onResize(updatePhone)', 1)

    # A response can arrive before the 400ms fade finishes. Disable immediately,
    # rather than letting a late tween callback disable an already-ready input.
    app = patch(app, '_this.input.progress=1,_this.flashing.progress=0,tween(_this.input,',
        '_this.input.div.disabled=!0,_this.input.progress=1,_this.flashing.progress=0,tween(_this.input,', 1)
    app = patch(app, '.onComplete((_=>_this.input.div.disabled=!0))', '', 1)
    app = patch(app, 'blinker.classList.remove("blink"),_this.input.div.disabled=!1',
        'blinker.classList.remove("blink"),clearTween(_this.input),clearTween(_this.flashing),'
        '_this.flashing.css({opacity:0}),_this.input.div.disabled=!1', 1)
    app = patch(app, 'Sessions may be recorded. By using chat, you acknowledge our ',
        'Search uses only this portfolio. Explore more on my ', 1)
    app = patch(app, 'disclaimer.slice(0,61*(1-text.progress))',
        'disclaimer.slice(0,disclaimer.length*(1-text.progress))', 1)

    # Filter anchors previously had no href and could not be reached with Tab.
    app = patch(app, 'link.onclick=async _=>{_this.get("disableFiltering",!0)||',
        'link.href="#",link.setAttribute("role","button"),'
        'link.onkeydown=e=>{if(e.key===" "){e.preventDefault();link.click()}},'
        'link.onclick=async e=>{e.preventDefault();_this.get("disableFiltering",!0)||', 1)

    # Do not download another showreel into a hidden player during startup.
    app = patch(app, '_this.video.src=Assets.getPath("/content/portfolio/showreel.mp4"),_this.video.controls=!0',
        '_this.video.preload="none",_this.video.playsInline=!0,_this.video.controls=!0', 1)
    app = patch(app, '_this.modal.css({display:"none"}),_this.modal.goob(',
        '_this.modal.css({display:"none"}),_this.modal.div.setAttribute("role","dialog"),'
        '_this.modal.div.setAttribute("aria-label","Project video"),'
        '_this.modal.div.setAttribute("aria-modal","true"),_this.modal.div.tabIndex=-1,'
        '_this.modal.div.classList.add("prevent_interactionScroll"),'
        'document.addEventListener("keydown",e=>{if(e.key==="Escape"&&_this.modal.div.style.display!=="none"){e.preventDefault();closeModal()}}),'
        '_this.modal.goob(', 1)
    app = patch(app,
        '_this.onFullscreenClick=_=>{_this.video.src=Assets.getPath(_this.get("Work/project",!0)?.videoURL||"/content/portfolio/showreel.mp4"),_this.modal.css({display:"flex",zIndex:"9999"}),_this.video.play()}',
        '_this.onFullscreenClick=_=>{let src=Assets.getPath(_this.get("Work/project",!0)?.videoURL||"/content/portfolio/showreel.mp4");'
        'if(_this.video.getAttribute("src")!==src)_this.video.src=src;'
        '_this.returnFocus=document.activeElement,_this.set("fullscreen",!0),'
        '_this.modal.css({display:"flex",zIndex:"9999"}),_this.modal.div.focus({preventScroll:!0}),'
        '_this.video.play().catch(()=>{})}', 1)
    app = patch(app,
        'function closeModal(){_this.video.pause(),_this.video.currentTime=0,_this.modal.css({display:"none"})}',
        'function closeModal(){let wasOpen=_this.modal.div.style.display!=="none";'
        '_this.video.pause(),_this.video.currentTime=0,_this.set("fullscreen",!1),_this.modal.css({display:"none"});'
        'if(wasOpen)_this.returnFocus?.focus({preventScroll:!0})}', 1)
    # Native video controls remain responsive while GPU drawing behind the
    # opaque modal is suspended. The animation clock and DOM input keep running.
    app = patch(app, 'function loop(t,delta){_controls&&_controls.enabled&&_controls.update(),RenderManager.render()}',
        'function loop(t,delta){if(AppState.get("WorkDetailContent/fullscreen"))return;'
        '_controls&&_controls.enabled&&_controls.update(),RenderManager.render()}', 1)
    return app


def render_fallback(profile):
    """Make the portfolio useful when WebGL is unavailable, without analytics."""
    esc = lambda value: html.escape(value, quote=True)
    projects = ''.join(
        '<article><h2>' + esc(p['name']) + '</h2><p>' + esc(p['description']) + '</p>'
        '<a href="' + esc(p['source']) + '">View source on GitHub ↗</a></article>'
        for p in profile['projects'])
    links = ''.join('<a href="' + esc(profile['links'][key]) + '">' + label + ' ↗</a>'
                    for key, label in [('github', 'GitHub'), ('linkedin', 'LinkedIn'), ('leetcode', 'LeetCode')])
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>''' + esc(profile['title']) + '''</title>
<link rel="icon" href="/content/portfolio/favicon.svg">
<style>
@font-face{font-family:nbarchitekt;src:url('/assets/fonts/NBArchitektStd-Regular-export/NBArchitektStd-Regular.woff2') format('woff2');font-display:swap}
*{box-sizing:border-box}body{margin:0;background:#090e13;color:#e0f0f6;font-family:nbarchitekt,monospace;line-height:1.65}
main{max-width:900px;margin:auto;padding:clamp(24px,6vw,72px)}h1{font-size:clamp(32px,7vw,64px);line-height:1.1;font-weight:400}h2{font-size:24px;font-weight:400;margin:0 0 12px}p{max-width:70ch}a{color:#b8e2f2;text-underline-offset:5px;display:inline-block;padding:10px 0;min-height:44px}a:focus-visible{outline:2px solid #b8e2f2;outline-offset:4px}nav{display:flex;flex-wrap:wrap;gap:12px 24px}article{padding:32px 0;border-top:1px solid #344c58}.note{color:#b9cbd5;margin:32px 0}article p{margin:0 0 12px}
</style></head><body><main><h1>''' + esc(profile['name']) + '''</h1><p>''' + esc(profile['description']) + '''</p>
<nav>''' + links + '<a href="mailto:' + esc(profile['email']) + '''">Email me ↗</a></nav>
<p class="note">The animated experience needs WebGL. You can browse my projects here, or <a href="/">try the animated site again</a>.</p>
''' + projects + '</main></body></html>\n'
