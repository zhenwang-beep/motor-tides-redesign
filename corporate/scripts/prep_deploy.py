#!/usr/bin/env python3
"""Bundle each direction into a self-contained, deployable static site.

Each direction lives at `corporate/<key>/` and references `../core/*` and `../data/*`.
A deployed bundle has to be flat, so this script copies core/, data/ and assets/ into the
bundle and rewrites the `../` references to root-absolute paths.

    python3 scripts/prep_deploy.py            # build every direction + the hub
    python3 scripts/prep_deploy.py tideline   # just one

Then, per bundle:
    cd deploy/<key>
    vercel link --yes --project wiseman-<key> --scope <scope>
    vercel deploy --prod --yes

The Vercel MCP token cannot create projects — use the CLI.
"""
import os, re, shutil, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "deploy")

HUB_URL = "https://wiseman-concepts.vercel.app"
DIRECTION_URL = {
    "tideline": "https://wiseman-tideline.vercel.app",
    "register": "https://wiseman-register.vercel.app",
    "fivebed":  "https://wiseman-fivebed.vercel.app",
    "nocturne": "https://wiseman-nocturne.vercel.app",
    # Clerestory (folder key `atrium`) is the canonical site.
    "atrium":   "https://wiseman-clerestory.vercel.app",
}

# `../x` and `../../x` both resolve to `/x` once core/, data/ and assets/ sit at the bundle root.
REWRITES = [
    (re.compile(r'(["\'(])\.\./\.\./(core|data|assets)/'), r"\1/\2/"),
    (re.compile(r'(["\'(])\.\./(core|data|assets)/'), r"\1/\2/"),
]


def stamp(path):
    """Content hash for cache-busting, so a shared asset never serves stale."""
    h = hashlib.md5(open(path, "rb").read()).hexdigest()[:8]
    return h


def rewrite_html(text, versions, depth):
    for pat, rep in REWRITES:
        text = pat.sub(rep, text)
    # normalise hand-written ?v= numbers to a content hash
    for name, v in versions.items():
        text = re.sub(r'(/?(?:core/)?' + re.escape(name) + r')\?v=[\w.]+', r"\1?v=" + v, text)
    # a page one level deep links back to the direction root with ../
    return text


def copy_tree(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)


def rewrite_paths_inplace(root):
    """core/ is copied verbatim, but its own text files can still carry `../data/`
    style references (core.js defaults its fetch to '../data/wiseman.json'). That
    resolves correctly in development, where a page sits at /<direction>/page.html,
    but a deployed bundle is flat — the page is at / — so the same relative path
    walks outside the site root and 404s. Rewrite the copied files the same way the
    direction's own pages are rewritten."""
    n = 0
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if not f.endswith((".js", ".css", ".html")):
                continue
            fp = os.path.join(dirpath, f)
            text = open(fp, encoding="utf-8").read()
            out = text
            for pat, rep in REWRITES:
                out = pat.sub(rep, out)
            if out != text:
                open(fp, "w", encoding="utf-8").write(out)
                n += 1
    return n


