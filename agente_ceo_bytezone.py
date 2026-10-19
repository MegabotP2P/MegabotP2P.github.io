import os
import sys
import json
import hashlib
import random
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import html
import re
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==========================================================
# AGENTE CEO BYTEZONE v14
# - Noticias frescas (sin repetir las de la semana anterior)
# - Chistes y "verdades tech" rotativos
# - Telemetría real (partidas, anuncios, dispositivos únicos) acumulada en el tiempo
# - Decisiones: rotar juegos titulares <-> Baúl según popularidad real
# - SEO: meta-tags con palabras clave de la semana, sitemap, ping IndexNow
# - Kit de promoción (textos listos para WhatsApp/Telegram/redes) + envío opcional a Telegram
# ==========================================================

# Hora de Venezuela (UTC-4)
VET_TZ = timezone(timedelta(hours=-4))
now_vet = datetime.now(VET_TZ)

def get_week_id(dt):
    monday = dt - timedelta(days=dt.weekday())
    return f"W{monday.strftime('%Y-%m-%d')}"

WEEK_ID = get_week_id(now_vet)
PREV_WEEK_ID = get_week_id(now_vet - timedelta(days=7))
FECHA_HUMANA = now_vet.strftime("%d/%m/%Y")
WEEK_NUM = int(now_vet.strftime("%U"))
CACHE_VERSION = 14

SITE_BASE = "https://megabotp2p.github.io/bytezone/"
INDEXNOW_KEY = "3f9a7c1e5b2d48a6b0c4e7d9a1f25683"
TELEMETRY_TOPIC = "bytezone_global_telemetry_v12"
GAMES = ["stacker", "reflex", "memory", "dodge"]
GAME_NAMES = {
    "stacker": "Neon Stacker Pro",
    "reflex": "Test de Reflejos",
    "memory": "Cyber Memory",
    "dodge": "Cyber Dodge",
}
GAME_UNITS = {"stacker": "pisos", "reflex": "ms", "memory": "rondas", "dodge": "seg"}
GAME_URLS = {
    "stacker": "juegos/neon-stacker.html",
    "reflex": "juegos/reflejos-visuales.html",
    "memory": "juegos/cyber-memory.html",
    "dodge": "juegos/cyber-dodge.html",
}
CLOUD_ALLTIME_IDS = {
    "stacker": "ff808181a09d98f701a1448611567237",
    "reflex": "ff808181a09d98f701a1448613fe7238",
    "memory": "ff808181a09d98f701a14486174a7239",
}
CLOUD_WEEKLY_IDS = {
    "stacker": "ff808181a09d98f701a14a82e347035f",
    "reflex": "ff808181a09d98f701a14a82e55d0360",
    "memory": "ff808181a09d98f701a14a82e7130361",
}

DATA_DIR = os.path.join("bytezone", "data")
PULSE_PATH = os.path.join(DATA_DIR, "weekly_pulse.json")
STATE_PATH = os.path.join(DATA_DIR, "agent_state.json")
TELEMETRY_LOG_PATH = os.path.join(DATA_DIR, "telemetry_log.json")
OUTPUT_ROOTS = ["portal_bytezone", "bytezone"]

RSS_SOURCES = [
    ("Hipertextual IA", "https://hipertextual.com/inteligencia-artificial/feed"),
    ("Xataka IA & Tech", "https://www.xataka.com/tag/inteligencia-artificial/rss2.xml"),
    ("Genbeta IA", "https://www.genbeta.com/tag/inteligencia-artificial/rss2.xml"),
    ("Xataka", "https://www.xataka.com/feedburner.xml"),
    ("Genbeta", "https://www.genbeta.com/feedburner.xml"),
    ("Hipertextual", "https://hipertextual.com/feed"),
    ("Google News IA & Gadgets", "https://news.google.com/rss/search?q=inteligencia+artificial+OR+invento+OR+robot+OR+smartphone&hl=es-419&gl=US&ceid=US:es-419"),
    ("Google News Gaming & Apps", "https://news.google.com/rss/search?q=videojuegos+OR+WhatsApp+OR+Telegram+OR+ciberseguridad&hl=es-419&gl=US&ceid=US:es-419"),
]

# Imágenes tecnológicas de alta definición de respaldo por temática
THEME_IMAGES = [
    "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=900&q=80",
]

# ----------------------------------------------------------
# Utilidades de archivos
# ----------------------------------------------------------
def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def http_get(url, timeout=10, headers=None):
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ByteZoneCEOAgent/3.0"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

# ----------------------------------------------------------
# Texto / noticias
# ----------------------------------------------------------
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
    try:
        page_html = http_get(url, timeout=6).decode('utf-8', errors='ignore')
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
    spoken_summary = make_complete_sentences(" ".join(body_paragraphs[:2]), max_sentences=2, max_chars=310)
    return spoken_summary, body_paragraphs

def title_key(title):
    return re.sub(r'[^a-z0-9áéíóúñ ]', '', (title or '').lower())[:40].strip()

