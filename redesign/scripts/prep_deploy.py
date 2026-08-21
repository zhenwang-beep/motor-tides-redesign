#!/usr/bin/env python3
"""Generate deploy-ready variants of the redesign pages.

Local repo keeps relative links (works with bundled images via any static host).
Deploy variants target four Vercel projects with images rewritten to the
property's RentCafe CDN via vercel.json rewrites.
"""
import json, os, shutil

ROOT = "/Users/wangzhen/Documents/wiseman website/redesign"
OUT = os.path.join(ROOT, "deploy")

HUB_URL = "https://motor-tides-concepts.vercel.app"
CONCEPT_URL = {
    "a": "https://motor-tides-concept-a.vercel.app",
    "b": "https://motor-tides-concept-b.vercel.app",
    "c": "https://motor-tides-concept-c.vercel.app",
    "e": "https://motor-tides-concept-e.vercel.app",
    "nocturne": "https://motor-tides-concept-nocturne.vercel.app",
    "riviera": "https://motor-tides-concept-riviera.vercel.app",
    "monogram": "https://motor-tides-concept-monogram.vercel.app",
    "grandtour": "https://motor-tides-concept-grandtour.vercel.app",
    "voyage": "https://motor-tides-concept-voyage.vercel.app",
    "current": "https://motor-tides-current.vercel.app",
}

CDN = "https://resource.rentcafe.com/image/upload/{t}/s3/2/9707/{f}"
PHOTO_T = "q_auto,f_auto,c_limit,w_1800"
PLAN_T = "q_auto,f_auto,c_limit,w_1200"
LOGO_T = "q_auto,f_auto,c_limit,w_400"

MAP = {
    "hero-living.jpg": (PHOTO_T, "motor%20tides%20-%20unit%20705%20-%20kithcenm%20small%20dining,%20lr,%20and%20patio_final.jpg"),
    "kitchen-dining.jpg": (PHOTO_T, "motor%20tides%20-%20unit%20705%20-%20kithcenm%20small%20dining_%20lr_%20and%20patio_final%20(1).jpg"),
    "bedroom-705.jpg": (PHOTO_T, "motor%20tides%20-%20unit%20705%20-%20bedroom%20and%20closets%20-%20add%20fridge%20in%20background_final%20(1).jpg"),
    "entry-705.jpg": (PHOTO_T, "motor%20tides%20-%20unit%20705%20-%20entryway,%20kitchen,%20lr_final_logo.jpg"),
    "kitchen-716.jpg": (PHOTO_T, "motor%20tides%20-%20unit%20716%20-%20kitchen%20and%20add%20fridge_final.jpg"),
    "living-panorama-716.jpg": (PHOTO_T, "motor%20tides%20-%20unit%20716%20-%20kitchen,%20small%20dining,%20living%20room,%20patio_final.jpg"),
    "living-art-716.jpg": (PHOTO_T, "motor%20tides%20-%20unit%20716%20-%20living%20room%20and%20patio_final_logo.jpg"),
    "patio-716.jpg": (PHOTO_T, "motor%20tides%20-%20unit%20716%20-%20patio_final_logo.jpg"),
    "exterior-facade.jpg": (PHOTO_T, "motor%20tabor%20street-1%20(1).jpg"),
    "exterior-glass.jpg": (PHOTO_T, "4g5a9749%20(1).jpg"),
    "rooftop-aerial.jpg": (PHOTO_T, "dji_0257%20(2).jpg"),
    "rooftop-1.jpg": (PHOTO_T, "3557%20motor%20ave%20rooftop%20hdr-4.jpg"),
    "rooftop-2.jpg": (PHOTO_T, "3557%20motor%20ave%20rooftop%20hdr-7.jpg"),
    "rooftop-3.jpg": (PHOTO_T, "3557%20motor%20ave%20rooftop%20hdr-10.jpg"),
    "rooftop-4.jpg": (PHOTO_T, "4g5a9728%20(1).jpg"),
    "kitchen-steel.jpg": (PHOTO_T, "4g5a9158.jpg"),
    "kitchen-oven.jpg": (PHOTO_T, "4g5a9323(1).jpg"),
    "view-city.jpg": (PHOTO_T, "4g5a9405(2).jpg"),
    "balcony-slider.jpg": (PHOTO_T, "4g5a9671(3).jpg"),
    "kitchen-view.jpg": (PHOTO_T, "4g5a9559(3).jpg"),
    "balcony-city.jpg": (PHOTO_T, "4g5a9711(3).jpg"),
    "bedroom-414.jpg": (PHOTO_T, "3557%20motor%20ave%20unit%20414%20hdr-9.jpg"),
    "living-green.jpg": (PHOTO_T, "3557%20motor%20ave%20unit%20414%20hdr-8.jpg"),
    "closet-414.jpg": (PHOTO_T, "3557%20motor%20ave%20unit%20414%20hdr-1.jpg"),
    "kitchen-714.jpg": (PHOTO_T, "3557%20motor%20ave%20unit%20ph%2014%20(714)%20hdr-7.jpg"),
    "plan-lighthouse.png": (PLAN_T, "mt-317,%20517,%20617,%20717(ph17).png"),
    "plan-channel.png": (PLAN_T, "mt-318_418_618_718(ph18).png"),
    "plan-pacific.png": (PLAN_T, "mt-307_407_507_607_707(ph7).png"),
    "plan-reef.png": (PLAN_T, "mt-422_622_722(ph22).png"),
    "plan-harbor.png": (PLAN_T, "mt-405_505_605_705(ph5).png"),
    "plan-seacliff.png": (PLAN_T, "mt-608.png"),
    "plan-coral.png": (PLAN_T, "mt-315,%20415,%20515,%20615,%20715(ph15).png"),
    "wiseman-logo.png": (LOGO_T, "logo(3).png"),
}

