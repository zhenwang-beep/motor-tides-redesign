#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble midway/deploy/ — one Vercel project holding the hub and all three
concepts.

Motor Tides needed a project per concept because each concept was its own
document root with its own image rewrites. Midway does not: the hub and the
three concepts are one tree of relative links, and the photography is loaded
straight from the property's RentCafe CDN rather than rewritten, so there is
nothing to give a separate project. One project, one URL, relative links that
work locally and deployed without being rewritten.

    python3 midway/build/build.py          # regenerate the pages
    python3 midway/scripts/prep_deploy.py  # stage them
    cd midway/deploy && vercel deploy --prod --yes
"""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "deploy")

CONCEPTS = ["golden-hour", "crossing", "open-door"]
PAGES = ["index", "floorplans", "amenities", "gallery", "tours", "map", "contact"]

VERCEL = {
    # cleanUrls MUST stay off. With it on, /golden-hour/index.html 308s to
    # /golden-hour — no trailing slash — and the browser then resolves every
    # relative link on that page against the ROOT: "floorplans.html" becomes
    # /floorplans.html, which 404s. A visitor arriving from a hub card got a
    # home page whose entire nav, footer and CTAs were dead. Verified against
    # the live deploy before changing.
    "cleanUrls": False,
    "trailingSlash": False,
    "headers": [
        {
            "source": "/(.*)",
            "headers": [
                # These are unreleased design concepts for a live property —
                # they should not be indexed alongside the real site.
                {"key": "X-Robots-Tag", "value": "noindex, nofollow"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "X-Content-Type-Options", "value": "nosniff"},
            ],
        },
        {
            # These concepts are redeployed while people are reviewing them, and
            # the filenames never change, so a long max-age just serves whoever
            # looked five minutes ago a stale stylesheet. The CDN still caches;
            # the browser revalidates.
            "source": "/assets/(.*)",
            "headers": [{"key": "Cache-Control",
                         "value": "public, max-age=0, must-revalidate"}],
        },
    ],
}


def main():
    if not os.path.isdir(os.path.join(ROOT, CONCEPTS[0])):
        raise SystemExit("No concept pages found — run build/build.py first.")

    # `vercel link` writes .vercel/ INTO this directory. Wiping the whole tree
    # threw that link away, and the next `vercel deploy` silently created a new
    # project named after the folder ("deploy") instead of updating the real
    # one. Preserve it across rebuilds.
    link = os.path.join(OUT, ".vercel")
    saved = None
    if os.path.isdir(link):
        saved = os.path.join(os.path.dirname(OUT), ".vercel.saved")
        shutil.rmtree(saved, ignore_errors=True)
        shutil.copytree(link, saved)

    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)

    if saved:
        shutil.copytree(saved, link)
        shutil.rmtree(saved, ignore_errors=True)

    total = 0
    shutil.copy2(os.path.join(ROOT, "index.html"), os.path.join(OUT, "index.html"))
    total += 1

    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))

    for c in CONCEPTS:
        dst = os.path.join(OUT, c)
        os.makedirs(dst)
        for p in PAGES:
            name = f"{p}.html"
            src = os.path.join(ROOT, c, name)
            if not os.path.isfile(src):
                raise SystemExit(f"missing page: {c}/{name}")
            shutil.copy2(src, os.path.join(dst, name))
            total += 1

    with open(os.path.join(OUT, "vercel.json"), "w", encoding="utf-8") as fp:
        json.dump(VERCEL, fp, indent=2)

    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fp:
        fp.write("User-agent: *\nDisallow: /\n")

    # No page may reference a build-only path, and nothing may point at a
    # local image directory — every photograph must come from the CDN.
    problems = []
    for dirpath, _dirs, files in os.walk(OUT):
        for f in files:
            if not f.endswith(".html"):
                continue
            path = os.path.join(dirpath, f)
            s = open(path, encoding="utf-8").read()
            rel = os.path.relpath(path, OUT)
            if "/build/" in s or "_audit" in s or "_sweep" in s:
                problems.append(f"{rel}: references build tooling")
            if 'src="/assets/img' in s or 'src="assets/img' in s:
                problems.append(f"{rel}: references a local image path")
            if "localhost" in s:
                problems.append(f"{rel}: references localhost")

    size = sum(os.path.getsize(os.path.join(dp, f))
               for dp, _d, fs in os.walk(OUT) for f in fs)
    print(f"  staged {total} pages + assets -> {os.path.relpath(OUT)}")
    print(f"  bundle {size/1024:.0f} KB")
    if problems:
        print("\n  PROBLEMS:")
        for p in problems:
            print("   ", p)
        raise SystemExit(1)
    print("  checks OK — no build refs, no local image paths, no localhost\n")


if __name__ == "__main__":
    main()