def collect_candidates():
    """Etapa 1: junta noticias candidatas de todas las fuentes (con fecha de publicación)."""
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/', 'media': 'http://search.yahoo.com/mrss/'}
    per_source = []
    for source_name, url in RSS_SOURCES:
        cands = []
        try:
            root = ET.fromstring(http_get(url, timeout=8))
            for item in root.findall('.//item'):
                title = clean_html_text(item.findtext('title') or '')
                link = (item.findtext('link') or '').strip()
                raw_desc = item.findtext('description') or ''
                raw_content = item.findtext('content:encoded', namespaces=ns) or ''
                if not title or len(title) < 20:
                    continue
                source_label = source_name
                if " - " in title:
                    parts = title.rsplit(" - ", 1)
                    if len(parts[1]) < 30:
                        source_label = parts[1].strip()
                        title = parts[0].strip()
                pub = None
                try:
                    pub = parsedate_to_datetime(item.findtext('pubDate') or '')
                    if pub.tzinfo is None:
                        pub = pub.replace(tzinfo=timezone.utc)
                except Exception:
                    pub = None
                media_el = item.find('media:content', namespaces=ns)
                if media_el is None:
                    media_el = item.find('enclosure')
                img_url = extract_first_image(raw_content) or extract_first_image(raw_desc)
                if not img_url and media_el is not None and media_el.attrib.get('url'):
                    img_url = media_el.attrib.get('url')
                cands.append({
                    "title": title, "link": link, "raw_desc": raw_desc, "raw_content": raw_content,
                    "source": source_label, "pub": pub, "img": img_url,
                })
        except Exception as e:
            print(f"[Aviso RSS] {source_name}: {e}")
        cands.sort(key=lambda c: c["pub"] or datetime(1970, 1, 1, tzinfo=timezone.utc), reverse=True)
        per_source.append(cands)
    return per_source

def fetch_latest_tech_news(exclude_keys):
    """Elige 5 noticias NUEVAS (que no estuvieron la semana pasada), alternando fuentes."""
    per_source = collect_candidates()
    chosen, seen = [], set()

    def take(from_stale):
        progressed = True
        while len(chosen) < 5 and progressed:
            progressed = False
            for cands in per_source:
                for c in cands:
                    k = title_key(c["title"])
                    if k in seen:
                        continue
                    stale = k in exclude_keys
                    if stale != from_stale:
                        continue
                    seen.add(k)
                    chosen.append(c)
                    progressed = True
                    break
                if len(chosen) >= 5:
                    return

    take(from_stale=False)
    if len(chosen) < 5:
        print(f"[Aviso] Solo {len(chosen)} noticias nuevas; se completan con anteriores.")
        take(from_stale=True)

    items = []
    for c in chosen[:5]:
        idx_img = THEME_IMAGES[len(items) % len(THEME_IMAGES)]
        img_url = c["img"]
        paras = extract_paragraphs_from_html(c["raw_content"]) or extract_paragraphs_from_html(c["raw_desc"])
        if (not img_url or len(paras) < 2) and c["link"] and "news.google.com" not in c["link"]:
            fetched_img, fetched_paras = fetch_article_details(c["link"], idx_img)
            if not img_url:
                img_url = fetched_img
            if len(fetched_paras) > len(paras):
                paras = fetched_paras
        if not img_url:
            img_url = idx_img
        short_desc = clean_html_text(c["raw_desc"])
        spoken_summary, full_paragraphs = build_rich_article(c["title"], c["source"], paras, short_desc)
        full_voice_script = f"{c['title']}. Noticia publicada por {c['source']}. " + " ".join(full_paragraphs)
        items.append({
            "id": f"news_{len(items) + 1}",
            "title": c["title"],
            "summary": spoken_summary,
            "voice_extra": spoken_summary,
            "full_paragraphs": full_paragraphs,
            "full_voice_script": full_voice_script,
            "image": img_url,
            "source": c["source"],
            "link": c["link"],
            "published": c["pub"].isoformat() if c["pub"] else None,
        })
    return items

def build_video_reel_scenes(news_list):
    icons = ["🤖", "🚀", "⚡", "🧠", "🔥"]
    badges = [
        "NOTICIA #1 • IA & FUTURO", "NOTICIA #2 • INNOVACIÓN", "NOTICIA #3 • TENDENCIA GLOBAL",
        "NOTICIA #4 • IMPACTO TECH", "NOTICIA #5 • CIERRE SEMANAL",
    ]
    colors = [
        "from-cyan-600 to-blue-900", "from-purple-600 to-indigo-900", "from-pink-600 to-rose-900",
        "from-emerald-600 to-teal-900", "from-amber-500 to-orange-900",
    ]
    scenes = []
    last = len(news_list[:5])
    for idx, item in enumerate(news_list[:5]):
        num = idx + 1
        closing_phrase = (
            " Pasamos a la siguiente noticia." if num < last
            else " Y con esto cerramos el resumen semanal de ByteZone. Recuerda tocar cualquier noticia para leerla completa o desbloquear el truco VIP abajo."
        )
        voice = f"Noticia número {num}: {item['title']}. {item['summary']}{closing_phrase}"
        scenes.append({
            "id": item["id"], "news_index": idx, "badge": badges[idx], "icon": icons[idx],
            "headline": item["title"], "subtext": item["summary"], "image": item["image"],
            "source": item["source"], "voice_script": voice, "bg_gradient": colors[idx],
            "is_vip_hook": (num == last),
        })
    return scenes

