#!/usr/bin/env python3
"""Publicador de Instagram de Bataká (Instagram API with Instagram Login).

Lee ig/queue.json y publica los posts cuya fecha ya pasó, solo si "aprobado": true.
Las imágenes se sirven desde GitHub Pages (https://batakataka.github.io/ig/...).
Guarda lo publicado en ig/published.json (el workflow lo commitea).

Modos:
  python ig_publish.py check     -> verifica el token (no publica nada)
  python ig_publish.py publish   -> publica lo vencido y aprobado
"""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone

API = "https://graph.instagram.com"
SITE = os.environ.get("SITE_URL", "https://batakataka.github.io").rstrip("/")
TOKEN = os.environ.get("IG_TOKEN", "").strip()
USER_ID = os.environ.get("IG_USER_ID", "").strip()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "ig", "queue.json")
DONE = os.path.join(ROOT, "ig", "published.json")


def call(method, path, params=None, base=API):
    params = dict(params or {})
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = f"{base}/{path}" if not path.startswith("http") else path
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise SystemExit(f"Error {e.code} en {path}: {body}")


def wait_ready(cid, tries=30):
    for _ in range(tries):
        st = call("GET", cid, {"fields": "status_code"}).get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise SystemExit(f"Contenedor {cid} falló: {st}")
        time.sleep(5)
    raise SystemExit(f"Contenedor {cid} no terminó a tiempo")


def url_of(img):
    return img if img.startswith("http") else f"{SITE}/ig/{img}"


def publish(item):
    kind = item.get("tipo", "post").lower()
    imgs = item["imagenes"]
    caption = item.get("caption", "")
    if kind == "story":
        cid = call("POST", f"{USER_ID}/media", {"image_url": url_of(imgs[0]), "media_type": "STORIES"})["id"]
    elif len(imgs) > 1 or kind == "carrusel":
        kids = []
        for im in imgs:
            kids.append(call("POST", f"{USER_ID}/media", {"image_url": url_of(im), "is_carousel_item": "true"})["id"])
        for k in kids:
            wait_ready(k)
        cid = call("POST", f"{USER_ID}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": caption})["id"]
    else:
        cid = call("POST", f"{USER_ID}/media", {"image_url": url_of(imgs[0]), "caption": caption})["id"]
    wait_ready(cid)
    return call("POST", f"{USER_ID}/media_publish", {"creation_id": cid})["id"]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "publish"
    if not TOKEN or not USER_ID:
        raise SystemExit("Faltan los secretos IG_TOKEN o IG_USER_ID")

    if mode == "check":
        me = call("GET", "me", {"fields": "user_id,username,account_type"})
        lim = call("GET", f"{USER_ID}/content_publishing_limit", {"fields": "quota_usage,config"})
        print("Token OK ->", me.get("username"), me.get("account_type"), "| cuota:", json.dumps(lim.get("data", lim)))
        return

    queue = json.load(open(QUEUE, encoding="utf-8"))
    done = json.load(open(DONE, encoding="utf-8")) if os.path.exists(DONE) else {}
    now = datetime.now(timezone.utc)
    changed = False
    for item in queue:
        pid = item["id"]
        if pid in done or not item.get("aprobado"):
            continue
        when = datetime.fromisoformat(item["fecha"])
        if when > now:
            continue
        print(f"Publicando {pid} ({item.get('tipo','post')}) programado para {item['fecha']}…")
        media_id = publish(item)
        done[pid] = {"media_id": media_id, "publicado": now.isoformat(timespec="seconds")}
        changed = True
        print(f"  ok -> media {media_id}")
        json.dump(done, open(DONE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        time.sleep(20)  # pausa entre publicaciones
    if not changed:
        print("Nada que publicar ahora.")


if __name__ == "__main__":
    main()