def vercel_json():
    # Vercel's router treats "(" ")" in destinations as regex groups; percent-encode them.
    rewrites = [
        {"source": f"/assets/img/{name}",
         "destination": CDN.format(t=t, f=f).replace("(", "%28").replace(")", "%29")}
        for name, (t, f) in MAP.items()
    ]
    return json.dumps({"rewrites": rewrites}, indent=1)

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    vj = vercel_json()

    # hub
    os.makedirs(os.path.join(OUT, "hub"))
    hub = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    for k, url in CONCEPT_URL.items():
        # handles both plain links and links with query strings (?chat=...)
        hub = hub.replace(f'href="option-{k}/index.html', f'href="{url}/index.html')
    with open(os.path.join(OUT, "hub", "index.html"), "w", encoding="utf-8") as fp:
        fp.write(hub)
    with open(os.path.join(OUT, "hub", "vercel.json"), "w", encoding="utf-8") as fp:
        fp.write(vj)
    prev_src = os.path.join(ROOT, "assets", "img", "previews")
    if os.path.isdir(prev_src):
        shutil.copytree(prev_src, os.path.join(OUT, "hub", "assets", "img", "previews"))
        print("hub", "assets/img/previews", len(os.listdir(prev_src)))

    # concepts (each option dir may hold several pages plus css/js assets)
    chat = open(os.path.join(ROOT, "assets", "chat.js"), encoding="utf-8").read()
    for k in ("a", "b", "c", "e", "nocturne", "riviera", "monogram", "grandtour", "voyage", "current"):
        d = os.path.join(OUT, k)
        os.makedirs(d)
        src_dir = os.path.join(ROOT, f"option-{k}")
        for name in sorted(os.listdir(src_dir)):
            src = os.path.join(src_dir, name)
            if not os.path.isfile(src):
                continue
            if name.endswith(".html"):
                html = open(src, encoding="utf-8").read()
                html = html.replace("../assets/chat.js", "/chat.js")
                html = html.replace("../assets/img/", "/assets/img/")
                html = html.replace('href="../index.html"', f'href="{HUB_URL}/"')
                html = html.replace("href='../index.html'", f"href='{HUB_URL}/'")
                with open(os.path.join(d, name), "w", encoding="utf-8") as fp:
                    fp.write(html)
            else:
                shutil.copy2(src, os.path.join(d, name))
        trim_src = os.path.join(ROOT, "assets", "img", "plans-trim")
        if os.path.isdir(trim_src):
            trim_dst = os.path.join(d, "assets", "img", "plans-trim")
            shutil.rmtree(trim_dst, ignore_errors=True)
            shutil.copytree(trim_src, trim_dst)
            print(k, "assets/img/plans-trim", len(os.listdir(trim_dst)))
        with open(os.path.join(d, "chat.js"), "w", encoding="utf-8") as fp:
            fp.write(chat)
        with open(os.path.join(d, "vercel.json"), "w", encoding="utf-8") as fp:
            fp.write(vj)

    # sanity: no stray relative refs remain
    problems = []
    for sub in ("hub", "a", "b", "c", "e", "nocturne", "riviera", "monogram", "grandtour", "voyage", "current"):
        for name in os.listdir(os.path.join(OUT, sub)):
            if not name.endswith(".html"):
                continue
            p = os.path.join(OUT, sub, name)
            s = open(p, encoding="utf-8").read()
            if "../assets" in s or "../index.html" in s:
                problems.append(p)
    print("OK" if not problems else f"PROBLEMS: {problems}")
    for sub in ("hub", "a", "b", "c", "e", "nocturne", "riviera", "monogram", "grandtour", "voyage", "current"):
        for f in sorted(os.listdir(os.path.join(OUT, sub))):
            print(sub, f, os.path.getsize(os.path.join(OUT, sub, f)))

if __name__ == "__main__":
    main()