# ----------------------------------------------------------
# Humor rotativo (chistes + "verdades tech")
# ----------------------------------------------------------
JOKE_POOL = [
    "— Tengo una idea genial para una app.<br>— ¿Cuál?<br>— Una que avise cuando el vecino cambie la clave del Wi-Fi.",
    "El Wi-Fi de mi casa tiene tres rayitas de señal y aun así la página tarda una eternidad. Mucha actitud y poca conexión.",
    "Cuando el celular dice 'almacenamiento casi lleno' yo borro dos fotos repetidas y una app que nunca abrí. Dolor mínimo, espacio máximo.",
    "— ¿Cuál es tu mayor miedo?<br>— Que alguien me pida el celular 'solo para ver una foto'.",
    "Mi cargador original lo perdí hace años. El que uso carga 1% por hora, pero le tengo cariño: me enseñó paciencia.",
    "Programador: 'En mi computadora funciona'.<br>Cliente: 'Pero en la mía no'.<br>Programador: 'Entonces te mando mi computadora'.",
    "Descargué una app para meditar. Me desconecté tan bien que olvidé abrirla.",
    "Mi PC tarda 10 minutos en encender y 2 segundos en congelarse justo cuando voy a guardar el trabajo. Puntería perfecta.",
    "— Hijo, ¿por qué llevas tanto tiempo en el teléfono?<br>— Estudiando, mamá.<br>— ¿Y por qué es un video de gatos?<br>— Biología felina avanzada.",
    "Mi mamá y la tecnología: 'Hijo, se me quitó el internet de la pantalla'. Traducción: se le cerró la aplicación.",
    "En mi casa hay dos tipos de personas: los que dicen 'reinicia el router' y los que ya lo reiniciaron tres veces.",
    "La batería al 1% es como mi motivación un lunes: ahí está, pero no promete nada.",
    "Le pedí consejo financiero a un chatbot y me dijo: 'Diversifica'. Ahora tengo diez apps de delivery y ninguna comida.",
    "Si el Wi-Fi fuera una persona, sería ese amigo que promete ir a la fiesta y aparece cuando ya te fuiste.",
    "Mi teléfono se cayó de la mesa y sobrevivió. Yo casi sufro un infarto. Resistencia emocional: 0, de pantalla: 100.",
    "Actualización disponible: 2 GB. Mi almacenamiento: 40 MB. Mi paciencia: agotada.",
    "Dicen que el dinero no da la felicidad, pero tener 100% de batería a las 11 de la noche se le parece muchísimo.",
    "— ¿Ya reinició el equipo?<br>— Sí.<br>— ¿Seguro?<br>— ...ahora sí.",
    "Mi estado de WhatsApp dura 24 horas. Mi arrepentimiento por subirlo, dos minutos.",
    "Instalé un antivirus tan potente que ahora mi computadora no deja pasar ni mis propios archivos.",
    "Los términos y condiciones son el único libro que todos hemos 'leído' y nadie ha abierto.",
    "El corrector automático tiene vida propia: escribo 'llego en cinco' y envía 'llevo un cinco en matemática'.",
    "Mi router tiene más lucecitas que un árbol de Navidad y aun así no hay internet.",
    "— Papá, ¿qué es la nube?<br>— Es donde el celular guarda lo que yo no quiero que mamá vea.",
    "Mi cuenta de ahorros y mi batería tienen algo en común: las dos llegan al 5% a mitad de mes.",
    "Un 'ya casi llego' por WhatsApp es el equivalente moderno a 'el cheque está en el correo'.",
    "Si grabas un video vertical te dirán 'ponlo horizontal'; si lo grabas horizontal, 'ponlo vertical'. La tecnología es una dictadura.",
    "Mi laptop tiene 47 pestañas abiertas y yo solo recuerdo por qué abrí dos.",
    "El que inventó 'Posponer alarma' sabía perfectamente lo que hacía. Le doy las gracias y las quejas.",
    "Mi hijo me explicó qué es un meme. Llevo tres semanas explicándoselo a mi familia y nadie se ríe.",
    "— Mesero, ¿cuál es la clave del Wi-Fi?<br>— Pida el combo y se la doy.<br>— ¿Y si pido solo el café?<br>— Le damos la clave... del negocio de enfrente.",
    "Antes uno buscaba pareja; ahora busca un enchufe. Y a veces el segundo aparece primero.",
    "Le pedí a una IA que dibujara un gato. Me dio un gato con siete patas y cara de ofendido. Igualito a mi jefe un lunes.",
    "Mi compu hace un ruido como de avión despegando. Dice el técnico que es normal: 'está pensando muy fuerte'.",
    "Nada te enseña a escribir más rápido que ver el 'Escribiendo...' de la persona con la que discutes por WhatsApp.",
    "La tía del grupo familiar: 'Cuidado con el 5G'. La misma tía a las 5 a.m.: reenvía 45 bendiciones con fotos de flores.",
    "Dormir 8 horas es fácil. Lo difícil es que el celular no te avise a las 3 a.m. que 'tu almacenamiento está casi lleno'.",
    "Yo: 'Voy a usar el teléfono 5 minutos'. El teléfono, 2 horas después: 'Hola de nuevo'.",
    "Mi contraseña tiene mayúsculas, números y símbolos... y aun así soy el único que no se la sabe.",
    "El GPS dijo 'a 200 metros gire a la derecha'. Doblé a la derecha. Ahora vivo en un campo de maíz.",
    "Mi modo 'No molestar' lleva activado desde 2021. A veces alguien se acuerda de mí por correo.",
    "Mi pantalla tiene tantas rayitas que ya no sé si es un teléfono o un mapa de carreteras.",
    "— ¿Dónde están mis lentes?<br>— En tu cara.<br>— Ah, es que los busqué con la linterna del celular.",
    "Mi cámara frontal es muy honesta; por eso le dejé de hablar.",
]

