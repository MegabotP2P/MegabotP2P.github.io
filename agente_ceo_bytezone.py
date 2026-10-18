import os
import sys
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
import html
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Hora de Venezuela (UTC-4)
VET_TZ = timezone(timedelta(hours=-4))
now_vet = datetime.now(VET_TZ)

def get_week_id(dt):
    weekday = dt.weekday() # 0 = Lunes, 6 = Domingo
    monday = dt - timedelta(days=weekday)
    return f"W{monday.strftime('%Y-%m-%d')}"

WEEK_ID = get_week_id(now_vet)
FECHA_HUMANA = now_vet.strftime("%d/%m/%Y")

RSS_SOURCES = [
    ("Hipertextual IA", "https://hipertextual.com/inteligencia-artificial/feed"),
    ("Xataka IA & Tech", "https://www.xataka.com/tag/inteligencia-artificial/rss2.xml"),
    ("Genbeta IA", "https://www.genbeta.com/tag/inteligencia-artificial/rss2.xml"),
    ("Google News IA & Gadgets", "https://news.google.com/rss/search?q=inteligencia+artificial+OR+invento+OR+robot+OR+smartphone&hl=es-419&gl=US&ceid=US:es-419"),
]

# Imágenes tecnológicas de alta definición de respaldo por temática
THEME_IMAGES = [
    "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=900&q=80",
]

def clean_html_text(raw):
    if not raw:
        return ""
    text = html.unescape(raw)
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_paragraphs_from_html(raw_html):
    if not raw_html:
        return []
    matches = re.findall(r'<p[^>]*>(.*?)</p>', raw_html, flags=re.DOTALL | re.IGNORECASE)
    paragraphs = []
    for m in matches:
        cleaned = clean_html_text(m)
        if len(cleaned) >= 45 and not cleaned.lower().startswith(("lee también", "te puede interesar", "suscríbete")):
            paragraphs.append(cleaned)
    return paragraphs

def extract_first_image(raw_html):
    if not raw_html:
        return None
    m = re.search(r'<img[^>]+src=["\'](https?://[^"\']+)["\']', raw_html, flags=re.IGNORECASE)
    if m:
        url = html.unescape(m.group(1)).strip()
        if not any(bad in url.lower() for bad in ["avatar", "pixel", "logo", "1x1", "feedburner"]):
            return url
    return None

def make_complete_sentences(text, max_sentences=3, max_chars=420):
    """Garantiza que el resumen SIEMPRE cierre en punto final completo y NUNCA quede cortado con '...' a mitad de frase."""
    if not text:
        return ""
    text = re.sub(r'\.\.\.+$', '.', text.strip())
    text = re.sub(r'…+$', '.', text.strip())
    # Proteger abreviaturas comunes (EE. UU., EE.UU., etc.) para no cortar la frase a mitad
    protected = text.replace("EE. UU.", "EE__UU__").replace("EE.UU.", "EE__UU__").replace("Dr.", "Dr__").replace("Sr.", "Sr__")
    sentence_list = re.split(r'(?<=[.!?])\s+', protected)
    selected = []
    total_len = 0
    for s in sentence_list:
        s = s.replace("EE__UU__", "Estados Unidos").replace("Dr__", "Dr.").replace("Sr__", "Sr.").strip()
        if not s:
            continue
        if (s.endswith("...") or s.endswith("…") or s[-1] not in ".!?") and len(selected) >= 1:
            break
        if total_len + len(s) > max_chars and len(selected) >= 1:
            break
        if s[-1] not in ".!?":
            s = s.rstrip(",;:") + "."
        selected.append(s)
        total_len += len(s)
        if len(selected) >= max_sentences:
            break
    if not selected:
        cleaned = text[:max_chars].rsplit(' ', 1)[0].rstrip(".,;:… ")
        return cleaned + "."
    return " ".join(selected)