def build(key, quiet=False):
    src = os.path.join(ROOT, key)
    if not os.path.isdir(src):
        print("  ! no such direction: %s" % key)
        return 0
    dst = os.path.join(OUT, key)
    # `vercel link` writes .vercel/project.json into the bundle, and that file is
    # the ONLY thing tying this folder to an existing Vercel project. Wiping it
    # with the rest of the bundle makes the next `vercel deploy` look unlinked,
    # and the CLI then silently creates a BRAND NEW project named after the
    # folder ("atrium") and ships there — while the link everyone has been given
    # (wiseman-clerestory.vercel.app) quietly stays on the previous build.
    # That happened twice. Carry the link across the rebuild.
    keep = os.path.join(dst, ".vercel")
    stash = None
    if os.path.isdir(keep):
        stash = os.path.join(OUT, ".vercel-%s.keep" % key)
        shutil.rmtree(stash, ignore_errors=True)
        shutil.move(keep, stash)
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(dst)
    if stash:
        shutil.move(stash, keep)

    copy_tree(os.path.join(ROOT, "core"), os.path.join(dst, "core"))
    rewrite_paths_inplace(os.path.join(dst, "core"))
    os.makedirs(os.path.join(dst, "data"), exist_ok=True)
    for f in ("wiseman.json", "index.json"):
        p = os.path.join(ROOT, "data", f)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(dst, "data", f))
    os.makedirs(os.path.join(dst, "assets", "img"), exist_ok=True)
    for f in sorted(os.listdir(os.path.join(ROOT, "assets", "img"))):
        if f.startswith("_"):
            continue
        shutil.copy2(os.path.join(ROOT, "assets", "img", f), os.path.join(dst, "assets", "img", f))

    versions = {}
    for rel in ("core/base.css", "core/core.js"):
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            versions[os.path.basename(rel)] = stamp(p)
    for rel in ("style.css", "app.js"):
        p = os.path.join(src, rel)
        if os.path.exists(p):
            versions[rel] = stamp(p)

    n = 0
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = [d for d in dirnames if d not in ("templates", "__pycache__", ".vercel")]
        for f in filenames:
            if f.endswith((".py", ".pyc", ".DS_Store")):
                continue
            s = os.path.join(dirpath, f)
            rel = os.path.relpath(s, src)
            d = os.path.join(dst, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            if f.endswith((".html", ".css", ".js")):
                text = open(s, encoding="utf-8").read()
                depth = rel.count(os.sep)
                open(d, "w", encoding="utf-8").write(rewrite_html(text, versions, depth))
            else:
                shutil.copy2(s, d)
            n += 1

    json.dump({"cleanUrls": False, "trailingSlash": False}, open(os.path.join(dst, "vercel.json"), "w"))

    # sanity: nothing may still reach outside the bundle
    bad = []
    for dirpath, _, filenames in os.walk(dst):
        for f in filenames:
            if f.endswith((".html", ".css", ".js")):
                t = open(os.path.join(dirpath, f), encoding="utf-8").read()
                if re.search(r'["\'(]\.\./(core|data|assets)/', t):
                    bad.append(os.path.relpath(os.path.join(dirpath, f), dst))
    if not quiet:
        size = sum(os.path.getsize(os.path.join(dp, f))
                   for dp, _, fs in os.walk(dst) for f in fs) / 1e6
        print("  %-10s %3d files  %5.1f MB  %s" % (key, n, size, "OK" if not bad else "PROBLEMS: %s" % bad[:4]))
    return n


def build_hub():
    src = os.path.join(ROOT, "hub")
    if not os.path.isdir(src):
        return 0
    dst = os.path.join(OUT, "hub")
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)
    copy_tree(os.path.join(ROOT, "assets", "img", "previews"), os.path.join(dst, "previews"))
    logo = os.path.join(ROOT, "assets", "img", "wiseman-logo.png")
    if os.path.exists(logo):
        os.makedirs(os.path.join(dst, "assets", "img"), exist_ok=True)
        shutil.copy2(logo, os.path.join(dst, "assets", "img", "wiseman-logo.png"))
    n = 0
    for dp, _, fs in os.walk(dst):
        for f in fs:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dp, f)
            t = open(p, encoding="utf-8").read()
            for k, url in DIRECTION_URL.items():
                t = t.replace('href="../%s/index.html"' % k, 'href="%s/"' % url)
                t = t.replace('href="../%s/' % k, 'href="%s/' % url)
            t = t.replace('"../assets/img/', '"assets/img/')
            open(p, "w", encoding="utf-8").write(t)
            n += 1
    print("  %-10s %3d files" % ("hub", n))
    return n


if __name__ == "__main__":
    targets = sys.argv[1:]
    if not targets:
        targets = [k for k in DIRECTION_URL if os.path.isdir(os.path.join(ROOT, k))]
        os.makedirs(OUT, exist_ok=True)
        print("building all directions + hub")
    else:
        os.makedirs(OUT, exist_ok=True)
    total = sum(build(t) for t in targets)
    if not sys.argv[1:]:
        total += build_hub()
    print("%d files bundled into %s" % (total, OUT))