TRUTH_POOL = [
    {"emoji": "🎙️", "color": "cyan", "title": "La Ley del Audio de WhatsApp",
     "body": "• <strong>0 a 15 seg:</strong> Escuchable con paciencia.<br>• <strong>15 a 45 seg:</strong> Lo pongo en 1.5x de inmediato.<br>• <strong>Más de 1 min:</strong> Eso ya no es un audio, es un podcast. ¡Llámame mejor!"},
    {"emoji": "🤖", "color": "purple", "title": "La IA: Expectativa vs Realidad",
     "body": "<strong>La gente:</strong> <em>\"La IA va a dominar el mundo con robots asesinos...\"</em><br><strong>La IA en la vida real:</strong> Dibuja personas con 7 dedos en una mano y confunde un chihuahua con un muffin."},
    {"emoji": "🔋", "color": "pink", "title": "El Milagro del 1%",
     "body": "Mi teléfono con <strong>99%</strong>: se descarga en un parpadeo si abro Instagram.<br>Mi teléfono con <strong>1%</strong>: aguanta 3 horas, 2 llamadas de emergencia y una alarma."},
    {"emoji": "🛒", "color": "emerald", "title": "Compras por Internet",
     "body": "<strong>En la foto:</strong> Camiseta ajustada estilo cyberpunk.<br><strong>Lo que llega:</strong> Un mantel de cocina transparente con dos huecos para los brazos."},
    {"emoji": "📶", "color": "blue", "title": "El Wi-Fi del Vecino",
     "body": "<strong>Señal:</strong> 5 rayitas.<br><strong>Velocidad:</strong> la de una tortuga con sueño.<br><strong>Clave:</strong> recién cambiada."},
    {"emoji": "📸", "color": "amber", "title": "La Galería del Celular",
     "body": "10.000 fotos: 9.800 son capturas de pantalla, 150 son la misma selfie y ninguna es la que estás buscando."},
    {"emoji": "🔔", "color": "pink", "title": "Notificaciones",
     "body": "<strong>Importante:</strong> 1 mensaje de tu jefe.<br><strong>Urgentísimo:</strong> 47 avisos de apps que no recuerdas haber instalado."},
    {"emoji": "💻", "color": "cyan", "title": "La Regla de las Pestañas",
     "body": "Una pestaña para trabajar. Cuarenta y seis para 'leer luego'. Cero lecturas posteriores."},
    {"emoji": "🧑‍💻", "color": "purple", "title": "Soporte Técnico",
     "body": "—¿Ya lo apagó y lo volvió a encender?<br>—Sí.<br>—¿Seguro?<br>—...<strong>Ahora sí</strong>. Y funciona. Nadie sabe por qué."},
    {"emoji": "🎮", "color": "emerald", "title": "Psicología Gamer",
     "body": "<strong>Pierdo:</strong> es culpa del lag.<br><strong>Gano:</strong> pura habilidad y talento natural."},
    {"emoji": "🔌", "color": "amber", "title": "El Cargador Sagrado",
     "body": "Todos tenemos <strong>un</strong> cargador que sí funciona. Se presta con ceremonia y se devuelve bajo juramento."},
    {"emoji": "📱", "color": "blue", "title": "La Pantalla Rota",
     "body": "Nivel 1: una rajadura pequeña.<br>Nivel 2: 'ya me acostumbré'.<br>Nivel 3: lees el mensaje en forma de rompecabezas."},
]

def pick_rotating(pool_len, count, week_id, avoid):
    """Elige 'count' índices de forma determinista por semana evitando los de la semana anterior."""
    rng = random.Random(week_id)
    idx = list(range(pool_len))
    rng.shuffle(idx)
    fresh = [i for i in idx if i not in set(avoid or [])]
    stale = [i for i in idx if i in set(avoid or [])]
    return (fresh + stale)[:count]

# ----------------------------------------------------------
# Telemetría real (acumulada en el tiempo)
# ----------------------------------------------------------
def snapshot_telemetry():
    """Lee los eventos recientes de ntfy.sh (solo guarda ~12 h) y los acumula en un log permanente."""
    log = load_json(TELEMETRY_LOG_PATH, {"days": {}, "seen": []})
    log.setdefault("days", {})
    log.setdefault("seen", [])
    seen = set(log["seen"])
    added = 0
    try:
        raw = http_get(f"https://ntfy.sh/{TELEMETRY_TOPIC}/json?poll=1&since=12h", timeout=15).decode("utf-8", errors="ignore")
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
                if evt.get("event") != "message" or not evt.get("message"):
                    continue
                p = json.loads(evt["message"])
            except Exception:
                continue
            eid = str(p.get("eid") or evt.get("id") or "")
            if not eid or eid in seen or eid.startswith("seed_"):
                continue
            seen.add(eid)
            ts = p.get("ts") or (evt.get("time", 0) * 1000)
            try:
                day = datetime.fromtimestamp(ts / 1000, VET_TZ).strftime("%Y-%m-%d")
            except Exception:
                day = now_vet.strftime("%Y-%m-%d")
            d = log["days"].setdefault(day, {"games": {}, "devices": [], "countries": {}, "ads": {"shown": 0, "fallback": 0}})
            dev = hashlib.sha1(str(p.get("d", "")).encode()).hexdigest()[:8]
            if dev not in d["devices"]:
                d["devices"].append(dev)
            cc = str(p.get("c") or "VE")[:2].upper()
            kind = p.get("kind")
            if kind == "game" and p.get("g") in GAMES and p.get("ev") in ("view", "play", "ad"):
                g = d["games"].setdefault(p["g"], {"view": 0, "play": 0, "ad": 0})
                g[p["ev"]] += 1
                d["countries"][cc] = d["countries"].get(cc, 0) + 1
                added += 1
            elif kind == "ad":
                d["ads"]["shown" if p.get("shown") else "fallback"] += 1
                added += 1
    except Exception as e:
        print(f"[Aviso telemetría] {e}")
    # Poda: 90 días y últimos 5000 ids
    cutoff = (now_vet - timedelta(days=90)).strftime("%Y-%m-%d")
    log["days"] = {k: v for k, v in log["days"].items() if k >= cutoff}
    log["seen"] = list(seen)[-5000:]
    log["updated_at"] = now_vet.isoformat()
    save_json(TELEMETRY_LOG_PATH, log)
    print(f"[Telemetría] {added} eventos nuevos acumulados.")
    return log

