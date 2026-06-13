#!/usr/bin/env python3
"""Generate the Solomon Nights site: a rich artist homepage (/) + one Spotify-save
landing page per song (/<slug>/). Add a song: append {title, trackId} to
songs.json and re-run. Cover art is fetched from Spotify oEmbed at build time.
No secrets here (pixel id is public)."""
import json, re, os, urllib.request

PIXEL    = "1022464693584913"
PLAYLIST = "053laY69PHb8Sy27Xnb7Yh"
TAGLINE  = "Raw acoustic · contemporary Christian"
DOMAIN   = "solomonnights.com"
HERE     = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.dirname(HERE)

def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t.lower())).strip("-")

def cover(track_id):
    url = "https://open.spotify.com/oembed?url=https://open.spotify.com/track/" + track_id
    with urllib.request.urlopen(url, timeout=25) as r:
        thumb = json.load(r).get("thumbnail_url", "")
    return thumb.replace("ab67616d00001e02", "ab67616d0000b273")

def render(tmpl, **kw):
    for k, v in kw.items():
        tmpl = tmpl.replace("@@" + k + "@@", v)
    return tmpl

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>Solomon Nights — @@TITLE@@</title>
<meta name="description" content="Listen to Solomon Nights and save the playlist on Spotify. Raw, stripped-back, acoustic contemporary Christian music." />
<meta property="og:type" content="music.song" />
<meta property="og:title" content="Solomon Nights — @@TITLE@@" />
<meta property="og:description" content="Save the playlist on Spotify. Raw acoustic contemporary Christian music." />
<meta property="og:image" content="@@COVER@@" />
<meta property="og:url" content="https://@@DOMAIN@@/@@SLUG@@" />
<meta name="theme-color" content="#15110f" />
<link rel="icon" href="@@COVER@@" />
<style>
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html, body { margin: 0; height: 100%; }
  body { background: #15110f; color: #f3ece4; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100svh; padding: 24px; }
  .card { width: 100%; max-width: 360px; text-align: center; }
  .artist { color: #c9a27a; font-size: 12px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 18px; }
  .artist a { color: inherit; text-decoration: none; }
  .cover { width: 100%; aspect-ratio: 1/1; border-radius: 10px; border: 0.5px solid #3a322c; display: block; object-fit: cover; background: #221b16; }
  .title { font-size: 22px; font-weight: 600; margin: 20px 0 4px; }
  .tag { color: #9c8a7b; font-size: 13px; margin: 0 0 24px; }
  .save { display: flex; align-items: center; justify-content: center; gap: 9px; background: #1db954; color: #0b3d20; font-size: 16px; font-weight: 600; text-decoration: none; padding: 15px; border-radius: 26px; width: 100%; }
  .save:active { transform: scale(0.985); }
  .hint { color: #8a7b6d; font-size: 12px; margin-top: 12px; line-height: 1.5; }
  .foot { color: #6f6157; font-size: 11px; margin-top: 22px; padding-top: 16px; border-top: 0.5px solid #2c251f; }
  .foot a { color: #8a7b6d; text-decoration: none; }
</style>
</head>
<body>
  <main class="card">
    <div class="artist"><a href="/">Solomon Nights</a></div>
    <img class="cover" alt="@@TITLE@@ — Solomon Nights cover art" src="@@COVER@@" />
    <h1 class="title">@@TITLE@@</h1>
    <p class="tag">@@TAGLINE@@</p>
    <a id="save" class="save" href="https://open.spotify.com/track/@@TRACK@@?context=spotify:playlist:@@PLAYLIST@@">
      <svg width="19" height="19" viewBox="0 0 24 24" fill="#0b3d20" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm4.59 14.44a.62.62 0 0 1-.86.21c-2.35-1.44-5.3-1.76-8.79-.96a.62.62 0 1 1-.28-1.21c3.82-.88 7.09-.5 9.72 1.1.3.18.39.57.21.86Zm1.22-2.72a.78.78 0 0 1-1.07.26c-2.69-1.66-6.79-2.14-9.97-1.17a.78.78 0 1 1-.45-1.49c3.63-1.1 8.15-.57 11.24 1.33.36.22.48.7.25 1.07Zm.11-2.84C14.8 8.92 9.5 8.74 6.45 9.67a.93.93 0 1 1-.54-1.78c3.5-1.06 9.35-.86 12.99 1.3a.93.93 0 1 1-.95 1.6Z"/></svg>
      Save on Spotify
    </a>
    <p class="hint">Opens in the Spotify app on this song —<br>tap the heart to save the playlist</p>
    <div class="foot">Part of the <a href="https://open.spotify.com/playlist/@@PLAYLIST@@">“This is Solomon Nights”</a> playlist</div>
  </main>
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','@@PIXEL@@');
var utm={};location.search.replace(/^\\?/,'').split('&').forEach(function(p){
  if(!p)return;var kv=p.split('=');if(/^utm_/.test(kv[0]))utm[kv[0]]=decodeURIComponent(kv[1]||'');});
var meta=Object.assign({artist:'solomon_nights',song:'@@TITLE@@',content_name:'@@TITLE@@',content_category:'solomon_nights'},utm);
fbq('track','PageView',meta);
fbq('track','ViewContent',meta);
document.getElementById('save').addEventListener('click',function(){fbq('trackCustom','SpotifySaveClick',meta);});
</script>
<noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=@@PIXEL@@&ev=PageView&noscript=1"/></noscript>
</body>
</html>
"""

HOME = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>Solomon Nights — stripped-back songs for the quiet hours</title>
<meta name="description" content="Solomon Nights: spare, acoustic songs about faith, doubt, grief and quiet hope. Listen and save the playlist on Spotify." />
<meta property="og:title" content="Solomon Nights" />
<meta property="og:description" content="Stripped-back songs about faith, doubt, grief and quiet hope. Listen on Spotify." />
<meta property="og:image" content="@@OG@@" />
<meta property="og:url" content="https://@@DOMAIN@@/" />
<meta name="theme-color" content="#15110f" />
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html, body { margin: 0; }
  body { background: #15110f; color: #f3ece4; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.65; }
  .serif { font-family: "Cormorant Garamond", Georgia, serif; }
  .wrap { max-width: 760px; margin: 0 auto; padding: 0 22px; }
  .hero { text-align: center; padding: 64px 22px 40px; }
  .eyebrow { color: #c9a27a; font-size: 12px; letter-spacing: 4px; text-transform: uppercase; }
  .name { font-size: 56px; font-weight: 500; line-height: 1.05; margin: 14px 0 8px; letter-spacing: 0.5px; }
  .sub { color: #b9a895; font-size: 21px; font-style: italic; margin: 0 auto 26px; max-width: 30ch; }
  .cta { display: inline-flex; align-items: center; gap: 9px; background: #1db954; color: #0b3d20; font-size: 16px; font-weight: 600; text-decoration: none; padding: 14px 26px; border-radius: 26px; }
  .cta:active { transform: scale(0.985); }
  .about { padding: 14px 0 8px; }
  .about p { color: #d8ccc0; font-size: 17px; margin: 0 0 18px; }
  .quote { font-size: 30px; color: #f3ece4; text-align: center; margin: 40px auto; max-width: 22ch; line-height: 1.25; }
  .quote .by { display: block; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-style: normal; font-size: 12px; letter-spacing: 2px; text-transform: uppercase; color: #c9a27a; margin-top: 14px; }
  h2 { font-size: 15px; letter-spacing: 2px; text-transform: uppercase; color: #c9a27a; font-weight: 500; margin: 48px 0 18px; text-align: center; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 14px; }
  .song { text-decoration: none; color: #e9ddd1; }
  .song img { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 9px; border: 0.5px solid #3a322c; display: block; }
  .song span { display: block; font-size: 13px; margin-top: 8px; }
  .song:active img { transform: scale(0.99); }
  .listen { text-align: center; margin: 40px 0 8px; }
  .listen a { color: #c4b5a6; text-decoration: none; font-size: 14px; margin: 0 12px; border-bottom: 0.5px solid #4a4038; padding-bottom: 2px; }
  .foot { text-align: center; color: #6f6157; font-size: 12px; margin: 48px 0 40px; padding-top: 22px; border-top: 0.5px solid #2c251f; }
  .foot a { color: #9c8a7b; text-decoration: none; margin: 0 9px; }
  .social { margin-bottom: 14px; }
  .social a { color: #c4b5a6; display: inline-block; margin: 0 11px; }
  .social svg { width: 23px; height: 23px; vertical-align: middle; }
  @media (max-width: 560px) { .name { font-size: 44px; } .sub { font-size: 19px; } .quote { font-size: 25px; } }
</style>
</head>
<body>
  <header class="hero">
    <div class="eyebrow">Singer · songwriter</div>
    <div class="name serif">Solomon Nights</div>
    <p class="sub serif">Stripped-back songs for faith, doubt, and the quiet hours.</p>
    <a class="cta" href="https://open.spotify.com/playlist/@@PLAYLIST@@">Save the playlist on Spotify</a>
  </header>

  <div class="wrap">
    <section class="about">
      <p>Solomon Nights makes music for the in-between hours, the late nights and early mornings, when the noise finally drops and the honest questions rise. The songs are spare and unhurried, words that sit with grief and grace, doubt and surrender, and the stubborn hope of being held when you can barely hold on.</p>
      <p>There are no easy answers here, and no easy hallelujahs, only the kind that cost something. If you’ve ever prayed in the dark, carried more than you let on, or kept walking when you couldn’t see the road, these songs were written for you.</p>
    </section>

    <blockquote class="quote serif">“Lead me when I cannot see, hold me when I cannot stand.”<span class="by">— When I Cannot See</span></blockquote>

    <h2>The songs</h2>
    <div class="grid">
@@GRID@@
    </div>

    <div class="listen">
      <a href="https://open.spotify.com/artist/7okTzi9u2gLE1dvRC6hnAm">Spotify</a>
      <a href="https://music.apple.com/gb/artist/solomon-nights/1896549972">Apple Music</a>
      <a href="https://www.youtube.com/@SolomonNights">YouTube</a>
      <a href="https://www.deezer.com/en/artist/390290591">Deezer</a>
    </div>

    <footer class="foot">
      <div class="social">
        <a href="https://www.instagram.com/solomonnightsartist/" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg></a>
        <a href="https://www.facebook.com/SolomonNights/" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7h2.4l.45-3H13.5V9.1c0-.86.27-1.45 1.5-1.45h1.5V5.03A20 20 0 0 0 14.36 4.9C12.13 4.9 10.5 6.26 10.5 8.77V11H8.1v3h2.4v7h3z"/></svg></a>
        <a href="https://www.tiktok.com/@solomon.nights" aria-label="TikTok"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.6 3c.32 2.06 1.5 3.43 3.5 3.6v2.66c-1.16.1-2.18-.26-3.36-.97v6.05c0 4.06-3.34 6.4-6.65 5.46-3.9-1.1-4.62-6.06-1.08-7.86.95-.48 1.86-.55 2.99-.4v2.79c-.43-.13-.86-.2-1.27-.13-1.07.18-1.74 1.05-1.55 2.13.18 1.02 1.2 1.66 2.26 1.46 1-.18 1.66-1.04 1.66-2.18V3h3.5z"/></svg></a>
      </div>
      <div>© Solomon Nights</div>
    </footer>
  </div>
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','@@PIXEL@@');fbq('track','PageView',{artist:'solomon_nights'});
</script>
</body>
</html>
"""

CARD = '      <a class="song" href="/@@SLUG@@"><img src="@@COVER@@" alt="@@TITLE@@ cover art" /><span>@@TITLE@@</span></a>'

def main():
    songs = json.load(open(os.path.join(HERE, "songs.json")))
    cards, first_cover = [], ""
    for s in songs:
        slug = slugify(s["title"]); cov = cover(s["trackId"])
        if not first_cover: first_cover = cov
        page = render(PAGE, TITLE=s["title"], SLUG=slug, COVER=cov, TRACK=s["trackId"],
                      PLAYLIST=PLAYLIST, PIXEL=PIXEL, DOMAIN=DOMAIN, TAGLINE=TAGLINE)
        os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
        open(os.path.join(ROOT, slug, "index.html"), "w", encoding="utf-8").write(page)
        cards.append(render(CARD, SLUG=slug, COVER=cov, TITLE=s["title"]))
        print("built /%s" % slug)
    home = render(HOME, PLAYLIST=PLAYLIST, PIXEL=PIXEL, DOMAIN=DOMAIN, OG=first_cover,
                  GRID="\n".join(cards))
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(home)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()
    print("built / (homepage) + .nojekyll : %d songs" % len(songs))

if __name__ == "__main__":
    main()
