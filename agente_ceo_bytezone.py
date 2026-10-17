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
    ("Hipertextual Tecnología", "https://hipertextual.com/tecnologia/feed"),
    ("Google News IA & Gadgets", "https://news.google.com/rss/search?q=inteligencia+artificial+OR+invento+OR+robot+OR+smartphone&hl=es-419&gl=US&ceid=US:es-419"),
]

def clean_html_text(raw):
    if not raw:
        return ""
    text = html.unescape(raw)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_latest_tech_news():
    items = []
    seen_titles = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ByteZoneCEOAgent/1.0'}

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
                desc = clean_html_text(item.findtext('description') or '')
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

                if not desc or desc.lower().startswith(title[:20].lower()) or len(desc) < 40:
                    summary = f"Noticia destacada en {source_label} que marca la pauta tecnológica de esta semana."
                    voice_extra = f"Según reporta {source_label}, este avance ya está dando la vuelta al mundo."
                else:
                    summary = desc[:185].rsplit(' ', 1)[0] + "..."
                    voice_extra = summary

                items.append({
                    "title": title,
                    "summary": summary,
                    "voice_extra": voice_extra,
                    "source": source_label,
                    "link": link
                })
                count_from_source += 1
                if count_from_source >= 3 or len(items) >= 6:
                    break
        except Exception as e:
            print(f"[Aviso RSS] {source_name}: {e}")
        if len(items) >= 6:
            break

    fallback_news = [
        {
            "title": "Nuevos Agentes de IA Autónomos que operan apps y páginas web sin intervención humana",
            "summary": "La nueva generación de modelos multimodales ejecuta tareas completas en segundo plano, programa código y administra portales en tiempo real.",
            "voice_extra": "La nueva generación de modelos multimodales ejecuta tareas completas en segundo plano sin que tengas que tocar nada.",
            "source": "ByteZone IA Radar",
            "link": "https://news.google.com/"
        },
        {
            "title": "Baterías de Silicio-Carbono: Teléfonos con hasta 3 días de carga real",
            "summary": "Los nuevos lanzamientos móviles integran celdas de alta densidad que cargan del 0 al 80% en menos de 18 minutos sin degradar la batería.",
            "voice_extra": "Los nuevos teléfonos cargan del cero al ochenta por ciento en menos de dieciocho minutos.",
            "source": "Tech Hardware Flash",
            "link": "https://news.google.com/"
        },
        {
            "title": "Gafas Inteligentes Ultraligeras con traducción simultánea y pantalla holográfica",
            "summary": "El invento que busca reemplazar el teléfono en el bolsillo: proyecta mensajes, mapas y subtítulos en vivo directamente frente a tus ojos.",
            "voice_extra": "Proyectan mensajes, mapas y traducción en vivo directamente frente a tus ojos.",
            "source": "Futuro & Gadgets",
            "link": "https://news.google.com/"
        },
        {
            "title": "Chips Fotónicos para Inteligencia Artificial: 10 veces más rápidos usando luz",
            "summary": "Investigadores logran procesar redes neuronales mediante pulsos láser microscópicos, reduciendo el calentamiento en un 85%.",
            "voice_extra": "Procesan inteligencia artificial con pulsos de luz en lugar de electricidad tradicional.",
            "source": "Ciencia & Futuro",
            "link": "https://news.google.com/"
        }
    ]

    for fb in fallback_news:
        if len(items) >= 5:
            break
        items.append(fb)

    return items[:5]

def build_video_reel_scenes(news_list):
    icons = ["🤖", "🚀", "⚡", "🧠", "🔥"]
    badges = ["BOMBAZO #1 • TECH & IA", "BOMBAZO #2 • LO NUEVO", "BOMBAZO #3 • TENDENCIA", "BONUS VIP • FUTURO"]
    colors = ["from-cyan-600 to-blue-900", "from-purple-600 to-indigo-900", "from-pink-600 to-rose-900", "from-emerald-600 to-teal-900"]

    scenes = []
    scenes.append({
        "id": "intro",
        "badge": f"FLASH IA • {WEEK_ID}",
        "icon": "⚡",
        "headline": "¡Resumen Tech & IA en 45 Segundos!",
        "subtext": "Lo más impactante de la semana en tecnología, inventos e Inteligencia Artificial explicado al instante.",
        "voice_script": "¡Qué tal equipo de ByteZone! Arrancamos el resumen flash de tecnología e inteligencia artificial de esta semana. ¡Vamos a toda velocidad!",
        "bg_gradient": "from-blue-600 via-purple-700 to-pink-700",
        "duration_ms": 6500
    })

    for idx, item in enumerate(news_list[:3]):
        num = idx + 1
        headline = item["title"]
        if len(headline) > 100:
            headline = headline[:97].rsplit(' ', 1)[0] + "..."
        voice = f"Número {num}: {item['title']}. {item.get('voice_extra', item['summary'])}"
        scenes.append({
            "id": f"news_{num}",
            "badge": badges[idx],
            "icon": icons[idx],
            "headline": headline,
            "subtext": item["summary"],
            "voice_script": voice,
            "bg_gradient": colors[idx],
            "duration_ms": 9500
        })

    vip_item = news_list[3] if len(news_list) > 3 else news_list[0]
    scenes.append({
        "id": "outro",
        "badge": "🔓 SECRETO VIP & TORNEO",
        "icon": "👑",
        "headline": vip_item["title"],
        "subtext": "¡Toca el botón dorado abajo para desbloquear el Truco VIP de la semana y compite en el Torneo Semanal!",
        "voice_script": f"Y cerramos con: {vip_item['title']}. Toca el botón dorado debajo del video para desbloquear el truco secreto VIP de esta semana y rompe el récord en el Torneo Semanal de ByteZone.",
        "bg_gradient": "from-amber-500 via-orange-600 to-rose-800",
        "duration_ms": 9500,
        "is_vip_hook": True
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
        "url": "juegos/cyber-dodge.html?v=9",
        "accent": "amber"
    }
]

def main():
    print(f"🤖 [Agente CEO ByteZone] Ejecutando actualización autónoma para la semana {WEEK_ID} ({FECHA_HUMANA})...")
    news = fetch_latest_tech_news()
    scenes = build_video_reel_scenes(news)
    vip_hack = WEEKLY_VIP_HACKS[WEEK_NUM % len(WEEKLY_VIP_HACKS)]

    pulse_data = {
        "version": 9,
        "week_id": WEEK_ID,
        "updated_at": now_vet.isoformat(),
        "updated_human": FECHA_HUMANA,
        "agent_status": {
            "name": "Agente CEO & SEO ByteZone",
            "mode": "Autónomo (Lunes 00:05 AM + Monitoreo Continuo)",
            "active_games_count": 3,
            "vault_games_count": len(VAULT_GAMES_CATALOG),
            "seo_keywords": [
                "juegos arcade online gratis",
                "torneo semanal mini juegos telegram",
                "noticias inteligencia artificial resumen",
                "test de reflejos online milisegundos",
                "trucos secretos smartphones 2026"
            ]
        },
        "video_reel": {
            "title": f"ByteZone Flash IA • Edición {WEEK_ID}",
            "subtitle": "Video-Resumen Rápido con Voz de Inteligencia Artificial",
            "duration_label": "45 seg",
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
        print(f"✅ Archivo actualizado: {out_path} ({len(news)} noticias, {len(scenes)} escenas de video IA)")

if __name__ == "__main__":
    main()