def sum_days(log, d_from, d_to):
    tot = {"games": {g: {"view": 0, "play": 0, "ad": 0} for g in GAMES}, "devices": set(),
           "ads_shown": 0, "ads_fallback": 0, "countries": Counter()}
    for ds, day in log.get("days", {}).items():
        if d_from <= ds <= d_to:
            for g, vals in day.get("games", {}).items():
                for k in ("view", "play", "ad"):
                    tot["games"][g][k] += vals.get(k, 0)
            tot["devices"].update(day.get("devices", []))
            tot["ads_shown"] += day.get("ads", {}).get("shown", 0)
            tot["ads_fallback"] += day.get("ads", {}).get("fallback", 0)
            for cc, n in day.get("countries", {}).items():
                tot["countries"][cc] += n
    return tot

def compute_stats(log):
    today = now_vet.date()
    last7 = sum_days(log, (today - timedelta(days=7)).isoformat(), (today - timedelta(days=1)).isoformat())
    prev7 = sum_days(log, (today - timedelta(days=14)).isoformat(), (today - timedelta(days=8)).isoformat())
    def flat(t):
        return {
            "plays": sum(t["games"][g]["play"] for g in GAMES),
            "views": sum(t["games"][g]["view"] for g in GAMES),
            "ad_actions": sum(t["games"][g]["ad"] for g in GAMES),
            "devices": len(t["devices"]),
            "ads_shown": t["ads_shown"],
            "per_game": {g: dict(t["games"][g]) for g in GAMES},
            "top_countries": t["countries"].most_common(3),
        }
    return {"last7": flat(last7), "prev7": flat(prev7)}

# ----------------------------------------------------------
# Decisiones del CEO (rotación de juegos, estado de tráfico)
# ----------------------------------------------------------
def default_state():
    return {
        "portada": ["stacker", "reflex", "memory"],
        "vault": ["dodge"],
        "entered": {g: WEEK_ID for g in GAMES},
        "history": [],
        "last_news_keys": [],
        "last_joke_ids": [],
        "last_truth_ids": [],
    }

def weeks_between(w_from, w_to):
    try:
        a = datetime.strptime(w_from[1:], "%Y-%m-%d")
        b = datetime.strptime(w_to[1:], "%Y-%m-%d")
        return (b - a).days // 7
    except Exception:
        return 99

def decide(stats, state):
    s = stats["last7"]
    p = stats["prev7"]
    decisions = []
    portada = list(state.get("portada", default_state()["portada"]))
    vault = list(state.get("vault", default_state()["vault"]))
    entered = dict(state.get("entered", {}))
    plays = {g: s["per_game"][g]["play"] for g in GAMES}
    total_portada_plays = sum(plays[g] for g in portada)

    # Tendencia de tráfico
    if s["devices"] < 25:
        traffic = "bajo"
    elif p["devices"] > 0 and (s["devices"] - p["devices"]) / p["devices"] >= 0.15:
        traffic = "creciendo"
    else:
        traffic = "estable"
    change_pct = None
    if p["devices"] > 0:
        change_pct = round((s["devices"] - p["devices"]) * 100 / p["devices"])

    # Rotación: el titular menos jugado cede su lugar a un juego del Baúl
    rotated = None
    if total_portada_plays >= 30 and vault:
        least = min(portada, key=lambda g: plays[g])
        share = plays[least] / total_portada_plays
        if share < 0.15 and weeks_between(entered.get(least, WEEK_ID), WEEK_ID) >= 2:
            incoming = vault[0]
            portada[portada.index(least)] = incoming
            vault = [least] + [v for v in vault if v != incoming]
            entered[incoming] = WEEK_ID
            rotated = {"out": least, "in": incoming, "share_pct": round(share * 100)}
            decisions.append(f"ROTACIÓN: '{GAME_NAMES[least]}' ({round(share*100)}% de las partidas) pasa al Baúl y '{GAME_NAMES[incoming]}' sube a la portada.")
        else:
            decisions.append(f"Sin rotación: el menos jugado ('{GAME_NAMES[least]}') tiene {round(share*100)}% de las partidas (umbral 15%) o aún está en su periodo mínimo de 2 semanas.")
    else:
        decisions.append(f"Sin rotación: solo {total_portada_plays} partidas registradas en 7 días (se necesitan 30 para decidir con datos).")

    # Orden de portada por popularidad (si hay datos) y etiquetas
    if total_portada_plays >= 10:
        portada.sort(key=lambda g: plays[g], reverse=True)
    badges = {}
    if total_portada_plays >= 10:
        badges[portada[0]] = "MÁS JUGADO DE LA SEMANA 🔥"
    for g in portada:
        if entered.get(g) == WEEK_ID and rotated and g == rotated["in"]:
            badges[g] = "NUEVO EN PORTADA ✨"

    return {
        "portada": portada, "vault": vault, "entered": entered, "badges": badges,
        "traffic": traffic, "change_pct": change_pct, "rotated": rotated, "decisions": decisions,
    }