def fetch_article_details(url, fallback_img):
    """Intenta extraer imagen og:image y párrafos completos de la página del artículo."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            page_html = resp.read().decode('utf-8', errors='ignore')
        img_url = fallback_img
        og_img = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](https?://[^"\']+)["\']', page_html, re.IGNORECASE)
        if not og_img:
            og_img = re.search(r'<meta[^>]+content=["\'](https?://[^"\']+)["\'][^>]+property=["\']og:image["\']', page_html, re.IGNORECASE)
        if og_img:
            img_url = og_img.group(1)
        paras = extract_paragraphs_from_html(page_html)
        return img_url, paras[:8]
    except Exception:
        return fallback_img, []

def build_rich_article(title, source_label, raw_paragraphs, short_desc):
    """Construye un artículo completo, cerrado y bien estructurado para leer y escuchar sin cortes."""
    valid_paras = [p for p in raw_paragraphs if len(p) > 50 and not p.endswith("...")]
    if len(valid_paras) >= 3:
        body_paragraphs = valid_paras[:6]
    else:
        lead = make_complete_sentences(short_desc, max_sentences=3, max_chars=420)
        if not lead or len(lead) < 60:
            lead = f"Un nuevo avance tecnológico reportado por {source_label} ha captado la atención de la industria esta semana en torno a: {title}."
        body_paragraphs = [
            lead,
            f"De acuerdo con el reporte publicado por {source_label}, este desarrollo forma parte de la nueva ola de innovaciones de 2026 que están transformando la manera en que los usuarios interactúan con la Inteligencia Artificial, la seguridad digital y los dispositivos inteligentes.",
            "Los especialistas destacan que la velocidad de adopción de estas herramientas está obligando tanto a empresas tecnológicas como a usuarios cotidianos a actualizar sus equipos y conocer las nuevas funciones integradas.",
            "En ByteZone seguiremos monitoreando de cerca cómo evoluciona esta noticia durante las próximas semanas para traerte todos los detalles y su impacto directo en tus dispositivos."
        ]

    # Resumen hablado cerrado (2 a 3 oraciones completas con cierre natural)
    spoken_summary = make_complete_sentences(" ".join(body_paragraphs[:2]), max_sentences=2, max_chars=310)
    return spoken_summary, body_paragraphs

def fetch_latest_tech_news():
    items = []
    seen_titles = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ByteZoneCEOAgent/2.0'}
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/', 'media': 'http://search.yahoo.com/mrss/'}

    for source_name, url in RSS_SOURCES:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                xml_data = resp.read()
            root = ET.fromstring(xml_data)
            count_from_source = 0
            for item in root.findall('.//item'):
                title = clean_html_text(item.findtext('title') or '')
                link = (item.findtext('link') or '').strip()
                raw_desc = item.findtext('description') or ''
                raw_content = item.findtext('content:encoded', namespaces=ns) or ''

                if not title or len(title) < 20:
                    continue
                if " - " in title:
                    parts = title.rsplit(" - ", 1)
                    if len(parts[1]) < 30:
                        source_label = parts[1].strip()
                        title = parts[0].strip()
                    else:
                        source_label = source_name
                else:
                    source_label = source_name

                key = title[:35].lower()
                if key in seen_titles:
                    continue
                seen_titles.add(key)

                idx_img = THEME_IMAGES[len(items) % len(THEME_IMAGES)]
                img_url = extract_first_image(raw_content) or extract_first_image(raw_desc)
                media_el = item.find('media:content', namespaces=ns) or item.find('enclosure')
                if not img_url and media_el is not None and media_el.attrib.get('url'):
                    img_url = media_el.attrib.get('url')

                paras = extract_paragraphs_from_html(raw_content)
                if not paras:
                    paras = extract_paragraphs_from_html(raw_desc)

                if (not img_url or len(paras) < 2) and link and "news.google.com" not in link:
                    fetched_img, fetched_paras = fetch_article_details(link, idx_img)
                    if not img_url:
                        img_url = fetched_img
                    if len(fetched_paras) > len(paras):
                        paras = fetched_paras

                if not img_url:
                    img_url = idx_img

                short_desc = clean_html_text(raw_desc)
                spoken_summary, full_paragraphs = build_rich_article(title, source_label, paras, short_desc)
                full_voice_script = f"{title}. Noticia publicada por {source_label}. " + " ".join(full_paragraphs)

                items.append({
                    "id": f"news_{len(items) + 1}",
                    "title": title,
                    "summary": spoken_summary,
                    "voice_extra": spoken_summary,
                    "full_paragraphs": full_paragraphs,
                    "full_voice_script": full_voice_script,
                    "image": img_url,
                    "source": source_label,
                    "link": link
                })
                count_from_source += 1
                if count_from_source >= 2 or len(items) >= 5:
                    break
        except Exception as e:
            print(f"[Aviso RSS] {source_name}: {e}")
        if len(items) >= 5:
            break

    return items[:5]

def build_video_reel_scenes(news_list):
    icons = ["🤖", "🚀", "⚡", "🧠", "🔥"]
    badges = [
        "NOTICIA #1 • IA & FUTURO",
        "NOTICIA #2 • INNOVACIÓN",
        "NOTICIA #3 • TENDENCIA GLOBAL",
        "NOTICIA #4 • IMPACTO TECH",
        "NOTICIA #5 • CIERRE SEMANAL"
    ]
    colors = [
        "from-cyan-600 to-blue-900",
        "from-purple-600 to-indigo-900",
        "from-pink-600 to-rose-900",
        "from-emerald-600 to-teal-900",
        "from-amber-500 to-orange-900"
    ]

    scenes = []
    for idx, item in enumerate(news_list[:5]):
        num = idx + 1
        # Cada escena cierra completamente su idea antes de pasar a la siguiente
        closing_phrase = (
            " Pasamos a la siguiente noticia." if num < len(news_list[:5])
            else " Y con esto cerramos el resumen semanal de ByteZone. Recuerda tocar cualquier noticia para leerla completa o desbloquear el truco VIP abajo."
        )
        voice = f"Noticia número {num}: {item['title']}. {item['summary']}{closing_phrase}"
        scenes.append({
            "id": item["id"],
            "news_index": idx,
            "badge": badges[idx],
            "icon": icons[idx],
            "headline": item["title"],
            "subtext": item["summary"],
            "image": item["image"],
            "source": item["source"],
            "voice_script": voice,
            "bg_gradient": colors[idx],
            "is_vip_hook": (num == len(news_list[:5]))
        })

    return scenes

WEEK_NUM = int(now_vet.strftime("%U"))

WEEKLY_VIP_HACKS = [
    {
        "tag": "Secreto de IA & Celular",
        "title": "Cómo activar el Modo Ultra-Velocidad de Red DNS Privado sin instalar apps",
        "body": "Entra en Ajustes > Conexiones > Más ajustes de conexión > DNS Privado y escribe 'dns.adguard.com' o 'one.one.one.one'. Tu teléfono resolverá páginas y juegos hasta un 35% más rápido y bloqueará rastreadores pesados automáticamente."
    },
    {
        "tag": "Truco Oculto WhatsApp",
        "title": "Enviar fotos y videos en calidad 4K original sin que WhatsApp los pixele",
        "body": "Antes de enviar cualquier foto o video, toca el botón 'HD' arriba en el editor, o adjúntalo como 'Documento' si quieres cero compresión. ¡La diferencia de nitidez es abismal!"
    },
    {
        "tag": "Optimización Gamer",
        "title": "Liberar memoria RAM oculta en 5 segundos antes de jugar",
        "body": "En Chrome o Telegram, cierra las pestañas en segundo plano y activa el modo 'No Molestar' durante tu partida: evita micro-tirones de pantalla cuando buscas récords de menos de 100 milisegundos."
    }
]

VAULT_GAMES_CATALOG = [
    {
        "id": "cyber-dodge",
        "title": "🚀 Cyber Dodge: Tormenta Neón",
        "category": "Reflejos & Esquiva",
        "status": "EN EL BAÚL (JUGABLE)",
        "badge": "JOYA DEL BAÚL 🗄️",
        "description": "Pilota la nave cuántica y esquiva la lluvia de meteoritos cibernéticos a velocidad extrema. Incluye Escudo de Segunda Oportunidad y Ranking en vivo.",
        "url": "juegos/cyber-dodge.html?v=11",
        "accent": "amber"
    }
]

def main():
    print(f"🤖 [Agente CEO ByteZone] Ejecutando actualización autónoma v=11 para la semana {WEEK_ID} ({FECHA_HUMANA})...")
    news = fetch_latest_tech_news()
    scenes = build_video_reel_scenes(news)
    vip_hack = WEEKLY_VIP_HACKS[WEEK_NUM % len(WEEKLY_VIP_HACKS)]

    pulse_data = {
        "version": 11,
        "week_id": WEEK_ID,
        "updated_at": now_vet.isoformat(),
        "updated_human": FECHA_HUMANA,
        "agent_status": {
            "name": "Agente CEO & SEO ByteZone",
            "mode": "Autónomo (Lunes 00:05 AM + Monitoreo Continuo)",
            "active_games_count": 3,
            "vault_games_count": len(VAULT_GAMES_CATALOG)
        },
        "video_reel": {
            "title": f"ByteZone TV • Noticiero IA ({WEEK_ID})",
            "subtitle": "5 Noticias Completas con Imagen + Voz IA + Lectura Completa",
            "duration_label": "5 Noticias",
            "scenes": scenes
        },
        "weekly_news": news,
        "vip_hack_of_the_week": vip_hack,
        "vault_games": VAULT_GAMES_CATALOG
    }

    for target_root in ["portal_bytezone", "bytezone"]:
        data_dir = os.path.join(target_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        out_path = os.path.join(data_dir, "weekly_pulse.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(pulse_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Archivo actualizado: {out_path} ({len(news)} noticias completas con imágenes y {len(scenes)} escenas)")

if __name__ == "__main__":
    main()