# ----------------------------------------------------------
# Rankings (para el kit de promoción)
# ----------------------------------------------------------
def parse_compact(v):
    out = []
    for part in (v or "").split(";"):
        bits = part.split("|")
        if len(bits) >= 2 and bits[1].strip().isdigit():
            out.append({"name": bits[0], "score": int(bits[1]), "country": (bits[2] if len(bits) > 2 else "VE")})
    return out

def fetch_leaderboards():
    champions, records = {}, {}
    for g in ("stacker", "reflex", "memory"):
        asc = (g == "reflex")
        try:
            data = json.loads(http_get(f"https://api.restful-api.dev/objects/{CLOUD_WEEKLY_IDS[g]}", timeout=10)).get("data", {})
            if data.get("w") == PREV_WEEK_ID:
                lst = sorted(parse_compact(data.get("v")), key=lambda x: x["score"], reverse=not asc)
                if lst:
                    champions[g] = lst[0]
        except Exception as e:
            print(f"[Aviso ranking semanal {g}] {e}")
        try:
            data = json.loads(http_get(f"https://api.restful-api.dev/objects/{CLOUD_ALLTIME_IDS[g]}", timeout=10)).get("data", {})
            lst = sorted(parse_compact(data.get("v")), key=lambda x: x["score"], reverse=not asc)
            if lst:
                records[g] = lst[0]
        except Exception as e:
            print(f"[Aviso ranking histórico {g}] {e}")
    return champions, records

# ----------------------------------------------------------
# SEO
# ----------------------------------------------------------
STOPWORDS = set("""este esta estos estas como para pero porque cuando donde desde hasta sobre entre tras ante bajo
según después antes también más menos muy solo todo toda todos todas nuevo nueva nuevos nuevas puede pueden
tiene tienen hace hacen será serán fue fueron está están ha han ser son por con sin los las del una uno unos unas
que qué cómo cuál cuáles año años semana lanza llega primer primera mejor mejores esto estos""".split())

BASE_KEYWORDS = [
    "juegos arcade online gratis", "juegos sin descargar", "test de reflejos", "test de velocidad de reacción",
    "juego de memoria", "torneo semanal", "ranking mundial de juegos", "noticias de inteligencia artificial",
    "resumen semanal de IA", "mini juegos para Telegram", "juegos para celular", "retos entre amigos",
]

def build_seo(news):
    words = Counter()
    for n in news:
        for w in re.findall(r"\b[A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ\-]{3,}\b", n["title"]):
            if w.lower() not in STOPWORDS:
                words[w] += 2
        for w in re.findall(r"\b[a-záéíóúñ]{6,}\b", n["title"].lower()):
            if w not in STOPWORDS:
                words[w] += 1
    trending = [w for w, _ in words.most_common(8)]
    headline = news[0]["title"] if news else "Noticias de IA y tecnología"
    headline_short = headline if len(headline) <= 70 else headline[:67].rsplit(" ", 1)[0] + "…"
    return {
        "title": "ByteZone Arcade | Juegos Gratis, Ranking Semanal y Noticias de IA",
        "description": f"Juega gratis Neon Stacker, Test de Reflejos y Cyber Memory, compite en el torneo semanal y entérate de lo último en IA: {headline_short}",
        "keywords": BASE_KEYWORDS + [t.lower() for t in trending],
        "trending_terms": trending,
        "og_image": (news[0]["image"] if news else THEME_IMAGES[0]),
        "lastmod": now_vet.strftime("%Y-%m-%d"),
    }

def write_sitemap():
    pages = ["", "hacks.html", "humor.html", "telegram.html", "stats.html"] + list(GAME_URLS.values())
    today = now_vet.strftime("%Y-%m-%d")
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for pg in pages:
        pr = "1.0" if pg == "" else ("0.9" if pg in ("hacks.html", "humor.html") else "0.8")
        parts.append(f"  <url><loc>{SITE_BASE}{pg}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>")
    parts.append("</urlset>")
    for root in OUTPUT_ROOTS:
        os.makedirs(root, exist_ok=True)
        with open(os.path.join(root, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write("\n".join(parts) + "\n")
    # Archivo-llave de IndexNow en la raíz del repositorio
    try:
        with open(f"{INDEXNOW_KEY}.txt", "w", encoding="utf-8") as f:
            f.write(INDEXNOW_KEY)
    except Exception:
        pass
    return [SITE_BASE + p for p in pages]

def ping_indexnow(urls):
    try:
        body = json.dumps({
            "host": "megabotp2p.github.io", "key": INDEXNOW_KEY,
            "keyLocation": f"https://megabotp2p.github.io/{INDEXNOW_KEY}.txt", "urlList": urls,
        }).encode("utf-8")
        req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                     headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as r:
            return f"IndexNow aceptó la notificación (HTTP {r.status})"
    except urllib.error.HTTPError as e:
        return f"IndexNow respondió HTTP {e.code} (normal en la primera ejecución si la llave aún no está publicada)"
    except Exception as e:
        return f"IndexNow no disponible: {e}"

# ----------------------------------------------------------
# Kit de promoción
# ----------------------------------------------------------
def build_promo_kit(news, champions, records, decision, seo):
    url = SITE_BASE
    lines = []
    if "reflex" in records:
        r = records["reflex"]
        lines.append(f"⚡ El récord de reflejos es {r['score']} ms ({r['name']}). ¿Puedes vencerlo?")
    if "stacker" in records:
        r = records["stacker"]
        lines.append(f"🏗️ Récord de Neon Stacker: {r['score']} pisos ({r['name']}). ¿Llegas más alto?")
    champ_txt = ""
    if champions:
        bits = []
        for g, c in champions.items():
            bits.append(f"{GAME_NAMES[g]}: {c['name']} ({c['score']} {GAME_UNITS[g]})")
        champ_txt = "🏆 Campeones de la semana pasada → " + " | ".join(bits)
    tags = ["#juegosgratis", "#arcade", "#reflejos", "#retos", "#IA", "#tecnologia", "#telegram"] + \
           [("#" + re.sub(r"[^A-Za-z0-9áéíóúñÁÉÍÓÚÑ]", "", t)) for t in seo["trending_terms"][:3]]
    headline = news[0]["title"] if news else ""
    wa = [
        "🎮 Torneo semanal nuevo en ByteZone: ranking reiniciado, ¡todos empiezan de cero! " + (lines[0] if lines else "") + f" Juega gratis 👉 {url}",
        (champ_txt + f"\n\nEsta semana puedes ser #1. Gratis y sin descargar 👉 {url}") if champ_txt else f"🔥 ¿Cuánto duras en Neon Stacker? Reta a tus amigos en el ranking semanal 👉 {url}",
        f"🤖 Noticia IA de la semana: {headline}\nResumen en 45 segundos + juegos gratis 👉 {url}" if headline else f"🤖 Resumen semanal de IA en video + mini juegos 👉 {url}",
    ]
    social = f"Nueva semana, ranking en cero 🏁 Juega {GAME_NAMES['stacker']}, {GAME_NAMES['reflex']} y {GAME_NAMES['memory']} gratis y compite con el mundo. {url} " + " ".join(tags)
    return {
        "whatsapp_status": wa,
        "social_caption": social,
        "hashtags": tags,
        "challenge_lines": lines,
        "last_week_champions_text": champ_txt,
    }

def send_telegram_promo(text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat:
        return "Telegram: sin token/chat configurados (envío automático desactivado)."
    try:
        body = json.dumps({"chat_id": chat, "text": text}).encode("utf-8")
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=body,
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as r:
            return f"Telegram: mensaje semanal publicado (HTTP {r.status})."
    except Exception as e:
        return f"Telegram: falló el envío ({e})."

# ----------------------------------------------------------
# Hacks VIP rotativos
# ----------------------------------------------------------
WEEKLY_VIP_HACKS = [
    {"tag": "Secreto de IA & Celular", "title": "Cómo activar el Modo Ultra-Velocidad de Red DNS Privado sin instalar apps",
     "body": "Entra en Ajustes > Conexiones > Más ajustes de conexión > DNS Privado y escribe 'dns.adguard.com' o 'one.one.one.one'. Tu teléfono resolverá páginas y juegos hasta un 35% más rápido y bloqueará rastreadores pesados automáticamente."},
    {"tag": "Truco Oculto WhatsApp", "title": "Enviar fotos y videos en calidad 4K original sin que WhatsApp los pixele",
     "body": "Antes de enviar cualquier foto o video, toca el botón 'HD' arriba en el editor, o adjúntalo como 'Documento' si quieres cero compresión. ¡La diferencia de nitidez es abismal!"},
    {"tag": "Optimización Gamer", "title": "Liberar memoria RAM oculta en 5 segundos antes de jugar",
     "body": "En Chrome o Telegram, cierra las pestañas en segundo plano y activa el modo 'No Molestar' durante tu partida: evita micro-tirones de pantalla cuando buscas récords de menos de 100 milisegundos."},
    {"tag": "Batería Inmortal", "title": "5 ajustes que alargan la batería de tu celular hasta 2 horas",
     "body": "1) Activa el modo oscuro en pantallas OLED. 2) Baja la tasa de refresco a 60 Hz. 3) Desactiva la ubicación 'siempre activa' en apps que no la necesitan. 4) Limita las apps en segundo plano. 5) Mantén la carga entre 20% y 80% para cuidar la batería a largo plazo."},
    {"tag": "Seguridad Digital", "title": "El truco de 30 segundos para que no te roben la cuenta de WhatsApp o Telegram",
     "body": "Activa la verificación en dos pasos (WhatsApp: Ajustes > Cuenta > Verificación en dos pasos; Telegram: Ajustes > Privacidad > Contraseña de dos pasos). Nunca compartas el código de 6 dígitos con nadie, ni con 'soporte'."},
    {"tag": "Productividad IA", "title": "Cómo pedirle a una IA que te resuma cualquier PDF o artículo en segundos",
     "body": "Pega el texto y escribe: 'Resúmelo en 5 puntos clave, dime la conclusión y qué debería hacer yo con esta información'. Ese prompt ordena la respuesta y te ahorra media hora de lectura."},
]

# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------
def main():
    print(f"🤖 [Agente CEO ByteZone v{CACHE_VERSION}] Semana {WEEK_ID} ({FECHA_HUMANA})")
    prev_pulse = load_json(PULSE_PATH, {})
    state = load_json(STATE_PATH, default_state())
    base = default_state()
    for k, v in base.items():
        state.setdefault(k, v)

    # 1) Noticias frescas
    exclude = set(state.get("last_news_keys", [])) | {title_key(n.get("title")) for n in prev_pulse.get("weekly_news", [])}
    news = fetch_latest_tech_news(exclude)
    scenes = build_video_reel_scenes(news)
    vip_hack = WEEKLY_VIP_HACKS[WEEK_NUM % len(WEEKLY_VIP_HACKS)]

    # 2) Telemetría y decisiones
    log = snapshot_telemetry()
    stats = compute_stats(log)
    decision = decide(stats, state)

    # 3) Humor rotativo
    joke_ids = pick_rotating(len(JOKE_POOL), 10, WEEK_ID, state.get("last_joke_ids"))
    truth_ids = pick_rotating(len(TRUTH_POOL), 4, WEEK_ID, state.get("last_truth_ids"))
    weekly_jokes = [JOKE_POOL[i] for i in joke_ids]
    weekly_truths = [TRUTH_POOL[i] for i in truth_ids]

    # 4) Rankings, SEO y promoción
    champions, records = fetch_leaderboards()
    seo = build_seo(news)
    promo = build_promo_kit(news, champions, records, decision, seo)
    urls = write_sitemap()
    indexnow_msg = ping_indexnow(urls)
    telegram_msg = send_telegram_promo(promo["whatsapp_status"][0])

    # 5) Reporte del CEO
    s7, p7 = stats["last7"], stats["prev7"]
    actions = [
        f"Noticias renovadas: {len(news)} historias nuevas (se evitaron los titulares de la semana anterior).",
        f"Humor renovado: {len(weekly_jokes)} chistes y {len(weekly_truths)} 'verdades tech' nuevas.",
        f"SEO: meta-tags actualizados con palabras clave de la semana ({', '.join(seo['trending_terms'][:5])}), sitemap regenerado. {indexnow_msg}",
        "Kit de promoción listo (textos para WhatsApp/Telegram/redes con los récords actuales).",
        telegram_msg,
    ] + decision["decisions"]
    if decision["traffic"] == "bajo":
        actions.append("ALERTA: tráfico bajo (menos de 25 dispositivos únicos en 7 días). Recomendación: difundir el kit de promoción en grupos y estados esta semana.")
    report = {
        "generated_at": now_vet.isoformat(),
        "week_id": WEEK_ID,
        "traffic_status": decision["traffic"],
        "traffic": {
            "devices_7d": s7["devices"], "plays_7d": s7["plays"], "views_7d": s7["views"],
            "ad_actions_7d": s7["ad_actions"], "ads_shown_7d": s7["ads_shown"],
            "devices_prev_7d": p7["devices"], "change_pct": decision["change_pct"],
            "per_game": s7["per_game"], "top_countries": s7["top_countries"],
        },
        "actions": actions,
        "rotation": decision["rotated"],
        "note": "Las métricas se acumulan desde el primer día de la telemetría global; los primeros reportes tienen pocos datos.",
    }

    pulse_data = {
        "version": CACHE_VERSION,
        "week_id": WEEK_ID,
        "updated_at": now_vet.isoformat(),
        "updated_human": FECHA_HUMANA,
        "agent_status": {
            "name": "Agente CEO & SEO ByteZone",
            "mode": "Autónomo (Lunes + monitoreo de telemetría cada 6 h)",
            "active_games_count": len(decision["portada"]),
            "vault_games_count": len(decision["vault"]),
        },
        "video_reel": {
            "title": f"ByteZone TV • Noticiero IA ({WEEK_ID})",
            "subtitle": "5 Noticias Completas con Imagen + Voz IA + Lectura Completa",
            "duration_label": "5 Noticias",
            "scenes": scenes,
        },
        "weekly_news": news,
        "vip_hack_of_the_week": vip_hack,
        "weekly_jokes": weekly_jokes,
        "weekly_truths": weekly_truths,
        "game_layout": {"portada": decision["portada"], "vault": decision["vault"], "badges": decision["badges"]},
        "vault_games": [{"id": g, "title": GAME_NAMES[g], "url": GAME_URLS[g] + f"?v={CACHE_VERSION}"} for g in decision["vault"]],
        "seo": seo,
        "promo_kit": promo,
        "last_week_champions": champions,
        "all_time_records": records,
        "agent_report": report,
    }

    for target_root in OUTPUT_ROOTS:
        data_dir = os.path.join(target_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        save_json(os.path.join(data_dir, "weekly_pulse.json"), pulse_data)
        print(f"✅ Archivo actualizado: {os.path.join(data_dir, 'weekly_pulse.json')} ({len(news)} noticias, {len(scenes)} escenas)")

    # 6) Persistir estado del CEO
    hist = [h for h in state.get("history", []) if h.get("week_id") != WEEK_ID]
    hist.append({"week_id": WEEK_ID, "plays": s7["plays"], "devices": s7["devices"], "views": s7["views"], "ads": s7["ads_shown"]})
    state.update({
        "portada": decision["portada"], "vault": decision["vault"], "entered": decision["entered"],
        "history": hist[-12:],
        "last_news_keys": [title_key(n["title"]) for n in news],
        "last_joke_ids": joke_ids, "last_truth_ids": truth_ids,
    })
    save_json(STATE_PATH, state)
    print("🧠 Estado del CEO guardado. Decisiones:")
    for d in decision["decisions"]:
        print("   -", d)

if __name__ == "__main__":
    main()
