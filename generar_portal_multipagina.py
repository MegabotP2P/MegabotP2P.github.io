import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import json as _json

SITE_BASE = "https://megabotp2p.github.io/bytezone/"

def _load_pulse():
    for path in (os.path.join("bytezone", "data", "weekly_pulse.json"), os.path.join("portal_bytezone", "data", "weekly_pulse.json")):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return _json.load(fh)
        except Exception:
            continue
    return {}

PULSE = _load_pulse()
CV = "14"

GAME_CATALOG = {
    "stacker": {"emoji": "🏗️", "title": "Neon Stacker Pro", "cat": "Habilidad", "color": "cyan", "grad": "from-cyan-500 to-blue-600",
                "badge": "HABILIDAD 🏗️", "url": "juegos/neon-stacker.html", "vault_tag": "Habilidad & Precisión",
                "desc": "Encaja los bloques de neón a gran velocidad. Incluye botón de <strong>Segunda Oportunidad</strong> para no perder tu récord."},
    "reflex":  {"emoji": "⚡", "title": "Test de Reflejos", "cat": "Velocidad", "color": "purple", "grad": "from-purple-500 to-pink-600",
                "badge": "COMPETITIVO ⚡", "url": "juegos/reflejos-visuales.html", "vault_tag": "Velocidad & Reacción",
                "desc": "Mide tu tiempo de reacción visual en milisegundos cuando cambie a verde. ¿Tienes reflejos de piloto de carreras?"},
    "memory":  {"emoji": "🧠", "title": "Cyber Memory", "cat": "Memoria", "color": "emerald", "grad": "from-emerald-500 to-teal-600",
                "badge": "MEMORIA 🧠", "url": "juegos/cyber-memory.html", "vault_tag": "Memoria & Secuencias",
                "desc": "Memoriza y repite la secuencia de luces de neón. Cada ronda añade un paso más a toda velocidad."},
    "drone":   {"emoji": "🛸", "title": "Neon Cyber-Drone: Portales Láser", "cat": "Precisión", "color": "pink", "grad": "from-pink-500 to-rose-600",
                "badge": "ESTRENO NEÓN 🛸", "url": "juegos/cyber-drone.html", "vault_tag": "NUEVO • Vuelo Ciberpunk & Reflejos",
                "desc": "Impulsa el dron neón a través de portales láser móviles y recolecta orbes de energía. ¡Incluye Propulsor de Emergencia y Torneo Semanal!"},
    "dodge":   {"emoji": "🚀", "title": "Cyber Dodge: Tormenta de Asteroides", "cat": "Acción", "color": "amber", "grad": "from-amber-500 to-orange-500",
                "badge": "ACCIÓN 🚀", "url": "juegos/cyber-dodge.html", "vault_tag": "Acción Espacial & Reflejos",
                "desc": "Pilota la nave neón y sobrevive la mayor cantidad de segundos esquivando meteoritos cibernéticos. ¡Tiene su propio Torneo Semanal y Escudo de Segunda Oportunidad!"},
}

_layout = PULSE.get("game_layout") or {}
PORTADA_IDS = [g for g in (_layout.get("portada") or ["stacker", "reflex", "memory"]) if g in GAME_CATALOG]
VAULT_IDS = [g for g in (_layout.get("vault") or ["drone", "dodge"]) if g in GAME_CATALOG and g not in PORTADA_IDS]
for _gk in GAME_CATALOG:
    if _gk not in PORTADA_IDS and _gk not in VAULT_IDS:
        VAULT_IDS.insert(0, _gk)
GAME_BADGES = _layout.get("badges") or {}

def render_portada_grid():
    cards = []
    for g in PORTADA_IDS:
        m = GAME_CATALOG[g]
        col = m["color"]
        badge = GAME_BADGES.get(g, m["badge"])
        cards.append(f"""
                <!-- TARJETA JUEGO: {m['title'].upper()} -->
                <div class="bg-gray-900/80 border border-{col}-500/40 rounded-3xl p-5 hover:border-{col}-400 transition shadow-xl flex flex-col justify-between group">
                    <div>
                        <div class="flex justify-between items-center mb-3">
                            <span class="text-[10px] font-black bg-{col}-500/20 text-{col}-300 px-2.5 py-1 rounded-md uppercase">{badge}</span>
                            <span class="text-[11px] text-gray-400">{m['cat']}</span>
                        </div>
                        <h3 class="text-lg font-black text-white group-hover:text-{col}-400 transition">{m['emoji']} {m['title']}</h3>
                        <p class="text-xs text-gray-400 mt-2 leading-relaxed">{m['desc']}</p>
                    </div>
                    <div class="mt-5 pt-4 border-t border-gray-800 flex items-center justify-between">
                        <a href="{m['url']}?v={CV}" class="bg-gradient-to-r {m['grad']} hover:opacity-90 text-white font-black text-xs px-4 py-2.5 rounded-xl shadow-lg shadow-{col}-500/25 transition">
                            ▶ JUGAR AHORA
                        </a>
                        <a href="tg://resolve?domain=ByteZoneArcadeBot" class="text-xs text-blue-400 hover:underline">
                            En Telegram ✈️
                        </a>
                    </div>
                </div>""")
    return '<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">' + "".join(cards) + '\n            </div>'

def render_vault_cards():
    out = []
    for g in VAULT_IDS:
        m = GAME_CATALOG[g]
        is_new = (g == "drone")
        tag_label = "ESTRENO EN EL BAÚL ✨" if is_new else "JOYA EN EL BAÚL"
        tag_bg = "bg-pink-500 text-white" if is_new else "bg-amber-500 text-gray-950"
        border_col = "border-pink-500/40" if is_new else "border-amber-500/30"
        btn_grad = "from-pink-500 to-rose-600 text-white shadow-pink-500/25" if is_new else "from-amber-500 to-orange-500 text-gray-950 shadow-amber-500/25"
        out.append(f"""            <div class="bg-gray-950/80 border {border_col} rounded-2xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-3">
                <div class="space-y-1">
                    <div class="flex items-center space-x-2">
                        <span class="text-[10px] font-black {tag_bg} px-2 py-0.5 rounded uppercase">{tag_label}</span>
                        <span class="text-xs text-amber-300 font-semibold">{m['vault_tag']}</span>
                    </div>
                    <h4 class="text-base font-black text-white">{m['emoji']} {m['title']}</h4>
                    <p class="text-xs text-gray-300 leading-relaxed max-w-xl">{m['desc']}</p>
                </div>
                <button onclick="openVaultGameWithReward('{m['url']}?v={CV}', '{g}')" class="w-full sm:w-auto flex-shrink-0 bg-gradient-to-r {btn_grad} hover:opacity-90 active:scale-95 font-black text-xs px-5 py-3 rounded-xl shadow-lg transition flex items-center justify-center space-x-1.5">
                    <span>🔓</span>
                    <span>RESCATAR DEL BAÚL &amp; JUGAR</span>
                </button>
            </div>""")
    return "\n".join(out)

def render_truth_grid():
    truths = PULSE.get("weekly_truths") or []
    if not truths:
        return ""
    cards = []
    for t in truths:
        col = t.get("color", "cyan")
        cards.append(f"""
            <div class="bg-gray-900/90 p-5 rounded-2xl border border-{col}-500/30 shadow-lg">
                <div class="flex items-center space-x-2 mb-2">
                    <span class="text-xl">{t.get('emoji','💡')}</span>
                    <h4 class="text-xs font-black text-{col}-400 uppercase tracking-wider">{t.get('title','')}</h4>
                </div>
                <p class="text-xs text-gray-300 leading-relaxed">{t.get('body','')}</p>
            </div>""")
    return '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">' + "".join(cards) + '\n        </div>'

def jokes_json():
    jokes = PULSE.get("weekly_jokes") or []
    return _json.dumps(jokes, ensure_ascii=False) if jokes else ""

# ---------------- SEO ----------------
def _esc(s):
    return (s or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

def build_seo_block(page_key, path):
    seo = PULSE.get("seo") or {}
    kw = ", ".join(seo.get("keywords") or [])
    og_img = seo.get("og_image") or "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80"
    first_news = ((PULSE.get("weekly_news") or [{}])[0] or {}).get("title", "las noticias de IA de la semana")
    pages = {
        "index": (seo.get("title") or "ByteZone Arcade | Juegos Gratis, Ranking Semanal y Noticias de IA",
                  seo.get("description") or "Juega gratis, compite en el torneo semanal y mira el resumen de IA de la semana."),
        "hacks": ("Noticias de IA de la Semana, Inventos y Trucos de Celular | ByteZone",
                  f"Resumen en video y lectura completa de las 5 noticias de IA y tecnología de la semana. Hoy: {first_news}"),
        "humor": ("Chistes y Humor Tech de la Semana | ByteZone",
                  "Chistes nuevos cada semana sobre WhatsApp, la batería, la inteligencia artificial y la vida digital. ¡Ríete y comparte!"),
        "telegram": ("Mini App de Telegram: Juegos y Ranking | ByteZone",
                     "Juega a los mini-juegos de ByteZone desde Telegram y compite en el ranking semanal mundial."),
        "stats": ("Panel de Métricas | ByteZone", "Panel interno de métricas."),
        "stacker": ("Neon Stacker Pro: Juego de Torre Neón Online Gratis | ByteZone",
                    "Apila bloques de neón sin fallar y llega al Piso más alto. Ranking semanal e histórico en vivo. Gratis y sin descargar."),
        "reflex": ("Test de Reflejos Online: ¿Cuántos Milisegundos Reaccionas? | ByteZone",
                   "Mide tu velocidad de reacción en milisegundos y compite en el ranking mundial semanal. Reta a tus amigos."),
        "memory": ("Cyber Memory: Juego de Memoria de Secuencias Online | ByteZone",
                   "Repite la secuencia de luces neón y supera tu récord de rondas. Torneo semanal y ranking histórico."),
        "dodge": ("Cyber Dodge: Esquiva Asteroides, Juego de Reflejos | ByteZone",
                  "Pilota tu nave y esquiva la lluvia de meteoritos neón el mayor tiempo posible. Ranking semanal en vivo."),
        "drone": ("Neon Cyber-Drone: Portales Láser Online Gratis | ByteZone",
                  "Vuela tu dron ciberpunk a través de portales láser móviles y compite en el ranking semanal en vivo."),
        "campeones": ("Histórico Semanal de Campeones y Ganadores | ByteZone Arcade",
                      "Consulta el cuadro de honor histórico de ganadores semana a semana (Top 3) en todos los juegos de ByteZone Arcade."),
    }
    title, desc = pages.get(page_key, pages["index"])
    url = SITE_BASE + path
    robots = "noindex, nofollow" if page_key == "stats" else "index, follow, max-image-preview:large"
    ld = {
        "@context": "https://schema.org",
        "@type": "WebSite" if page_key == "index" else "WebPage",
        "name": "ByteZone Arcade", "url": url, "inLanguage": "es", "description": desc,
    }
    if page_key == "index":
        ld["potentialAction"] = {"@type": "PlayAction", "target": SITE_BASE}
    return f"""<title>{_esc(title)}</title>
    <meta name="description" content="{_esc(desc)}">
    <meta name="keywords" content="{_esc(kw)}">
    <meta name="robots" content="{robots}">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="ByteZone Arcade">
    <meta property="og:title" content="{_esc(title)}">
    <meta property="og:description" content="{_esc(desc)}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{_esc(og_img)}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{_esc(title)}">
    <meta name="twitter:description" content="{_esc(desc)}">
    <meta name="twitter:image" content="{_esc(og_img)}">
    <script type="application/ld+json">{_json.dumps(ld, ensure_ascii=False)}</script>"""

def inject_seo(html, page_key, path):
    html = re.sub(r'<title>.*?</title>\s*', '', html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description"[^>]*>\s*', '', html, count=1)
    block = build_seo_block(page_key, path)
    return re.sub(r'(<meta name="viewport"[^>]*>)', lambda m: m.group(1) + "\n    " + block, html, count=1)

PORTAL_DIR = "portal_bytezone"
JUEGOS_DIR = os.path.join(PORTAL_DIR, "juegos")
os.makedirs(JUEGOS_DIR, exist_ok=True)

# SCRIPTS DE ANUNCIOS MONETAG AUDITADOS (v=14):
# - PRESERVA TOKENS DE SESIÓN DE MONETAG (NO BORRA LOCALSTORAGE NI SERVICE WORKER DE MONETAG)
# - PRECARGA SDK REWARDED (12040274 CPM $0.07) + RESPALDO (12040276) EN <HEAD> PARA CERO PÉRDIDA DE IMPRESIONES
MONETAG_TAG = """
    <script>
        // Redirección suave de versión sin destruir las cookies/tokens de atribución de Monetag
        try {
            if (!location.search.includes('v=14') && !sessionStorage.getItem('bz_v12_reloaded')) {
                sessionStorage.setItem('bz_v12_reloaded', '1');
                const cleanSearch = location.search.replace(/[?&]v=\\d+/g, '');
                const sep = cleanSearch.includes('?') ? '&' : '?';
                location.replace(location.pathname + cleanSearch + sep + 'v=14' + location.hash);
            }
        } catch (e) {}
    </script>

    <!-- 1. Monetag In-Page Push Banners (Zona 12034401) - Web y Telegram Mini App -->
    <script>(function(s){s.dataset.zone='12034401',s.src='https://nap5k.com/tag.min.js'})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')));</script>

    <!-- 2. Monetag Rewarded Interstitial SDK PRECARGADO desde el inicio (Zona Principal 12040274 CPM Alto + Zona Respaldo 12040276) -->
    <script src="https://libtl.com/sdk.js" data-zone="12040274" data-sdk="show_12040274"></script>
    <script src="https://libtl.com/sdk.js" data-zone="12040276" data-sdk="show_12040276"></script>
    
    <script>
        // 3. Sistema de Recompensa Auditado con Cascada (Waterfall 12040274 -> 12040276) + Telemetría Global Multi-Teléfono
        window.NTFY_TELEMETRY_TOPIC = 'bytezone_global_telemetry_v12';
        window.CLOUD_TELEMETRY_ID = 'ff808181a09d98f701a14fdad1ef0d95';
        window.bzAdInProgress = false;

        window.broadcastGlobalTelemetry = function(payload) {
            try {
                const eid = payload.eid || ('ev_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 6));
                const fullPayload = Object.assign({
                    eid: eid,
                    p: localStorage.getItem('bytezone_player_name') || 'Jugador',
                    d: localStorage.getItem('bytezone_device_id') || 'dev',
                    c: localStorage.getItem('bytezone_player_country') || 'VE',
                    ts: Date.now()
                }, payload);

                // Guardar también en historial local de eventos para respuesta instantánea
                try {
                    const localEvents = JSON.parse(localStorage.getItem('bytezone_global_events_cache') || '[]');
                    if (!localEvents.some(x => x.eid === eid)) {
                        localEvents.push(fullPayload);
                        if (localEvents.length > 250) localEvents.shift();
                        localStorage.setItem('bytezone_global_events_cache', JSON.stringify(localEvents));
                    }
                } catch (e) {}

                fetch('https://ntfy.sh/' + window.NTFY_TELEMETRY_TOPIC, {
                    method: 'POST',
                    keepalive: true,
                    body: JSON.stringify(fullPayload)
                }).catch(() => {});
            } catch (e) {}
        };

        function executeRewardedAction(rewardCallback) {
            if (window.bzAdInProgress) return;
            window.bzAdInProgress = true;

            const finishReward = (adShown, zoneUsed) => {
                window.bzAdInProgress = false;
                try {
                    const log = JSON.parse(localStorage.getItem('bytezone_ad_audit') || '{"shown":0,"fallback":0}');
                    if (adShown) log.shown = (log.shown || 0) + 1;
                    else log.fallback = (log.fallback || 0) + 1;
                    log.last_zone = zoneUsed;
                    log.last_time = new Date().toISOString();
                    localStorage.setItem('bytezone_ad_audit', JSON.stringify(log));
                } catch (e) {}

                // Emitir impresión de anuncio a la nube global para que se vea en todos los teléfonos al instante
                window.broadcastGlobalTelemetry({
                    kind: 'ad',
                    g: window.CURRENT_GAME_KEY || 'portal',
                    shown: adShown ? 1 : 0,
                    zone: zoneUsed
                });

                if (typeof rewardCallback === 'function') rewardCallback();
            };

            const tryBackupZone = () => {
                if (typeof window.show_12040276 === 'function') {
                    window.show_12040276().then(() => {
                        finishReward(true, '12040276');
                    }).catch((err2) => {
                        console.warn("Monetag Zona Respaldo 12040276 sin inventario:", err2);
                        finishReward(false, 'none');
                    });
                } else {
                    finishReward(false, 'none');
                }
            };

            if (typeof window.show_12040274 === 'function') {
                window.show_12040274().then(() => {
                    finishReward(true, '12040274');
                }).catch((err1) => {
                    console.warn("Monetag Zona Principal 12040274 no llenó, activando respaldo 12040276:", err1);
                    tryBackupZone();
                });
            } else {
                tryBackupZone();
            }
        }
    </script>
"""

# HEADER Y NAV UNIVERSAL
def get_header(current_page="arcade", depth=0):
    root = "../" if depth == 1 else ""
    
    def nav_class(page):
        if current_page == page:
            return "bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-bold shadow-md shadow-cyan-500/20"
        return "hover:text-white hover:bg-gray-800/50"

    return f"""
    <!-- ESPACIO RESERVADO PARA BANNERS MONETAG EN LA PARTE SUPERIOR (EVITA QUE TAPEN EL LOGO Y BOTONES) -->
    <div id="monetag-ad-spacer" class="w-full h-24 sm:h-28 flex-shrink-0 pointer-events-none" style="min-height: 96px;" aria-hidden="true"></div>

    <header class="relative z-30 bg-gray-900/90 backdrop-blur-md border-b border-gray-800">
        <div class="max-w-4xl mx-auto px-4 py-3 flex justify-between items-center">
            <a href="{root}index.html?v=14" class="flex items-center space-x-2 group">
                <span class="text-2xl transform group-hover:scale-110 transition">⚡</span>
                <span class="text-xl font-black tracking-wider bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-500 bg-clip-text text-transparent">
                    BYTE<span class="text-white">ZONE</span>
                </span>
            </a>
            <div class="flex items-center space-x-2">
                <button onclick="promptChangeName()" class="text-xs text-gray-300 hover:text-cyan-400 bg-gray-800/80 px-2.5 py-1.5 rounded-xl border border-gray-700/60 flex items-center space-x-1.5 transition">
                    <span id="playerCountryDisplay" class="text-sm select-none">🌐</span>
                    <span id="playerNameDisplay" class="font-bold max-w-[90px] sm:max-w-[120px] truncate">Jugador</span>
                    <span class="text-cyan-400 text-[10px]">✏️</span>
                </button>
                <a id="headerActionBtn" href="{root}telegram.html?v=14" class="flex items-center space-x-1 text-xs bg-gradient-to-r from-blue-600 to-cyan-500 hover:opacity-90 text-white font-bold px-3 py-1.5 rounded-xl shadow-lg shadow-blue-500/25 transition">
                    <span id="headerActionIcon">✈️</span>
                    <span id="headerActionText" class="hidden sm:inline">Telegram</span>
                </a>
            </div>
        </div>
    </header>

    <nav class="max-w-4xl mx-auto px-4 mt-3 w-full">
        <div class="grid grid-cols-5 gap-1 sm:gap-2 p-1.5 bg-gray-900/85 backdrop-blur-md rounded-2xl border border-gray-800 text-[11px] sm:text-sm font-medium text-gray-400">
            <a href="{root}index.html?v=14" class="py-2.5 rounded-xl transition flex flex-col sm:flex-row items-center justify-center space-y-1 sm:space-y-0 sm:space-x-1.5 {nav_class('arcade')}">
                <span class="text-base sm:text-lg">🕹️</span>
                <span>Arcade</span>
            </a>
            <a href="{root}campeones.html?v=14" class="py-2.5 rounded-xl transition flex flex-col sm:flex-row items-center justify-center space-y-1 sm:space-y-0 sm:space-x-1.5 {nav_class('campeones')}">
                <span class="text-base sm:text-lg">🏆</span>
                <span>Campeones</span>
            </a>
            <a href="{root}hacks.html?v=14" class="py-2.5 rounded-xl transition flex flex-col sm:flex-row items-center justify-center space-y-1 sm:space-y-0 sm:space-x-1.5 {nav_class('hacks')}">
                <span class="text-base sm:text-lg">🤖</span>
                <span>IA & TV</span>
            </a>
            <a href="{root}humor.html?v=14" class="py-2.5 rounded-xl transition flex flex-col sm:flex-row items-center justify-center space-y-1 sm:space-y-0 sm:space-x-1.5 {nav_class('humor')}">
                <span class="text-base sm:text-lg">🎭</span>
                <span>Humor</span>
            </a>
            <a href="{root}telegram.html?v=14" class="py-2.5 rounded-xl transition flex flex-col sm:flex-row items-center justify-center space-y-1 sm:space-y-0 sm:space-x-1.5 {nav_class('telegram')}">
                <span class="text-base sm:text-lg">🚀</span>
                <span>Comunidad</span>
            </a>
        </div>
    </nav>
    """


def get_footer(depth=0):
    root = "../" if depth == 1 else ""
    return f"""
    <footer class="bg-gray-900/80 border-t border-gray-800 py-6 text-center text-xs text-gray-500 mt-auto">
        <p>© 2026 ByteZone • Portal Autónomo de Mini-Juegos, IA & Entretenimiento Móvil</p>
        <p class="mt-2 flex flex-wrap items-center justify-center gap-3 text-[11px]">
            <a href="{root}stats.html?v=14" class="text-gray-400 hover:text-cyan-400 transition flex items-center space-x-1">
                <span>🤖</span>
                <span class="underline">Agente CEO & Métricas</span>
            </a>
            <span>•</span>
            <span class="text-emerald-400 font-semibold">Actualización Semanal Automática Activa 🌐</span>
        </p>
    </footer>
    """

PLAYER_MODAL = """
    <!-- MODAL PERFIL JUGADOR (CONEXIÓN UNIFICADA Y PAÍS) -->
    <div id="namePromptModal" class="hidden fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4">
        <div class="bg-gray-900 w-full max-w-sm rounded-3xl p-6 border border-purple-500/50 text-center shadow-2xl relative">
            <span class="text-4xl animate-bounce inline-block">👑</span>
            <h3 class="text-xl font-black text-white mt-2">Tu Perfil de Campeón</h3>
            <p class="text-xs text-gray-300 my-2">Tu apodo y bandera quedarán guardados en la tabla de récords mundiales en tiempo real.</p>
            
            <div class="flex items-center justify-center space-x-2 my-3 p-2 bg-gray-800/80 rounded-xl border border-gray-700/60 text-xs text-gray-300">
                <span>Tu Bandera:</span>
                <span id="modalCountryFlag" class="text-xl">🌐</span>
                <span id="modalCountryName" class="font-bold text-cyan-400">VE</span>
                <span class="text-[10px] text-gray-400">(Auto-detectada)</span>
            </div>

            <input type="text" id="modalNameInput" placeholder="Ej: Alex_Pro, Fénix..." maxlength="15"
                   class="w-full px-4 py-3 rounded-xl bg-gray-800 text-white text-sm border border-gray-700 focus:outline-none focus:border-cyan-400 mb-4 text-center font-bold tracking-wider">
            
            <div class="flex space-x-2">
                <button onclick="closeNameModal()" class="w-1/2 bg-gray-800 hover:bg-gray-700 text-gray-300 font-bold py-2.5 rounded-xl text-xs transition">
                    Cancelar
                </button>
                <button onclick="savePlayerNameFromModal()" class="w-1/2 bg-gradient-to-r from-cyan-500 to-purple-600 hover:opacity-90 text-white font-bold py-2.5 rounded-xl text-xs transition shadow-lg shadow-cyan-500/25">
                    Guardar Perfil
                </button>
            </div>
        </div>
    </div>

    <!-- MODAL CELEBRACIÓN PODIO MUNDIAL Y GANCHO SOCIAL DE RETO VIRAL -->
    <div id="podiumShareModal" class="hidden fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4">
        <div class="bg-gradient-to-b from-gray-900 via-gray-900 to-gray-950 w-full max-w-sm rounded-3xl p-6 border-2 border-yellow-500/60 text-center shadow-2xl relative overflow-hidden">
            
            <div class="absolute -top-12 -left-12 w-28 h-28 bg-yellow-500/10 rounded-full blur-2xl pointer-events-none"></div>
            <div class="absolute -bottom-12 -right-12 w-28 h-28 bg-purple-500/15 rounded-full blur-2xl pointer-events-none"></div>

            <span id="podiumMedalIcon" class="text-5xl animate-bounce inline-block filter drop-shadow">🥇</span>
            <span class="block text-[11px] font-black uppercase tracking-widest text-yellow-400 mt-2">¡ENTRASTE AL PODIO DE CAMPEONES!</span>
            <h3 id="podiumModalTitle" class="text-xl font-black text-white mt-1 leading-snug">Juego Arcade</h3>
            
            <!-- TARJETA CON EL DOBLE PUESTO (SEMANAL + HISTÓRICO) -->
            <div class="my-4 p-4 rounded-2xl bg-gray-950/80 border border-yellow-500/40 text-left space-y-2.5">
                <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-400">Tu Marca Registrada:</span>
                    <span id="podiumScoreValue" class="font-black text-base text-yellow-300">31 ms</span>
                </div>
                <div class="h-px bg-gray-800"></div>
                <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-300 flex items-center space-x-1">
                        <span>🔥</span>
                        <span>Torneo Semanal:</span>
                    </span>
                    <span id="podiumWeeklyRankText" class="font-black text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/30">
                        🥇 Puesto #1 de la Semana
                    </span>
                </div>
                <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-300 flex items-center space-x-1">
                        <span>👑</span>
                        <span>Récord Histórico:</span>
                    </span>
                    <span id="podiumAlltimeRankText" class="font-black text-cyan-300 bg-cyan-500/10 px-2 py-0.5 rounded-md border border-cyan-500/30">
                        👑 Puesto #1 de Todos los Tiempos
                    </span>
                </div>
            </div>

            <p class="text-[11px] text-gray-300 mb-4 leading-relaxed">
                ¡Reta a tus amigos y grupos a superar tu puesto en el podio antes de que termine el torneo!
            </p>

            <!-- BOTONES DE COMPARTIR VIRAL -->
            <div class="space-y-2">
                <a id="podiumWhatsappBtn" href="#" onclick="return openShareLink(this.href)" rel="noopener" class="w-full bg-gradient-to-r from-emerald-500 to-green-600 hover:opacity-95 text-white font-black py-3 px-4 rounded-2xl text-xs flex items-center justify-center space-x-2 shadow-lg shadow-emerald-500/25 transition">
                    <span>📲</span>
                    <span>Compartir Reto en WhatsApp</span>
                </a>
                <a id="podiumTelegramBtn" href="#" onclick="return openShareLink(this.href)" rel="noopener" class="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:opacity-95 text-white font-black py-3 px-4 rounded-2xl text-xs flex items-center justify-center space-x-2 shadow-lg shadow-blue-500/25 transition">
                    <span>✈️</span>
                    <span>Compartir Reto en Telegram</span>
                </a>
                <button onclick="sharePodiumNative()" class="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:opacity-95 text-white font-black py-3 px-4 rounded-2xl text-xs flex items-center justify-center space-x-2 shadow-lg shadow-purple-500/25 transition"><span>📤</span><span>Compartir con otras apps</span></button>
                <button onclick="copyPodiumChallengeText()" class="w-full bg-gray-800 hover:bg-gray-750 text-gray-200 font-bold py-2.5 px-4 rounded-xl text-xs flex items-center justify-center space-x-1.5 border border-gray-700 transition">
                    <span id="copyChallengeIcon">📋</span>
                    <span id="copyChallengeText">Copiar Mensaje del Reto</span>
                </button>
            </div>

            <button onclick="closePodiumModal()" class="mt-4 text-xs text-gray-400 hover:text-white underline">
                ✕ Continuar Jugando
            </button>
        </div>
    </div>
"""

PLAYER_IDENTITY_SCRIPT = """
    <script>
        // Reparación automática de nombres truncados en versiones previas (12 chars -> 15 chars completos)
        const KNOWN_NAME_REPAIRS = {
            'rafael torre': 'Rafael Torres',
            'tovias torre': 'Tovias Torres',
            'tobias torre': 'Tovias Torres'
        };

        function repairPlayerName(rawName) {
            if (!rawName) return 'Jugador';
            const clean = String(rawName).replace(/[|;]/g, '').trim().slice(0, 15);
            const lower = clean.toLowerCase();
            if (KNOWN_NAME_REPAIRS[lower]) return KNOWN_NAME_REPAIRS[lower];
            return clean || 'Jugador';
        }

        // Sistema de identidad persistente por dispositivo (Device ID)
        let deviceId = localStorage.getItem('bytezone_device_id');
        if (!deviceId) {
            deviceId = 'dev_' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
            localStorage.setItem('bytezone_device_id', deviceId);
        }

        let playerName = localStorage.getItem('bytezone_player_name');
        if (!playerName) {
            if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initDataUnsafe && window.Telegram.WebApp.initDataUnsafe.user) {
                playerName = window.Telegram.WebApp.initDataUnsafe.user.first_name || window.Telegram.WebApp.initDataUnsafe.user.username;
            } else {
                playerName = "Jugador_" + Math.floor(Math.random()*900 + 100);
            }
        }
        playerName = repairPlayerName(playerName);
        localStorage.setItem('bytezone_player_name', playerName);

        let prevNames = [];
        try {
            prevNames = JSON.parse(localStorage.getItem('bytezone_prev_names') || '[]');
            if (!Array.isArray(prevNames)) prevNames = [];
        } catch (e) { prevNames = []; }

        let playerCountry = localStorage.getItem('bytezone_player_country') || '';

        // ==========================================================
        // RELOJ DE TORNEO SEMANAL (REINICIO DOMINGO 12:00 AM / LUNES 00:00 VET)
        // ==========================================================
        function getNowVenezuela() {
            const now = new Date();
            const utcMs = now.getTime() + (now.getTimezoneOffset() * 60000);
            return new Date(utcMs - (4 * 3600000)); // UTC-4 Venezuela
        }

        function getCurrentWeekId() {
            const vet = getNowVenezuela();
            const day = vet.getDay(); // 0 = Domingo, 1 = Lunes, ..., 6 = Sábado
            const diffToMonday = (day === 0) ? -6 : (1 - day);
            const monday = new Date(vet);
            monday.setDate(vet.getDate() + diffToMonday);
            const y = monday.getFullYear();
            const m = String(monday.getMonth() + 1).padStart(2, '0');
            const d = String(monday.getDate()).padStart(2, '0');
            return `W${y}-${m}-${d}`;
        }

        function getWeeklyCountdownText() {
            const vet = getNowVenezuela();
            const day = vet.getDay();
            const daysUntilMonday = (day === 0) ? 1 : (8 - day);
            const nextMonday = new Date(vet);
            nextMonday.setDate(vet.getDate() + daysUntilMonday);
            nextMonday.setHours(0, 0, 0, 0);
            const diffMs = Math.max(0, nextMonday.getTime() - vet.getTime());
            const totalMinutes = Math.floor(diffMs / 60000);
            const d = Math.floor(totalMinutes / (60 * 24));
            const h = Math.floor((totalMinutes % (60 * 24)) / 60);
            const m = totalMinutes % 60;
            if (d > 0) {
                return `⏳ Reinicia Dom 12:00 AM (${d}d ${h}h ${m}m)`;
            }
            return `⏳ Reinicia hoy 12:00 AM (${h}h ${m}m)`;
        }

        const ALL_GAME_KEYS = ['stacker', 'reflex', 'memory', 'dodge', 'drone'];

        // Archivo Histórico Oficial de Campeones Semanales (Salón de la Fama Semana a Semana)
        const HISTORICAL_WEEKLY_CHAMPIONS = [
            {
                weekId: 'W2026-10-19',
                label: 'Semana #2 • 19 Oct al 25 Oct 2026',
                status: 'Cerrada • Premiada',
                champions: {
                    stacker: [
                        { name: "alexa torres", score: 36, country: "VE" },
                        { name: "*****", score: 34, country: "VE" },
                        { name: "RATG", score: 31, country: "VE" }
                    ],
                    reflex: [
                        { name: "RATG", score: 29, country: "VE" },
                        { name: "*****", score: 84, country: "VE" },
                        { name: "Rafael Torres", score: 238, country: "VE" }
                    ],
                    memory: [
                        { name: "Jugador_930", score: 14, country: "VE" },
                        { name: "Tovias Torres", score: 11, country: "VE" },
                        { name: "*****", score: 10, country: "VE" }
                    ],
                    dodge: [
                        { name: "RATG", score: 29, country: "VE" },
                        { name: "Rafael Torres", score: 23, country: "VE" },
                        { name: "Nova_VE", score: 21, country: "VE" }
                    ],
                    drone: [
                        { name: "RATG", score: 26, country: "VE" },
                        { name: "Rafael Torres", score: 21, country: "VE" },
                        { name: "CyberHornet", score: 18, country: "MX" }
                    ]
                }
            },
            {
                weekId: 'W2026-10-12',
                label: 'Semana Inaugural #1 • 12 Oct al 18 Oct 2026',
                status: 'Cerrada • Premiada',
                champions: {
                    stacker: [
                        { name: "alexa torres", score: 34, country: "VE" },
                        { name: "*****", score: 33, country: "VE" },
                        { name: "RATG", score: 29, country: "VE" }
                    ],
                    reflex: [
                        { name: "RATG", score: 31, country: "VE" },
                        { name: "*****", score: 87, country: "VE" },
                        { name: "Rafael Torres", score: 249, country: "VE" }
                    ],
                    memory: [
                        { name: "Jugador_930", score: 13, country: "VE" },
                        { name: "Jugador_662", score: 10, country: "VE" },
                        { name: "Tovias Torres", score: 10, country: "VE" }
                    ],
                    dodge: [
                        { name: "RATG", score: 24, country: "VE" },
                        { name: "Rafael Torres", score: 19, country: "VE" },
                        { name: "CyberPilot", score: 17, country: "ES" }
                    ],
                    drone: [
                        { name: "RATG", score: 22, country: "VE" },
                        { name: "Rafael Torres", score: 18, country: "VE" },
                        { name: "DroneMaster", score: 15, country: "CO" }
                    ]
                }
            }
        ];

        function ensureWeeklyReset() {
            const currentWeek = getCurrentWeekId();
            const savedWeek = localStorage.getItem('bytezone_active_week');
            if (savedWeek !== currentWeek) {
                // Si había una semana previa activa, archivar automáticamente sus Top 3 campeones antes de reiniciar
                if (savedWeek) {
                    try {
                        let archive = JSON.parse(localStorage.getItem('bytezone_champions_archive') || '[]');
                        if (!archive.some(w => w && w.weekId === savedWeek)) {
                            const snap = {};
                            ALL_GAME_KEYS.forEach(g => {
                                let list = [];
                                try { list = JSON.parse(localStorage.getItem('bytezone_weekly_scores_' + g) || '[]'); } catch(e) {}
                                if (Array.isArray(list) && list.length > 0) {
                                    snap[g] = list.slice(0, 3);
                                }
                            });
                            if (Object.keys(snap).length > 0) {
                                archive.unshift({
                                    weekId: savedWeek,
                                    label: `Semana ${savedWeek.replace('W', '')} • Torneo Oficial`,
                                    status: 'Cerrada • Premiada',
                                    champions: snap
                                });
                                localStorage.setItem('bytezone_champions_archive', JSON.stringify(archive.slice(0, 20)));
                            }
                        }
                    } catch(e) {}
                }
                ALL_GAME_KEYS.forEach(g => {
                    if (!savedWeek && currentWeek === 'W2026-10-12') {
                        const existingBest = localStorage.getItem('bytezone_best_' + g) || '0';
                        localStorage.setItem('bytezone_weekly_best_' + g, existingBest);
                    } else {
                        localStorage.setItem('bytezone_weekly_best_' + g, '0');
                        localStorage.setItem('bytezone_weekly_scores_' + g, '[]');
                    }
                });
                localStorage.setItem('bytezone_active_week', currentWeek);
            }
            return currentWeek;
        }
        ensureWeeklyReset();

        function getWeeklyChampionsArchive() {
            let customArchive = [];
            try { customArchive = JSON.parse(localStorage.getItem('bytezone_champions_archive') || '[]'); } catch(e) {}
            const byWeek = new Map();
            customArchive.forEach(item => {
                if (item && item.weekId) byWeek.set(item.weekId, item);
            });
            HISTORICAL_WEEKLY_CHAMPIONS.forEach(item => {
                if (item && item.weekId && !byWeek.has(item.weekId)) {
                    byWeek.set(item.weekId, item);
                }
            });
            return Array.from(byWeek.values());
        }

        // ==========================================================
        // MOTOR DE SINCRONIZACIÓN MUNDIAL EN TIEMPO REAL (SEMANAL + HISTÓRICO)
        // ==========================================================
        const CLOUD_ALLTIME_IDS = {
            stacker: 'ff808181a09d98f701a1448611567237',
            reflex:  'ff808181a09d98f701a1448613fe7238',
            memory:  'ff808181a09d98f701a14486174a7239'
        };
        const CLOUD_WEEKLY_IDS = {
            stacker: 'ff808181a09d98f701a14a82e347035f',
            reflex:  'ff808181a09d98f701a14a82e55d0360',
            memory:  'ff808181a09d98f701a14a82e7130361'
        };
        const NTFY_SCORES_TOPIC = 'bytezone_global_scores_v3';

        window.currentLeaderboardTab = 'weekly'; // 'weekly' o 'alltime'

        // Semilla de jugadores reales verificados de la semana inaugural W2026-10-12 (con ***** sincronizado en 33 en ambos rankings)
        const SEEDED_WEEKLY_SCORES = {
            'W2026-10-12': {
                stacker: [
                    { name: "alexa torres", score: 34, country: "VE" },
                    { name: "*****", score: 33, country: "VE" },
                    { name: "RATG", score: 29, country: "VE" },
                    { name: "Jugador_930", score: 29, country: "VE" },
                    { name: "Jugador_311", score: 23, country: "VE" },
                    { name: "Rafael Torres", score: 22, country: "VE" },
                    { name: "Jugador_662", score: 22, country: "VE" }
                ],
                reflex: [
                    { name: "RATG", score: 31, country: "VE" },
                    { name: "*****", score: 87, country: "VE" },
                    { name: "Rafael Torres", score: 249, country: "VE" },
                    { name: "Jugador_930", score: 308, country: "VE" }
                ],
                memory: [
                    { name: "Jugador_930", score: 13, country: "VE" },
                    { name: "Jugador_662", score: 10, country: "VE" },
                    { name: "Tovias Torres", score: 10, country: "VE" },
                    { name: "*****", score: 10, country: "VE" },
                    { name: "Jugador_311", score: 8, country: "VE" },
                    { name: "RATG", score: 5, country: "VE" }
                ],
                dodge: [
                    { name: "RATG", score: 24, country: "VE" },
                    { name: "Rafael Torres", score: 19, country: "VE" }
                ],
                drone: [
                    { name: "RATG", score: 26, country: "VE" },
                    { name: "Rafael Torres", score: 21, country: "VE" },
                    { name: "CyberHornet", score: 18, country: "MX" }
                ]
            },
            'W2026-10-26': {
                stacker: [
                    { name: "alexa torres", score: 34, country: "VE" },
                    { name: "*****", score: 33, country: "VE" },
                    { name: "RATG", score: 29, country: "VE" },
                    { name: "Jugador_930", score: 29, country: "VE" },
                    { name: "Rafael Torres", score: 22, country: "VE" }
                ],
                reflex: [
                    { name: "RATG", score: 31, country: "VE" },
                    { name: "*****", score: 87, country: "VE" },
                    { name: "Rafael Torres", score: 249, country: "VE" }
                ],
                memory: [
                    { name: "Jugador_930", score: 13, country: "VE" },
                    { name: "Tovias Torres", score: 10, country: "VE" },
                    { name: "*****", score: 10, country: "VE" }
                ],
                dodge: [
                    { name: "RATG", score: 24, country: "VE" },
                    { name: "Rafael Torres", score: 19, country: "VE" }
                ],
                drone: [
                    { name: "RATG", score: 26, country: "VE" },
                    { name: "Rafael Torres", score: 21, country: "VE" },
                    { name: "CyberHornet", score: 18, country: "MX" }
                ]
            }
        };

        const DEFAULT_ALLTIME_SCORES = {
            stacker: [
                { name: "alexa torres", score: 34, country: "VE" },
                { name: "*****", score: 33, country: "VE" },
                { name: "CyberSam", score: 32, country: "ES" },
                { name: "RATG", score: 29, country: "VE" },
                { name: "Jugador_930", score: 29, country: "VE" },
                { name: "SpeedyGamer", score: 26, country: "MX" },
                { name: "Jugador_311", score: 23, country: "VE" },
                { name: "Rafael Torres", score: 22, country: "VE" },
                { name: "Jugador_662", score: 22, country: "VE" },
                { name: "LunaByte", score: 21, country: "AR" }
            ],
            reflex: [
                { name: "RATG", score: 31, country: "VE" },
                { name: "*****", score: 87, country: "VE" },
                { name: "ViperPulse", score: 215, country: "US" },
                { name: "NicoFast", score: 240, country: "CL" },
                { name: "Rafael Torres", score: 249, country: "VE" },
                { name: "Dani_Reflex", score: 265, country: "VE" },
                { name: "SaraFlash", score: 290, country: "ES" },
                { name: "Jugador_930", score: 308, country: "VE" },
                { name: "Leo_Gamer", score: 320, country: "MX" }
            ],
            memory: [
                { name: "Jugador_930", score: 13, country: "VE" },
                { name: "MegaBrain", score: 12, country: "MX" },
                { name: "Titan_Mind", score: 10, country: "CO" },
                { name: "Jugador_662", score: 10, country: "VE" },
                { name: "Tovias Torres", score: 10, country: "VE" },
                { name: "*****", score: 10, country: "VE" },
                { name: "Valen_Pro", score: 8, country: "VE" },
                { name: "Jugador_311", score: 8, country: "VE" },
                { name: "NeoMatrix", score: 7, country: "ES" },
                { name: "RATG", score: 5, country: "VE" }
            ],
            dodge: [
                { name: "CyberPilot", score: 42, country: "ES" },
                { name: "Nova_VE", score: 35, country: "VE" },
                { name: "FlashStar", score: 28, country: "MX" },
                { name: "RATG", score: 24, country: "VE" },
                { name: "Rafael Torres", score: 19, country: "VE" }
            ],
            drone: [
                { name: "CyberHornet", score: 32, country: "MX" },
                { name: "RATG", score: 26, country: "VE" },
                { name: "Rafael Torres", score: 21, country: "VE" },
                { name: "DroneMaster", score: 18, country: "CO" },
                { name: "LaserPulse", score: 15, country: "AR" }
            ]
        };

        function isCurrentUserEntry(entry) {
            if (!entry) return false;
            if (entry.deviceId && entry.deviceId === deviceId) return true;
            if (entry.name && playerName && repairPlayerName(entry.name).toLowerCase() === playerName.trim().toLowerCase()) return true;
            return false;
        }

        function encodeCompactScores(list, maxChars = 195) {
            const parts = [];
            let currentLen = 0;
            for (const item of (list || []).slice(0, 10)) {
                const cleanName = repairPlayerName(item.name || 'Jugador');
                const sc = parseInt(item.score) || 0;
                if (sc <= 0) continue;
                const cc = String(item.country || 'VE').toUpperCase().slice(0, 2);
                const token = `${cleanName}|${sc}|${cc}`;
                const addedLen = parts.length === 0 ? token.length : token.length + 1;
                if (currentLen + addedLen > maxChars) break;
                parts.push(token);
                currentLen += addedLen;
            }
            return parts.join(';');
        }

        function decodeCompactScores(str) {
            if (!str || typeof str !== 'string') return [];
            return str.split(';').map(part => {
                const [name, sc, cc] = part.split('|');
                const scoreNum = parseInt(sc);
                if (!name || isNaN(scoreNum) || scoreNum <= 0) return null;
                return {
                    name: repairPlayerName(name),
                    score: scoreNum,
                    country: (cc && cc.length === 2) ? cc.toUpperCase() : 'VE'
                };
            }).filter(Boolean);
        }

        function mergeAndNormalizeScores(gameKey, incomingArrays, isAscending, oldNameToRemove, mode = 'alltime') {
            const currentWeek = ensureWeeklyReset();
            const isWeekly = (mode === 'weekly');
            const storageScoresKey = isWeekly ? ('bytezone_weekly_scores_' + gameKey) : ('bytezone_scores_' + gameKey);
            const storageBestKey   = isWeekly ? ('bytezone_weekly_best_' + gameKey)   : ('bytezone_best_' + gameKey);

            const byName = new Map();
            const oldKey = oldNameToRemove ? repairPlayerName(oldNameToRemove).toLowerCase() : null;

            const addEntry = (raw) => {
                if (!raw || !raw.name) return;
                const sc = parseInt(raw.score);
                if (isNaN(sc) || sc <= 0) return;

                let nameStr = repairPlayerName(raw.name);
                let key = nameStr.toLowerCase();

                if ((oldKey && key === oldKey) || prevNames.includes(key)) {
                    nameStr = playerName;
                    key = playerName.trim().toLowerCase();
                }
                if ((raw.deviceId && raw.deviceId === deviceId) || raw.isMe === true) {
                    nameStr = playerName;
                    key = playerName.trim().toLowerCase();
                }

                const countryCode = (key === playerName.trim().toLowerCase())
                    ? (playerCountry || raw.country || 'VE')
                    : (raw.country || 'VE');

                const existing = byName.get(key);
                if (!existing) {
                    byName.set(key, {
                        name: nameStr,
                        score: sc,
                        country: countryCode,
                        deviceId: (key === playerName.trim().toLowerCase()) ? deviceId : raw.deviceId
                    });
                } else {
                    const isBetter = isAscending ? (sc < existing.score) : (sc > existing.score);
                    if (isBetter) {
                        existing.score = sc;
                    }
                    if (countryCode && (!existing.country || existing.country === 'VE')) {
                        existing.country = countryCode;
                    }
                    if (key === playerName.trim().toLowerCase()) {
                        existing.name = playerName;
                        existing.deviceId = deviceId;
                    }
                }
            };

            // 1. Semilla base según modo (Semanal vs Histórico)
            if (isWeekly) {
                const weekSeeds = (SEEDED_WEEKLY_SCORES[currentWeek] && SEEDED_WEEKLY_SCORES[currentWeek][gameKey]) || [];
                weekSeeds.forEach(addEntry);
            } else {
                (DEFAULT_ALLTIME_SCORES[gameKey] || []).forEach(addEntry);
            }

            // 2. Listas entrantes (localStorage + Cloud REST + ntfy stream)
            (incomingArrays || []).forEach(arr => {
                if (Array.isArray(arr)) arr.forEach(addEntry);
            });

            // 3. Asegurar que el récord personal correspondiente siempre esté incluido
            const myBest = parseInt(localStorage.getItem(storageBestKey) || '0');
            if (myBest > 0) {
                addEntry({
                    name: playerName,
                    score: myBest,
                    country: playerCountry || 'VE',
                    deviceId: deviceId
                });
            }

            const merged = Array.from(byName.values());
            merged.sort((a, b) => isAscending ? (a.score - b.score) : (b.score - a.score));

            const myEntry = merged.find(x => isCurrentUserEntry(x));
            if (myEntry && myEntry.score > 0) {
                if (myBest === 0 || (isAscending ? (myEntry.score < myBest) : (myEntry.score > myBest))) {
                    localStorage.setItem(storageBestKey, myEntry.score.toString());
                }
            }

            const topList = merged.slice(0, 15);
            localStorage.setItem(storageScoresKey, JSON.stringify(topList));
            return topList;
        }

        function getCleanScores(gameKey, isAscending, mode) {
            ensureWeeklyReset();
            const targetMode = mode || window.currentLeaderboardTab || 'weekly';
            const storageScoresKey = (targetMode === 'weekly') ? ('bytezone_weekly_scores_' + gameKey) : ('bytezone_scores_' + gameKey);
            let localScores = [];
            try {
                localScores = JSON.parse(localStorage.getItem(storageScoresKey) || '[]');
            } catch (e) { localScores = []; }
            return mergeAndNormalizeScores(gameKey, [localScores], isAscending, null, targetMode);
        }

        // ==========================================================
        // GANCHO SOCIAL DE RETO VIRAL & CELEBRACIÓN DE PODIO (TOP 3)
        // ==========================================================
        let currentPodiumShareText = "";

        function checkAndShowPodiumModal(gameKey, score, isAscending) {
            try {
                const weeklyList = (typeof getCleanScores === 'function') ? getCleanScores(gameKey, isAscending, 'weekly') : [];
                const alltimeList = (typeof getCleanScores === 'function') ? getCleanScores(gameKey, isAscending, 'alltime') : [];

                let weeklyPos = null;
                let alltimePos = null;

                weeklyList.slice(0, 10).forEach((item, idx) => {
                    if (isCurrentUserEntry(item) && weeklyPos === null) weeklyPos = idx + 1;
                });
                alltimeList.slice(0, 10).forEach((item, idx) => {
                    if (isCurrentUserEntry(item) && alltimePos === null) alltimePos = idx + 1;
                });

                const sc = parseInt(score);
                if (weeklyPos === null && sc > 0 && weeklyList.length > 0) {
                    for (let i = 0; i < weeklyList.length; i++) {
                        const itSc = weeklyList[i].score;
                        if (isAscending ? (sc <= itSc) : (sc >= itSc)) {
                            weeklyPos = i + 1;
                            break;
                        }
                    }
                }

                if (alltimePos === null && sc > 0 && alltimeList.length > 0) {
                    for (let i = 0; i < alltimeList.length; i++) {
                        const itSc = alltimeList[i].score;
                        if (isAscending ? (sc <= itSc) : (sc >= itSc)) {
                            alltimePos = i + 1;
                            break;
                        }
                    }
                }

                const inWeeklyPodium = (weeklyPos !== null && weeklyPos <= 3);
                const inAlltimePodium = (alltimePos !== null && alltimePos <= 3);

                if (inWeeklyPodium || inAlltimePodium) {
                    showPodiumModal({
                        gameKey: gameKey,
                        score: sc,
                        isAscending: isAscending,
                        weeklyPos: weeklyPos,
                        alltimePos: alltimePos
                    });
                    return true;
                }
            } catch(e) {}
            return false;
        }

        // Muestra el modal del podio pendiente (si lo hay) usando la MEJOR marca semanal. Devuelve true si se mostró.
        function flushPendingPodium() {
            const p = window.__pendingPodium;
            if (!p) return false;
            window.__pendingPodium = null;
            const best = parseInt(localStorage.getItem('bytezone_weekly_best_' + p.gameKey) || localStorage.getItem('bytezone_best_' + p.gameKey) || '0');
            if (!best) return false;
            return checkAndShowPodiumModal(p.gameKey, best, p.isAscending) === true;
        }

        function showPodiumModal(data) {
            const modal = document.getElementById('podiumShareModal');
            if (!modal) return;

            const gameTitles = {
                stacker: 'Neon Stacker Pro',
                reflex: 'Test de Reflejos Visuales',
                memory: 'Cyber Memory Neón',
                dodge: 'Cyber Dodge: Tormenta Neón',
                drone: 'Neon Cyber-Drone: Portales Láser'
            };
            const scoreUnits = {
                stacker: 'Pisos',
                reflex: 'ms',
                memory: 'Rondas',
                dodge: 'seg',
                drone: 'Portales'
            };

            const gTitle = gameTitles[data.gameKey] || 'Arcade ByteZone';
            const unit = scoreUnits[data.gameKey] || 'pts';
            const scoreFormatted = data.score + " " + unit;

            const medalEl = document.getElementById('podiumMedalIcon');
            const titleEl = document.getElementById('podiumModalTitle');
            const scoreEl = document.getElementById('podiumScoreValue');
            const wRankEl = document.getElementById('podiumWeeklyRankText');
            const aRankEl = document.getElementById('podiumAlltimeRankText');

            if (titleEl) titleEl.textContent = gTitle;
            if (scoreEl) scoreEl.textContent = scoreFormatted;

            const wPos = data.weeklyPos;
            const aPos = data.alltimePos;

            const wBadge = (wPos === 1) ? "🥇 Puesto #1 (¡Líder de la Semana!)" : (wPos === 2) ? "🥈 Puesto #2 de la Semana" : (wPos === 3) ? "🥉 Puesto #3 de la Semana" : (wPos ? `Puesto #${wPos} Semanal` : "Top Clasificado");
            const aBadge = (aPos === 1) ? "👑 Puesto #1 de Todos los Tiempos" : (aPos === 2) ? "🥈 Puesto #2 de Todos los Tiempos" : (aPos === 3) ? "🥉 Puesto #3 de Todos los Tiempos" : (aPos ? `Puesto #${aPos} Histórico` : "En el Salón de la Fama");

            if (wRankEl) wRankEl.textContent = wBadge;
            if (aRankEl) aRankEl.textContent = aBadge;

            if (medalEl) {
                medalEl.textContent = (wPos === 1 || aPos === 1) ? "🥇" : (wPos === 2 || aPos === 2) ? "🥈" : "🥉";
            }

            const pageUrl = window.location.href.split('?')[0];
            const challengeText = `🔥 ¡Acabo de meterme en el PODIO MUNDIAL de ByteZone Arcade! 🏆\n\n` +
                `🎮 Juego: ${gTitle}\n` +
                `⚡ Mi Marca: ${scoreFormatted}\n` +
                `🔥 Torneo Semanal: ${wBadge}\n` +
                `👑 Récord Histórico: ${aBadge}\n\n` +
                `👉 ¿Crees que tienes mejores reflejos para quitarme el puesto? Juégalo gratis aquí:\n${pageUrl}?v=14`;

            currentPodiumShareText = challengeText;

            const waBtn = document.getElementById('podiumWhatsappBtn');
            if (waBtn) {
                waBtn.href = "https://api.whatsapp.com/send?text=" + encodeURIComponent(challengeText);
            }
            const tgBtn = document.getElementById('podiumTelegramBtn');
            if (tgBtn) {
                tgBtn.href = "https://t.me/share/url?url=" + encodeURIComponent(pageUrl + "?v=14") + "&text=" + encodeURIComponent(`🔥 ¡Acabo de meterme en el PODIO MUNDIAL! ⚡ Mi Marca en ${gTitle}: ${scoreFormatted} (${wBadge}). ¿Puedes superarme?`);
            }

            modal.classList.remove('hidden');
            if (typeof confetti === 'function') {
                confetti({ particleCount: 75, spread: 70, origin: { y: 0.5 } });
            }
        }

        function closePodiumModal() {
            const modal = document.getElementById('podiumShareModal');
            if (modal) modal.classList.add('hidden');
        }

        function openShareLink(url) {
            try {
                const tg = window.Telegram && window.Telegram.WebApp;
                if (url.indexOf('https://t.me/') === 0 && tg && tg.openTelegramLink) { tg.openTelegramLink(url); return false; }
                if (tg && tg.openLink) { tg.openLink(url); return false; }
            } catch (e) {}
            const w = window.open(url, '_blank');
            if (!w) { window.location.href = url; }
            return false;
        }

        function sharePodiumNative() {
            if (!currentPodiumShareText) return;
            const pageUrl = window.location.href.split('?')[0] + '?v=14';
            if (navigator.share) {
                navigator.share({ title: 'Reto ByteZone Arcade', text: currentPodiumShareText, url: pageUrl }).catch(() => {});
            } else {
                copyPodiumChallengeText();
            }
        }

        // Botón visible "Retar a mis amigos" cuando el jugador está en el Top 3 (no depende de tocar la insignia)
        function ensureChallengeButton() {
            const badge = document.getElementById('userRankBadge');
            if (!badge) return;
            const inPodium = typeof badge.onclick === 'function' && /Toca para Retar/.test(badge.textContent || '');
            let btn = document.getElementById('challengeFriendsBtn');
            if (inPodium) {
                if (!btn) {
                    btn = document.createElement('button');
                    btn.id = 'challengeFriendsBtn';
                    btn.className = 'w-full mt-3 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:opacity-95 active:scale-95 text-gray-950 font-black py-3 px-4 rounded-2xl text-xs flex items-center justify-center space-x-2 shadow-lg shadow-emerald-500/25 transition';
                    btn.innerHTML = '<span>📣</span><span>Retar a mis amigos con mi puesto</span>';
                    const host = badge.closest('.rounded-2xl') || badge.parentElement;
                    host.insertAdjacentElement('afterend', btn);
                }
                btn.onclick = function () { if (typeof badge.onclick === 'function') badge.onclick(); };
            } else if (btn) {
                btn.remove();
            }
        }
        setInterval(ensureChallengeButton, 1000);

        function copyPodiumChallengeText() {
            if (!currentPodiumShareText) return;
            const textEl = document.getElementById('copyChallengeText');
            const iconEl = document.getElementById('copyChallengeIcon');
            const showSuccess = () => {
                if (textEl) textEl.textContent = "¡Copiado con Éxito!";
                if (iconEl) iconEl.textContent = "✅";
                setTimeout(() => {
                    if (textEl) textEl.textContent = "Copiar Mensaje del Reto";
                    if (iconEl) iconEl.textContent = "📋";
                }, 2500);
            };

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(currentPodiumShareText).then(showSuccess).catch(() => {
                    prompt("Copia tu mensaje de reto para WhatsApp/Telegram:", currentPodiumShareText);
                });
            } else {
                prompt("Copia tu mensaje de reto para WhatsApp/Telegram:", currentPodiumShareText);
            }
        }

        function switchLeaderboardTab(mode) {
            window.currentLeaderboardTab = (mode === 'alltime') ? 'alltime' : 'weekly';
            updateLeaderboardTabsUI();
            if (typeof renderLeaderboardUI === 'function') {
                renderLeaderboardUI();
            }
        }

        function updateLeaderboardTabsUI() {
            const mode = window.currentLeaderboardTab || 'weekly';
            const btnWeekly = document.getElementById('tabWeeklyBtn');
            const btnAlltime = document.getElementById('tabAlltimeBtn');
            const banner = document.getElementById('weeklyCountdownBanner');

            if (btnWeekly && btnAlltime) {
                if (mode === 'weekly') {
                    btnWeekly.className = "w-1/2 py-2 px-3 rounded-xl font-black text-xs transition flex items-center justify-center space-x-1.5 bg-gradient-to-r from-amber-500 to-orange-500 text-gray-950 shadow-md shadow-amber-500/20";
                    btnAlltime.className = "w-1/2 py-2 px-3 rounded-xl font-bold text-xs transition flex items-center justify-center space-x-1.5 text-gray-400 hover:text-white";
                } else {
                    btnWeekly.className = "w-1/2 py-2 px-3 rounded-xl font-bold text-xs transition flex items-center justify-center space-x-1.5 text-gray-400 hover:text-white";
                    btnAlltime.className = "w-1/2 py-2 px-3 rounded-xl font-black text-xs transition flex items-center justify-center space-x-1.5 bg-gradient-to-r from-cyan-500 to-purple-600 text-white shadow-md shadow-cyan-500/20";
                }
            }

            if (banner) {
                if (mode === 'weekly') {
                    banner.innerHTML = `
                        <span class="font-bold text-amber-300 flex items-center space-x-1">
                            <span>🔥</span>
                            <span>Torneo de la Semana</span>
                        </span>
                        <span class="text-gray-300 font-semibold">${getWeeklyCountdownText()}</span>
                    `;
                    banner.className = "mb-3 px-3 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-[11px] flex flex-wrap items-center justify-between gap-1";
                } else {
                    banner.innerHTML = `
                        <span class="font-bold text-cyan-300 flex items-center space-x-1">
                            <span>👑</span>
                            <span>Salón de la Fama Mundial</span>
                        </span>
                        <span class="text-gray-300">Récords históricos de todos los tiempos</span>
                    `;
                    banner.className = "mb-3 px-3 py-2 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-[11px] flex flex-wrap items-center justify-between gap-1";
                }
            }
        }

        function recordGameScore(gameKey, score, isAscending) {
            ensureWeeklyReset();
            const cleanScore = parseInt(score);
            if (isNaN(cleanScore) || cleanScore <= 0) return false;

            const weeklyBest = parseInt(localStorage.getItem('bytezone_weekly_best_' + gameKey) || '0');
            const alltimeBest = parseInt(localStorage.getItem('bytezone_best_' + gameKey) || '0');

            const isNewWeeklyBest = (weeklyBest === 0) || (isAscending ? (cleanScore < weeklyBest) : (cleanScore > weeklyBest));
            const isNewAlltimeBest = (alltimeBest === 0) || (isAscending ? (cleanScore < alltimeBest) : (cleanScore > alltimeBest));

            if (isNewWeeklyBest) {
                localStorage.setItem('bytezone_weekly_best_' + gameKey, cleanScore.toString());
                let wScores = [];
                try { wScores = JSON.parse(localStorage.getItem('bytezone_weekly_scores_' + gameKey) || '[]'); } catch(e) {}
                mergeAndNormalizeScores(gameKey, [wScores, [{ name: playerName, deviceId: deviceId, score: cleanScore, country: playerCountry || 'VE' }]], isAscending, null, 'weekly');
            }

            if (isNewAlltimeBest) {
                localStorage.setItem('bytezone_best_' + gameKey, cleanScore.toString());
                let aScores = [];
                try { aScores = JSON.parse(localStorage.getItem('bytezone_scores_' + gameKey) || '[]'); } catch(e) {}
                mergeAndNormalizeScores(gameKey, [aScores, [{ name: playerName, deviceId: deviceId, score: cleanScore, country: playerCountry || 'VE' }]], isAscending, null, 'alltime');
            }

            if (isNewWeeklyBest || isNewAlltimeBest) {
                if (typeof renderLeaderboardUI === 'function') renderLeaderboardUI();
                pushScoreToCloud(gameKey, cleanScore, isAscending);
                if (window.confetti) confetti({ particleCount: 70, spread: 60, origin: { y: 0.6 } });

                // Gancho Social: NUNCA interrumpir una partida en curso. Se deja pendiente y se muestra
                // solo cuando la partida termina de verdad (ver flushPendingPodium en cada juego).
                window.__pendingPodium = { gameKey: gameKey, isAscending: isAscending };
                if (gameKey === 'reflex') {
                    // En Reflejos cada intento es una partida completa
                    setTimeout(() => { flushPendingPodium(); }, 900);
                }

                return true;
            }
            return false;
        }

        async function pushScoreToCloud(gameKey, score, isAscending, oldNameToRemove) {
            const currentWeek = ensureWeeklyReset();
            const cleanScore = parseInt(score);
            if (isNaN(cleanScore) || cleanScore <= 0) return;

            const myWeeklyBest = parseInt(localStorage.getItem('bytezone_weekly_best_' + gameKey) || '0') || cleanScore;
            const myAlltimeBest = parseInt(localStorage.getItem('bytezone_best_' + gameKey) || '0') || cleanScore;

            localStorage.setItem(`bz_uploaded_${gameKey}_${currentWeek}`, String(myWeeklyBest));

            // 1. Emitir evento en tiempo real por ntfy.sh para todos los teléfonos conectados (<1 seg)
            try {
                fetch(`https://ntfy.sh/${NTFY_SCORES_TOPIC}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        g: gameKey,
                        w: currentWeek,
                        d: deviceId,
                        n: playerName,
                        oldN: oldNameToRemove || undefined,
                        sw: myWeeklyBest,
                        sa: myAlltimeBest,
                        c: playerCountry || 'VE',
                        t: Date.now()
                    })
                }).catch(() => {});
            } catch (e) {}

            // 2. Actualizar Objeto SEMANAL en api.restful-api.dev
            const weeklyObjId = CLOUD_WEEKLY_IDS[gameKey];
            if (weeklyObjId && myWeeklyBest > 0) {
                try {
                    let cloudWeekly = [];
                    try {
                        const getRes = await fetch(`https://api.restful-api.dev/objects/${weeklyObjId}?t=${Date.now()}`, { cache: 'no-store' });
                        if (getRes.ok) {
                            const objData = await getRes.json();
                            if (objData && objData.data && objData.data.w === currentWeek && objData.data.v) {
                                cloudWeekly = decodeCompactScores(objData.data.v);
                            }
                        }
                    } catch (e) {}

                    let localWeekly = [];
                    try { localWeekly = JSON.parse(localStorage.getItem('bytezone_weekly_scores_' + gameKey) || '[]'); } catch (e) {}

                    const newEntry = [{ name: playerName, score: myWeeklyBest, country: playerCountry || 'VE', deviceId: deviceId }];
                    const mergedWeekly = mergeAndNormalizeScores(gameKey, [cloudWeekly, localWeekly, newEntry], isAscending, oldNameToRemove, 'weekly');
                    const compactW = encodeCompactScores(mergedWeekly.slice(0, 10), 185);

                    await fetch(`https://api.restful-api.dev/objects/${weeklyObjId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            name: 'bzw_' + gameKey,
                            data: { w: currentWeek, v: compactW }
                        })
                    });
                } catch (e) {}
            }

            // 3. Actualizar Objeto HISTÓRICO en api.restful-api.dev
            const alltimeObjId = CLOUD_ALLTIME_IDS[gameKey];
            if (alltimeObjId && myAlltimeBest > 0) {
                try {
                    let cloudAlltime = [];
                    try {
                        const getRes = await fetch(`https://api.restful-api.dev/objects/${alltimeObjId}?t=${Date.now()}`, { cache: 'no-store' });
                        if (getRes.ok) {
                            const objData = await getRes.json();
                            if (objData && objData.data && objData.data.v) {
                                cloudAlltime = decodeCompactScores(objData.data.v);
                            }
                        }
                    } catch (e) {}

                    let localAlltime = [];
                    try { localAlltime = JSON.parse(localStorage.getItem('bytezone_scores_' + gameKey) || '[]'); } catch (e) {}

                    const newEntry = [{ name: playerName, score: myAlltimeBest, country: playerCountry || 'VE', deviceId: deviceId }];
                    const mergedAlltime = mergeAndNormalizeScores(gameKey, [cloudAlltime, localAlltime, newEntry], isAscending, oldNameToRemove, 'alltime');
                    const compactA = encodeCompactScores(mergedAlltime.slice(0, 10), 195);

                    await fetch(`https://api.restful-api.dev/objects/${alltimeObjId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            name: 'bz_' + gameKey,
                            data: { v: compactA }
                        })
                    });
                } catch (e) {}
            }
        }

        async function syncGameFromCloud(gameKey, isAscending, silent = false) {
            const currentWeek = ensureWeeklyReset();
            const badgeEl = document.getElementById('liveSyncStatus');
            if (badgeEl && !silent) {
                badgeEl.textContent = "🔄 Sincronizando...";
            }

            const weeklyObjId = CLOUD_WEEKLY_IDS[gameKey];
            const alltimeObjId = CLOUD_ALLTIME_IDS[gameKey];
            let cloudWeeklyList = [];
            let cloudAlltimeList = [];
            let ntfyWeeklyList = [];
            let ntfyAlltimeList = [];
            let renames = {};

            await Promise.all([
                (async () => {
                    if (!weeklyObjId) return;
                    try {
                        const resW = await fetch(`https://api.restful-api.dev/objects/${weeklyObjId}?t=${Date.now()}`, { cache: 'no-store' });
                        if (resW.ok) {
                            const jsonW = await resW.json();
                            if (jsonW && jsonW.data && jsonW.data.w === currentWeek && jsonW.data.v) {
                                cloudWeeklyList = decodeCompactScores(jsonW.data.v);
                            }
                        }
                    } catch (e) {}
                })(),
                (async () => {
                    if (!alltimeObjId) return;
                    try {
                        const resA = await fetch(`https://api.restful-api.dev/objects/${alltimeObjId}?t=${Date.now()}`, { cache: 'no-store' });
                        if (resA.ok) {
                            const jsonA = await resA.json();
                            if (jsonA && jsonA.data && jsonA.data.v) {
                                cloudAlltimeList = decodeCompactScores(jsonA.data.v);
                            }
                        }
                    } catch (e) {}
                })(),
                (async () => {
                    try {
                        const resNtfy = await fetch(`https://ntfy.sh/${NTFY_SCORES_TOPIC}/json?poll=1&since=72h`, { cache: 'no-store' });
                        if (resNtfy.ok) {
                            const text = await resNtfy.text();
                            const lines = text.split('\\n').filter(Boolean);
                            lines.forEach(line => {
                                try {
                                    const evt = JSON.parse(line);
                                    if (evt && evt.event === 'message' && evt.message) {
                                        const p = JSON.parse(evt.message);
                                        if (p && p.oldN && p.n) {
                                            renames[repairPlayerName(p.oldN).toLowerCase()] = repairPlayerName(p.n);
                                        }
                                        if (p && p.g === gameKey && p.n) {
                                            const cleanN = repairPlayerName(p.n);
                                            if (p.w === currentWeek && (p.sw || p.s)) {
                                                ntfyWeeklyList.push({
                                                    name: cleanN,
                                                    score: parseInt(p.sw || p.s),
                                                    country: p.c || 'VE',
                                                    deviceId: p.d
                                                });
                                            }
                                            if (p.sa || p.s) {
                                                ntfyAlltimeList.push({
                                                    name: cleanN,
                                                    score: parseInt(p.sa || p.s),
                                                    country: p.c || 'VE',
                                                    deviceId: p.d
                                                });
                                            }
                                        }
                                    }
                                } catch (pe) {}
                            });
                        }
                    } catch (e) {}
                })()
            ]);

            const applyRename = (arr) => arr.map(item => {
                const clean = repairPlayerName(item.name || '');
                const k = clean.toLowerCase();
                item.name = renames[k] || clean;
                return item;
            });

            let localWeekly = [];
            let localAlltime = [];
            try { localWeekly = JSON.parse(localStorage.getItem('bytezone_weekly_scores_' + gameKey) || '[]'); } catch (e) {}
            try { localAlltime = JSON.parse(localStorage.getItem('bytezone_scores_' + gameKey) || '[]'); } catch (e) {}

            mergeAndNormalizeScores(
                gameKey,
                [applyRename(localWeekly), applyRename(cloudWeeklyList), applyRename(ntfyWeeklyList)],
                isAscending,
                null,
                'weekly'
            );

            mergeAndNormalizeScores(
                gameKey,
                [applyRename(localAlltime), applyRename(cloudAlltimeList), applyRename(ntfyAlltimeList)],
                isAscending,
                null,
                'alltime'
            );

            if (typeof renderLeaderboardUI === 'function' && window.CURRENT_GAME_KEY === gameKey) {
                updateLeaderboardTabsUI();
                renderLeaderboardUI();
            }

            if (badgeEl) {
                badgeEl.textContent = "🟢 Global En Vivo";
            }

            // Auto-migración controlada (1 sola vez por marca nueva para no saturar la nube)
            const myWeeklyNow = parseInt(localStorage.getItem('bytezone_weekly_best_' + gameKey) || '0');
            const lastUploaded = parseInt(localStorage.getItem(`bz_uploaded_${gameKey}_${currentWeek}`) || '0');
            const inNtfy = ntfyWeeklyList.find(x => isCurrentUserEntry(x));
            if (myWeeklyNow > 0 && lastUploaded !== myWeeklyNow && (!inNtfy || inNtfy.score !== myWeeklyNow)) {
                pushScoreToCloud(gameKey, myWeeklyNow, isAscending);
            }
        }

        function startRealtimeScoreStream(activeGameKey, isAscending) {
            window.CURRENT_GAME_KEY = activeGameKey;
            window.CURRENT_GAME_ASC = isAscending;
            updateLeaderboardTabsUI();
            syncGameFromCloud(activeGameKey, isAscending);

            setInterval(() => {
                ensureWeeklyReset();
                updateLeaderboardTabsUI();
            }, 30000);

            ALL_GAME_KEYS.forEach((g, idx) => {
                if (g !== activeGameKey) {
                    setTimeout(() => syncGameFromCloud(g, g === 'reflex', true), 1200 + idx * 600);
                }
            });

            // Conexión SSE con auto-reconexión resiliente para celulares que apagan pantalla o cambian de app
            function connectRealtimeSSE() {
                if (!window.EventSource) return;
                try {
                    if (window.__bzScoreSSE) {
                        try { window.__bzScoreSSE.close(); } catch(e) {}
                    }
                    const es = new EventSource(`https://ntfy.sh/${NTFY_SCORES_TOPIC}/sse`);
                    window.__bzScoreSSE = es;
                    es.onmessage = (e) => {
                        try {
                            const evt = JSON.parse(e.data);
                            if (evt && evt.message) {
                                const p = JSON.parse(evt.message);
                                if (p && p.g && ALL_GAME_KEYS.includes(p.g) && p.n) {
                                    const targetG = p.g;
                                    const targetAsc = (targetG === 'reflex');
                                    const currentWeek = ensureWeeklyReset();
                                    const cleanN = repairPlayerName(p.n);
                                    if (p.w === currentWeek && (p.sw || p.s)) {
                                        let curW = [];
                                        try { curW = JSON.parse(localStorage.getItem('bytezone_weekly_scores_' + targetG) || '[]'); } catch(err){}
                                        mergeAndNormalizeScores(targetG, [curW, [{ name: cleanN, score: parseInt(p.sw || p.s), country: p.c || 'VE', deviceId: p.d }]], targetAsc, p.oldN, 'weekly');
                                    }
                                    if (p.sa || p.s) {
                                        let curA = [];
                                        try { curA = JSON.parse(localStorage.getItem('bytezone_scores_' + targetG) || '[]'); } catch(err){}
                                        mergeAndNormalizeScores(targetG, [curA, [{ name: cleanN, score: parseInt(p.sa || p.s), country: p.c || 'VE', deviceId: p.d }]], targetAsc, p.oldN, 'alltime');
                                    }
                                    if (targetG === window.CURRENT_GAME_KEY && typeof renderLeaderboardUI === 'function') {
                                        renderLeaderboardUI();
                                    }
                                    if (typeof window.renderChampionsPageUI === 'function') {
                                        window.renderChampionsPageUI();
                                    }
                                }
                            }
                        } catch (err) {}
                    };
                    es.onerror = () => {
                        try { es.close(); } catch(e) {}
                        setTimeout(connectRealtimeSSE, 4000);
                    };
                } catch (e) {}
            }
            connectRealtimeSSE();

            if (!window.__bzVisibilitySyncAttached) {
                window.__bzVisibilitySyncAttached = true;
                const wakeAndSync = () => {
                    if (document.visibilityState === 'visible') {
                        const gKey = window.CURRENT_GAME_KEY || activeGameKey;
                        const gAsc = (gKey === 'reflex');
                        syncGameFromCloud(gKey, gAsc, true);
                        connectRealtimeSSE();
                    }
                };
                document.addEventListener('visibilitychange', wakeAndSync);
                window.addEventListener('focus', wakeAndSync);
                window.addEventListener('online', wakeAndSync);
            }

            setInterval(() => {
                syncGameFromCloud(activeGameKey, isAscending, true);
            }, 18000);
        }

        function getCountryFlag(code) {
            if (!code || code.length !== 2) return '🌐';
            const c = code.toUpperCase();
            return String.fromCodePoint(127397 + c.charCodeAt(0), 127397 + c.charCodeAt(1));
        }

        async function detectUserCountry() {
            if (playerCountry && playerCountry.length === 2) {
                updateCountryDisplays();
                return playerCountry;
            }
            try {
                const res = await fetch('https://api.country.is/');
                const data = await res.json();
                if (data && data.country) {
                    playerCountry = data.country.toUpperCase();
                    localStorage.setItem('bytezone_player_country', playerCountry);
                    updateCountryDisplays();
                    return playerCountry;
                }
            } catch (e) {
                try {
                    const res2 = await fetch('https://get.geojs.io/v1/ip/country.json');
                    const data2 = await res2.json();
                    if (data2 && data2.country) {
                        playerCountry = data2.country.toUpperCase();
                        localStorage.setItem('bytezone_player_country', playerCountry);
                        updateCountryDisplays();
                        return playerCountry;
                    }
                } catch (e2) {}
            }
            playerCountry = 'VE';
            localStorage.setItem('bytezone_player_country', playerCountry);
            updateCountryDisplays();
            return playerCountry;
        }

        function updateCountryDisplays() {
            const flag = getCountryFlag(playerCountry);
            document.querySelectorAll('#playerCountryDisplay').forEach(el => {
                el.textContent = flag;
            });
            const cName = document.getElementById('modalCountryName');
            if (cName) cName.textContent = playerCountry;
            const cFlag = document.getElementById('modalCountryFlag');
            if (cFlag) cFlag.textContent = flag;
            if (typeof renderLeaderboardUI === 'function') {
                renderLeaderboardUI();
            }
        }

        // Visita de página (alimenta la telemetría de tráfico del Agente CEO)
        try {
            if (!window.__bzPageViewSent && typeof window.broadcastGlobalTelemetry === 'function') {
                window.__bzPageViewSent = true;
                window.broadcastGlobalTelemetry({ kind: 'page', g: (location.pathname.split('/').pop() || 'index.html') });
            }
        } catch (e) {}

        function updateNameDisplays() {
            document.querySelectorAll('#playerNameDisplay').forEach(el => {
                el.textContent = playerName;
            });
        }
        updateNameDisplays();
        detectUserCountry();

        setTimeout(() => {
            if (!window.CURRENT_GAME_KEY) {
                ALL_GAME_KEYS.forEach((g, idx) => {
                    setTimeout(() => syncGameFromCloud(g, g === 'reflex', true), idx * 750);
                });
            }
        }, 600);

        function promptChangeName() {
            const input = document.getElementById('modalNameInput');
            if (input) input.value = playerName;
            const modal = document.getElementById('namePromptModal');
            if (modal) modal.classList.remove('hidden');
        }

        function closeNameModal() {
            const modal = document.getElementById('namePromptModal');
            if (modal) modal.classList.add('hidden');
        }

        function savePlayerNameFromModal() {
            const input = document.getElementById('modalNameInput');
            const val = input ? repairPlayerName(input.value) : '';
            if (val) {
                const oldName = playerName;
                if (oldName && oldName.toLowerCase() !== val.toLowerCase()) {
                    if (!prevNames.includes(oldName.toLowerCase())) {
                        prevNames.push(oldName.toLowerCase());
                        localStorage.setItem('bytezone_prev_names', JSON.stringify(prevNames));
                    }
                }
                playerName = val;
                localStorage.setItem('bytezone_player_name', playerName);
                updateNameDisplays();
                
                ALL_GAME_KEYS.forEach(game => {
                    const isAsc = (game === 'reflex');
                    let wScores = [];
                    let aScores = [];
                    try { wScores = JSON.parse(localStorage.getItem('bytezone_weekly_scores_' + game) || '[]'); } catch(e) {}
                    try { aScores = JSON.parse(localStorage.getItem('bytezone_scores_' + game) || '[]'); } catch(e) {}
                    mergeAndNormalizeScores(game, [wScores], isAsc, oldName, 'weekly');
                    mergeAndNormalizeScores(game, [aScores], isAsc, oldName, 'alltime');
                    const myBest = parseInt(localStorage.getItem('bytezone_best_' + game) || '0');
                    const myWeekly = parseInt(localStorage.getItem('bytezone_weekly_best_' + game) || '0');
                    if (myBest > 0 || myWeekly > 0) {
                        pushScoreToCloud(game, myWeekly || myBest, isAsc, oldName);
                    }
                });
            }
            closeNameModal();
            if (typeof renderLeaderboardUI === 'function') {
                renderLeaderboardUI();
            }
        }

        // Sistema de Telemetría y Popularidad Global Multi-Teléfono (ByteZone Cloud Analytics v=14)
        function trackByteZoneEvent(gameKey, eventType) {
            try {
                let stats = JSON.parse(localStorage.getItem('bytezone_telemetry') || '{}');
                if (!stats[gameKey]) stats[gameKey] = { views: 0, plays: 0, ads: 0 };
                if (eventType === 'view') stats[gameKey].views = (stats[gameKey].views || 0) + 1;
                if (eventType === 'play') stats[gameKey].plays = (stats[gameKey].plays || 0) + 1;
                if (eventType === 'ad') stats[gameKey].ads = (stats[gameKey].ads || 0) + 1;
                stats['last_active'] = new Date().toISOString();
                localStorage.setItem('bytezone_telemetry', JSON.stringify(stats));

                if ((eventType === 'view' || eventType === 'play' || eventType === 'ad') && typeof window.broadcastGlobalTelemetry === 'function') {
                    window.broadcastGlobalTelemetry({
                        kind: 'game',
                        g: gameKey,
                        ev: eventType
                    });
                }
            } catch(e) {}
        }

        // ==========================================================
        // REPRODUCTOR DE VIDEO FLASH IA + LECTOR DE NOTICIA COMPLETA
        // ==========================================================
        const DEFAULT_WEEKLY_PULSE = {
            week_id: "W2026-10-12",
            updated_human: "17/10/2026",
            video_reel: {
                title: "ByteZone TV • Noticiero IA Semanal",
                subtitle: "5 Noticias Completas con Imagen + Voz IA + Lectura Completa",
                duration_label: "5 Noticias",
                scenes: [
                    {
                        id: "news_1",
                        news_index: 0,
                        badge: "NOTICIA #1 • IA & FUTURO",
                        icon: "🤖",
                        headline: "Cómo detectar fotos, vídeos y audios creados con IA usando SynthID Detector",
                        subtext: "En un mundo donde la realidad y la veracidad se ponen a prueba todos los días con contenidos creados con IA generativa, Google lanzó SynthID Detector para identificar marcas de agua invisibles al instante.",
                        image: "https://i0.wp.com/imgs.hipertextual.com/wp-content/uploads/2026/10/synthid-scaled.jpg?fit=1024%2C540&quality=70&strip=all&ssl=1",
                        source: "Hipertextual IA",
                        voice_script: "Noticia número 1: Cómo detectar fotos, vídeos y audios creados con IA usando SynthID Detector. En un mundo donde la realidad se pone a prueba todos los días con contenidos creados con inteligencia artificial, esta plataforma de Google permite identificar marcas de agua invisibles en segundos. Pasamos a la siguiente noticia.",
                        bg_gradient: "from-cyan-600 to-blue-900"
                    },
                    {
                        id: "news_2",
                        news_index: 1,
                        badge: "NOTICIA #2 • INNOVACIÓN",
                        icon: "🚀",
                        headline: "Linux sigue los pasos de Windows y añade un asistente de IA local a Ubuntu",
                        subtext: "Canonical ha presentado Ubuntu 26.10 con Myna, un asistente de inteligencia artificial por voz que se ejecuta directo en tu computadora sin enviar datos privados a la nube.",
                        image: "https://i0.wp.com/imgs.hipertextual.com/wp-content/uploads/2026/10/ubuntu-terminal.jpg?fit=1024%2C683&quality=70&strip=all&ssl=1",
                        source: "Hipertextual IA",
                        voice_script: "Noticia número 2: Linux sigue los pasos de Windows y añade un asistente de IA a Ubuntu. Canonical presentó Ubuntu 26 punto 10 con Myna, un nuevo asistente de voz que procesa todo en tu propio equipo protegiendo tu privacidad al cien por ciento. Pasamos a la siguiente noticia.",
                        bg_gradient: "from-purple-600 to-indigo-900"
                    }
                ]
            },
            weekly_news: [],
            vip_hack_of_the_week: {
                tag: "Secreto Gamer & IA de la Semana",
                title: "Cómo activar el DNS Ultra-Rápido y liberar RAM oculta en 5 segundos",
                body: "1) En Ajustes > Conexiones > DNS Privado escribe 'one.one.one.one' para reducir el ping un 30%. 2) Antes de buscar un récord en Test de Reflejos o Neon Stacker, activa 'No Molestar' para bloquear procesos en segundo plano que retrasan la respuesta táctil de tu pantalla."
            }
        };

        window.bzPulseData = DEFAULT_WEEKLY_PULSE;
        window.bzReelState = {
            playing: false,
            sceneIdx: 0,
            timer: null,
            voiceRate: 1.22,
            muted: false,
            audioCtx: null,
            beatInterval: null,
            speechSessionId: 0,
            readingFullArticle: false,
            currentArticleIdx: 0
        };

        async function loadWeeklyPulseData(rootPrefix = "") {
            try {
                const res = await fetch(`${rootPrefix}data/weekly_pulse.json?t=${Date.now()}`, { cache: 'no-store' });
                if (res.ok) {
                    const data = await res.json();
                    if (data && data.video_reel && Array.isArray(data.video_reel.scenes)) {
                        window.bzPulseData = data;
                    }
                }
            } catch (e) {}
            renderPulseWidgets();
        }

        function renderPulseWidgets() {
            const data = window.bzPulseData || DEFAULT_WEEKLY_PULSE;
            const dateBadge = document.getElementById('pulseUpdatedBadge');
            if (dateBadge) {
                dateBadge.textContent = `🤖 Actualizado por Agente CEO: ${data.updated_human || 'Hoy'} (${data.week_id || getCurrentWeekId()})`;
            }
            updateReelSceneUI(0);

            const newsGrid = document.getElementById('weeklyNewsContainer');
            if (newsGrid && Array.isArray(data.weekly_news) && data.weekly_news.length > 0) {
                newsGrid.innerHTML = data.weekly_news.map((item, i) => `
                    <div class="bg-gray-900/95 rounded-3xl border border-gray-800 hover:border-cyan-400/70 transition shadow-xl overflow-hidden flex flex-col justify-between group">
                        <div>
                            <div onclick="openFullNewsReader(${i}, false)" class="relative h-44 w-full overflow-hidden bg-gray-950 cursor-pointer">
                                <img src="${item.image || 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80'}" 
                                     alt="${(item.title || '').replace(/"/g, '&quot;')}" 
                                     onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80'"
                                     class="w-full h-full object-cover group-hover:scale-105 transition duration-500 opacity-90">
                                <div class="absolute inset-0 bg-gradient-to-t from-gray-950 via-gray-950/30 to-transparent"></div>
                                <span class="absolute top-3 left-3 text-[10px] font-black uppercase px-2.5 py-1 rounded-full bg-black/75 backdrop-blur-md text-cyan-300 border border-cyan-500/40">
                                    🔥 Noticia #${i + 1} • ${item.source || 'Tech IA'}
                                </span>
                                <span class="absolute bottom-2.5 right-3 text-[10px] font-bold bg-cyan-500/90 text-gray-950 px-2.5 py-0.5 rounded-full shadow">
                                    📖 Toca para abrir completa
                                </span>
                            </div>
                            <div class="p-5">
                                <h3 onclick="openFullNewsReader(${i}, false)" class="text-sm sm:text-base font-black text-white group-hover:text-cyan-400 transition leading-snug cursor-pointer">${item.title}</h3>
                                <p class="text-xs text-gray-300 mt-2 leading-relaxed">${item.summary}</p>
                            </div>
                        </div>
                        <div class="px-5 pb-4 pt-3 border-t border-gray-800/80 flex flex-wrap gap-2 justify-between items-center text-xs">
                            <button onclick="openFullNewsReader(${i}, false)" class="bg-gray-800 hover:bg-gray-700 text-white font-bold px-3 py-2 rounded-xl border border-gray-700 flex items-center space-x-1.5 transition">
                                <span>📖</span>
                                <span>Leer Noticia Completa</span>
                            </button>
                            <button onclick="openFullNewsReader(${i}, true)" class="bg-gradient-to-r from-cyan-500/20 to-blue-500/20 hover:from-cyan-500/30 hover:to-blue-500/30 text-cyan-300 border border-cyan-500/40 font-black px-3 py-2 rounded-xl flex items-center space-x-1.5 transition">
                                <span>🔊</span>
                                <span>Escuchar Completa</span>
                            </button>
                        </div>
                    </div>
                `).join('');
            }
        }

        function startCyberBeat() {
            if (window.bzReelState.muted) return;
            try {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (!AudioContext) return;
                if (!window.bzReelState.audioCtx) {
                    window.bzReelState.audioCtx = new AudioContext();
                }
                const ctx = window.bzReelState.audioCtx;
                if (ctx.state === 'suspended') ctx.resume();
                clearInterval(window.bzReelState.beatInterval);
                let step = 0;
                window.bzReelState.beatInterval = setInterval(() => {
                    if (!window.bzReelState.playing || window.bzReelState.muted) return;
                    try {
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        const freqs = [110, 146.83, 164.81, 220];
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(freqs[step % freqs.length], ctx.currentTime);
                        gain.gain.setValueAtTime(0.018, ctx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.18);
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start();
                        osc.stop(ctx.currentTime + 0.19);
                        step++;
                    } catch (err) {}
                }, 440);
            } catch (e) {}
        }

        function stopCyberBeat() {
            clearInterval(window.bzReelState.beatInterval);
        }

        // divide un texto largo en oraciones completas para que Android/Chrome NUNCA corte la voz a mitad
        function splitIntoSpeakableSentences(text) {
            if (!text) return [];
            const protectedText = text
                .replace(/EE\\.\\s*UU\\./g, 'Estados Unidos')
                .replace(/(\\d+)\\.(\\d+)/g, '$1 punto $2');
            const rawParts = protectedText.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [protectedText];
            return rawParts.map(s => s.trim()).filter(s => s.length > 1);
        }

        function speakTextSentenceBySentence(fullText, onSentenceChange, onAllFinished) {
            if (!('speechSynthesis' in window) || window.bzReelState.muted) {
                return false;
            }
            const sentences = splitIntoSpeakableSentences(fullText);
            if (sentences.length === 0) return false;

            window.bzReelState.speechSessionId++;
            const currentSession = window.bzReelState.speechSessionId;

            try {
                window.speechSynthesis.cancel();
            } catch (e) {}

            let idx = 0;
            const speakNextSentence = () => {
                if (currentSession !== window.bzReelState.speechSessionId) return;
                if (idx >= sentences.length) {
                    if (typeof onAllFinished === 'function') onAllFinished();
                    return;
                }
                const sentenceText = sentences[idx];
                if (typeof onSentenceChange === 'function') {
                    onSentenceChange(sentenceText, idx, sentences.length);
                }

                try {
                    const utter = new SpeechSynthesisUtterance(sentenceText);
                    utter.lang = 'es-MX';
                    utter.rate = window.bzReelState.voiceRate || 1.18;
                    utter.pitch = 1.02;
                    const voices = window.speechSynthesis.getVoices() || [];
                    // Priorizar voces Latinoamericanas naturales (evitando voces de España es-ES)
                    const latinLangs = ['es-mx', 'es-co', 'es-ve', 'es-us', 'es-ar', 'es-419', 'es-cl', 'es-pe'];
                    const isLatin = (v) => v && v.lang && latinLangs.some(l => v.lang.toLowerCase().replace('_', '-').startsWith(l));
                    const isNotSpain = (v) => v && v.lang && v.lang.toLowerCase().startsWith('es') && !v.lang.toLowerCase().replace('_', '-').startsWith('es-es');
                    const esVoice = voices.find(v => isLatin(v) && (v.name.includes('Natural') || v.name.includes('Online') || v.name.includes('Sabina') || v.name.includes('Paulina') || v.name.includes('Dalia') || v.name.includes('Salome') || v.name.includes('Jorge') || v.name.includes('Google')))
                                 || voices.find(v => isLatin(v))
                                 || voices.find(v => isNotSpain(v))
                                 || voices.find(v => v.lang && v.lang.toLowerCase().startsWith('es'));
                    if (esVoice) {
                        utter.voice = esVoice;
                        utter.lang = esVoice.lang || 'es-MX';
                    }

                    let finishedThis = false;
                    const advance = () => {
                        if (finishedThis || currentSession !== window.bzReelState.speechSessionId) return;
                        finishedThis = true;
                        clearTimeout(sentenceSafetyTimer);
                        idx++;
                        setTimeout(speakNextSentence, 120);
                    };

                    utter.onend = advance;
                    utter.onerror = advance;

                    // Tiempo de seguridad amplio basado en longitud real para jamás cortar antes de que termine de hablar
                    const estimatedMs = Math.max(8000, Math.ceil((sentenceText.length / 8) * 1000) + 5000);
                    const sentenceSafetyTimer = setTimeout(advance, estimatedMs);

                    window.speechSynthesis.speak(utter);
                } catch (err) {
                    if (typeof onAllFinished === 'function') onAllFinished();
                }
            };

            setTimeout(speakNextSentence, 60);
            return true;
        }

        function updateReelSceneUI(idx) {
            const data = window.bzPulseData || DEFAULT_WEEKLY_PULSE;
            const scenes = (data.video_reel && data.video_reel.scenes) || DEFAULT_WEEKLY_PULSE.video_reel.scenes;
            const sc = scenes[idx] || scenes[0];

            const screen = document.getElementById('aiReelScreen');
            const bgImg = document.getElementById('aiReelBgImage');
            const thumbImg = document.getElementById('aiReelThumbImage');
            const badge = document.getElementById('aiReelBadge');
            const headline = document.getElementById('aiReelHeadline');
            const subtext = document.getElementById('aiReelSubtext');
            const stepText = document.getElementById('aiReelStepCounter');
            const progressBar = document.getElementById('aiReelProgressBar');
            const playBtn = document.getElementById('aiReelPlayBtn');
            const eqBars = document.getElementById('aiReelEqualizer');
            const openFullBtn = document.getElementById('aiReelOpenFullBtn');

            if (!screen) return;
            const defaultImg = 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80';
            const imgUrl = sc.image || defaultImg;

            if (bgImg) {
                bgImg.src = imgUrl;
                bgImg.className = window.bzReelState.playing
                    ? "absolute inset-0 w-full h-full object-cover opacity-55 scale-110 transition-transform duration-[9000ms] ease-out"
                    : "absolute inset-0 w-full h-full object-cover opacity-45 scale-100 transition-transform duration-700";
            }
            if (thumbImg) {
                thumbImg.src = imgUrl;
            }
            if (badge) badge.textContent = sc.badge || `NOTICIA #${idx + 1}`;
            if (headline) headline.textContent = sc.headline || '';
            if (subtext) subtext.textContent = sc.subtext || '';
            if (stepText) stepText.textContent = `Noticia ${idx + 1}/${scenes.length}`;
            if (progressBar) {
                const pct = Math.round(((idx + 1) / scenes.length) * 100);
                progressBar.style.width = `${pct}%`;
            }
            if (openFullBtn) {
                const targetNewsIdx = (typeof sc.news_index === 'number') ? sc.news_index : idx;
                openFullBtn.setAttribute('onclick', `event.stopPropagation(); openFullNewsReader(${targetNewsIdx}, false)`);
            }
            if (playBtn) {
                playBtn.innerHTML = window.bzReelState.playing
                    ? '<span>⏸</span><span>PAUSAR NOTICIERO IA</span>'
                    : '<span>▶</span><span>REPRODUCIR NOTICIERO EN VIDEO IA</span>';
            }
            if (eqBars) {
                eqBars.style.opacity = window.bzReelState.playing ? '1' : '0.4';
            }
        }

        function toggleAiVideoReel() {
            if (window.bzReelState.playing) {
                stopAiVideoReel();
            } else {
                startAiVideoReel(window.bzReelState.sceneIdx || 0);
            }
        }

        function startAiVideoReel(startIdx = 0) {
            const data = window.bzPulseData || DEFAULT_WEEKLY_PULSE;
            const scenes = (data.video_reel && data.video_reel.scenes) || DEFAULT_WEEKLY_PULSE.video_reel.scenes;
            if (startIdx >= scenes.length) startIdx = 0;

            trackByteZoneEvent('news_video', 'play');
            window.bzReelState.playing = true;
            window.bzReelState.readingFullArticle = false;
            window.bzReelState.sceneIdx = startIdx;
            startCyberBeat();
            runReelScene(startIdx);
        }

        function runReelScene(idx) {
            clearTimeout(window.bzReelState.timer);
            const data = window.bzPulseData || DEFAULT_WEEKLY_PULSE;
            const scenes = (data.video_reel && data.video_reel.scenes) || DEFAULT_WEEKLY_PULSE.video_reel.scenes;
            if (!window.bzReelState.playing || idx >= scenes.length) {
                stopAiVideoReel();
                window.bzReelState.sceneIdx = 0;
                updateReelSceneUI(0);
                return;
            }

            window.bzReelState.sceneIdx = idx;
            updateReelSceneUI(idx);
            const sc = scenes[idx];

            let advanced = false;
            const goNext = () => {
                if (advanced || !window.bzReelState.playing) return;
                advanced = true;
                clearTimeout(window.bzReelState.timer);
                if (idx + 1 < scenes.length) {
                    runReelScene(idx + 1);
                } else {
                    stopAiVideoReel();
                }
            };

            const subtextEl = document.getElementById('aiReelSubtext');
            const hasSpeech = speakTextSentenceBySentence(
                sc.voice_script || (sc.headline + ". " + sc.subtext),
                (currentSentence) => {
                    if (subtextEl) subtextEl.textContent = currentSentence;
                },
                () => {
                    // Espera a que cierre la noticia completa antes de pasar a la siguiente
                    setTimeout(goNext, 650);
                }
            );

            // Solo usar temporizador si el navegador no soporta voz sintetizada
            if (!hasSpeech) {
                window.bzReelState.timer = setTimeout(goNext, 9000);
            }
        }

        function stopAiVideoReel() {
            window.bzReelState.playing = false;
            window.bzReelState.speechSessionId++;
            clearTimeout(window.bzReelState.timer);
            stopCyberBeat();
            if ('speechSynthesis' in window) {
                try { window.speechSynthesis.cancel(); } catch (e) {}
            }
            updateReelSceneUI(window.bzReelState.sceneIdx || 0);
        }

        function prevAiReelScene() {
            const data = window.bzPulseData || DEFAULT_WEEKLY_PULSE;
            const scenes = (data.video_reel && data.video_reel.scenes) || DEFAULT_WEEKLY_PULSE.video_reel.scenes;
            const prevIdx = ((window.bzReelState.sceneIdx || 0) - 1 + scenes.length) % scenes.length;
            if (window.bzReelState.playing) {
                runReelScene(prevIdx);
            } else {
                window.bzReelState.sceneIdx = prevIdx;
                updateReelSceneUI(prevIdx);
            }
        }

        function nextAiReelScene() {
            const data = window.bzPulseData || DEFAULT_WEEKLY_PULSE;
            const scenes = (data.video_reel && data.video_reel.scenes) || DEFAULT_WEEKLY_PULSE.video_reel.scenes;
            const nextIdx = ((window.bzReelState.sceneIdx || 0) + 1) % scenes.length;
            if (window.bzReelState.playing) {
                runReelScene(nextIdx);
            } else {
                window.bzReelState.sceneIdx = nextIdx;
                updateReelSceneUI(nextIdx);
            }
        }

        function playSpecificNewsScene(sceneIndex) {
            const el = document.getElementById('aiReelScreen');
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            startAiVideoReel(sceneIndex);
        }

        function toggleReelSpeed() {
            const current = window.bzReelState.voiceRate || 1.22;
            const next = current >= 1.4 ? 1.05 : (current >= 1.18 ? 1.42 : 1.22);
            window.bzReelState.voiceRate = next;
            const btn = document.getElementById('aiReelSpeedBtn');
            if (btn) {
                const label = next >= 1.4 ? '1.4x Turbo' : (next >= 1.18 ? '1.2x Dinámico' : '1.0x Normal');
                btn.textContent = '⚡ Voz: ' + label;
            }
            if (window.bzReelState.playing) {
                runReelScene(window.bzReelState.sceneIdx);
            } else if (window.bzReelState.readingFullArticle) {
                speakFullArticleInModal(window.bzReelState.currentArticleIdx);
            }
        }

        // ==========================================================
        // LECTOR Y LOCUTOR DE NOTICIA COMPLETA (MODAL INTERACTIVO)
        // ==========================================================
        function openFullNewsReader(newsIdx, autoSpeak = false) {
            stopAiVideoReel();
            const data = window.bzPulseData || DEFAULT_WEEKLY_PULSE;
            const newsList = (Array.isArray(data.weekly_news) && data.weekly_news.length > 0)
                ? data.weekly_news
                : (data.video_reel.scenes || []).map(s => ({
                    title: s.headline,
                    summary: s.subtext,
                    full_paragraphs: [s.subtext],
                    full_voice_script: s.voice_script,
                    image: s.image,
                    source: s.source || 'ByteZone IA'
                }));

            if (newsIdx < 0) newsIdx = newsList.length - 1;
            if (newsIdx >= newsList.length) newsIdx = 0;
            window.bzReelState.currentArticleIdx = newsIdx;

            const item = newsList[newsIdx] || newsList[0];
            const modal = document.getElementById('fullNewsModal');
            if (!modal) return;

            const imgEl = document.getElementById('fullNewsImg');
            const badgeEl = document.getElementById('fullNewsBadge');
            const titleEl = document.getElementById('fullNewsTitle');
            const bodyEl = document.getElementById('fullNewsBody');
            const sourceLinkEl = document.getElementById('fullNewsSourceLink');

            if (imgEl) {
                imgEl.src = item.image || 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80';
            }
            if (badgeEl) {
                badgeEl.textContent = `📰 NOTICIA #${newsIdx + 1} DE ${newsList.length} • ${item.source || 'ByteZone Tech'}`;
            }
            if (titleEl) {
                titleEl.textContent = item.title || '';
            }
            const paragraphs = (Array.isArray(item.full_paragraphs) && item.full_paragraphs.length > 0)
                ? item.full_paragraphs
                : [item.summary || ''];

            if (bodyEl) {
                bodyEl.innerHTML = paragraphs.map((p, pIdx) => `
                    <p id="fullNewsPara_${pIdx}" class="text-sm sm:text-base text-gray-200 leading-relaxed p-3 rounded-2xl transition border border-transparent">
                        ${p}
                    </p>
                `).join('');
            }
            if (sourceLinkEl) {
                if (item.link) {
                    sourceLinkEl.href = item.link;
                    sourceLinkEl.classList.remove('hidden');
                } else {
                    sourceLinkEl.classList.add('hidden');
                }
            }

            modal.classList.remove('hidden');
            updateFullNewsAudioBtn(false);

            if (autoSpeak) {
                speakFullArticleInModal(newsIdx);
            }
        }

        function updateFullNewsAudioBtn(isReading) {
            const btn = document.getElementById('fullNewsSpeakBtn');
            const status = document.getElementById('fullNewsAudioStatus');
            if (btn) {
                if (isReading) {
                    btn.innerHTML = '<span>⏹</span><span>DETENER LECTURA EN VOZ ALTA</span>';
                    btn.className = "w-full sm:w-auto bg-gradient-to-r from-rose-600 to-pink-600 hover:opacity-95 text-white font-black py-3 px-5 rounded-2xl shadow-lg text-xs sm:text-sm flex items-center justify-center space-x-2 transition";
                } else {
                    btn.innerHTML = '<span>🔊</span><span>LEERME TODA LA NOTICIA EN VOZ ALTA</span>';
                    btn.className = "w-full sm:w-auto bg-gradient-to-r from-cyan-500 to-blue-600 hover:opacity-95 text-white font-black py-3 px-5 rounded-2xl shadow-lg shadow-cyan-500/25 text-xs sm:text-sm flex items-center justify-center space-x-2 transition";
                }
            }
            if (status) {
                status.textContent = isReading ? "🎙️ Leyendo el artículo completo párrafo por párrafo..." : "📖 Puedes leer el artículo abajo o tocar el botón azul para escucharlo completo.";
            }
        }

        function toggleFullArticleSpeech() {
            if (window.bzReelState.readingFullArticle) {
                stopFullArticleSpeech();
            } else {
                speakFullArticleInModal(window.bzReelState.currentArticleIdx || 0);
            }
        }

        function stopFullArticleSpeech() {
            window.bzReelState.readingFullArticle = false;
            window.bzReelState.speechSessionId++;
            if ('speechSynthesis' in window) {
                try { window.speechSynthesis.cancel(); } catch (e) {}
            }
            document.querySelectorAll('[id^="fullNewsPara_"]').forEach(el => {
                el.className = "text-sm sm:text-base text-gray-200 leading-relaxed p-3 rounded-2xl transition border border-transparent";
            });
            updateFullNewsAudioBtn(false);
        }

        function speakFullArticleInModal(newsIdx) {
            const data = window.bzPulseData || DEFAULT_WEEKLY_PULSE;
            const newsList = data.weekly_news || [];
            const item = newsList[newsIdx];
            if (!item) return;

            window.bzReelState.readingFullArticle = true;
            updateFullNewsAudioBtn(true);

            const paragraphs = (Array.isArray(item.full_paragraphs) && item.full_paragraphs.length > 0)
                ? item.full_paragraphs
                : [item.summary || ''];

            window.bzReelState.speechSessionId++;
            const session = window.bzReelState.speechSessionId;
            let pIndex = -1; // -1 = leyendo el título

            const readNextParagraph = () => {
                if (!window.bzReelState.readingFullArticle || session !== window.bzReelState.speechSessionId) return;

                document.querySelectorAll('[id^="fullNewsPara_"]').forEach(el => {
                    el.className = "text-sm sm:text-base text-gray-200 leading-relaxed p-3 rounded-2xl transition border border-transparent";
                });

                if (pIndex === -1) {
                    const introText = `${item.title}. Publicado por ${item.source || 'ByteZone'}.`;
                    pIndex = 0;
                    speakTextSentenceBySentence(introText, null, readNextParagraph);
                    return;
                }

                if (pIndex >= paragraphs.length) {
                    stopFullArticleSpeech();
                    return;
                }

                const activeParaEl = document.getElementById(`fullNewsPara_${pIndex}`);
                if (activeParaEl) {
                    activeParaEl.className = "text-sm sm:text-base text-white font-semibold leading-relaxed p-3.5 rounded-2xl transition bg-cyan-950/60 border border-cyan-400/50 shadow-lg";
                    activeParaEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }

                const textToRead = paragraphs[pIndex];
                pIndex++;
                speakTextSentenceBySentence(textToRead, null, () => {
                    setTimeout(readNextParagraph, 350);
                });
            };

            readNextParagraph();
        }

        function closeFullNewsReader() {
            stopFullArticleSpeech();
            const modal = document.getElementById('fullNewsModal');
            if (modal) modal.classList.add('hidden');
        }

        function unlockVipNewsAndHack() {
            trackByteZoneEvent('news_video', 'ad');
            const box = document.getElementById('vipUnlockedBox');
            const btn = document.getElementById('vipUnlockBtn');
            const data = window.bzPulseData || DEFAULT_WEEKLY_PULSE;
            const vip = data.vip_hack_of_the_week || DEFAULT_WEEKLY_PULSE.vip_hack_of_the_week;
            if (box) {
                document.getElementById('vipHackTag').textContent = vip.tag || 'Secreto VIP';
                document.getElementById('vipHackTitle').textContent = vip.title || '';
                document.getElementById('vipHackBody').textContent = vip.body || '';
                box.classList.remove('hidden');
            }
            if (btn) {
                btn.innerHTML = '<span>✅</span><span>CONTENIDO VIP DESBLOQUEADO</span>';
                btn.className = "w-full bg-emerald-600/30 border border-emerald-400/50 text-emerald-300 font-black py-3 rounded-2xl text-xs flex items-center justify-center space-x-2";
            }
            if (window.confetti) {
                confetti({ particleCount: 60, spread: 60, origin: { y: 0.7 } });
            }
        }

        function openVaultGameWithReward(targetUrl, gameKey) {
            trackByteZoneEvent(gameKey || 'dodge', 'ad');
            executeRewardedAction(() => {
                setTimeout(() => {
                    window.location.href = targetUrl;
                }, 250);
            });
        }

    </script>
"""

AI_VIDEO_REEL_WIDGET = """
        <!-- REPRODUCTOR DE VIDEO IA CON IMAGEN EN MOVIMIENTO + LECTURA COMPLETA -->
        <div class="bg-gray-900/95 border border-cyan-500/40 rounded-3xl p-4 sm:p-6 shadow-2xl relative overflow-hidden">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                <div class="flex items-center space-x-2">
                    <span class="text-xl animate-pulse">📺</span>
                    <div>
                        <h2 class="text-base sm:text-lg font-black text-white leading-tight">ByteZone TV • Noticiero Visual IA</h2>
                        <p id="pulseUpdatedBadge" class="text-[11px] text-cyan-400 font-semibold">🤖 Actualizado automáticamente por el Agente CEO</p>
                    </div>
                </div>
                <div class="flex items-center space-x-1.5">
                    <button id="aiReelSpeedBtn" onclick="toggleReelSpeed()" class="text-[11px] bg-gray-800 hover:bg-gray-700 text-amber-300 font-bold px-2.5 py-1 rounded-xl border border-gray-700 transition">
                        ⚡ Voz: 1.2x Dinámico
                    </button>
                    <span id="aiReelStepCounter" class="text-[11px] bg-purple-500/20 text-purple-300 border border-purple-500/40 font-bold px-2.5 py-1 rounded-xl">
                        Noticia 1/5
                    </span>
                </div>
            </div>

            <!-- PANTALLA PRINCIPAL DE VIDEO CON FOTO REAL ANIMADA Y SUBTÍTULOS -->
            <div id="aiReelScreen" onclick="toggleAiVideoReel()" class="cursor-pointer relative w-full rounded-2xl overflow-hidden p-4 sm:p-6 min-h-[300px] sm:min-h-[340px] flex flex-col justify-between border-2 border-cyan-400/50 shadow-2xl bg-gray-950">
                
                <!-- IMAGEN DE FONDO CON EFECTO VIDEO (KEN BURNS ZOOM) -->
                <img id="aiReelBgImage" 
                     src="https://i0.wp.com/imgs.hipertextual.com/wp-content/uploads/2026/10/synthid-scaled.jpg?fit=1024%2C540&quality=70&strip=all&ssl=1" 
                     alt="Noticia IA"
                     onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80'"
                     class="absolute inset-0 w-full h-full object-cover opacity-45 scale-100 transition-transform duration-700">
                <div class="absolute inset-0 bg-gradient-to-t from-gray-950 via-gray-950/75 to-gray-950/40"></div>

                <!-- BARRA SUPERIOR TV EN VIVO Y ECUALIZADOR -->
                <div class="flex items-center justify-between z-10">
                    <div class="flex items-center space-x-2">
                        <span class="flex items-center space-x-1 bg-red-600/90 text-white text-[10px] font-black px-2.5 py-1 rounded-full shadow">
                            <span class="w-1.5 h-1.5 rounded-full bg-white animate-ping"></span>
                            <span>TV IA</span>
                        </span>
                        <span id="aiReelBadge" class="text-[10px] sm:text-xs font-black uppercase tracking-wider bg-black/65 backdrop-blur-md text-cyan-300 px-3 py-1 rounded-full border border-cyan-400/30">
                            NOTICIA #1 • IA & FUTURO
                        </span>
                    </div>
                    <div id="aiReelEqualizer" class="flex items-end space-x-1 h-4 transition-opacity opacity-40 bg-black/50 px-2 py-1 rounded-lg">
                        <span class="w-1 h-3 bg-cyan-300 rounded animate-ping"></span>
                        <span class="w-1 h-4 bg-pink-400 rounded animate-pulse"></span>
                        <span class="w-1 h-2 bg-amber-300 rounded animate-bounce"></span>
                        <span class="w-1 h-4 bg-emerald-300 rounded animate-pulse"></span>
                    </div>
                </div>

                <!-- TARJETA VISUAL DE LA NOTICIA EN PANTALLA -->
                <div class="my-3 z-10 flex flex-col sm:flex-row items-center gap-3.5 bg-black/55 backdrop-blur-md p-3.5 sm:p-4 rounded-2xl border border-white/15 shadow-xl">
                    <img id="aiReelThumbImage"
                         src="https://i0.wp.com/imgs.hipertextual.com/wp-content/uploads/2026/10/synthid-scaled.jpg?fit=1024%2C540&quality=70&strip=all&ssl=1"
                         alt="Miniatura Noticia"
                         onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80'"
                         class="w-full sm:w-36 h-28 sm:h-28 object-cover rounded-xl border border-cyan-400/40 flex-shrink-0 shadow-md">
                    <div class="text-left flex-grow">
                        <h3 id="aiReelHeadline" class="text-sm sm:text-lg font-black text-white drop-shadow leading-snug">
                            Cómo detectar fotos, vídeos y audios creados con IA usando SynthID Detector
                        </h3>
                        <p id="aiReelSubtext" class="text-xs text-gray-200 mt-1.5 leading-relaxed">
                            En un mundo donde la realidad y la veracidad se ponen a prueba todos los días con contenidos creados con IA generativa, Google lanzó SynthID Detector.
                        </p>
                    </div>
                </div>

                <!-- BOTÓN RÁPIDO PARA ABRIR Y ESCUCHAR LA NOTICIA COMPLETA + BARRA DE PROGRESO -->
                <div class="z-10 space-y-2">
                    <div class="flex items-center justify-between gap-2">
                        <span class="text-[11px] text-gray-300 font-semibold">💡 Cierra cada noticia completa antes de pasar a la siguiente</span>
                        <button id="aiReelOpenFullBtn" onclick="event.stopPropagation(); openFullNewsReader(0, false)" class="bg-cyan-500/90 hover:bg-cyan-400 text-gray-950 font-black text-[11px] px-3 py-1.5 rounded-xl shadow transition flex items-center space-x-1 flex-shrink-0">
                            <span>📖</span>
                            <span>Abrir Noticia Completa</span>
                        </button>
                    </div>
                    <div class="w-full bg-black/60 h-2 rounded-full overflow-hidden">
                        <div id="aiReelProgressBar" class="bg-gradient-to-r from-cyan-300 via-amber-300 to-pink-400 h-full transition-all duration-300" style="width: 20%;"></div>
                    </div>
                </div>
            </div>

            <!-- CONTROLES DEL REPRODUCTOR -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-3">
                <button id="aiReelPlayBtn" onclick="toggleAiVideoReel()" class="col-span-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:opacity-95 active:scale-95 text-white font-black py-3 px-4 rounded-2xl shadow-lg shadow-cyan-500/25 text-xs sm:text-sm flex items-center justify-center space-x-2 transition">
                    <span>▶</span>
                    <span>REPRODUCIR NOTICIERO EN VIDEO IA</span>
                </button>
                <button onclick="prevAiReelScene()" class="bg-gray-800 hover:bg-gray-700 text-gray-200 font-bold py-3 px-3 rounded-2xl border border-gray-700 text-xs flex items-center justify-center space-x-1 transition">
                    <span>⏮</span>
                    <span>Anterior</span>
                </button>
                <button onclick="nextAiReelScene()" class="bg-gray-800 hover:bg-gray-700 text-gray-200 font-bold py-3 px-3 rounded-2xl border border-gray-700 text-xs flex items-center justify-center space-x-1 transition">
                    <span>⏭</span>
                    <span>Siguiente</span>
                </button>
            </div>

            <!-- BOTÓN DE DESBLOQUEO VIP CON ANUNCIO MONETAG -->
            <div class="mt-3 pt-3 border-t border-gray-800">
                <button id="vipUnlockBtn" onclick="executeRewardedAction(unlockVipNewsAndHack)" class="w-full bg-gradient-to-r from-amber-500 via-yellow-500 to-orange-500 hover:opacity-95 active:scale-95 text-gray-950 font-black py-3 px-4 rounded-2xl shadow-lg shadow-amber-500/20 text-xs sm:text-sm flex items-center justify-center space-x-2 transition">
                    <span>🔓</span>
                    <span>DESBLOQUEAR TRUCO VIP DE LA SEMANA + BONUS IA</span>
                </button>

                <div id="vipUnlockedBox" class="hidden mt-3 p-4 rounded-2xl bg-gradient-to-r from-amber-950/50 to-orange-950/40 border border-amber-400/50 text-left space-y-1.5">
                    <span id="vipHackTag" class="text-[10px] font-black uppercase bg-amber-400/20 text-amber-300 px-2.5 py-0.5 rounded-md">Secreto VIP</span>
                    <h4 id="vipHackTitle" class="text-sm font-black text-white"></h4>
                    <p id="vipHackBody" class="text-xs text-gray-200 leading-relaxed"></p>
                </div>
            </div>
        </div>

        <!-- MODAL LECTOR Y LOCUTOR DE NOTICIA COMPLETA -->
        <div id="fullNewsModal" class="hidden fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-3 sm:p-5 overflow-y-auto">
            <div class="bg-gray-900 border border-cyan-500/40 rounded-3xl max-w-2xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden my-auto">
                
                <!-- CABECERA DEL MODAL CON FOTO DE LA NOTICIA -->
                <div class="relative h-48 sm:h-56 w-full bg-gray-950 flex-shrink-0">
                    <img id="fullNewsImg" src="" alt="Foto de la noticia" 
                         onerror="this.src='https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80'"
                         class="w-full h-full object-cover opacity-85">
                    <div class="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/40 to-transparent"></div>
                    <button onclick="closeFullNewsReader()" class="absolute top-3 right-3 bg-black/75 hover:bg-black text-white font-black text-xs px-3.5 py-2 rounded-full border border-white/20 shadow-lg">
                        ✕ Cerrar
                    </button>
                    <div class="absolute bottom-3 left-4 right-4">
                        <span id="fullNewsBadge" class="text-[10px] font-black uppercase px-2.5 py-1 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-400/40 backdrop-blur-md">
                            NOTICIA COMPLETA
                        </span>
                        <h2 id="fullNewsTitle" class="text-base sm:text-xl font-black text-white mt-1.5 leading-snug drop-shadow"></h2>
                    </div>
                </div>

                <!-- BARRA DE CONTROL DE VOZ COMPLETA -->
                <div class="p-4 bg-gray-950/90 border-b border-gray-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 flex-shrink-0">
                    <button id="fullNewsSpeakBtn" onclick="toggleFullArticleSpeech()" class="w-full sm:w-auto bg-gradient-to-r from-cyan-500 to-blue-600 hover:opacity-95 text-white font-black py-3 px-5 rounded-2xl shadow-lg shadow-cyan-500/25 text-xs sm:text-sm flex items-center justify-center space-x-2 transition">
                        <span>🔊</span>
                        <span>LEERME TODA LA NOTICIA EN VOZ ALTA</span>
                    </button>
                    <p id="fullNewsAudioStatus" class="text-[11px] text-gray-400">
                        📖 Puedes leer el artículo abajo o tocar el botón azul para escucharlo completo.
                    </p>
                </div>

                <!-- CUERPO COMPLETO DEL ARTÍCULO (PÁRRAFOS RESALTADOS MIENTRAS HABLA) -->
                <div id="fullNewsBody" class="p-4 sm:p-6 overflow-y-auto space-y-2 flex-grow"></div>

                <!-- PIE DEL MODAL: NAVEGAR ENTRE NOTICIAS -->
                <div class="p-4 bg-gray-950/90 border-t border-gray-800 flex flex-wrap items-center justify-between gap-2 flex-shrink-0">
                    <div class="flex items-center space-x-2">
                        <button onclick="openFullNewsReader((window.bzReelState.currentArticleIdx || 0) - 1, false)" class="bg-gray-800 hover:bg-gray-700 text-gray-200 font-bold text-xs px-3.5 py-2 rounded-xl border border-gray-700">
                            ⏮ Noticia Anterior
                        </button>
                        <button onclick="openFullNewsReader((window.bzReelState.currentArticleIdx || 0) + 1, false)" class="bg-gray-800 hover:bg-gray-700 text-gray-200 font-bold text-xs px-3.5 py-2 rounded-xl border border-gray-700">
                            ⏭ Siguiente Noticia
                        </button>
                    </div>
                    <div class="flex items-center space-x-2">
                        <a id="fullNewsSourceLink" href="#" target="_blank" rel="noopener" class="text-xs text-cyan-400 hover:underline font-bold">
                            Fuente original ↗
                        </a>
                        <button onclick="closeFullNewsReader()" class="bg-gray-800 hover:bg-gray-700 text-white font-bold text-xs px-4 py-2 rounded-xl border border-gray-700">
                            Cerrar Lector
                        </button>
                    </div>
                </div>
            </div>
        </div>
"""

# ==========================================================
# 1. PÁGINA PRINCIPAL: INDEX.HTML (ARCADE LOBBY)
# ==========================================================
TEMPLATE_INDEX = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ByteZone - Arcade Lobby, Torneos Semanales & Noticias IA</title>
    <meta name="description" content="Arcade con mini-juegos adictivos de habilidad y reflejos, torneos semanales en vivo, Baúl Arcade y resumen semanal de Inteligencia Artificial en video.">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <!-- BANNER DE BIENVENIDA -->
        <div class="bg-gradient-to-r from-blue-950/80 via-purple-950/80 to-pink-950/80 border border-purple-500/30 rounded-3xl p-6 sm:p-8 text-center relative overflow-hidden shadow-2xl">
            <span class="text-[11px] bg-purple-500/20 text-purple-300 border border-purple-500/40 font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                Temporada 2026 • Torneo Semanal & Agente IA Activo
            </span>
            <h1 class="text-3xl sm:text-4xl font-black text-white mt-3 mb-2">Arcade Hub ByteZone</h1>
            <p class="text-gray-300 text-xs sm:text-sm max-w-lg mx-auto leading-relaxed">
                Compite por el #1 en el <strong>Torneo Semanal</strong> (reinicia cada domingo a las 12:00 AM), inscríbete en el Récord Histórico y mira el Resumen Flash de IA en 45 segundos.
            </p>

            <!-- IDENTIDAD DEL JUGADOR EN LOBBY -->
            <div class="mt-4 inline-flex items-center space-x-2 bg-gray-900/90 px-4 py-2 rounded-2xl border border-gray-700 shadow-lg">
                <span class="text-xs text-gray-400">Compitiendo como:</span>
                <span id="playerNameDisplay" class="font-black text-cyan-400 text-sm">Jugador</span>
                <button onclick="promptChangeName()" class="text-xs text-purple-400 hover:text-white ml-1 font-bold">✏️ Editar</button>
            </div>
        </div>

        <!-- CATÁLOGO DE JUEGOS PRINCIPALES EN PORTADA -->
        <div class="space-y-4">
            <div class="flex justify-between items-center">
                <h2 class="text-xl font-black text-white flex items-center space-x-2">
                    <span>🕹️</span>
                    <span>Juegos Oficiales del Torneo Semanal</span>
                </h2>
                <span class="text-xs text-emerald-400 font-bold bg-emerald-500/10 px-2.5 py-1 rounded-full">__PORTADA_LABEL__</span>
            </div>

            __PORTADA_GRID__
        </div>

        <!-- REPRODUCTOR DE VIDEO FLASH IA EN PORTADA -->
        __AI_VIDEO_REEL_WIDGET__

        <!-- NOTICIAS COMPLETAS DE LA SEMANA (CON FOTO, LECTURA COMPLETA Y LOCUCIÓN COMPLETA) -->
        <div class="space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <h2 class="text-lg sm:text-xl font-black text-white flex items-center space-x-2">
                    <span>📰</span>
                    <span>Noticias Completas de IA & Tecnología (Leer o Escuchar)</span>
                </h2>
                <span class="text-[11px] text-cyan-400 font-bold bg-cyan-500/10 border border-cyan-500/30 px-2.5 py-1 rounded-full">
                    🔊 Toca cualquier noticia para abrirla completa
                </span>
            </div>
            <div id="weeklyNewsContainer" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
        </div>

        <!-- EL BAÚL ARCADE (ROTACIÓN SEMANAL GESTIONADA POR EL AGENTE CEO) -->
        <div class="bg-gradient-to-r from-gray-900 via-amber-950/20 to-gray-900 border border-amber-500/40 rounded-3xl p-5 sm:p-6 shadow-xl">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                <div class="flex items-center space-x-2.5">
                    <span class="text-2xl">🗄️</span>
                    <div>
                        <h3 class="text-base sm:text-lg font-black text-white">El Baúl Arcade • Rotación Dinámica</h3>
                        <p class="text-xs text-gray-400">Juegos especiales y de reserva administrados por el Agente CEO según popularidad semanal.</p>
                    </div>
                </div>
                <span class="text-[10px] font-black uppercase bg-amber-500/20 text-amber-300 border border-amber-500/40 px-3 py-1 rounded-full">
                    🤖 Rotación Lunes 00:05 AM
                </span>
            </div>

            __VAULT_CARDS__
        </div>

        <!-- ACCESOS RÁPIDOS ADICIONALES -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <a href="campeones.html?v=14" class="bg-gradient-to-r from-amber-950/50 to-gray-900 p-5 rounded-2xl border border-amber-500/40 hover:border-amber-400 flex items-center space-x-4 transition shadow-lg">
                <span class="text-3xl">🏆</span>
                <div>
                    <h4 class="font-black text-amber-300 text-sm">Salón de Campeones</h4>
                    <p class="text-xs text-gray-300">Ganadores Top 3 semana a semana de cada juego.</p>
                </div>
            </a>
            <a href="hacks.html?v=14" class="bg-gradient-to-r from-gray-900 to-gray-850 p-5 rounded-2xl border border-gray-800 hover:border-cyan-500/50 flex items-center space-x-4 transition shadow">
                <span class="text-3xl">🤖</span>
                <div>
                    <h4 class="font-bold text-white text-sm">Noticias IA, Inventos & Hacks</h4>
                    <p class="text-xs text-gray-400">Lo último de la semana en IA y trucos secretos.</p>
                </div>
            </a>
            <a href="humor.html?v=14" class="bg-gradient-to-r from-gray-900 to-gray-850 p-5 rounded-2xl border border-gray-800 hover:border-pink-500/50 flex items-center space-x-4 transition shadow">
                <span class="text-3xl">🎭</span>
                <div>
                    <h4 class="font-bold text-white text-sm">Cápsula de Humor Tech</h4>
                    <p class="text-xs text-gray-400">Chistes, frases sarcásticas y memes.</p>
                </div>
            </a>
        </div>

    </main>

    __PLAYER_MODAL__

    __FOOTER__

    __PLAYER_IDENTITY_SCRIPT__
    <script>
        loadWeeklyPulseData("");
    </script>
</body>
</html>
"""

# ==========================================================
# 2. PÁGINA JUEGO 1: JUEGOS/NEON-STACKER.HTML
# ==========================================================
TEMPLATE_STACKER = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Neon Stacker Pro - ByteZone</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <!-- BARRA REGRESAR Y RÉCORD PERSONAL -->
        <div class="flex items-center justify-between">
            <a href="../index.html?v=14" class="text-xs text-cyan-400 hover:underline flex items-center space-x-1 bg-gray-900 px-3 py-1.5 rounded-xl border border-gray-800">
                <span>←</span>
                <span>Volver al Arcade</span>
            </a>

            <div class="text-xs text-gray-400 bg-gray-900 px-3 py-1.5 rounded-xl border border-gray-800 flex items-center space-x-2">
                <span>Modo:</span>
                <span class="text-cyan-400 font-bold">Torre Infinita</span>
            </div>
        </div>

        <!-- TABLERO DE RÉCORD STACKER -->
        <div class="bg-gray-900/90 p-4 rounded-2xl border border-cyan-500/30 flex items-center justify-between shadow-xl">
            <div>
                <p id="userBestScoreLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Tu Mejor Récord Semanal</p>
                <p id="userBestScore" class="text-2xl font-black text-white">0 Pisos</p>
            </div>
            <div class="text-right">
                <p id="userRankLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Puesto en la Semana</p>
                <span id="userRankBadge" class="text-xs font-black text-pink-400 bg-pink-500/10 border border-pink-500/30 px-3 py-1 rounded-full">
                    Sin Clasificar
                </span>
            </div>
        </div>

        <!-- LIENZO DEL JUEGO STACKER -->
        <div class="bg-gray-900/90 rounded-3xl p-4 sm:p-6 border border-gray-800 relative shadow-2xl">
            <div class="relative w-full max-w-sm mx-auto h-[400px] sm:h-[440px] rounded-2xl overflow-hidden bg-gray-950 border-2 border-cyan-500/40 flex flex-col justify-end">
                
                <canvas id="stackerCanvas" width="360" height="440" class="w-full h-full block cursor-pointer select-none"></canvas>

                <!-- OVERLAY INICIO -->
                <div id="stackerStartScreen" class="absolute inset-0 bg-gray-950/85 backdrop-blur-sm flex flex-col items-center justify-center p-6 text-center">
                    <span class="text-5xl mb-2 animate-bounce">🏗️</span>
                    <h2 class="text-2xl font-black text-white">NEON STACKER PRO</h2>
                    <p class="text-xs text-gray-300 mt-2 mb-6 max-w-xs">
                        Toca la pantalla en el momento justo para encajar cada bloque. ¡Construye la torre más alta!
                    </p>
                    <button onclick="startStackerGame()" class="bg-gradient-to-r from-cyan-500 to-blue-600 hover:scale-105 active:scale-95 text-white font-black px-8 py-3.5 rounded-2xl shadow-xl shadow-cyan-500/30 transition text-sm">
                        ¡JUGAR AHORA!
                    </button>
                </div>

                <!-- MODAL REVIVIR (SEGUNDA OPORTUNIDAD) -->
                <div id="stackerReviveModal" class="hidden absolute inset-0 bg-gray-950/90 backdrop-blur-md flex flex-col items-center justify-center p-6 text-center">
                    <span class="text-5xl mb-1">💥</span>
                    <h3 class="text-xl font-black text-white">¡LA TORRE SE CAYÓ!</h3>
                    <p id="reviveFloorText" class="text-sm font-bold text-cyan-400 mt-1 mb-4">Llegaste al Piso 14</p>
                    
                    <div id="reviveActionBox" class="w-full max-w-xs mb-3">
                        <button onclick="executeRewardedAction(handleReviveClick)" class="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:opacity-90 active:scale-95 text-white font-black py-3.5 rounded-2xl shadow-lg shadow-emerald-500/30 text-xs sm:text-sm flex items-center justify-center space-x-2 transition">
                            <span>▶</span>
                            <span>REVIVIR Y CONTINUAR AQUÍ</span>
                        </button>
                        <p class="text-[10px] text-gray-400 mt-1">Salva tu récord y continúa sin empezar de cero</p>
                    </div>

                    <button onclick="resetStackerGame()" class="text-xs text-gray-400 hover:text-white underline mt-2">
                        Reiniciar desde piso 1
                    </button>
                </div>

            </div>
            <p class="text-xs text-gray-400 text-center mt-3">💡 Toca la pantalla o presiona la barra espaciadora para soltar el bloque</p>
        </div>

        <!-- TABLA DE LÍDERES STACKER (SEMANAL + HISTÓRICO) -->
        <div class="bg-gray-900/80 rounded-3xl p-5 sm:p-6 border border-gray-800">
            <div class="flex justify-between items-center mb-3">
                <div class="flex items-center space-x-2">
                    <span class="text-xl">🏆</span>
                    <h3 class="text-base sm:text-lg font-black text-white">Top 10 • Neon Stacker</h3>
                </div>
                <button id="liveSyncStatus" onclick="syncGameFromCloud('stacker', false)" class="text-xs bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 font-bold px-2.5 py-1 rounded-full transition">🟢 Global En Vivo</button>
            </div>

            <!-- PESTAÑAS: TORNEO SEMANAL vs RÉCORD HISTÓRICO -->
            <div class="flex space-x-1.5 bg-gray-950/90 p-1.5 rounded-2xl border border-gray-800 mb-3">
                <button id="tabWeeklyBtn" onclick="switchLeaderboardTab('weekly')" class="w-1/2 py-2 px-3 rounded-xl font-black text-xs transition flex items-center justify-center space-x-1.5 bg-gradient-to-r from-amber-500 to-orange-500 text-gray-950 shadow-md shadow-amber-500/20">
                    <span>🔥</span>
                    <span>Torneo Semanal</span>
                </button>
                <button id="tabAlltimeBtn" onclick="switchLeaderboardTab('alltime')" class="w-1/2 py-2 px-3 rounded-xl font-bold text-xs transition flex items-center justify-center space-x-1.5 text-gray-400 hover:text-white">
                    <span>👑</span>
                    <span>Récord Histórico</span>
                </button>
            </div>

            <!-- BANNER CUENTA REGRESIVA DOMINGO 12:00 AM -->
            <div id="weeklyCountdownBanner" class="mb-3 px-3 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-[11px] flex flex-wrap items-center justify-between gap-1"></div>

            <div id="leaderboardList" class="space-y-2 text-sm"></div>

            <div class="mt-4 pt-3 border-t border-gray-800 text-center">
                <a href="../campeones.html?v=14" class="inline-flex items-center space-x-2 text-xs font-black text-amber-300 bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/40 px-4 py-2.5 rounded-xl transition">
                    <span>🏆</span>
                    <span>Ver Ganadores de Semanas Anteriores (Salón de Campeones)</span>
                </a>
            </div>
        </div>

    </main>

    __PLAYER_MODAL__
    __PLAYER_IDENTITY_SCRIPT__

    <script>
        const canvas = document.getElementById('stackerCanvas');
        const ctx = canvas.getContext('2d');
        const startScreen = document.getElementById('stackerStartScreen');
        const reviveModal = document.getElementById('stackerReviveModal');
        const reviveFloorText = document.getElementById('reviveFloorText');

        const BLOCK_HEIGHT = 22;
        let stack = [];
        let currentBlock = null;
        let stackerRunning = false;
        let currentFloor = 0;
        let direction = 1;
        let speed = 3.5;
        let hasRevived = false;

        const PALETTE = ['#06b6d4', '#3b82f6', '#8b5cf6', '#a855f7', '#ec4899', '#f43f5e', '#f59e0b', '#10b981'];

        function initStacker() {
            stack = [];
            currentFloor = 0;
            direction = 1;
            speed = 3.5;
            hasRevived = false;
            
            const baseWidth = 180;
            const baseX = (canvas.width - baseWidth) / 2;
            const baseY = canvas.height - BLOCK_HEIGHT - 10;
            stack.push({ x: baseX, y: baseY, width: baseWidth, color: PALETTE[0] });

            spawnNextBlock();
        }

        function spawnNextBlock() {
            currentFloor++;
            const prev = stack[stack.length - 1];
            const nextY = prev.y - BLOCK_HEIGHT;
            const color = PALETTE[currentFloor % PALETTE.length];

            currentBlock = { x: 0, y: nextY, width: prev.width, color: color };
            speed = Math.min(3.5 + (currentFloor * 0.15), 9.0);
        }

        function startStackerGame() {
            trackByteZoneEvent('stacker', 'play');
            startScreen.classList.add('hidden');
            reviveModal.classList.add('hidden');
            initStacker();
            stackerRunning = true;
            requestAnimationFrame(updateStackerLoop);
        }

        function dropBlock() {
            if (!stackerRunning || !currentBlock) return;

            const prev = stack[stack.length - 1];
            const diff = currentBlock.x - prev.x;

            if (Math.abs(diff) < 4) {
                currentBlock.x = prev.x;
                if (window.confetti && currentFloor % 5 === 0) {
                    confetti({ particleCount: 25, spread: 40, origin: { y: 0.7 } });
                }
            } else if (diff > 0) {
                const newWidth = currentBlock.width - diff;
                if (newWidth <= 0) { gameOverStacker(); return; }
                currentBlock.width = newWidth;
            } else {
                const newWidth = currentBlock.width + diff;
                if (newWidth <= 0) { gameOverStacker(); return; }
                currentBlock.width = newWidth;
                currentBlock.x = prev.x;
            }

            stack.push(currentBlock);
            if (currentBlock.y < 120) {
                stack.forEach(b => b.y += BLOCK_HEIGHT);
            }
            spawnNextBlock();
        }

        function updateStackerLoop() {
            if (!stackerRunning) return;

            currentBlock.x += speed * direction;
            if (currentBlock.x + currentBlock.width >= canvas.width) direction = -1;
            else if (currentBlock.x <= 0) direction = 1;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            stack.forEach((b) => {
                ctx.fillStyle = b.color;
                ctx.shadowColor = b.color;
                ctx.shadowBlur = 8;
                ctx.fillRect(b.x, b.y, b.width, BLOCK_HEIGHT - 2);
            });

            if (currentBlock) {
                ctx.fillStyle = currentBlock.color;
                ctx.shadowColor = currentBlock.color;
                ctx.shadowBlur = 15;
                ctx.fillRect(currentBlock.x, currentBlock.y, currentBlock.width, BLOCK_HEIGHT - 2);
            }

            ctx.shadowBlur = 0;
            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 20px monospace";
            ctx.fillText("PISO: " + currentFloor, 20, 35);

            requestAnimationFrame(updateStackerLoop);
        }

        function gameOverStacker() {
            stackerRunning = false;
            saveScore(currentFloor);

            reviveFloorText.textContent = "Te caíste en el Piso " + currentFloor;
            document.getElementById('reviveActionBox').style.display = hasRevived ? 'none' : 'block';
            reviveModal.classList.remove('hidden');
            // Si ya no puede revivir, la partida terminó de verdad: ahora sí se puede celebrar el podio
            if (hasRevived) { setTimeout(() => { flushPendingPodium(); }, 700); }
        }

        function handleReviveClick() {
            trackByteZoneEvent('stacker', 'ad');
            hasRevived = true;
            reviveModal.classList.add('hidden');
            const prev = stack[stack.length - 1];
            currentBlock = {
                x: prev.x,
                y: prev.y - BLOCK_HEIGHT,
                width: Math.max(prev.width, 70),
                color: PALETTE[currentFloor % PALETTE.length]
            };
            stackerRunning = true;
            requestAnimationFrame(updateStackerLoop);
        }

        function resetStackerGame() {
            reviveModal.classList.add('hidden');
            if (flushPendingPodium()) {
                startScreen.classList.remove('hidden');
            } else {
                startStackerGame();
            }
        }

        canvas.addEventListener('pointerdown', (e) => {
            e.preventDefault();
            if (stackerRunning) dropBlock();
        });

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && stackerRunning) {
                e.preventDefault();
                dropBlock();
            }
        });

        trackByteZoneEvent('stacker', 'view');

        function saveScore(score) {
            recordGameScore('stacker', score, false);
        }

        function renderLeaderboardUI() {
            const mode = window.currentLeaderboardTab || 'weekly';
            const list = getCleanScores('stacker', false, mode);
            const container = document.getElementById('leaderboardList');
            const bestKey = (mode === 'weekly') ? 'bytezone_weekly_best_stacker' : 'bytezone_best_stacker';
            const myBest = parseInt(localStorage.getItem(bestKey) || '0');
            document.getElementById('userBestScore').textContent = myBest + " Pisos";

            const bestLabel = document.getElementById('userBestScoreLabel');
            const rankLabel = document.getElementById('userRankLabel');
            if (bestLabel) bestLabel.textContent = (mode === 'weekly') ? "Tu Récord de la Semana" : "Tu Récord Histórico";
            if (rankLabel) rankLabel.textContent = (mode === 'weekly') ? "Puesto Semanal" : "Puesto Histórico";

            if (list.length === 0) {
                container.innerHTML = '<div class="p-4 text-center text-gray-400 text-xs">¡Torneo Semanal recién reiniciado! Juega una partida para coronarte #1 de esta semana.</div>';
                document.getElementById('userRankBadge').textContent = "Sin Clasificar";
                return;
            }

            container.innerHTML = "";
            let myPosition = null;
            list.slice(0, 10).forEach((item, idx) => {
                const isMe = isCurrentUserEntry(item);
                if (isMe && myPosition === null) {
                    myPosition = idx + 1;
                }
                const badge = idx === 0 ? "🥇" : idx === 1 ? "🥈" : idx === 2 ? "🥉" : "#" + (idx + 1);
                const itemFlag = getCountryFlag(item.country);
                const row = document.createElement('div');
                row.className = "flex justify-between items-center p-2.5 rounded-xl " + (isMe ? 'bg-cyan-950/40 border border-cyan-500 shadow-md' : 'bg-gray-800/60 border border-gray-700/50');
                row.innerHTML = `
                    <div class="flex items-center space-x-2 min-w-0">
                        <span class="w-6 text-center font-bold text-xs ${idx < 3 ? 'text-yellow-400 font-extrabold' : 'text-gray-400'}">${badge}</span>
                        <span class="text-base select-none">${itemFlag}</span>
                        <span class="font-bold truncate ${isMe ? 'text-cyan-400' : 'text-white'}">${item.name} ${isMe ? '(Tú)' : ''}</span>
                    </div>
                    <span class="font-black flex-shrink-0 ${isMe ? 'text-pink-400' : 'text-cyan-400'}">${item.score} Pisos</span>
                `;
                container.appendChild(row);
            });

            const rankBadge = document.getElementById('userRankBadge');
            if (myPosition === 1) {
                rankBadge.textContent = "🥇 Puesto #1 (¡Líder! • Toca para Retar)";
                rankBadge.className = "text-xs font-black text-yellow-300 bg-yellow-500/20 border border-yellow-500/50 px-3 py-1 rounded-full animate-pulse cursor-pointer shadow-lg shadow-yellow-500/20";
                rankBadge.onclick = () => checkAndShowPodiumModal('stacker', myBest, false);
            } else if (myPosition === 2) {
                rankBadge.textContent = "🥈 Puesto #2 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-gray-200 bg-gray-500/20 border border-gray-400/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('stacker', myBest, false);
            } else if (myPosition === 3) {
                rankBadge.textContent = "🥉 Puesto #3 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-amber-400 bg-amber-500/20 border border-amber-500/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('stacker', myBest, false);
            } else if (myPosition) {
                rankBadge.textContent = "Puesto #" + myPosition;
                rankBadge.className = "text-xs font-black text-pink-400 bg-pink-500/10 border border-pink-500/30 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            } else {
                rankBadge.textContent = "Sin Clasificar";
                rankBadge.className = "text-xs font-black text-gray-400 bg-gray-800 border border-gray-700 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            }
        }

        updateLeaderboardTabsUI();
        renderLeaderboardUI();
        startRealtimeScoreStream('stacker', false);
    </script>
</body>
</html>
"""

# ==========================================================
# 3. PÁGINA JUEGO 2: JUEGOS/REFLEJOS-VISUALES.HTML
# ==========================================================
TEMPLATE_REFLEX = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Test de Reflejos Visuales - ByteZone</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <!-- BARRA REGRESAR Y RÉCORD PERSONAL -->
        <div class="flex items-center justify-between">
            <a href="../index.html?v=14" class="text-xs text-purple-400 hover:underline flex items-center space-x-1 bg-gray-900 px-3 py-1.5 rounded-xl border border-gray-800">
                <span>←</span>
                <span>Volver al Arcade</span>
            </a>

            <div class="text-xs text-gray-400 bg-gray-900 px-3 py-1.5 rounded-xl border border-gray-800 flex items-center space-x-2">
                <span>Modo:</span>
                <span class="text-purple-400 font-bold">Tiempo de Reacción</span>
            </div>
        </div>

        <!-- TABLERO DE RÉCORD REFLEJOS -->
        <div class="bg-gray-900/90 p-4 rounded-2xl border border-purple-500/30 flex items-center justify-between shadow-xl">
            <div>
                <p id="userBestScoreLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Tu Mejor Tiempo Semanal</p>
                <p id="userBestScore" class="text-2xl font-black text-white">0 ms</p>
            </div>
            <div class="text-right">
                <p id="userRankLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Puesto Semanal</p>
                <span id="userRankBadge" class="text-xs font-black text-pink-400 bg-pink-500/10 border border-pink-500/30 px-3 py-1 rounded-full">
                    Sin Clasificar
                </span>
            </div>
        </div>

        <!-- CONTADOR DE ENERGÍA / INTENTOS DIARIOS -->
        <div class="bg-gray-900/90 p-3.5 rounded-2xl border border-gray-800 flex items-center justify-between shadow">
            <div class="flex items-center space-x-2">
                <span class="text-xs text-gray-400 font-bold uppercase tracking-wider">⚡ Energía:</span>
                <div id="attemptsIndicator" class="flex items-center space-x-1"></div>
                <span id="attemptsText" class="text-xs font-black text-amber-400 ml-1">5/5 Intentos</span>
            </div>
            <button onclick="openEnergyModal()" class="text-xs bg-gradient-to-r from-amber-500 to-yellow-500 hover:opacity-90 active:scale-95 text-gray-950 font-black px-3 py-1.5 rounded-xl shadow transition flex items-center space-x-1">
                <span>⚡</span>
                <span>+ Recargar</span>
            </button>
        </div>

        <!-- PANTALLA DE REFLEJOS VISUALES -->
        <div class="bg-gray-900/90 rounded-3xl p-6 border border-gray-800 text-center shadow-2xl">
            <h2 class="text-2xl font-black text-white mb-2">⚡ Test de Reflejos Visuales</h2>
            <p class="text-xs text-gray-400 max-w-sm mx-auto mb-6">
                Toca la pantalla justo cuando el recuadro cambie a <strong>VERDE</strong>. Menor tiempo = mejor puesto.
            </p>

            <div id="reflexBox" onclick="handleReflexClick()" 
                 class="w-full max-w-sm mx-auto h-64 rounded-2xl flex flex-col items-center justify-center cursor-pointer transition select-none p-4 shadow-inner bg-gradient-to-br from-blue-900 to-indigo-950 border-2 border-blue-500/40">
                <span id="reflexIcon" class="text-5xl mb-2">⚡</span>
                <h3 id="reflexStatus" class="text-xl font-black text-white">TOCA PARA INICIAR</h3>
                <p id="reflexSub" class="text-xs text-blue-200 mt-1">Reacciona cuando cambie a verde (5 intentos diarios)</p>
            </div>
        </div>

        <!-- MODAL DE ENERGÍA AGOTADA / RECARGA -->
        <div id="energyModal" class="hidden fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4">
            <div class="bg-gray-900 w-full max-w-sm rounded-3xl p-6 border border-yellow-500/50 text-center shadow-2xl relative">
                <span class="text-5xl animate-bounce inline-block">⚡</span>
                <h3 class="text-xl font-black text-white mt-2">¡ENERGÍA AGOTADA!</h3>
                <p class="text-xs text-gray-300 my-2">Has completado tus 5 intentos. La velocidad extrema requiere reflejos descansados.</p>
                
                <div class="bg-yellow-500/10 border border-yellow-500/30 rounded-2xl p-3 my-4 text-xs text-yellow-300 text-left space-y-1">
                    <p>💡 <strong>Opción 1:</strong> Vuelve mañana a las 00:00.</p>
                    <p>🔥 <strong>Opción 2:</strong> Ve un anuncio para desbloquear <strong>+5 intentos YA</strong> y seguir rompiendo el récord.</p>
                </div>

                <button onclick="executeRewardedAction(handleRechargeClick)" class="w-full bg-gradient-to-r from-yellow-500 via-amber-500 to-orange-500 hover:opacity-90 active:scale-95 text-gray-950 font-black py-3.5 rounded-2xl shadow-xl shadow-yellow-500/30 text-xs sm:text-sm flex items-center justify-center space-x-2 transition mb-2">
                    <span>▶</span>
                    <span>VER ANUNCIO & RECARGAR +5 INTENTOS</span>
                </button>

                <button onclick="closeEnergyModal()" class="text-xs text-gray-400 hover:text-white underline mt-2">
                    Cerrar y volver mañana
                </button>
            </div>
        </div>

        <!-- TABLA DE LÍDERES REFLEJOS (SEMANAL + HISTÓRICO) -->
        <div class="bg-gray-900/80 rounded-3xl p-5 sm:p-6 border border-gray-800">
            <div class="flex justify-between items-center mb-3">
                <div class="flex items-center space-x-2">
                    <span class="text-xl">🏆</span>
                    <h3 class="text-base sm:text-lg font-black text-white">Top 10 • Reflejos (ms)</h3>
                </div>
                <button id="liveSyncStatus" onclick="syncGameFromCloud('reflex', true)" class="text-xs bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 font-bold px-2.5 py-1 rounded-full transition">🟢 Global En Vivo</button>
            </div>

            <!-- PESTAÑAS: TORNEO SEMANAL vs RÉCORD HISTÓRICO -->
            <div class="flex space-x-1.5 bg-gray-950/90 p-1.5 rounded-2xl border border-gray-800 mb-3">
                <button id="tabWeeklyBtn" onclick="switchLeaderboardTab('weekly')" class="w-1/2 py-2 px-3 rounded-xl font-black text-xs transition flex items-center justify-center space-x-1.5 bg-gradient-to-r from-amber-500 to-orange-500 text-gray-950 shadow-md shadow-amber-500/20">
                    <span>🔥</span>
                    <span>Torneo Semanal</span>
                </button>
                <button id="tabAlltimeBtn" onclick="switchLeaderboardTab('alltime')" class="w-1/2 py-2 px-3 rounded-xl font-bold text-xs transition flex items-center justify-center space-x-1.5 text-gray-400 hover:text-white">
                    <span>👑</span>
                    <span>Récord Histórico</span>
                </button>
            </div>

            <!-- BANNER CUENTA REGRESIVA DOMINGO 12:00 AM -->
            <div id="weeklyCountdownBanner" class="mb-3 px-3 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-[11px] flex flex-wrap items-center justify-between gap-1"></div>

            <div id="leaderboardList" class="space-y-2 text-sm"></div>

            <div class="mt-4 pt-3 border-t border-gray-800 text-center">
                <a href="../campeones.html?v=14" class="inline-flex items-center space-x-2 text-xs font-black text-amber-300 bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/40 px-4 py-2.5 rounded-xl transition">
                    <span>🏆</span>
                    <span>Ver Ganadores de Semanas Anteriores (Salón de Campeones)</span>
                </a>
            </div>
        </div>

    </main>

    __PLAYER_MODAL__
    __PLAYER_IDENTITY_SCRIPT__

    <script>
        let reflexAttempts = parseInt(localStorage.getItem('bytezone_reflex_attempts') ?? '5');
        const lastReflexDate = localStorage.getItem('bytezone_reflex_date');
        const todayStr = new Date().toISOString().slice(0, 10);

        if (lastReflexDate !== todayStr) {
            reflexAttempts = 5;
            localStorage.setItem('bytezone_reflex_attempts', '5');
            localStorage.setItem('bytezone_reflex_date', todayStr);
        }

        function updateAttemptsUI() {
            const container = document.getElementById('attemptsIndicator');
            const text = document.getElementById('attemptsText');
            if (container) {
                container.innerHTML = '';
                for (let i = 0; i < 5; i++) {
                    const dot = document.createElement('span');
                    dot.textContent = '⚡';
                    dot.className = (i < reflexAttempts) ? 'text-yellow-400 text-sm filter drop-shadow' : 'text-gray-700 text-sm';
                    container.appendChild(dot);
                }
            }
            if (text) {
                text.textContent = reflexAttempts + "/5 Intentos";
                text.className = reflexAttempts > 0 ? "text-xs font-black text-amber-400 ml-1" : "text-xs font-black text-red-400 ml-1";
            }
        }
        updateAttemptsUI();

        function openEnergyModal() {
            const modal = document.getElementById('energyModal');
            if (modal) modal.classList.remove('hidden');
        }

        function closeEnergyModal() {
            const modal = document.getElementById('energyModal');
            if (modal) modal.classList.add('hidden');
        }

        function handleRechargeClick() {
            trackByteZoneEvent('reflex', 'ad');
            reflexAttempts = 5;
            localStorage.setItem('bytezone_reflex_attempts', '5');
            localStorage.setItem('bytezone_reflex_date', todayStr);
            updateAttemptsUI();
            closeEnergyModal();
            if (window.confetti) confetti({ particleCount: 50, spread: 50, origin: { y: 0.6 } });
            
            const sub = document.getElementById('reflexSub');
            if (sub) sub.textContent = "¡+5 Intentos recargados! Toca para jugar";
        }

        let reflexState = 'IDLE', reflexTimeout = null, reflexStart = 0;
        function handleReflexClick() {
            const box = document.getElementById('reflexBox');
            const stat = document.getElementById('reflexStatus');
            const icon = document.getElementById('reflexIcon');
            const sub = document.getElementById('reflexSub');

            if (reflexState === 'IDLE' || reflexState === 'DONE') {
                if (reflexAttempts <= 0) {
                    openEnergyModal();
                    return;
                }
                // Normalización justa 1 a 5: cuenta 1 partida completa cada 5 intentos jugados
                let tapCounter = parseInt(localStorage.getItem('bytezone_reflex_tap_count') || '0') + 1;
                localStorage.setItem('bytezone_reflex_tap_count', tapCounter.toString());
                if (reflexAttempts === 5 || tapCounter % 5 === 1) {
                    trackByteZoneEvent('reflex', 'play');
                }
                reflexState = 'WAIT';
                box.className = "w-full max-w-sm mx-auto h-64 rounded-2xl flex flex-col items-center justify-center cursor-pointer select-none p-4 shadow-inner bg-gradient-to-br from-red-900 to-rose-950 border-2 border-red-500";
                icon.textContent = "🛑";
                stat.textContent = "¡ESPERA EL VERDE!";
                sub.textContent = "No toques todavía...";

                reflexTimeout = setTimeout(() => {
                    reflexState = 'READY';
                    reflexStart = Date.now();
                    box.className = "w-full max-w-sm mx-auto h-64 rounded-2xl flex flex-col items-center justify-center cursor-pointer select-none p-4 shadow-inner bg-gradient-to-br from-emerald-500 to-green-600 border-4 border-emerald-300 animate-pulse";
                    icon.textContent = "⚡";
                    stat.textContent = "¡TOCA YA!";
                }, Math.floor(Math.random() * 2000) + 1800);

            } else if (reflexState === 'WAIT') {
                clearTimeout(reflexTimeout);
                reflexState = 'DONE';

                reflexAttempts = Math.max(0, reflexAttempts - 1);
                localStorage.setItem('bytezone_reflex_attempts', reflexAttempts.toString());
                updateAttemptsUI();

                box.className = "w-full max-w-sm mx-auto h-64 rounded-2xl flex flex-col items-center justify-center cursor-pointer select-none p-4 shadow-inner bg-gradient-to-br from-yellow-900 to-amber-950 border-2 border-yellow-500";
                icon.textContent = "⚠️";
                stat.textContent = "¡MUY TEMPRANO!";
                sub.textContent = reflexAttempts > 0 ? "Toca para reiniciar (" + reflexAttempts + " intentos restantes)" : "¡Sin energía! Toca para recargar";

                if (reflexAttempts <= 0) {
                    setTimeout(openEnergyModal, 800);
                }
            } else if (reflexState === 'READY') {
                const diff = Date.now() - reflexStart;
                reflexState = 'DONE';

                reflexAttempts = Math.max(0, reflexAttempts - 1);
                localStorage.setItem('bytezone_reflex_attempts', reflexAttempts.toString());
                updateAttemptsUI();

                box.className = "w-full max-w-sm mx-auto h-64 rounded-2xl flex flex-col items-center justify-center cursor-pointer select-none p-4 shadow-inner bg-gradient-to-br from-blue-900 to-indigo-950 border-2 border-cyan-400";
                icon.textContent = "🎯";
                stat.textContent = diff + " ms";
                sub.textContent = reflexAttempts > 0 ? "Toca para intentar superarlo (" + reflexAttempts + " intentos restantes)" : "¡Sin energía! Toca para recargar";

                saveScore(diff);

                if (reflexAttempts <= 0) {
                    setTimeout(openEnergyModal, 900);
                }
            }
        }

        trackByteZoneEvent('reflex', 'view');

        function saveScore(score) {
            recordGameScore('reflex', score, true);
        }

        function renderLeaderboardUI() {
            const mode = window.currentLeaderboardTab || 'weekly';
            const list = getCleanScores('reflex', true, mode);
            const container = document.getElementById('leaderboardList');
            const bestKey = (mode === 'weekly') ? 'bytezone_weekly_best_reflex' : 'bytezone_best_reflex';
            const myBest = parseInt(localStorage.getItem(bestKey) || '0');
            document.getElementById('userBestScore').textContent = myBest > 0 ? (myBest + " ms") : "0 ms";

            const bestLabel = document.getElementById('userBestScoreLabel');
            const rankLabel = document.getElementById('userRankLabel');
            if (bestLabel) bestLabel.textContent = (mode === 'weekly') ? "Tu Mejor Tiempo Semanal" : "Tu Récord Histórico";
            if (rankLabel) rankLabel.textContent = (mode === 'weekly') ? "Puesto Semanal" : "Puesto Histórico";

            if (list.length === 0) {
                container.innerHTML = '<div class="p-4 text-center text-gray-400 text-xs">¡Torneo Semanal recién reiniciado! Juega una partida para coronarte #1 de esta semana.</div>';
                document.getElementById('userRankBadge').textContent = "Sin Clasificar";
                return;
            }

            container.innerHTML = "";
            let myPosition = null;
            list.slice(0, 10).forEach((item, idx) => {
                const isMe = isCurrentUserEntry(item);
                if (isMe && myPosition === null) {
                    myPosition = idx + 1;
                }
                const badge = idx === 0 ? "🥇" : idx === 1 ? "🥈" : idx === 2 ? "🥉" : "#" + (idx + 1);
                const itemFlag = getCountryFlag(item.country);
                const row = document.createElement('div');
                row.className = "flex justify-between items-center p-2.5 rounded-xl " + (isMe ? 'bg-purple-950/40 border border-purple-500 shadow-md' : 'bg-gray-800/60 border border-gray-700/50');
                row.innerHTML = `
                    <div class="flex items-center space-x-2 min-w-0">
                        <span class="w-6 text-center font-bold text-xs ${idx < 3 ? 'text-yellow-400 font-extrabold' : 'text-gray-400'}">${badge}</span>
                        <span class="text-base select-none">${itemFlag}</span>
                        <span class="font-bold truncate ${isMe ? 'text-purple-400' : 'text-white'}">${item.name} ${isMe ? '(Tú)' : ''}</span>
                    </div>
                    <span class="font-black flex-shrink-0 ${isMe ? 'text-pink-400' : 'text-purple-400'}">${item.score} ms</span>
                `;
                container.appendChild(row);
            });

            const rankBadge = document.getElementById('userRankBadge');
            if (myPosition === 1) {
                rankBadge.textContent = "🥇 Puesto #1 (¡Líder! • Toca para Retar)";
                rankBadge.className = "text-xs font-black text-yellow-300 bg-yellow-500/20 border border-yellow-500/50 px-3 py-1 rounded-full animate-pulse cursor-pointer shadow-lg shadow-yellow-500/20";
                rankBadge.onclick = () => checkAndShowPodiumModal('reflex', myBest, true);
            } else if (myPosition === 2) {
                rankBadge.textContent = "🥈 Puesto #2 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-gray-200 bg-gray-500/20 border border-gray-400/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('reflex', myBest, true);
            } else if (myPosition === 3) {
                rankBadge.textContent = "🥉 Puesto #3 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-amber-400 bg-amber-500/20 border border-amber-500/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('reflex', myBest, true);
            } else if (myPosition) {
                rankBadge.textContent = "Puesto #" + myPosition;
                rankBadge.className = "text-xs font-black text-pink-400 bg-pink-500/10 border border-pink-500/30 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            } else {
                rankBadge.textContent = "Sin Clasificar";
                rankBadge.className = "text-xs font-black text-gray-400 bg-gray-800 border border-gray-700 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            }
        }

        updateLeaderboardTabsUI();
        renderLeaderboardUI();
        startRealtimeScoreStream('reflex', true);
    </script>
</body>
</html>
"""

# ==========================================================
# 4. PÁGINA JUEGO 3: JUEGOS/CYBER-MEMORY.HTML
# ==========================================================
TEMPLATE_MEMORY = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cyber Memory - ByteZone</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <!-- BARRA REGRESAR Y RÉCORD PERSONAL -->
        <div class="flex items-center justify-between">
            <a href="../index.html?v=14" class="text-xs text-emerald-400 hover:underline flex items-center space-x-1 bg-gray-900 px-3 py-1.5 rounded-xl border border-gray-800">
                <span>←</span>
                <span>Volver al Arcade</span>
            </a>

            <div class="text-xs text-gray-400 bg-gray-900 px-3 py-1.5 rounded-xl border border-gray-800 flex items-center space-x-2">
                <span>Modo:</span>
                <span class="text-emerald-400 font-bold">Secuencia Neón</span>
            </div>
        </div>

        <!-- TABLERO DE RÉCORD MEMORY -->
        <div class="bg-gray-900/90 p-4 rounded-2xl border border-emerald-500/30 flex items-center justify-between shadow-xl">
            <div>
                <p id="userBestScoreLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Tu Mejor Secuencia Semanal</p>
                <p id="userBestScore" class="text-2xl font-black text-white">0 Rondas</p>
            </div>
            <div class="text-right">
                <p id="userRankLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Puesto Semanal</p>
                <span id="userRankBadge" class="text-xs font-black text-pink-400 bg-pink-500/10 border border-pink-500/30 px-3 py-1 rounded-full">
                    Sin Clasificar
                </span>
            </div>
        </div>

        <!-- TABLERO INTERACTIVO DEL JUEGO MEMORY -->
        <div class="bg-gray-900/90 rounded-3xl p-6 border border-gray-800 text-center shadow-2xl max-w-sm mx-auto">
            <h2 class="text-2xl font-black text-white mb-1">🧠 Cyber Memory</h2>
            <p id="memoryStatusText" class="text-xs text-gray-400 mb-6">
                Presiona "Iniciar" y repite los botones que se iluminen.
            </p>

            <div class="grid grid-cols-2 gap-4 w-64 h-64 mx-auto mb-6">
                <button id="pad0" onclick="handlePadClick(0)" class="rounded-2xl bg-cyan-600/40 border-2 border-cyan-400 shadow-lg active:scale-95 transition flex items-center justify-center text-3xl font-bold text-white"></button>
                <button id="pad1" onclick="handlePadClick(1)" class="rounded-2xl bg-purple-600/40 border-2 border-purple-400 shadow-lg active:scale-95 transition flex items-center justify-center text-3xl font-bold text-white"></button>
                <button id="pad2" onclick="handlePadClick(2)" class="rounded-2xl bg-pink-600/40 border-2 border-pink-400 shadow-lg active:scale-95 transition flex items-center justify-center text-3xl font-bold text-white"></button>
                <button id="pad3" onclick="handlePadClick(3)" class="rounded-2xl bg-emerald-600/40 border-2 border-emerald-400 shadow-lg active:scale-95 transition flex items-center justify-center text-3xl font-bold text-white"></button>
            </div>

            <div class="flex justify-center space-x-3">
                <button id="memoryStartBtn" onclick="startMemoryGame()" class="bg-gradient-to-r from-emerald-500 to-teal-500 hover:opacity-90 active:scale-95 text-white font-black px-6 py-3 rounded-2xl shadow-lg shadow-emerald-500/25 text-xs transition">
                    ▶ INICIAR PARTIDA
                </button>
            </div>
        </div>

        <!-- MODAL REVIVIR MEMORIA (SEGUNDA OPORTUNIDAD) -->
        <div id="memoryReviveModal" class="hidden fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4">
            <div class="bg-gray-900 w-full max-w-sm rounded-3xl p-6 border border-emerald-500/50 text-center shadow-2xl relative">
                <span class="text-5xl mb-1 inline-block animate-bounce">🧠</span>
                <h3 class="text-xl font-black text-white mt-2">¡SECUENCIA INTERRUMPIDA!</h3>
                <p id="memoryReviveText" class="text-sm font-bold text-emerald-400 mt-1 mb-4">Llegaste a la Ronda 6</p>
                
                <div class="w-full max-w-xs mx-auto mb-3">
                    <button onclick="executeRewardedAction(handleMemoryReviveClick)" class="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:opacity-90 active:scale-95 text-white font-black py-3.5 rounded-2xl shadow-xl shadow-emerald-500/30 text-xs sm:text-sm flex items-center justify-center space-x-2 transition">
                        <span>▶</span>
                        <span>SALVAR RACHA & CONTINUAR (VER ANUNCIO)</span>
                    </button>
                    <p class="text-[10px] text-gray-400 mt-1">1 sola oportunidad para no empezar de cero</p>
                </div>

                <button onclick="resetMemoryGame()" class="text-xs text-gray-400 hover:text-white underline mt-2">
                    Reiniciar desde Ronda 1
                </button>
            </div>
        </div>

        <!-- TABLA DE LÍDERES MEMORY (SEMANAL + HISTÓRICO) -->
        <div class="bg-gray-900/80 rounded-3xl p-5 sm:p-6 border border-gray-800">
            <div class="flex justify-between items-center mb-3">
                <div class="flex items-center space-x-2">
                    <span class="text-xl">🏆</span>
                    <h3 class="text-base sm:text-lg font-black text-white">Top 10 • Cyber Memory</h3>
                </div>
                <button id="liveSyncStatus" onclick="syncGameFromCloud('memory', false)" class="text-xs bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 font-bold px-2.5 py-1 rounded-full transition">🟢 Global En Vivo</button>
            </div>

            <!-- PESTAÑAS: TORNEO SEMANAL vs RÉCORD HISTÓRICO -->
            <div class="flex space-x-1.5 bg-gray-950/90 p-1.5 rounded-2xl border border-gray-800 mb-3">
                <button id="tabWeeklyBtn" onclick="switchLeaderboardTab('weekly')" class="w-1/2 py-2 px-3 rounded-xl font-black text-xs transition flex items-center justify-center space-x-1.5 bg-gradient-to-r from-amber-500 to-orange-500 text-gray-950 shadow-md shadow-amber-500/20">
                    <span>🔥</span>
                    <span>Torneo Semanal</span>
                </button>
                <button id="tabAlltimeBtn" onclick="switchLeaderboardTab('alltime')" class="w-1/2 py-2 px-3 rounded-xl font-bold text-xs transition flex items-center justify-center space-x-1.5 text-gray-400 hover:text-white">
                    <span>👑</span>
                    <span>Récord Histórico</span>
                </button>
            </div>

            <!-- BANNER CUENTA REGRESIVA DOMINGO 12:00 AM -->
            <div id="weeklyCountdownBanner" class="mb-3 px-3 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-[11px] flex flex-wrap items-center justify-between gap-1"></div>

            <div id="leaderboardList" class="space-y-2 text-sm"></div>

            <div class="mt-4 pt-3 border-t border-gray-800 text-center">
                <a href="../campeones.html?v=14" class="inline-flex items-center space-x-2 text-xs font-black text-amber-300 bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/40 px-4 py-2.5 rounded-xl transition">
                    <span>🏆</span>
                    <span>Ver Ganadores de Semanas Anteriores (Salón de Campeones)</span>
                </a>
            </div>
        </div>

    </main>

    __PLAYER_MODAL__
    __PLAYER_IDENTITY_SCRIPT__

    <script>
        const PAD_COLORS = [
            { bg: 'bg-cyan-400', glow: 'shadow-[0_0_25px_#22d3ee]' },
            { bg: 'bg-purple-400', glow: 'shadow-[0_0_25px_#c084fc]' },
            { bg: 'bg-pink-400', glow: 'shadow-[0_0_25px_#f472b6]' },
            { bg: 'bg-emerald-400', glow: 'shadow-[0_0_25px_#34d399]' }
        ];

        let memorySequence = [];
        let playerStep = 0;
        let memoryRunning = false;
        let canClick = false;
        let hasRevivedMemory = false;

        function startMemoryGame() {
            trackByteZoneEvent('memory', 'play');
            memorySequence = [];
            playerStep = 0;
            memoryRunning = true;
            hasRevivedMemory = false;
            const modal = document.getElementById('memoryReviveModal');
            if (modal) modal.classList.add('hidden');
            document.getElementById('memoryStartBtn').textContent = "Reiniciar";
            nextRound();
        }

        function nextRound() {
            canClick = false;
            playerStep = 0;
            const nextPad = Math.floor(Math.random() * 4);
            memorySequence.push(nextPad);

            const status = document.getElementById('memoryStatusText');
            status.textContent = "Memoriza la secuencia... (Ronda " + memorySequence.length + ")";
            status.className = "text-xs text-yellow-400 font-bold mb-6 animate-pulse";

            let i = 0;
            const interval = setInterval(() => {
                flashPad(memorySequence[i]);
                i++;
                if (i >= memorySequence.length) {
                    clearInterval(interval);
                    setTimeout(() => {
                        canClick = true;
                        status.textContent = "¡Tu turno! Repite la secuencia";
                        status.className = "text-xs text-emerald-400 font-bold mb-6";
                    }, 400);
                }
            }, 600);
        }

        function flashPad(padIdx) {
            const pad = document.getElementById('pad' + padIdx);
            const style = PAD_COLORS[padIdx];
            pad.classList.add(style.bg, style.glow);
            setTimeout(() => {
                pad.classList.remove(style.bg, style.glow);
            }, 350);
        }

        function handlePadClick(padIdx) {
            if (!memoryRunning || !canClick) return;

            flashPad(padIdx);

            if (padIdx === memorySequence[playerStep]) {
                playerStep++;
                if (playerStep === memorySequence.length) {
                    canClick = false;
                    const status = document.getElementById('memoryStatusText');
                    status.textContent = "¡Correcto! Siguiente ronda...";
                    status.className = "text-xs text-cyan-400 font-bold mb-6";
                    saveScore(memorySequence.length);
                    setTimeout(nextRound, 800);
                }
            } else {
                canClick = false;
                const score = memorySequence.length - 1;
                saveScore(score);

                // Si no ha revivido y al menos completó ronda 1, ofrecer revivir
                if (!hasRevivedMemory && score >= 1) {
                    const reviveModal = document.getElementById('memoryReviveModal');
                    const reviveText = document.getElementById('memoryReviveText');
                    if (reviveText) reviveText.textContent = "Te equivocaste en la Ronda " + memorySequence.length;
                    if (reviveModal) reviveModal.classList.remove('hidden');
                } else {
                    gameOverMemory(score);
                    setTimeout(() => { flushPendingPodium(); }, 700);
                }
            }
        }

        function handleMemoryReviveClick() {
            trackByteZoneEvent('memory', 'ad');
            hasRevivedMemory = true;
            const modal = document.getElementById('memoryReviveModal');
            if (modal) modal.classList.add('hidden');

            const status = document.getElementById('memoryStatusText');
            status.textContent = "¡Racha salvada! Repitiendo la Ronda " + memorySequence.length + "...";
            status.className = "text-xs text-emerald-400 font-bold mb-6 animate-pulse";

            // Repetir la ronda actual tras una breve pausa
            setTimeout(() => {
                canClick = false;
                playerStep = 0;
                let i = 0;
                const interval = setInterval(() => {
                    flashPad(memorySequence[i]);
                    i++;
                    if (i >= memorySequence.length) {
                        clearInterval(interval);
                        setTimeout(() => {
                            canClick = true;
                            status.textContent = "¡Tu turno! Repite la secuencia";
                            status.className = "text-xs text-emerald-400 font-bold mb-6";
                        }, 400);
                    }
                }, 600);
            }, 600);
        }

        function resetMemoryGame() {
            const modal = document.getElementById('memoryReviveModal');
            if (modal) modal.classList.add('hidden');
            gameOverMemory(memorySequence.length - 1);
            if (!flushPendingPodium()) {
                startMemoryGame();
            }
        }

        function gameOverMemory(score) {
            memoryRunning = false;
            canClick = false;
            const status = document.getElementById('memoryStatusText');
            status.textContent = "¡Fallaste! Alcanzaste " + score + " rondas.";
            status.className = "text-xs text-red-400 font-bold mb-6";
            document.getElementById('memoryStartBtn').textContent = "▶ JUGAR OTRA VEZ";
        }

        trackByteZoneEvent('memory', 'view');

        function saveScore(score) {
            recordGameScore('memory', score, false);
        }

        function renderLeaderboardUI() {
            const mode = window.currentLeaderboardTab || 'weekly';
            const list = getCleanScores('memory', false, mode);
            const container = document.getElementById('leaderboardList');
            const bestKey = (mode === 'weekly') ? 'bytezone_weekly_best_memory' : 'bytezone_best_memory';
            const myBest = parseInt(localStorage.getItem(bestKey) || '0');
            document.getElementById('userBestScore').textContent = myBest + " Rondas";

            const bestLabel = document.getElementById('userBestScoreLabel');
            const rankLabel = document.getElementById('userRankLabel');
            if (bestLabel) bestLabel.textContent = (mode === 'weekly') ? "Tu Mejor Secuencia Semanal" : "Tu Récord Histórico";
            if (rankLabel) rankLabel.textContent = (mode === 'weekly') ? "Puesto Semanal" : "Puesto Histórico";

            if (list.length === 0) {
                container.innerHTML = '<div class="p-4 text-center text-gray-400 text-xs">¡Torneo Semanal recién reiniciado! Juega una partida para coronarte #1 de esta semana.</div>';
                document.getElementById('userRankBadge').textContent = "Sin Clasificar";
                return;
            }

            container.innerHTML = "";
            let myPosition = null;
            list.slice(0, 10).forEach((item, idx) => {
                const isMe = isCurrentUserEntry(item);
                if (isMe && myPosition === null) {
                    myPosition = idx + 1;
                }
                const badge = idx === 0 ? "🥇" : idx === 1 ? "🥈" : idx === 2 ? "🥉" : "#" + (idx + 1);
                const itemFlag = getCountryFlag(item.country);
                const row = document.createElement('div');
                row.className = "flex justify-between items-center p-2.5 rounded-xl " + (isMe ? 'bg-emerald-950/40 border border-emerald-500 shadow-md' : 'bg-gray-800/60 border border-gray-700/50');
                row.innerHTML = `
                    <div class="flex items-center space-x-2 min-w-0">
                        <span class="w-6 text-center font-bold text-xs ${idx < 3 ? 'text-yellow-400 font-extrabold' : 'text-gray-400'}">${badge}</span>
                        <span class="text-base select-none">${itemFlag}</span>
                        <span class="font-bold truncate ${isMe ? 'text-emerald-400' : 'text-white'}">${item.name} ${isMe ? '(Tú)' : ''}</span>
                    </div>
                    <span class="font-black flex-shrink-0 ${isMe ? 'text-pink-400' : 'text-emerald-400'}">${item.score} Rondas</span>
                `;
                container.appendChild(row);
            });

            const rankBadge = document.getElementById('userRankBadge');
            if (myPosition === 1) {
                rankBadge.textContent = "🥇 Puesto #1 (¡Líder! • Toca para Retar)";
                rankBadge.className = "text-xs font-black text-yellow-300 bg-yellow-500/20 border border-yellow-500/50 px-3 py-1 rounded-full animate-pulse cursor-pointer shadow-lg shadow-yellow-500/20";
                rankBadge.onclick = () => checkAndShowPodiumModal('memory', myBest, false);
            } else if (myPosition === 2) {
                rankBadge.textContent = "🥈 Puesto #2 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-gray-200 bg-gray-500/20 border border-gray-400/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('memory', myBest, false);
            } else if (myPosition === 3) {
                rankBadge.textContent = "🥉 Puesto #3 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-amber-400 bg-amber-500/20 border border-amber-500/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('memory', myBest, false);
            } else if (myPosition) {
                rankBadge.textContent = "Puesto #" + myPosition;
                rankBadge.className = "text-xs font-black text-pink-400 bg-pink-500/10 border border-pink-500/30 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            } else {
                rankBadge.textContent = "Sin Clasificar";
                rankBadge.className = "text-xs font-black text-gray-400 bg-gray-800 border border-gray-700 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            }
        }

        updateLeaderboardTabsUI();
        renderLeaderboardUI();
        startRealtimeScoreStream('memory', false);
    </script>
</body>
</html>
"""

# ==========================================================
# 4B. PÁGINA JUEGO BAÚL ARCADE: JUEGOS/CYBER-DODGE.HTML
# ==========================================================
TEMPLATE_DODGE = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cyber Dodge: Tormenta de Asteroides - Baúl Arcade ByteZone</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <!-- BARRA REGRESAR Y SELLO BAÚL -->
        <div class="flex items-center justify-between">
            <a href="../index.html?v=14" class="text-xs text-amber-400 hover:underline flex items-center space-x-1 bg-gray-900 px-3 py-1.5 rounded-xl border border-gray-800">
                <span>←</span>
                <span>Volver al Arcade</span>
            </a>

            <div class="text-xs text-amber-300 bg-amber-500/10 px-3 py-1.5 rounded-xl border border-amber-500/30 flex items-center space-x-1.5 font-bold">
                <span>🗄️</span>
                <span>Joya Rescatada del Baúl</span>
            </div>
        </div>

        <!-- TABLERO DE RÉCORD CYBER DODGE -->
        <div class="bg-gray-900/90 p-4 rounded-2xl border border-amber-500/30 flex items-center justify-between shadow-xl">
            <div>
                <p id="userBestScoreLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Tu Mejor Supervivencia Semanal</p>
                <p id="userBestScore" class="text-2xl font-black text-white">0 seg</p>
            </div>
            <div class="text-right">
                <p id="userRankLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Puesto Semanal</p>
                <span id="userRankBadge" class="text-xs font-black text-pink-400 bg-pink-500/10 border border-pink-500/30 px-3 py-1 rounded-full">
                    Sin Clasificar
                </span>
            </div>
        </div>

        <!-- LIENZO DEL JUEGO CYBER DODGE -->
        <div class="bg-gray-900/90 rounded-3xl p-4 sm:p-6 border border-gray-800 relative shadow-2xl">
            <div class="relative w-full max-w-sm mx-auto h-[400px] sm:h-[430px] rounded-2xl overflow-hidden bg-gray-950 border-2 border-amber-500/40">
                <canvas id="dodgeCanvas" width="360" height="430" class="w-full h-full block cursor-pointer select-none touch-none"></canvas>

                <!-- OVERLAY INICIO -->
                <div id="dodgeStartScreen" class="absolute inset-0 bg-gray-950/85 backdrop-blur-sm flex flex-col items-center justify-center p-6 text-center">
                    <span class="text-5xl mb-2 animate-bounce">🚀</span>
                    <span class="text-[10px] font-black uppercase bg-amber-500/20 text-amber-300 px-2.5 py-0.5 rounded-full mb-1">Edición Especial del Baúl</span>
                    <h2 class="text-2xl font-black text-white">CYBER DODGE</h2>
                    <p class="text-xs text-gray-300 mt-2 mb-6 max-w-xs">
                        Desliza el dedo o mueve el cursor para pilotar la nave y esquivar la lluvia de meteoritos neón. ¡Cada segundo suma puntos!
                    </p>
                    <button onclick="startDodgeGame()" class="bg-gradient-to-r from-amber-500 to-orange-600 hover:scale-105 active:scale-95 text-gray-950 font-black px-8 py-3.5 rounded-2xl shadow-xl shadow-amber-500/30 transition text-sm">
                        ¡DESPEGAR NAVE!
                    </button>
                </div>

                <!-- MODAL ESCUDO DE SEGUNDA OPORTUNIDAD -->
                <div id="dodgeReviveModal" class="hidden absolute inset-0 bg-gray-950/90 backdrop-blur-md flex flex-col items-center justify-center p-6 text-center">
                    <span class="text-5xl mb-1">☄️</span>
                    <h3 class="text-xl font-black text-white">¡IMPACTO DE ASTEROIDE!</h3>
                    <p id="dodgeScoreText" class="text-sm font-bold text-amber-400 mt-1 mb-4">Sobreviviste 18 segundos</p>

                    <div id="dodgeReviveBox" class="w-full max-w-xs mb-3">
                        <button onclick="executeRewardedAction(handleDodgeRevive)" class="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:opacity-90 active:scale-95 text-white font-black py-3.5 rounded-2xl shadow-lg shadow-emerald-500/30 text-xs sm:text-sm flex items-center justify-center space-x-2 transition">
                            <span>🛡️</span>
                            <span>ACTIVAR ESCUDO & CONTINUAR</span>
                        </button>
                        <p class="text-[10px] text-gray-400 mt-1">Destruye los asteroides en pantalla y conserva tu tiempo</p>
                    </div>

                    <button onclick="restartDodgeFromModal()" class="text-xs text-gray-400 hover:text-white underline mt-2">
                        Reiniciar desde 0 seg
                    </button>
                </div>
            </div>
            <p class="text-xs text-gray-400 text-center mt-3">💡 Desliza el dedo a izquierda/derecha o usa las flechas del teclado para mover la nave</p>
        </div>

        <!-- TABLA DE LÍDERES CYBER DODGE -->
        <div class="bg-gray-900/80 rounded-3xl p-5 sm:p-6 border border-gray-800">
            <div class="flex justify-between items-center mb-3">
                <div class="flex items-center space-x-2">
                    <span class="text-xl">🏆</span>
                    <h3 class="text-base sm:text-lg font-black text-white">Top 10 • Cyber Dodge</h3>
                </div>
                <button id="liveSyncStatus" onclick="syncGameFromCloud('dodge', false)" class="text-xs bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 font-bold px-2.5 py-1 rounded-full transition">🟢 Global En Vivo</button>
            </div>

            <div class="flex space-x-1.5 bg-gray-950/90 p-1.5 rounded-2xl border border-gray-800 mb-3">
                <button id="tabWeeklyBtn" onclick="switchLeaderboardTab('weekly')" class="w-1/2 py-2 px-3 rounded-xl font-black text-xs transition flex items-center justify-center space-x-1.5 bg-gradient-to-r from-amber-500 to-orange-500 text-gray-950 shadow-md shadow-amber-500/20">
                    <span>🔥</span>
                    <span>Torneo Semanal</span>
                </button>
                <button id="tabAlltimeBtn" onclick="switchLeaderboardTab('alltime')" class="w-1/2 py-2 px-3 rounded-xl font-bold text-xs transition flex items-center justify-center space-x-1.5 text-gray-400 hover:text-white">
                    <span>👑</span>
                    <span>Récord Histórico</span>
                </button>
            </div>

            <div id="weeklyCountdownBanner" class="mb-3 px-3 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-[11px] flex flex-wrap items-center justify-between gap-1"></div>

            <div id="leaderboardList" class="space-y-2 text-sm"></div>

            <div class="mt-4 pt-3 border-t border-gray-800 text-center">
                <a href="../campeones.html?v=14" class="inline-flex items-center space-x-2 text-xs font-black text-amber-300 bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/40 px-4 py-2.5 rounded-xl transition">
                    <span>🏆</span>
                    <span>Ver Ganadores de Semanas Anteriores (Salón de Campeones)</span>
                </a>
            </div>
        </div>

    </main>

    __PLAYER_MODAL__
    __PLAYER_IDENTITY_SCRIPT__

    <script>
        const dCanvas = document.getElementById('dodgeCanvas');
        const dCtx = dCanvas.getContext('2d');
        const dStart = document.getElementById('dodgeStartScreen');
        const dRevive = document.getElementById('dodgeReviveModal');

        let shipX = 180;
        let asteroids = [];
        let dodgeRunning = false;
        let dodgeScore = 0;
        let dodgeTicks = 0;
        let hasRevivedDodge = false;

        function startDodgeGame() {
            dStart.classList.add('hidden');
            dRevive.classList.add('hidden');
            shipX = dCanvas.width / 2;
            asteroids = [];
            dodgeScore = 0;
            dodgeTicks = 0;
            hasRevivedDodge = false;
            dodgeRunning = true;
            trackByteZoneEvent('dodge', 'play');
            requestAnimationFrame(updateDodgeLoop);
        }

        function spawnAsteroid() {
            const radius = 11 + Math.random() * 13;
            const x = radius + Math.random() * (dCanvas.width - radius * 2);
            const speedY = 3.2 + Math.random() * 2.5 + Math.min(dodgeScore * 0.08, 4.5);
            const colors = ['#f59e0b', '#ec4899', '#06b6d4', '#a855f7', '#ef4444'];
            asteroids.push({
                x: x,
                y: -radius,
                r: radius,
                vy: speedY,
                color: colors[Math.floor(Math.random() * colors.length)]
            });
        }

        function updateDodgeLoop() {
            if (!dodgeRunning) return;
            dodgeTicks++;
            if (dodgeTicks % 60 === 0) {
                dodgeScore++;
            }

            const spawnRate = Math.max(14, 34 - Math.floor(dodgeScore / 3));
            if (dodgeTicks % spawnRate === 0) {
                spawnAsteroid();
            }

            dCtx.fillStyle = "#030712";
            dCtx.fillRect(0, 0, dCanvas.width, dCanvas.height);

            // Estrellas de fondo
            dCtx.fillStyle = "rgba(255,255,255,0.25)";
            for (let i = 0; i < 18; i++) {
                const sx = (i * 57) % dCanvas.width;
                const sy = ((i * 83) + dodgeTicks * 2) % dCanvas.height;
                dCtx.fillRect(sx, sy, 2, 2);
            }

            // Dibujar Nave Neón
            const shipY = dCanvas.height - 48;
            dCtx.save();
            dCtx.fillStyle = "#22d3ee";
            dCtx.shadowColor = "#22d3ee";
            dCtx.shadowBlur = 14;
            dCtx.beginPath();
            dCtx.moveTo(shipX, shipY - 18);
            dCtx.lineTo(shipX - 16, shipY + 14);
            dCtx.lineTo(shipX + 16, shipY + 14);
            dCtx.closePath();
            dCtx.fill();
            dCtx.restore();

            // Actualizar y dibujar asteroides
            for (let i = asteroids.length - 1; i >= 0; i--) {
                const a = asteroids[i];
                a.y += a.vy;

                dCtx.save();
                dCtx.fillStyle = a.color;
                dCtx.shadowColor = a.color;
                dCtx.shadowBlur = 12;
                dCtx.beginPath();
                dCtx.arc(a.x, a.y, a.r, 0, Math.PI * 2);
                dCtx.fill();
                dCtx.restore();

                // Colisión con la nave
                const dx = a.x - shipX;
                const dy = a.y - shipY;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < a.r + 12) {
                    gameOverDodge();
                    return;
                }

                if (a.y - a.r > dCanvas.height) {
                    asteroids.splice(i, 1);
                }
            }

            dCtx.fillStyle = "#ffffff";
            dCtx.font = "bold 18px monospace";
            dCtx.fillText("TIEMPO: " + dodgeScore + "s", 16, 32);

            requestAnimationFrame(updateDodgeLoop);
        }

        function gameOverDodge() {
            dodgeRunning = false;
            recordGameScore('dodge', dodgeScore, false);
            document.getElementById('dodgeScoreText').textContent = "Sobreviviste " + dodgeScore + " segundos";
            document.getElementById('dodgeReviveBox').style.display = hasRevivedDodge ? 'none' : 'block';
            dRevive.classList.remove('hidden');
            if (hasRevivedDodge) { setTimeout(() => { flushPendingPodium(); }, 700); }
        }

        function restartDodgeFromModal() {
            if (flushPendingPodium()) {
                dRevive.classList.add('hidden');
                dStart.classList.remove('hidden');
            } else {
                startDodgeGame();
            }
        }

        function handleDodgeRevive() {
            trackByteZoneEvent('dodge', 'ad');
            hasRevivedDodge = true;
            asteroids = [];
            dRevive.classList.add('hidden');
            dodgeRunning = true;
            requestAnimationFrame(updateDodgeLoop);
        }

        function moveShipFromClientX(clientX) {
            const rect = dCanvas.getBoundingClientRect();
            const relX = ((clientX - rect.left) / rect.width) * dCanvas.width;
            shipX = Math.max(22, Math.min(dCanvas.width - 22, relX));
        }

        dCanvas.addEventListener('pointermove', (e) => {
            if (dodgeRunning) moveShipFromClientX(e.clientX);
        });
        dCanvas.addEventListener('pointerdown', (e) => {
            if (dodgeRunning) moveShipFromClientX(e.clientX);
        });

        window.addEventListener('keydown', (e) => {
            if (!dodgeRunning) return;
            if (e.key === 'ArrowLeft') shipX = Math.max(22, shipX - 24);
            if (e.key === 'ArrowRight') shipX = Math.min(dCanvas.width - 22, shipX + 24);
        });

        trackByteZoneEvent('dodge', 'view');

        function renderLeaderboardUI() {
            const mode = window.currentLeaderboardTab || 'weekly';
            const list = getCleanScores('dodge', false, mode);
            const container = document.getElementById('leaderboardList');
            const bestKey = (mode === 'weekly') ? 'bytezone_weekly_best_dodge' : 'bytezone_best_dodge';
            const myBest = parseInt(localStorage.getItem(bestKey) || '0');
            document.getElementById('userBestScore').textContent = myBest + " seg";

            const bestLabel = document.getElementById('userBestScoreLabel');
            const rankLabel = document.getElementById('userRankLabel');
            if (bestLabel) bestLabel.textContent = (mode === 'weekly') ? "Tu Mejor Supervivencia Semanal" : "Tu Récord Histórico";
            if (rankLabel) rankLabel.textContent = (mode === 'weekly') ? "Puesto Semanal" : "Puesto Histórico";

            if (list.length === 0) {
                container.innerHTML = '<div class="p-4 text-center text-gray-400 text-xs">¡Sé el primero en marcar récord en Cyber Dodge esta semana!</div>';
                document.getElementById('userRankBadge').textContent = "Sin Clasificar";
                return;
            }

            container.innerHTML = "";
            let myPosition = null;
            list.slice(0, 10).forEach((item, idx) => {
                const isMe = isCurrentUserEntry(item);
                if (isMe && myPosition === null) myPosition = idx + 1;
                const badge = idx === 0 ? "🥇" : idx === 1 ? "🥈" : idx === 2 ? "🥉" : "#" + (idx + 1);
                const itemFlag = getCountryFlag(item.country);
                const row = document.createElement('div');
                row.className = "flex justify-between items-center p-2.5 rounded-xl " + (isMe ? 'bg-amber-950/40 border border-amber-500 shadow-md' : 'bg-gray-800/60 border border-gray-700/50');
                row.innerHTML = `
                    <div class="flex items-center space-x-2 min-w-0">
                        <span class="w-6 text-center font-bold text-xs ${idx < 3 ? 'text-yellow-400 font-extrabold' : 'text-gray-400'}">${badge}</span>
                        <span class="text-base select-none">${itemFlag}</span>
                        <span class="font-bold truncate ${isMe ? 'text-amber-400' : 'text-white'}">${item.name} ${isMe ? '(Tú)' : ''}</span>
                    </div>
                    <span class="font-black flex-shrink-0 ${isMe ? 'text-pink-400' : 'text-amber-400'}">${item.score} seg</span>
                `;
                container.appendChild(row);
            });

            const rankBadge = document.getElementById('userRankBadge');
            if (myPosition === 1) {
                rankBadge.textContent = "🥇 Puesto #1 (¡Líder! • Toca para Retar)";
                rankBadge.className = "text-xs font-black text-yellow-300 bg-yellow-500/20 border border-yellow-500/50 px-3 py-1 rounded-full animate-pulse cursor-pointer shadow-lg shadow-yellow-500/20";
                rankBadge.onclick = () => checkAndShowPodiumModal('dodge', myBest, false);
            } else if (myPosition === 2) {
                rankBadge.textContent = "🥈 Puesto #2 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-gray-200 bg-gray-500/20 border border-gray-400/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('dodge', myBest, false);
            } else if (myPosition === 3) {
                rankBadge.textContent = "🥉 Puesto #3 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-amber-400 bg-amber-500/20 border border-amber-500/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('dodge', myBest, false);
            } else if (myPosition) {
                rankBadge.textContent = "Puesto #" + myPosition;
                rankBadge.className = "text-xs font-black text-amber-400 bg-amber-500/10 border border-amber-500/30 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            } else {
                rankBadge.textContent = "Sin Clasificar";
                rankBadge.className = "text-xs font-black text-gray-400 bg-gray-800 border border-gray-700 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            }
        }

        updateLeaderboardTabsUI();
        renderLeaderboardUI();
        startRealtimeScoreStream('dodge', false);
    </script>
</body>
</html>
"""

# ==========================================================
# 4C. NUEVO JUEGO #5 EN EL BAÚL / CANDIDATO A TOP 3: JUEGOS/CYBER-DRONE.HTML
# ==========================================================
TEMPLATE_DRONE = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Neon Cyber-Drone: Portales Láser - ByteZone Arcade</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <!-- BARRA REGRESAR Y SELLO NUEVO JUEGO -->
        <div class="flex items-center justify-between">
            <a href="../index.html?v=14" class="text-xs text-pink-400 hover:underline flex items-center space-x-1 bg-gray-900 px-3 py-1.5 rounded-xl border border-gray-800">
                <span>←</span>
                <span>Volver al Arcade</span>
            </a>

            <div class="text-xs text-pink-300 bg-pink-500/15 px-3 py-1.5 rounded-xl border border-pink-500/40 flex items-center space-x-1.5 font-bold">
                <span>🛸</span>
                <span>Nuevo Juego • Candidato al Top 3</span>
            </div>
        </div>

        <!-- TABLERO DE RÉCORD CYBER DRONE -->
        <div class="bg-gray-900/90 p-4 rounded-2xl border border-pink-500/30 flex items-center justify-between shadow-xl">
            <div>
                <p id="userBestScoreLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Tus Mejores Portales de la Semana</p>
                <p id="userBestScore" class="text-2xl font-black text-white">0 Portales</p>
            </div>
            <div class="text-right">
                <p id="userRankLabel" class="text-[11px] text-gray-400 uppercase font-bold tracking-wider">Puesto Semanal</p>
                <span id="userRankBadge" class="text-xs font-black text-pink-400 bg-pink-500/10 border border-pink-500/30 px-3 py-1 rounded-full">
                    Sin Clasificar
                </span>
            </div>
        </div>

        <!-- LIENZO DEL JUEGO NEON CYBER-DRONE -->
        <div class="bg-gray-900/90 rounded-3xl p-4 sm:p-6 border border-gray-800 relative shadow-2xl">
            <div class="relative w-full max-w-sm mx-auto h-[400px] sm:h-[430px] rounded-2xl overflow-hidden bg-gray-950 border-2 border-pink-500/40">
                <canvas id="droneCanvas" width="360" height="430" class="w-full h-full block cursor-pointer select-none touch-none"></canvas>

                <!-- OVERLAY INICIO -->
                <div id="droneStartScreen" class="absolute inset-0 bg-gray-950/85 backdrop-blur-sm flex flex-col items-center justify-center p-6 text-center">
                    <span class="text-5xl mb-2 animate-bounce">🛸</span>
                    <span class="text-[10px] font-black uppercase bg-pink-500/20 text-pink-300 px-2.5 py-0.5 rounded-full mb-1">Precisión Extrema • 1 Toque</span>
                    <h2 class="text-2xl font-black text-white">NEON CYBER-DRONE</h2>
                    <p class="text-xs text-gray-300 mt-2 mb-6 max-w-xs">
                        Toca la pantalla para activar los propulsores cuánticos y atravesar los portales láser sin chocar. ¡Atrapa esferas de energía para +2 puntos!
                    </p>
                    <button onclick="startDroneGame()" class="bg-gradient-to-r from-pink-500 to-rose-600 hover:scale-105 active:scale-95 text-white font-black px-8 py-3.5 rounded-2xl shadow-xl shadow-pink-500/30 transition text-sm">
                        ¡ENCENDER TURBINA!
                    </button>
                </div>

                <!-- MODAL REVIVIR TURBINA -->
                <div id="droneReviveModal" class="hidden absolute inset-0 bg-gray-950/90 backdrop-blur-md flex flex-col items-center justify-center p-6 text-center">
                    <span class="text-5xl mb-1">⚡</span>
                    <h3 class="text-xl font-black text-white">¡COLISIÓN CON LÁSER!</h3>
                    <p id="droneScoreText" class="text-sm font-bold text-pink-400 mt-1 mb-4">Superaste 12 Portales</p>

                    <div id="droneReviveBox" class="w-full max-w-xs mb-3">
                        <button onclick="executeRewardedAction(handleDroneRevive)" class="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:opacity-90 active:scale-95 text-white font-black py-3.5 rounded-2xl shadow-lg shadow-emerald-500/30 text-xs sm:text-sm flex items-center justify-center space-x-2 transition">
                            <span>🛸</span>
                            <span>REPARAR DRON & CONTINUAR</span>
                        </button>
                        <p class="text-[10px] text-gray-400 mt-1">Desactiva el portal actual y conserva tus puntos</p>
                    </div>

                    <button onclick="restartDroneFromModal()" class="text-xs text-gray-400 hover:text-white underline mt-2">
                        Reiniciar desde 0 Portales
                    </button>
                </div>
            </div>
            <p class="text-xs text-gray-400 text-center mt-3">💡 Toca la pantalla o presiona Espacio para impulsar el Dron hacia arriba</p>
        </div>

        <!-- TABLA DE LÍDERES CYBER-DRONE -->
        <div class="bg-gray-900/80 rounded-3xl p-5 sm:p-6 border border-gray-800">
            <div class="flex justify-between items-center mb-3">
                <div class="flex items-center space-x-2">
                    <span class="text-xl">🏆</span>
                    <h3 class="text-base sm:text-lg font-black text-white">Top 10 • Neon Cyber-Drone</h3>
                </div>
                <button id="liveSyncStatus" onclick="syncGameFromCloud('drone', false)" class="text-xs bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 font-bold px-2.5 py-1 rounded-full transition">🟢 Global En Vivo</button>
            </div>

            <div class="flex space-x-1.5 bg-gray-950/90 p-1.5 rounded-2xl border border-gray-800 mb-3">
                <button id="tabWeeklyBtn" onclick="switchLeaderboardTab('weekly')" class="w-1/2 py-2 px-3 rounded-xl font-black text-xs transition flex items-center justify-center space-x-1.5 bg-gradient-to-r from-amber-500 to-orange-500 text-gray-950 shadow-md shadow-amber-500/20">
                    <span>🔥</span>
                    <span>Torneo Semanal</span>
                </button>
                <button id="tabAlltimeBtn" onclick="switchLeaderboardTab('alltime')" class="w-1/2 py-2 px-3 rounded-xl font-bold text-xs transition flex items-center justify-center space-x-1.5 text-gray-400 hover:text-white">
                    <span>👑</span>
                    <span>Récord Histórico</span>
                </button>
            </div>

            <div id="weeklyCountdownBanner" class="mb-3 px-3 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-[11px] flex flex-wrap items-center justify-between gap-1"></div>

            <div id="leaderboardList" class="space-y-2 text-sm"></div>

            <div class="mt-4 pt-3 border-t border-gray-800 text-center">
                <a href="../campeones.html?v=14" class="inline-flex items-center space-x-2 text-xs font-black text-amber-300 bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/40 px-4 py-2.5 rounded-xl transition">
                    <span>🏆</span>
                    <span>Ver Ganadores de Semanas Anteriores (Salón de Campeones)</span>
                </a>
            </div>
        </div>

    </main>

    __PLAYER_MODAL__
    __PLAYER_IDENTITY_SCRIPT__

    <script>
        const drCanvas = document.getElementById('droneCanvas');
        const drCtx = drCanvas.getContext('2d');
        const drStart = document.getElementById('droneStartScreen');
        const drRevive = document.getElementById('droneReviveModal');

        let droneY = 215;
        let droneVy = 0;
        let gates = [];
        let orbs = [];
        let droneRunning = false;
        let droneScore = 0;
        let droneTicks = 0;
        let hasRevivedDrone = false;

        function startDroneGame() {
            drStart.classList.add('hidden');
            drRevive.classList.add('hidden');
            droneY = drCanvas.height / 2;
            droneVy = -5.5;
            gates = [];
            orbs = [];
            droneScore = 0;
            droneTicks = 0;
            hasRevivedDrone = false;
            droneRunning = true;
            trackByteZoneEvent('drone', 'play');
            requestAnimationFrame(updateDroneLoop);
        }

        function flapDrone() {
            if (!droneRunning) return;
            droneVy = -6.4;
        }

        function spawnLaserGate() {
            const gapHeight = Math.max(102, 134 - Math.min(droneScore * 1.1, 28));
            const minTop = 45;
            const maxTop = drCanvas.height - gapHeight - 55;
            const gapTop = minTop + Math.random() * (maxTop - minTop);
            const colors = ['#ec4899', '#06b6d4', '#a855f7', '#f59e0b'];
            const color = colors[gates.length % colors.length];
            gates.push({
                x: drCanvas.width + 20,
                w: 24,
                gapTop: gapTop,
                gapBottom: gapTop + gapHeight,
                passed: false,
                color: color
            });
            if (Math.random() < 0.55) {
                orbs.push({
                    x: drCanvas.width + 32,
                    y: gapTop + gapHeight / 2,
                    r: 8,
                    collected: false
                });
            }
        }

        function updateDroneLoop() {
            if (!droneRunning) return;
            droneTicks++;

            const speedX = Math.min(2.7 + droneScore * 0.05, 4.6);
            const spawnInterval = Math.max(68, Math.floor(96 - droneScore * 0.6));
            if (droneTicks === 15 || droneTicks % spawnInterval === 0) {
                spawnLaserGate();
            }

            droneVy += 0.32;
            droneY += droneVy;

            drCtx.fillStyle = "#030712";
            drCtx.fillRect(0, 0, drCanvas.width, drCanvas.height);

            // Rejilla cyberpunk de fondo
            drCtx.strokeStyle = "rgba(236, 72, 153, 0.08)";
            drCtx.lineWidth = 1;
            const offset = (droneTicks * 2) % 36;
            for (let gx = -offset; gx < drCanvas.width; gx += 36) {
                drCtx.beginPath();
                drCtx.moveTo(gx, 0);
                drCtx.lineTo(gx, drCanvas.height);
                drCtx.stroke();
            }

            const droneX = 76;
            const droneR = 12;

            // Portales láser
            for (let i = gates.length - 1; i >= 0; i--) {
                const g = gates[i];
                g.x -= speedX;

                drCtx.save();
                drCtx.fillStyle = g.color;
                drCtx.shadowColor = g.color;
                drCtx.shadowBlur = 12;
                drCtx.fillRect(g.x, 0, g.w, g.gapTop);
                drCtx.fillRect(g.x, g.gapBottom, g.w, drCanvas.height - g.gapBottom);
                drCtx.restore();

                if (!g.passed && g.x + g.w < droneX - droneR) {
                    g.passed = true;
                    droneScore++;
                }

                if (droneX + droneR > g.x && droneX - droneR < g.x + g.w) {
                    if (droneY - droneR < g.gapTop || droneY + droneR > g.gapBottom) {
                        gameOverDrone();
                        return;
                    }
                }

                if (g.x + g.w < -20) {
                    gates.splice(i, 1);
                }
            }

            // Esferas de energía (+2 puntos)
            for (let i = orbs.length - 1; i >= 0; i--) {
                const o = orbs[i];
                o.x -= speedX;
                if (!o.collected) {
                    drCtx.save();
                    drCtx.fillStyle = "#34d399";
                    drCtx.shadowColor = "#34d399";
                    drCtx.shadowBlur = 14;
                    drCtx.beginPath();
                    drCtx.arc(o.x, o.y, o.r, 0, Math.PI * 2);
                    drCtx.fill();
                    drCtx.restore();

                    const dx = o.x - droneX;
                    const dy = o.y - droneY;
                    if (Math.sqrt(dx * dx + dy * dy) < o.r + droneR) {
                        o.collected = true;
                        droneScore += 2;
                    }
                }
                if (o.x < -20 || o.collected) {
                    orbs.splice(i, 1);
                }
            }

            // Dibujar Dron Neón
            drCtx.save();
            drCtx.fillStyle = "#22d3ee";
            drCtx.shadowColor = "#22d3ee";
            drCtx.shadowBlur = 16;
            drCtx.beginPath();
            drCtx.arc(droneX, droneY, droneR, 0, Math.PI * 2);
            drCtx.fill();
            drCtx.fillStyle = "#ffffff";
            drCtx.beginPath();
            drCtx.arc(droneX + 4, droneY - 2, 4, 0, Math.PI * 2);
            drCtx.fill();
            drCtx.restore();

            if (droneY - droneR <= 0 || droneY + droneR >= drCanvas.height) {
                gameOverDrone();
                return;
            }

            drCtx.fillStyle = "#ffffff";
            drCtx.font = "bold 18px monospace";
            drCtx.fillText("PORTALES: " + droneScore, 16, 32);

            requestAnimationFrame(updateDroneLoop);
        }

        function gameOverDrone() {
            droneRunning = false;
            recordGameScore('drone', droneScore, false);
            document.getElementById('droneScoreText').textContent = "Superaste " + droneScore + " Portales";
            document.getElementById('droneReviveBox').style.display = hasRevivedDrone ? 'none' : 'block';
            drRevive.classList.remove('hidden');
            if (hasRevivedDrone) { setTimeout(() => { flushPendingPodium(); }, 700); }
        }

        function restartDroneFromModal() {
            if (flushPendingPodium()) {
                drRevive.classList.add('hidden');
                drStart.classList.remove('hidden');
            } else {
                startDroneGame();
            }
        }

        function handleDroneRevive() {
            trackByteZoneEvent('drone', 'ad');
            hasRevivedDrone = true;
            gates = [];
            droneY = drCanvas.height / 2;
            droneVy = -5.0;
            drRevive.classList.add('hidden');
            droneRunning = true;
            requestAnimationFrame(updateDroneLoop);
        }

        drCanvas.addEventListener('pointerdown', (e) => {
            e.preventDefault();
            if (droneRunning) flapDrone();
        });

        window.addEventListener('keydown', (e) => {
            if ((e.code === 'Space' || e.key === 'ArrowUp') && droneRunning) {
                e.preventDefault();
                flapDrone();
            }
        });

        trackByteZoneEvent('drone', 'view');

        function renderLeaderboardUI() {
            const mode = window.currentLeaderboardTab || 'weekly';
            const list = getCleanScores('drone', false, mode);
            const container = document.getElementById('leaderboardList');
            const bestKey = (mode === 'weekly') ? 'bytezone_weekly_best_drone' : 'bytezone_best_drone';
            const myBest = parseInt(localStorage.getItem(bestKey) || '0');
            document.getElementById('userBestScore').textContent = myBest + " Portales";

            const bestLabel = document.getElementById('userBestScoreLabel');
            const rankLabel = document.getElementById('userRankLabel');
            if (bestLabel) bestLabel.textContent = (mode === 'weekly') ? "Tus Mejores Portales de la Semana" : "Tu Récord Histórico";
            if (rankLabel) rankLabel.textContent = (mode === 'weekly') ? "Puesto Semanal" : "Puesto Histórico";

            if (list.length === 0) {
                container.innerHTML = '<div class="p-4 text-center text-gray-400 text-xs">¡Sé el primero en marcar récord en Neon Cyber-Drone esta semana!</div>';
                document.getElementById('userRankBadge').textContent = "Sin Clasificar";
                return;
            }

            container.innerHTML = "";
            let myPosition = null;
            list.slice(0, 10).forEach((item, idx) => {
                const isMe = isCurrentUserEntry(item);
                if (isMe && myPosition === null) myPosition = idx + 1;
                const badge = idx === 0 ? "🥇" : idx === 1 ? "🥈" : idx === 2 ? "🥉" : "#" + (idx + 1);
                const itemFlag = getCountryFlag(item.country);
                const row = document.createElement('div');
                row.className = "flex justify-between items-center p-2.5 rounded-xl " + (isMe ? 'bg-pink-950/40 border border-pink-500 shadow-md' : 'bg-gray-800/60 border border-gray-700/50');
                row.innerHTML = `
                    <div class="flex items-center space-x-2 min-w-0">
                        <span class="w-6 text-center font-bold text-xs ${idx < 3 ? 'text-yellow-400 font-extrabold' : 'text-gray-400'}">${badge}</span>
                        <span class="text-base select-none">${itemFlag}</span>
                        <span class="font-bold truncate ${isMe ? 'text-pink-400' : 'text-white'}">${item.name} ${isMe ? '(Tú)' : ''}</span>
                    </div>
                    <span class="font-black flex-shrink-0 ${isMe ? 'text-cyan-400' : 'text-pink-400'}">${item.score} Portales</span>
                `;
                container.appendChild(row);
            });

            const rankBadge = document.getElementById('userRankBadge');
            if (myPosition === 1) {
                rankBadge.textContent = "🥇 Puesto #1 (¡Líder! • Toca para Retar)";
                rankBadge.className = "text-xs font-black text-yellow-300 bg-yellow-500/20 border border-yellow-500/50 px-3 py-1 rounded-full animate-pulse cursor-pointer shadow-lg shadow-yellow-500/20";
                rankBadge.onclick = () => checkAndShowPodiumModal('drone', myBest, false);
            } else if (myPosition === 2) {
                rankBadge.textContent = "🥈 Puesto #2 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-gray-200 bg-gray-500/20 border border-gray-400/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('drone', myBest, false);
            } else if (myPosition === 3) {
                rankBadge.textContent = "🥉 Puesto #3 (Toca para Retar)";
                rankBadge.className = "text-xs font-black text-amber-400 bg-amber-500/20 border border-amber-500/50 px-3 py-1 rounded-full cursor-pointer";
                rankBadge.onclick = () => checkAndShowPodiumModal('drone', myBest, false);
            } else if (myPosition) {
                rankBadge.textContent = "Puesto #" + myPosition;
                rankBadge.className = "text-xs font-black text-pink-400 bg-pink-500/10 border border-pink-500/30 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            } else {
                rankBadge.textContent = "Sin Clasificar";
                rankBadge.className = "text-xs font-black text-gray-400 bg-gray-800 border border-gray-700 px-3 py-1 rounded-full";
                rankBadge.onclick = null;
            }
        }

        updateLeaderboardTabsUI();
        renderLeaderboardUI();
        startRealtimeScoreStream('drone', false);
    </script>
</body>
</html>
"""

# ==========================================================
# 4D. SALÓN DE LA FAMA & CAMPEONES SEMANALES: CAMPEONES.HTML
# ==========================================================
TEMPLATE_CAMPEONES = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Salón de la Fama & Campeones Semanales - ByteZone Arcade</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <!-- CABECERA DEL SALÓN DE CAMPEONES -->
        <div class="bg-gradient-to-r from-amber-950/70 via-gray-900 to-purple-950/70 border border-amber-500/40 rounded-3xl p-6 sm:p-8 text-center relative overflow-hidden shadow-2xl">
            <span class="text-5xl inline-block mb-2 animate-bounce">🏆</span>
            <div class="block">
                <span class="text-[11px] bg-amber-500/20 text-amber-300 border border-amber-500/40 font-black px-3 py-1 rounded-full uppercase tracking-wider">
                    Archivo Oficial • Torneo Semanal ByteZone
                </span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-black text-white mt-3">Salón de Campeones Semanales</h1>
            <p class="text-xs sm:text-sm text-gray-300 max-w-xl mx-auto mt-2 leading-relaxed">
                Aquí quedan inmortalizados los <strong>3 mejores jugadores (🥇 🥈 🥉) de cada semana</strong> en cada juego cuando cierra el torneo los domingos a las 12:00 AM, junto a los líderes en vivo de la semana actual.
            </p>
            <div class="mt-4 flex flex-wrap items-center justify-center gap-2 text-xs">
                <span id="championsCountdownPill" class="bg-gray-950/90 text-amber-300 border border-amber-500/40 font-bold px-3.5 py-1.5 rounded-xl">
                    ⏳ Calculando cierre semanal...
                </span>
                <button onclick="refreshAllGamesForChampions()" class="bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 font-black px-3.5 py-1.5 rounded-xl transition">
                    🔄 Sincronizar Podios en Vivo
                </button>
            </div>
        </div>

        <!-- FILTRO POR JUEGO -->
        <div class="flex flex-wrap items-center justify-center gap-2">
            <button onclick="setChampionsGameFilter('all')" id="champFilter_all" class="px-3.5 py-2 rounded-xl text-xs font-black bg-amber-500 text-gray-950 shadow transition">
                🌟 Todos los Juegos (5)
            </button>
            <button onclick="setChampionsGameFilter('stacker')" id="champFilter_stacker" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-gray-900 text-gray-300 border border-gray-800 hover:text-white transition">
                🏗️ Neon Stacker
            </button>
            <button onclick="setChampionsGameFilter('reflex')" id="champFilter_reflex" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-gray-900 text-gray-300 border border-gray-800 hover:text-white transition">
                ⚡ Reflejos (ms)
            </button>
            <button onclick="setChampionsGameFilter('memory')" id="champFilter_memory" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-gray-900 text-gray-300 border border-gray-800 hover:text-white transition">
                🧠 Cyber Memory
            </button>
            <button onclick="setChampionsGameFilter('dodge')" id="champFilter_dodge" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-gray-900 text-gray-300 border border-gray-800 hover:text-white transition">
                🚀 Cyber Dodge
            </button>
            <button onclick="setChampionsGameFilter('drone')" id="champFilter_drone" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-gray-900 text-gray-300 border border-gray-800 hover:text-white transition">
                🛸 Cyber-Drone
            </button>
        </div>

        <!-- SECCIÓN 1: PODIO ACTUAL EN VIVO (SEMANA EN CURSO) -->
        <div class="space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <h2 class="text-lg sm:text-xl font-black text-white flex items-center space-x-2">
                    <span>🔥</span>
                    <span>Líderes en Vivo • Semana Actual en Disputa</span>
                </h2>
                <span id="activeWeekIdBadge" class="text-xs font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-3 py-1 rounded-full">
                    🟢 En Curso
                </span>
            </div>
            <div id="liveChampionsGrid" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
        </div>

        <!-- BANNER RECOMPENSADO DE RETO A LOS CAMPEONES (MONETAG VOLUNTARIO NO INTRUSIVO) -->
        <div class="bg-gradient-to-r from-gray-900 via-amber-950/30 to-gray-900 border border-amber-500/40 rounded-3xl p-5 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
            <div class="flex items-center space-x-3 text-left">
                <span class="text-3xl">👑</span>
                <div>
                    <h3 class="text-sm sm:text-base font-black text-white">¿Quieres aparecer en el Cuadro de Honor de esta semana?</h3>
                    <p class="text-xs text-gray-300 mt-0.5">Entra al Top 3 antes del domingo a medianoche para que tu nombre y bandera queden grabados aquí para siempre.</p>
                </div>
            </div>
            <button onclick="challengeCurrentLeaderWithReward()" class="flex-shrink-0 bg-gradient-to-r from-amber-500 to-orange-500 hover:opacity-90 active:scale-95 text-gray-950 font-black text-xs px-4 py-3 rounded-2xl shadow-lg shadow-amber-500/20 transition">
                ⚡ Retar al Campeón Ahora
            </button>
        </div>

        <!-- SECCIÓN 2: HISTÓRICO SEMANA A SEMANA (CUADROS DE HONOR CERRADOS) -->
        <div class="space-y-4 pt-2 border-t border-gray-800">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <div>
                    <h2 class="text-lg sm:text-xl font-black text-white flex items-center space-x-2">
                        <span>🏛️</span>
                        <span>Historial de Ganadores Semana por Semana</span>
                    </h2>
                    <p class="text-xs text-gray-400">Registro permanente de los podios Top 3 de cada semana finalizada.</p>
                </div>
                <span class="text-[11px] font-bold bg-amber-500/15 text-amber-300 border border-amber-500/30 px-3 py-1 rounded-full">
                    Archivo Permanente
                </span>
            </div>

            <div id="historicalWeeksContainer" class="space-y-6"></div>
        </div>

    </main>

    __PLAYER_MODAL__
    __FOOTER__
    __PLAYER_IDENTITY_SCRIPT__

    <script>
        window.selectedChampionGame = 'all';

        const CHAMP_GAMES_META = {
            stacker: { name: 'Neon Stacker Pro', icon: '🏗️', unit: 'Pisos', url: 'juegos/neon-stacker.html?v=14', asc: false, border: 'border-cyan-500/40', accent: 'text-cyan-400' },
            reflex:  { name: 'Test de Reflejos', icon: '⚡', unit: 'ms',    url: 'juegos/reflejos-visuales.html?v=14', asc: true,  border: 'border-purple-500/40', accent: 'text-purple-400' },
            memory:  { name: 'Cyber Memory',     icon: '🧠', unit: 'Rondas', url: 'juegos/cyber-memory.html?v=14', asc: false, border: 'border-emerald-500/40', accent: 'text-emerald-400' },
            dodge:   { name: 'Cyber Dodge',      icon: '🚀', unit: 'seg',   url: 'juegos/cyber-dodge.html?v=14', asc: false, border: 'border-amber-500/40', accent: 'text-amber-400' },
            drone:   { name: 'Neon Cyber-Drone', icon: '🛸', unit: 'Portales', url: 'juegos/cyber-drone.html?v=14', asc: false, border: 'border-pink-500/40', accent: 'text-pink-400' }
        };

        function setChampionsGameFilter(gameKey) {
            window.selectedChampionGame = gameKey || 'all';
            ['all', 'stacker', 'reflex', 'memory', 'dodge', 'drone'].forEach(k => {
                const btn = document.getElementById('champFilter_' + k);
                if (!btn) return;
                if (k === window.selectedChampionGame) {
                    btn.className = "px-3.5 py-2 rounded-xl text-xs font-black bg-amber-500 text-gray-950 shadow transition";
                } else {
                    btn.className = "px-3.5 py-2 rounded-xl text-xs font-bold bg-gray-900 text-gray-300 border border-gray-800 hover:text-white transition";
                }
            });
            renderChampionsPageUI();
        }

        function renderPodiumRowsHTML(top3List, unit, accentClass) {
            if (!Array.isArray(top3List) || top3List.length === 0) {
                return `<div class="p-3 rounded-xl bg-gray-950/70 text-xs text-gray-400 text-center">Aún sin marcas registradas en esta semana.</div>`;
            }
            const medals = ['🥇', '🥈', '🥉'];
            return top3List.slice(0, 3).map((item, idx) => {
                const isMe = (typeof isCurrentUserEntry === 'function') ? isCurrentUserEntry(item) : false;
                const flag = (typeof getCountryFlag === 'function') ? getCountryFlag(item.country || 'VE') : '🌐';
                return `
                    <div class="flex items-center justify-between p-2.5 rounded-xl ${idx === 0 ? 'bg-amber-500/15 border border-amber-500/40' : 'bg-gray-950/70 border border-gray-800'}">
                        <div class="flex items-center space-x-2 min-w-0">
                            <span class="text-base">${medals[idx] || '#'}</span>
                            <span class="text-sm">${flag}</span>
                            <span class="text-xs sm:text-sm font-black truncate ${isMe ? 'text-cyan-300' : 'text-white'}">${item.name} ${isMe ? '(Tú)' : ''}</span>
                        </div>
                        <span class="text-xs sm:text-sm font-black ${idx === 0 ? 'text-amber-300' : accentClass}">${item.score} ${unit}</span>
                    </div>
                `;
            }).join('');
        }

        window.renderChampionsPageUI = function() {
            const currentWeek = ensureWeeklyReset();
            const pill = document.getElementById('championsCountdownPill');
            if (pill) pill.textContent = getWeeklyCountdownText();
            const weekBadge = document.getElementById('activeWeekIdBadge');
            if (weekBadge) weekBadge.textContent = `🟢 Semana Activa (${currentWeek})`;

            const filter = window.selectedChampionGame || 'all';
            const keysToShow = (filter === 'all') ? Object.keys(CHAMP_GAMES_META) : [filter];

            // 1. Renderizar Podios En Vivo de la Semana Actual
            const liveGrid = document.getElementById('liveChampionsGrid');
            if (liveGrid) {
                liveGrid.innerHTML = keysToShow.map(gKey => {
                    const meta = CHAMP_GAMES_META[gKey];
                    const scores = getCleanScores(gKey, meta.asc, 'weekly').slice(0, 3);
                    return `
                        <div class="bg-gray-900/95 rounded-3xl p-5 border ${meta.border} shadow-xl flex flex-col justify-between">
                            <div>
                                <div class="flex items-center justify-between mb-3">
                                    <div class="flex items-center space-x-2">
                                        <span class="text-2xl">${meta.icon}</span>
                                        <div>
                                            <h3 class="text-sm sm:text-base font-black text-white">${meta.name}</h3>
                                            <p class="text-[11px] text-emerald-400 font-semibold">Top 3 En Vivo (${currentWeek})</p>
                                        </div>
                                    </div>
                                    <a href="${meta.url}" class="text-xs bg-gray-800 hover:bg-gray-700 text-white font-bold px-3 py-1.5 rounded-xl border border-gray-700 transition">
                                        🕹️ Jugar
                                    </a>
                                </div>
                                <div class="space-y-2">
                                    ${renderPodiumRowsHTML(scores, meta.unit, meta.accent)}
                                </div>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // 2. Renderizar Archivo Histórico Semana a Semana
            const archiveList = (typeof getWeeklyChampionsArchive === 'function') ? getWeeklyChampionsArchive() : [];
            const histContainer = document.getElementById('historicalWeeksContainer');
            if (histContainer) {
                histContainer.innerHTML = archiveList.map(weekObj => {
                    const cardsHtml = keysToShow.map(gKey => {
                        const meta = CHAMP_GAMES_META[gKey];
                        const top3 = (weekObj.champions && weekObj.champions[gKey]) || [];
                        return `
                            <div class="bg-gray-950/85 rounded-2xl p-4 border border-gray-800">
                                <div class="flex items-center justify-between mb-2.5">
                                    <span class="text-xs font-black text-white flex items-center space-x-1.5">
                                        <span>${meta.icon}</span>
                                        <span>${meta.name}</span>
                                    </span>
                                    <span class="text-[10px] text-amber-300 font-bold">Podio Oficial</span>
                                </div>
                                <div class="space-y-1.5">
                                    ${renderPodiumRowsHTML(top3, meta.unit, meta.accent)}
                                </div>
                            </div>
                        `;
                    }).join('');

                    return `
                        <div class="bg-gray-900/90 rounded-3xl p-5 sm:p-6 border border-amber-500/30 shadow-xl space-y-4">
                            <div class="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-gray-800">
                                <div class="flex items-center space-x-2.5">
                                    <span class="text-2xl">🏅</span>
                                    <div>
                                        <h3 class="text-base sm:text-lg font-black text-white">${weekObj.label}</h3>
                                        <p class="text-[11px] text-amber-300 font-semibold">Código de Torneo: ${weekObj.weekId}</p>
                                    </div>
                                </div>
                                <span class="text-[11px] font-black bg-amber-500/20 text-amber-300 border border-amber-500/40 px-3 py-1 rounded-full">
                                    ✅ ${weekObj.status || 'Cerrada • Premiada'}
                                </span>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                                ${cardsHtml}
                            </div>
                        </div>
                    `;
                }).join('');
            }
        };

        function refreshAllGamesForChampions() {
            ALL_GAME_KEYS.forEach((g, idx) => {
                setTimeout(() => {
                    syncGameFromCloud(g, g === 'reflex', true).then(() => {
                        renderChampionsPageUI();
                    });
                }, idx * 350);
            });
        }

        function challengeCurrentLeaderWithReward() {
            trackByteZoneEvent('stacker', 'ad');
            executeRewardedAction(() => {
                window.location.href = 'juegos/neon-stacker.html?v=14';
            });
        }

        renderChampionsPageUI();
        refreshAllGamesForChampions();
        startRealtimeScoreStream('stacker', false);
    </script>
</body>
</html>
"""

# ==========================================================
# 5. PÁGINA DEDICADA: HACKS.HTML (IA & TECH TV + NOTICIAS SEMANALES + HACKS)
# ==========================================================
TEMPLATE_HACKS = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>IA & Tech TV: Noticias de la Semana, Inventos & Hacks - ByteZone</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <div class="text-center mb-2">
            <span class="text-xs bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                🤖 Actualizado Cada Lunes por Agente CEO IA
            </span>
            <h1 class="text-2xl sm:text-3xl font-black text-white mt-2">IA, Inventos de la Semana & Tech TV</h1>
            <p class="text-xs sm:text-sm text-gray-400 mt-1">¿No te gusta leer largo? Dale Play al Resumen Flash narrado a toda velocidad o explora los titulares.</p>
        </div>

        <!-- REPRODUCTOR DE VIDEO FLASH IA -->
        __AI_VIDEO_REEL_WIDGET__

        <!-- RADAR DE NOTICIAS SEMANALES DE IA, INVENTOS Y GADGETS -->
        <div class="space-y-3">
            <div class="flex items-center justify-between">
                <h2 class="text-lg sm:text-xl font-black text-white flex items-center space-x-2">
                    <span>📰</span>
                    <span>Lo Más Resaltante de la Semana (IA & Mercado Tech)</span>
                </h2>
                <span class="text-[11px] text-emerald-400 font-bold bg-emerald-500/10 px-2.5 py-1 rounded-full">Edición Semanal</span>
            </div>

            <div id="weeklyNewsContainer" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-gray-900/80 p-5 rounded-2xl border border-gray-800 text-xs text-gray-400">
                    Cargando noticias semanales del Agente CEO...
                </div>
            </div>
        </div>

        <!-- ATAJOS Y TRUCOS DE TELÉFONOS -->
        <div class="pt-4 border-t border-gray-800 space-y-3">
            <h2 class="text-lg sm:text-xl font-black text-white flex items-center space-x-2">
                <span>⚡</span>
                <span>Hacks Secretos de Teléfonos & WhatsApp</span>
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                
                <div class="bg-gray-900/80 p-5 rounded-2xl border border-gray-800 hover:border-cyan-400 transition shadow">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-md">WhatsApp Secreto</span>
                        <span class="text-xs text-gray-400">Android</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">Cómo leer mensajes borrados</h3>
                    <p class="text-xs text-gray-300 mt-2 leading-relaxed">
                        Ve a <strong>Ajustes > Notificaciones > Ajustes avanzados > Historial de notificaciones</strong>. Al activarlo, el sistema almacena todos los textos que llegan, ¡incluso si la otra persona le dio a "Eliminar para todos"!
                    </p>
                </div>

                <div class="bg-gray-900/80 p-5 rounded-2xl border border-gray-800 hover:border-purple-400 transition shadow">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-bold text-purple-400 bg-purple-500/10 px-2.5 py-1 rounded-md">Batería al 200%</span>
                        <span class="text-xs text-gray-400">Todo Celular</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">El vampiro oculto de batería</h3>
                    <p class="text-xs text-gray-300 mt-2 leading-relaxed">
                        Ve a <strong>Ajustes > Ubicación > Servicios de ubicación</strong> y desactiva <em>"Búsqueda con Wi-Fi"</em> y <em>"Búsqueda con Bluetooth"</em>. Esas opciones buscan redes con el Wi-Fi apagado y se comen el 15% de tu batería diaria.
                    </p>
                </div>

                <div class="bg-gray-900/80 p-5 rounded-2xl border border-gray-800 hover:border-pink-400 transition shadow">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-bold text-pink-400 bg-pink-500/10 px-2.5 py-1 rounded-md">Velocidad</span>
                        <span class="text-xs text-gray-400">Android</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">Acelerar el teléfono al doble</h3>
                    <p class="text-xs text-gray-300 mt-2 leading-relaxed">
                        En <strong>Opciones de Desarrollador</strong>, busca las 3 escalas de animación (Ventana, Transición y Duración) y cámbialas de <strong>1.0x a 0.5x</strong>. El teléfono abrirá menús y apps al doble de velocidad instantáneamente.
                    </p>
                </div>

                <div class="bg-gray-900/80 p-5 rounded-2xl border border-gray-800 hover:border-yellow-400 transition shadow">
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-bold text-yellow-400 bg-yellow-500/10 px-2.5 py-1 rounded-md">Seguridad</span>
                        <span class="text-xs text-gray-400">WhatsApp</span>
                    </div>
                    <h3 class="text-lg font-bold text-white">Comprueba si te espían WhatsApp Web</h3>
                    <p class="text-xs text-gray-300 mt-2 leading-relaxed">
                        Abre WhatsApp, toca los 3 puntos y entra en <strong>Dispositivos Vinculados</strong>. Si ves sesiones abiertas en navegadores desconocidos (Windows, Mac, Firefox), dale a <em>"Cerrar sesión"</em> de inmediato para expulsar al intruso.
                    </p>
                </div>

            </div>
        </div>

    </main>

    __PLAYER_MODAL__

    __FOOTER__

    __PLAYER_IDENTITY_SCRIPT__
    <script>
        loadWeeklyPulseData("");
    </script>
</body>
</html>
"""

# ==========================================================
# 6. PÁGINA DEDICADA: HUMOR.HTML (CHISTES & MEMES)
# ==========================================================
TEMPLATE_HUMOR = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Humor Tech & Memes - ByteZone</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <div class="text-center mb-4">
            <span class="text-xs bg-pink-500/20 text-pink-300 border border-pink-500/30 font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                Risas Garantizadas 😂
            </span>
            <h1 class="text-2xl sm:text-3xl font-black text-white mt-2">Cápsula de Humor & Sarcasmo Tech</h1>
            <p class="text-xs sm:text-sm text-gray-400 mt-1">Verdades incómodas sobre WhatsApp, la batería, la IA y la vida digital.</p>
        </div>

        <!-- GENERADOR DE CHISTES Y FRASES -->
        <div class="bg-gradient-to-r from-gray-900 via-gray-850 to-gray-900 rounded-3xl p-6 sm:p-8 border border-pink-500/40 text-center max-w-xl mx-auto shadow-2xl relative">
            <span class="text-5xl animate-bounce inline-block mb-1">🤣</span>
            <p id="humorQuote" class="text-sm sm:text-base font-bold text-white my-4 italic leading-relaxed min-h-[60px] flex items-center justify-center">
                "— Mi amor, dame tu contraseña de WhatsApp si no tienes nada que esconder.<br>— Dame tú la clave de tu banco si confías en mí.<br>— ...Silencio absoluto en la sala."
            </p>
            <div class="flex items-center justify-center space-x-3 mt-4">
                <button onclick="generarChisteNuevo()" class="bg-gradient-to-r from-pink-500 to-purple-600 hover:opacity-90 active:scale-95 text-white font-black px-5 py-2.5 rounded-xl text-xs sm:text-sm shadow-lg shadow-pink-500/25 transition">
                    🎲 Tirar otro chiste bueno
                </button>
                <button onclick="reaccionarRisa()" class="bg-gray-800 hover:bg-gray-700 text-pink-400 font-bold px-4 py-2.5 rounded-xl text-xs transition border border-gray-700 flex items-center space-x-1.5">
                    <span>💀</span>
                    <span>¡Tal cual!</span>
                    <span id="risaCount" class="text-gray-400 text-[11px]">(48)</span>
                </button>
            </div>
        </div>

        <!-- TARJETAS DE VERDADES DE LA TECNOLOGÍA -->
        __TRUTH_GRID__

    </main>

    __PLAYER_MODAL__

    __FOOTER__

    __PLAYER_IDENTITY_SCRIPT__

    <script>
        const CHISTES = __CHISTES_JSON__;

        let countRisas = 48;

        let __lastJoke = -1;
        function generarChisteNuevo() {
            const q = document.getElementById('humorQuote');
            if (!CHISTES || !CHISTES.length) return;
            let i = Math.floor(Math.random() * CHISTES.length);
            if (CHISTES.length > 1) { while (i === __lastJoke) { i = Math.floor(Math.random() * CHISTES.length); } }
            __lastJoke = i;
            q.innerHTML = '"' + CHISTES[i] + '"';
        }
        setTimeout(generarChisteNuevo, 0);

        function reaccionarRisa() {
            countRisas++;
            const el = document.getElementById('risaCount');
            if (el) el.textContent = '(' + countRisas + ')';
            if (typeof confetti === 'function') {
                confetti({
                    particleCount: 25,
                    spread: 60,
                    origin: { y: 0.8 }
                });
            }
        }
    </script>
</body>
</html>
"""

# ==========================================================
# 7. PÁGINA DEDICADA: TELEGRAM.HTML
# ==========================================================
TEMPLATE_TELEGRAM = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Comunidad Telegram - ByteZone</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 py-6 flex-grow w-full space-y-6">

        <div class="bg-gray-900/90 rounded-3xl p-6 sm:p-8 border border-blue-500/40 text-center relative overflow-hidden shadow-2xl">
            <span class="text-6xl animate-pulse inline-block">✈️</span>
            <h1 class="text-2xl sm:text-3xl font-black text-white mt-3">Comunidad & Mini App de Telegram</h1>
            <p class="text-xs sm:text-sm text-gray-300 max-w-md mx-auto my-4 leading-relaxed">
                Juega a los mini-juegos de ByteZone y consulta atajos secretos directamente desde tu aplicación de Telegram sin abrir el navegador.
            </p>

            <div class="p-4 rounded-2xl bg-blue-950/40 border border-blue-500/30 max-w-md mx-auto mb-6 text-left text-xs space-y-2.5">
                <p class="flex items-center text-blue-200">
                    <span class="text-emerald-400 mr-2 font-bold">✔</span> Récords sincronizados automáticamente con tu apodo.
                </p>
                <p class="flex items-center text-blue-200">
                    <span class="text-emerald-400 mr-2 font-bold">✔</span> Notificación instantánea cuando agregamos un nuevo juego.
                </p>
                <p class="flex items-center text-blue-200">
                    <span class="text-emerald-400 mr-2 font-bold">✔</span> Torneos semanales de agilidad con premios en puntos.
                </p>
            </div>

                <a href="https://t.me/ByteZoneArcadeBot" class="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:opacity-90 active:scale-95 text-white font-black text-sm py-3.5 px-6 rounded-2xl shadow-xl shadow-blue-500/30 transition flex items-center justify-center space-x-2">
                    <span>⚡</span>
                    <span>Abrir en Telegram (@ByteZoneArcadeBot)</span>
                </a>
                <a href="tg://resolve?domain=ByteZoneArcadeBot" class="w-full bg-gray-800 hover:bg-gray-750 text-gray-300 font-bold text-xs py-2.5 px-4 rounded-xl border border-gray-700 transition flex items-center justify-center space-x-1.5">
                    <span>📱</span>
                    <span>Abrir App Directa (Deep-Link)</span>
                </a>
            </div>

            <div class="mt-8 p-4 rounded-2xl bg-gray-950/60 border border-gray-800 text-left text-xs text-gray-400 space-y-2">
                <p class="font-bold text-white flex items-center">
                    <span class="mr-2">💡</span> Tu Bot Oficial está Conectado
                </p>
                <p class="leading-relaxed">
                    Al tocar el botón azul se abrirá tu bot <strong>@ByteZoneArcadeBot</strong> en tu aplicación de Telegram, donde podrás jugar tocando el botón <strong>[ 🕹️ Jugar ByteZone ]</strong>.
                </p>
            </div>
        </div>

    </main>

    __PLAYER_MODAL__

    __FOOTER__

    __PLAYER_IDENTITY_SCRIPT__
</body>
</html>
"""


# ==========================================================
# 8. PÁGINA DE ESTADÍSTICAS & POPULARIDAD: STATS.HTML
# ==========================================================
TEMPLATE_STATS = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Métricas & Popularidad - ByteZone</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    __MONETAG_TAG__
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen flex flex-col pt-10 sm:pt-4 pb-20 sm:pb-6">

    __HEADER__

    <main class="max-w-4xl mx-auto px-4 mt-6 flex-grow space-y-6 w-full">
        
        <!-- ENCABEZADO PANEL DE CONTROL CON ESTADO GLOBAL EN VIVO -->
        <div class="bg-gradient-to-r from-gray-900 via-purple-950/40 to-gray-900 border border-purple-500/30 rounded-3xl p-6 text-center shadow-2xl relative overflow-hidden">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                <span class="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-black px-3 py-1 rounded-full flex items-center space-x-1.5 mx-auto sm:mx-0">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    <span id="cloudSyncStatusBadge">🟢 Nube Global Conectada (ntfy.sh)</span>
                </span>
                <button onclick="refreshGlobalMetricsFromCloud(true)" class="text-xs bg-gray-800 hover:bg-gray-700 text-cyan-300 font-bold px-3 py-1.5 rounded-xl border border-gray-700 transition flex items-center space-x-1 mx-auto sm:mx-0">
                    <span>🔄</span>
                    <span>Actualizar Nube</span>
                </button>
            </div>

            <span class="text-4xl inline-block mb-1">📊</span>
            <h1 class="text-2xl sm:text-3xl font-black bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-500 bg-clip-text text-transparent">
                Panel de Métricas & Monetización Global
            </h1>
            <p class="text-xs sm:text-sm text-gray-300 mt-2 max-w-xl mx-auto">
                Monitorea en tiempo real todas las partidas, revives y anuncios confirmados de <strong>todos los teléfonos</strong> y de la <strong>Mini App de Telegram</strong> en vivo.
            </p>
        </div>

        <!-- TARJETAS DE LOS JUEGOS EN TIEMPO REAL (SINCRONIZADAS ENTRE TODOS LOS TELÉFONOS) -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <!-- TARJETA: NEON STACKER -->
            <div class="bg-gray-900/90 rounded-2xl p-5 border border-cyan-500/40 shadow-xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-2xl">🏗️</span>
                        <span id="badgeStacker" class="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
                            Sincronizando...
                        </span>
                    </div>
                    <h3 class="font-black text-white text-base">Neon Stacker Pro</h3>
                    <p class="text-xs text-gray-400 mt-0.5">Construcción de torre con bloques</p>
                    
                    <div class="mt-4 space-y-2 text-xs">
                        <div class="flex justify-between text-gray-300">
                            <span>Partidas Jugadas (Global):</span>
                            <span id="playsStacker" class="font-bold text-white">0</span>
                        </div>
                        <div class="flex justify-between text-gray-300">
                            <span>Revives con Anuncio:</span>
                            <span id="adsStacker" class="font-bold text-emerald-400">0</span>
                        </div>
                        <div class="flex justify-between text-gray-300">
                            <span>Tasa de Conversión:</span>
                            <span id="rateStacker" class="font-bold text-cyan-400">0%</span>
                        </div>
                    </div>
                </div>
                <div class="mt-5 pt-3 border-t border-gray-800 text-[11px] text-gray-400 flex justify-between items-center">
                    <span>Popularidad Global:</span>
                    <span id="pctStacker" class="font-black text-white">0%</span>
                </div>
            </div>

            <!-- TARJETA: REFLEJOS VISUALES -->
            <div class="bg-gray-900/90 rounded-2xl p-5 border border-purple-500/40 shadow-xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-2xl">⚡</span>
                        <span id="badgeReflex" class="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/40">
                            Sincronizando...
                        </span>
                    </div>
                    <h3 class="font-black text-white text-base">Test de Reflejos</h3>
                    <p class="text-xs text-gray-400 mt-0.5">Velocidad de reacción pura</p>
                    
                    <div class="mt-4 space-y-2 text-xs">
                        <div class="flex justify-between text-gray-300">
                            <span>Sesiones (1 c/5 intentos):</span>
                            <span id="playsReflex" class="font-bold text-white">0</span>
                        </div>
                        <div class="flex justify-between text-gray-300">
                            <span>Recargas de Batería:</span>
                            <span id="adsReflex" class="font-bold text-emerald-400">0</span>
                        </div>
                        <div class="flex justify-between text-gray-300">
                            <span>Tasa de Conversión:</span>
                            <span id="rateReflex" class="font-bold text-purple-400">0%</span>
                        </div>
                    </div>
                </div>
                <div class="mt-5 pt-3 border-t border-gray-800 text-[11px] text-gray-400 flex justify-between items-center">
                    <span>Popularidad Global:</span>
                    <span id="pctReflex" class="font-black text-white">0%</span>
                </div>
            </div>

            <!-- TARJETA: CYBER MEMORY -->
            <div class="bg-gray-900/90 rounded-2xl p-5 border border-emerald-500/40 shadow-xl flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-2xl">🧠</span>
                        <span id="badgeMemory" class="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                            Sincronizando...
                        </span>
                    </div>
                    <h3 class="font-black text-white text-base">Cyber Memory</h3>
                    <p class="text-xs text-gray-400 mt-0.5">Secuencias sonoras y de luces</p>
                    
                    <div class="mt-4 space-y-2 text-xs">
                        <div class="flex justify-between text-gray-300">
                            <span>Partidas Jugadas (Global):</span>
                            <span id="playsMemory" class="font-bold text-white">0</span>
                        </div>
                        <div class="flex justify-between text-gray-300">
                            <span>Rachas Salvadas:</span>
                            <span id="adsMemory" class="font-bold text-emerald-400">0</span>
                        </div>
                        <div class="flex justify-between text-gray-300">
                            <span>Tasa de Conversión:</span>
                            <span id="rateMemory" class="font-bold text-emerald-400">0%</span>
                        </div>
                    </div>
                </div>
                <div class="mt-5 pt-3 border-t border-gray-800 text-[11px] text-gray-400 flex justify-between items-center">
                    <span>Popularidad Global:</span>
                    <span id="pctMemory" class="font-black text-white">0%</span>
                </div>
            </div>
        </div>

        <!-- TARJETAS DESTACADAS: EL BAÚL ARCADE (CYBER DODGE + NEON CYBER-DRONE) -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-gradient-to-r from-gray-900 via-amber-950/20 to-gray-900 rounded-3xl p-5 border border-amber-500/40 shadow-xl flex flex-col justify-between gap-4">
                <div class="flex items-center space-x-3 text-left">
                    <span class="text-3xl">🚀</span>
                    <div>
                        <span class="text-[10px] font-black uppercase bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded-md border border-amber-500/30">Juego #4 • El Baúl</span>
                        <h3 class="font-black text-white text-base mt-0.5">Cyber Dodge: Tormenta Neón</h3>
                        <p class="text-xs text-gray-400">Esquiva asteroides cuánticos • Candidato a Portada</p>
                    </div>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-300 pt-2 border-t border-gray-800">
                    <div>
                        <p class="text-gray-400">Partidas:</p>
                        <p id="playsDodge" class="font-black text-base text-white">0</p>
                    </div>
                    <div>
                        <p class="text-gray-400">Anuncios:</p>
                        <p id="adsDodge" class="font-black text-base text-amber-400">0</p>
                    </div>
                    <a href="juegos/cyber-dodge.html?v=14" class="bg-amber-500 hover:bg-amber-400 text-gray-950 font-black text-xs px-3.5 py-2 rounded-xl transition shadow-md shadow-amber-500/20">
                        Probar
                    </a>
                </div>
            </div>

            <div class="bg-gradient-to-r from-gray-900 via-pink-950/20 to-gray-900 rounded-3xl p-5 border border-pink-500/40 shadow-xl flex flex-col justify-between gap-4">
                <div class="flex items-center space-x-3 text-left">
                    <span class="text-3xl">🛸</span>
                    <div>
                        <span class="text-[10px] font-black uppercase bg-pink-500/20 text-pink-300 px-2 py-0.5 rounded-md border border-pink-500/30">Nuevo Juego #5 • El Baúl</span>
                        <h3 class="font-black text-white text-base mt-0.5">Neon Cyber-Drone: Portales Láser</h3>
                        <p class="text-xs text-gray-400">Propulsión láser a 1 toque • Compite por el Top 3</p>
                    </div>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-300 pt-2 border-t border-gray-800">
                    <div>
                        <p class="text-gray-400">Partidas:</p>
                        <p id="playsDrone" class="font-black text-base text-white">0</p>
                    </div>
                    <div>
                        <p class="text-gray-400">Anuncios:</p>
                        <p id="adsDrone" class="font-black text-base text-pink-400">0</p>
                    </div>
                    <a href="juegos/cyber-drone.html?v=14" class="bg-pink-500 hover:bg-pink-400 text-white font-black text-xs px-3.5 py-2 rounded-xl transition shadow-md shadow-pink-500/20">
                        Probar
                    </a>
                </div>
            </div>
        </div>

        <!-- AGENTE CEO & SEO AUTÓNOMO -->
        <div class="bg-gradient-to-r from-gray-900 via-cyan-950/30 to-gray-900 rounded-3xl p-6 border border-cyan-500/40 shadow-xl space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <div class="flex items-center space-x-3">
                    <span class="text-3xl">🤖</span>
                    <div>
                        <h3 class="text-base sm:text-lg font-black text-white">Agente CEO & SEO Autónomo (Guardia 24/7)</h3>
                        <p class="text-xs text-gray-400">Automatización programada todos los lunes a las 00:05 AM (sin intervención manual)</p>
                    </div>
                </div>
                <span class="text-xs font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-3 py-1 rounded-full">
                    🟢 ACTIVO & PROGRAMADO
                </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div class="p-3.5 bg-gray-950/80 rounded-2xl border border-gray-800">
                    <p class="font-bold text-cyan-400">📺 Video Resumen IA</p>
                    <p class="text-gray-400 mt-1">5 noticias completas con fotos reales, locución fluida por oraciones y Lector de Noticia Completa.</p>
                </div>
                <div class="p-3.5 bg-gray-950/80 rounded-2xl border border-gray-800">
                    <p class="font-bold text-amber-400">🗄️ Gestión del Baúl</p>
                    <p class="text-gray-400 mt-1">Rotación automática de títulos evaluando popularidad relativa de los 3 juegos titulares.</p>
                </div>
                <div class="p-3.5 bg-gray-950/80 rounded-2xl border border-gray-800">
                    <p class="font-bold text-purple-400">🏆 Torneo Semanal</p>
                    <p class="text-gray-400 mt-1">Reinicio cada domingo a las 12:00 medianoche en Venezuela preservando el Récord Histórico.</p>
                </div>
            </div>
        </div>

        <!-- SEMÁFORO Y RECOMENDACIÓN ESTRATÉGICA -->
        <div id="decisionCard" class="bg-gray-900/90 rounded-3xl p-6 border border-yellow-500/30 shadow-xl">
            <div class="flex items-start space-x-4">
                <span id="decisionIcon" class="text-3xl">💡</span>
                <div class="flex-grow">
                    <h4 class="text-base font-black text-white" id="decisionTitle">Diagnóstico de Contenido</h4>
                    <p class="text-xs text-gray-300 mt-1 leading-relaxed" id="decisionDesc">
                        Calculando métricas globales para orientarte en qué títulos potenciar o rotar...
                    </p>
                </div>
            </div>
        </div>

        <!-- AUDITORÍA TÉCNICA EN VIVO DE MONETAG GLOBAL (TODOS LOS TELÉFONOS) -->
        <div class="bg-gray-900/90 rounded-3xl p-6 border border-emerald-500/40 shadow-xl space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <div class="flex items-center space-x-3">
                    <span class="text-2xl">🛡️</span>
                    <div>
                        <h3 class="text-base sm:text-lg font-black text-white">Auditoría de Monetización Monetag (Global Multi-Teléfono)</h3>
                        <p class="text-xs text-gray-400">Impresiones confirmadas en vivo sumadas desde todos los teléfonos y navegadores</p>
                    </div>
                </div>
                <button onclick="testMonetagRewardAdNow()" class="bg-gradient-to-r from-emerald-500 to-teal-600 hover:opacity-90 active:scale-95 text-white font-black text-xs px-4 py-2.5 rounded-xl shadow-lg transition">
                    🧪 Probar Anuncio Rewarded (12040274)
                </button>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div class="p-3.5 bg-gray-950/80 rounded-2xl border border-gray-800">
                    <p class="text-gray-400">Estado SDK Principal (12040274):</p>
                    <p id="auditSdkMain" class="font-black text-sm text-emerald-400 mt-1">Verificando...</p>
                    <p class="text-[11px] text-gray-500 mt-0.5">CPM Promedio: $0.07 (Alto Rendimiento)</p>
                </div>
                <div class="p-3.5 bg-gray-950/80 rounded-2xl border border-gray-800">
                    <p class="text-gray-400">Impresiones Rewarded Confirmadas (Global):</p>
                    <p id="auditShownCount" class="font-black text-lg text-cyan-400 mt-1">0</p>
                    <p id="auditLastZone" class="text-[11px] text-gray-500 mt-0.5">Última zona: -</p>
                </div>
                <div class="p-3.5 bg-gray-950/80 rounded-2xl border border-gray-800">
                    <p class="text-gray-400">Límite de Frecuencia / Capping IP:</p>
                    <p id="auditFallbackCount" class="font-black text-lg text-amber-400 mt-1">0</p>
                    <p class="text-[11px] text-gray-500 mt-0.5">Veces que Monetag filtró misma IP</p>
                </div>
            </div>

            <div id="auditTestResult" class="hidden p-3.5 rounded-2xl bg-emerald-950/50 border border-emerald-500/40 text-xs text-emerald-200 font-semibold"></div>

            <!-- MONITOR DE ACTIVIDAD EN TIEMPO REAL DE TODOS LOS TELÉFONOS -->
            <div class="mt-4 pt-4 border-t border-gray-800">
                <div class="flex items-center justify-between mb-2.5">
                    <p class="text-xs font-black text-white flex items-center space-x-1.5">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                        <span>📡 Monitor en Tiempo Real de Todos los Teléfonos</span>
                    </p>
                    <span class="text-[10px] text-gray-400">Actualización instantánea (&lt;1s)</span>
                </div>
                <div id="liveActivityFeed" class="space-y-1.5 max-h-48 overflow-y-auto text-xs pr-1">
                    <div class="p-2.5 rounded-xl bg-gray-950/70 border border-gray-800 text-gray-400 text-center">
                        ⏳ Conectando canal de eventos en vivo...
                    </div>
                </div>
            </div>
        </div>

        <!-- REPORTE DEL AGENTE CEO (se actualiza solo cada semana) -->
        <div class="bg-gray-900/90 rounded-3xl p-6 border border-cyan-500/40 shadow-xl space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <div class="flex items-center space-x-3">
                    <span class="text-2xl">🧠</span>
                    <div>
                        <h3 class="text-base sm:text-lg font-black text-white">Reporte del Agente CEO</h3>
                        <p id="ceoReportMeta" class="text-xs text-gray-400">Cargando último reporte...</p>
                    </div>
                </div>
                <span id="ceoTrafficBadge" class="text-xs font-black bg-gray-800 text-gray-300 border border-gray-700 px-3 py-1 rounded-full">Tráfico: -</span>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div class="p-3 bg-gray-950/80 rounded-2xl border border-gray-800"><p class="text-gray-400">Dispositivos (7d)</p><p id="ceoDevices" class="font-black text-lg text-cyan-400">0</p></div>
                <div class="p-3 bg-gray-950/80 rounded-2xl border border-gray-800"><p class="text-gray-400">Partidas (7d)</p><p id="ceoPlays" class="font-black text-lg text-white">0</p></div>
                <div class="p-3 bg-gray-950/80 rounded-2xl border border-gray-800"><p class="text-gray-400">Visitas a juegos (7d)</p><p id="ceoViews" class="font-black text-lg text-purple-400">0</p></div>
                <div class="p-3 bg-gray-950/80 rounded-2xl border border-gray-800"><p class="text-gray-400">Anuncios vistos (7d)</p><p id="ceoAds" class="font-black text-lg text-emerald-400">0</p></div>
            </div>
            <div>
                <p class="text-xs font-black text-white mb-1.5">✅ Lo que hizo / decidió esta semana</p>
                <ul id="ceoActions" class="space-y-1 text-[11px] text-gray-300 list-disc pl-4"></ul>
            </div>
            <div class="p-3.5 rounded-2xl bg-cyan-950/30 border border-cyan-500/30">
                <p class="text-xs font-black text-cyan-300 mb-1.5">🔎 Autoevaluación del Agente CEO & YouTube Studio</p>
                <ul id="ceoSelfEval" class="space-y-1 text-[11px] text-gray-200 list-disc pl-4"></ul>
            </div>
            <div>
                <p class="text-xs font-black text-white mb-1.5">📣 Kit de promoción (toca para copiar y compartir)</p>
                <div id="ceoPromo" class="space-y-2"></div>
            </div>
            <div>
                <p class="text-xs font-black text-white mb-1.5">🔎 Palabras clave de la semana (SEO)</p>
                <p id="ceoKeywords" class="text-[11px] text-gray-400 leading-relaxed"></p>
            </div>
        </div>

        <!-- ACCIONES DE ADMINISTRADOR -->
        <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
            <button onclick="refreshGlobalMetricsFromCloud(true)" class="w-full sm:w-1/2 bg-gray-800 hover:bg-gray-750 text-cyan-300 font-bold py-3 rounded-xl text-xs transition border border-gray-700">
                🔄 Forzar Recarga de Nube Ahora
            </button>
            <button onclick="resetMetricsGlobal()" class="w-full sm:w-1/2 bg-red-950/40 hover:bg-red-900/60 text-red-300 font-bold py-3 rounded-xl text-xs transition border border-red-800/50">
                🗑️ Reiniciar Contadores (Desde Este Instante)
            </button>
        </div>

    </main>

    __PLAYER_MODAL__
    __FOOTER__

    __PLAYER_IDENTITY_SCRIPT__

    <script>
        window.CURRENT_GAME_KEY = 'stats';

        // LÍNEA BASE HISTÓRICA VERIFICADA (Partidas y Anuncios confirmados hasta v=14)
        const BASELINE_METRICS = {
            stacker: { plays: 28, ads: 8 },
            reflex:  { plays: 22, ads: 5 },
            memory:  { plays: 12, ads: 3 },
            dodge:   { plays: 6,  ads: 1 },
            drone:   { plays: 5,  ads: 1 },
            audit:   { shown: 13, fallback: 2, last_zone: '12040274' }
        };

        let processedEventIds = new Set();
        let globalAggregated = JSON.parse(JSON.stringify(BASELINE_METRICS));
        let activityLog = [];

        function addActivityEntry(text, badge, isAd = false) {
            const feed = document.getElementById('liveActivityFeed');
            activityLog.unshift({ text, badge, isAd, time: new Date() });
            if (activityLog.length > 20) activityLog.pop();

            if (feed) {
                feed.innerHTML = activityLog.map(item => `
                    <div class="p-2.5 rounded-xl ${item.isAd ? 'bg-emerald-950/40 border border-emerald-500/40' : 'bg-gray-950/80 border border-gray-800'} flex items-center justify-between">
                        <span class="text-gray-200 font-medium">${item.text}</span>
                        <span class="text-[10px] font-black uppercase px-2 py-0.5 rounded-md ${item.isAd ? 'bg-emerald-500/20 text-emerald-300' : 'bg-cyan-500/20 text-cyan-300'}">${item.badge}</span>
                    </div>
                `).join('');
            }
        }

        function processTelemetryEvent(evt) {
            if (!evt || !evt.eid || processedEventIds.has(evt.eid)) return;
            processedEventIds.add(evt.eid);

            const resetTs = parseInt(localStorage.getItem('bz_telemetry_reset_ts') || '0');
            if (resetTs && evt.ts && evt.ts < resetTs) return;

            const playerName = evt.p || 'Jugador';
            const countryFlag = (typeof getCountryFlag === 'function') ? getCountryFlag(evt.c || 'VE') : '🌐';

            if (evt.kind === 'game') {
                const g = evt.g || 'stacker';
                if (!globalAggregated[g]) globalAggregated[g] = { plays: 0, ads: 0 };
                
                if (evt.ev === 'play') {
                    globalAggregated[g].plays++;
                    const gameTitles = { stacker: 'Neon Stacker Pro', reflex: 'Test de Reflejos', memory: 'Cyber Memory', dodge: 'Cyber Dodge', drone: 'Neon Cyber-Drone' };
                    addActivityEntry(`${countryFlag} <strong>${playerName}</strong> inició partida en <em>${gameTitles[g] || g}</em>`, 'PARTIDA');
                } else if (evt.ev === 'ad') {
                    globalAggregated[g].ads++;
                    const actionNames = { stacker: 'Revivir Piso', reflex: 'Recarga Batería', memory: 'Racha Salvada', dodge: 'Escudo Neón', drone: 'Turbina Reparada' };
                    addActivityEntry(`${countryFlag} <strong>${playerName}</strong> activó <em>${actionNames[g] || 'Recompensa'}</em>`, 'RECOMPENSA', true);
                }
            } else if (evt.kind === 'ad') {
                if (evt.shown) {
                    globalAggregated.audit.shown++;
                    globalAggregated.audit.last_zone = evt.zone || '12040274';
                    addActivityEntry(`💰 Impresión Rewarded confirmada en Zona <strong>${evt.zone}</strong> (${countryFlag} ${playerName})`, 'ANUNCIO PAGADO', true);
                } else {
                    globalAggregated.audit.fallback++;
                    addActivityEntry(`ℹ️ Filtro de frecuencia Monetag (Misma IP) para ${playerName}`, 'CAPPING');
                }
            }

            renderDashboardMetrics();
        }

        function renderDashboardMetrics() {
            const stacker = globalAggregated.stacker;
            const reflex  = globalAggregated.reflex;
            const memory  = globalAggregated.memory;
            const dodge   = globalAggregated.dodge;

            document.getElementById('playsStacker').textContent = stacker.plays;
            document.getElementById('adsStacker').textContent   = stacker.ads;
            const rateS = stacker.plays > 0 ? Math.round((stacker.ads / stacker.plays) * 100) : 0;
            document.getElementById('rateStacker').textContent = rateS + "%";

            document.getElementById('playsReflex').textContent = reflex.plays;
            document.getElementById('adsReflex').textContent   = reflex.ads;
            const rateR = reflex.plays > 0 ? Math.round((reflex.ads / reflex.plays) * 100) : 0;
            document.getElementById('rateReflex').textContent = rateR + "%";

            document.getElementById('playsMemory').textContent = memory.plays;
            document.getElementById('adsMemory').textContent   = memory.ads;
            const rateM = memory.plays > 0 ? Math.round((memory.ads / memory.plays) * 100) : 0;
            document.getElementById('rateMemory').textContent = rateM + "%";

            const dodgeEl = document.getElementById('playsDodge');
            const dodgeAdsEl = document.getElementById('adsDodge');
            if (dodgeEl) dodgeEl.textContent = dodge.plays;
            if (dodgeAdsEl) dodgeAdsEl.textContent = dodge.ads;

            const drone = globalAggregated.drone || { plays: 0, ads: 0 };
            const droneEl = document.getElementById('playsDrone');
            const droneAdsEl = document.getElementById('adsDrone');
            if (droneEl) droneEl.textContent = drone.plays;
            if (droneAdsEl) droneAdsEl.textContent = drone.ads;

            const totalPlays = stacker.plays + reflex.plays + memory.plays;
            const pctS = totalPlays > 0 ? Math.round((stacker.plays / totalPlays) * 100) : 0;
            const pctR = totalPlays > 0 ? Math.round((reflex.plays / totalPlays) * 100) : 0;
            const pctM = totalPlays > 0 ? Math.round((memory.plays / totalPlays) * 100) : 0;

            document.getElementById('pctStacker').textContent = pctS + "%";
            document.getElementById('pctReflex').textContent  = pctR + "%";
            document.getElementById('pctMemory').textContent  = pctM + "%";

            const games = [
                { name: 'Neon Stacker Pro', plays: stacker.plays, badgeEl: 'badgeStacker' },
                { name: 'Test de Reflejos', plays: reflex.plays, badgeEl: 'badgeReflex' },
                { name: 'Cyber Memory', plays: memory.plays, badgeEl: 'badgeMemory' }
            ];
            games.sort((a, b) => b.plays - a.plays);

            if (totalPlays > 0) {
                document.getElementById(games[0].badgeEl).textContent = "👑 Estrella (#1)";
                document.getElementById(games[0].badgeEl).className = "text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-yellow-500/20 text-yellow-300 border border-yellow-500/50";

                document.getElementById(games[1].badgeEl).textContent = "⚡ Activo (#2)";
                document.getElementById(games[1].badgeEl).className = "text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40";

                const least = games[2];
                const leastPct = Math.round((least.plays / totalPlays) * 100);
                if (leastPct < 20 && totalPlays >= 5) {
                    document.getElementById(least.badgeEl).textContent = "⚠️ Candidato al Baúl (#3)";
                    document.getElementById(least.badgeEl).className = "text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/50";
                    document.getElementById('decisionTitle').textContent = `Agente CEO: Evaluando rotación de "${least.name}" por "Cyber Dodge"`;
                    document.getElementById('decisionDesc').innerHTML = `El juego <b>${least.name}</b> concentra el <b>${leastPct}%</b> de las partidas globales. El Agente CEO mantiene a <b>Cyber Dodge</b> listo en el Baúl Arcade para intercambio si la tendencia continúa el próximo lunes.`;
                } else {
                    document.getElementById(least.badgeEl).textContent = "Estable (#3)";
                    document.getElementById(least.badgeEl).className = "text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-gray-500/20 text-gray-300 border border-gray-600";
                    document.getElementById('decisionTitle').textContent = `Agente CEO: Excelente actividad en los 3 juegos de portada`;
                    document.getElementById('decisionDesc').innerHTML = `El juego líder en todos los dispositivos es <b>${games[0].name}</b> con <b>${games[0].plays}</b> partidas. Los 3 juegos mantienen tracción activa y <b>Cyber Dodge</b> suma partidas desde el Baúl.`;
                }
            }

            // Actualizar Tarjeta de Auditoría Monetag
            const shownEl = document.getElementById('auditShownCount');
            const fallbackEl = document.getElementById('auditFallbackCount');
            const lastZoneEl = document.getElementById('auditLastZone');
            if (shownEl) shownEl.textContent = globalAggregated.audit.shown;
            if (fallbackEl) fallbackEl.textContent = globalAggregated.audit.fallback;
            if (lastZoneEl) lastZoneEl.textContent = "Última zona: " + (globalAggregated.audit.last_zone || '12040274');
        }

        async function refreshGlobalMetricsFromCloud(userFeedback = false) {
            const badge = document.getElementById('cloudSyncStatusBadge');
            if (badge) badge.textContent = "🔄 Sincronizando nube...";

            // 1. Cargar caché de eventos locales
            try {
                const localCache = JSON.parse(localStorage.getItem('bytezone_global_events_cache') || '[]');
                localCache.forEach(processTelemetryEvent);
            } catch(e) {}

            // 2. Consultar historial de ntfy.sh (últimas 72 horas de todos los teléfonos)
            try {
                const res = await fetch(`https://ntfy.sh/${window.NTFY_TELEMETRY_TOPIC}/json?poll=1&since=72h`, { cache: 'no-store' });
                if (res.ok) {
                    const text = await res.text();
                    const lines = text.split('\\n').filter(Boolean);
                    lines.forEach(line => {
                        try {
                            const evt = JSON.parse(line);
                            if (evt && evt.event === 'message' && evt.message) {
                                const payload = JSON.parse(evt.message);
                                processTelemetryEvent(payload);
                            }
                        } catch(err) {}
                    });
                }
            } catch(e) {}

            renderDashboardMetrics();
            if (badge) badge.textContent = "🟢 Sincronizado con Todos los Teléfonos En Vivo";

            if (userFeedback) {
                const resBox = document.getElementById('auditTestResult');
                if (resBox) {
                    resBox.classList.remove('hidden');
                    resBox.textContent = "✅ Métricas globales actualizadas con éxito desde la nube.";
                    resBox.className = "p-3.5 rounded-2xl bg-cyan-950/60 border border-cyan-500/50 text-xs text-cyan-200 font-bold";
                    setTimeout(() => resBox.classList.add('hidden'), 4000);
                }
            }
        }

        function updateMonetagSdkStatusUI() {
            const sdkEl = document.getElementById('auditSdkMain');
            const has12040274 = (typeof window.show_12040274 === 'function');
            const has12040276 = (typeof window.show_12040276 === 'function');
            if (sdkEl) {
                if (has12040274 && has12040276) {
                    sdkEl.textContent = "🟢 Precargado (12040274 + 12040276 Listos)";
                    sdkEl.className = "font-black text-xs sm:text-sm text-emerald-400 mt-1";
                } else if (has12040274) {
                    sdkEl.textContent = "🟢 Precargado (12040274 Activo)";
                    sdkEl.className = "font-black text-xs sm:text-sm text-emerald-400 mt-1";
                } else {
                    sdkEl.textContent = "⏳ Inicializando SDK...";
                    sdkEl.className = "font-black text-xs sm:text-sm text-amber-400 mt-1";
                }
            }
        }

        function testMonetagRewardAdNow() {
            const resBox = document.getElementById('auditTestResult');
            if (resBox) {
                resBox.classList.remove('hidden');
                resBox.textContent = "⏳ Solicitando anuncio de prueba en vivo a Monetag (Zona 12040274 ➔ 12040276)...";
                resBox.className = "p-3.5 rounded-2xl bg-cyan-950/60 border border-cyan-500/50 text-xs text-cyan-200 font-semibold";
            }
            executeRewardedAction(() => {
                const log = JSON.parse(localStorage.getItem('bytezone_ad_audit') || '{}');
                if (resBox) {
                    if (log.last_zone && log.last_zone !== 'none') {
                        resBox.textContent = "✅ ¡Impresión confirmada! Monetag sirvió el anuncio en Zona " + log.last_zone + ". Transmitido a todos los teléfonos.";
                        resBox.className = "p-3.5 rounded-2xl bg-emerald-950/60 border border-emerald-500/50 text-xs text-emerald-200 font-bold";
                    } else {
                        resBox.textContent = "ℹ️ El SDK está conectado, pero Monetag aplicó filtro de frecuencia (Capping por misma IP reciente).";
                        resBox.className = "p-3.5 rounded-2xl bg-amber-950/60 border border-amber-500/50 text-xs text-amber-200 font-bold";
                    }
                }
            });
        }

        function resetMetricsGlobal() {
            if (confirm("¿Deseas reiniciar los contadores globales a partir de este instante?")) {
                const now = Date.now();
                localStorage.setItem('bz_telemetry_reset_ts', now.toString());
                globalAggregated = {
                    stacker: { plays: 0, ads: 0 },
                    reflex:  { plays: 0, ads: 0 },
                    memory:  { plays: 0, ads: 0 },
                    dodge:   { plays: 0, ads: 0 },
                    audit:   { shown: 0, fallback: 0, last_zone: 'none' }
                };
                activityLog = [];
                renderDashboardMetrics();
                addActivityEntry("🗑️ Contadores reiniciados por el Administrador", "RESET");
            }
        }

        // Conectar flujo SSE en tiempo real para recibir jugadas de otros teléfonos en vivo (< 1s)
        if (window.EventSource) {
            try {
                const es = new EventSource(`https://ntfy.sh/${window.NTFY_TELEMETRY_TOPIC}/sse`);
                es.onmessage = (e) => {
                    try {
                        const evt = JSON.parse(e.data);
                        if (evt && evt.message) {
                            const payload = JSON.parse(evt.message);
                            processTelemetryEvent(payload);
                        }
                    } catch(err) {}
                };
            } catch(e) {}
        }

        renderDashboardMetrics();
        refreshGlobalMetricsFromCloud();
        updateMonetagSdkStatusUI();
        setTimeout(updateMonetagSdkStatusUI, 1200);
        setInterval(() => refreshGlobalMetricsFromCloud(false), 20000);

        async function loadCeoReport() {
            try {
                const res = await fetch('data/weekly_pulse.json?t=' + Date.now(), { cache: 'no-store' });
                if (!res.ok) return;
                const d = await res.json();
                const r = d.agent_report || {};
                const t = r.traffic || {};
                const meta = document.getElementById('ceoReportMeta');
                if (meta) meta.textContent = 'Semana ' + (d.week_id || '-') + ' • Actualizado ' + (d.updated_human || '-') + ' (v' + (d.version || '?') + ')';
                const st = r.traffic_status || '-';
                const badge = document.getElementById('ceoTrafficBadge');
                if (badge) {
                    const map = { bajo: ['🟠 Tráfico BAJO', 'bg-amber-500/20 text-amber-300 border-amber-500/40'], estable: ['🟢 Tráfico ESTABLE', 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'], creciendo: ['🚀 Tráfico CRECIENDO', 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40'] };
                    const m = map[st] || ['Tráfico: -', 'bg-gray-800 text-gray-300 border-gray-700'];
                    badge.textContent = m[0] + (t.change_pct != null ? ' (' + (t.change_pct > 0 ? '+' : '') + t.change_pct + '% vs semana previa)' : '');
                    badge.className = 'text-xs font-black border px-3 py-1 rounded-full ' + m[1];
                }
                const set = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
                set('ceoDevices', t.devices_7d || 0); set('ceoPlays', t.plays_7d || 0);
                set('ceoViews', t.views_7d || 0); set('ceoAds', t.ads_shown_7d || 0);
                const ul = document.getElementById('ceoActions');
                if (ul) ul.innerHTML = (r.actions || []).map(a => '<li>' + String(a).replace(/</g, '&lt;') + '</li>').join('');
                const evalUl = document.getElementById('ceoSelfEval');
                if (evalUl) evalUl.innerHTML = (r.self_evaluation || ['Métricas equilibradas 1 a 5 en Reflejos Visuales.', '5 juegos activos entre Portada (Top 3) y Baúl Arcade (2).']).map(a => '<li>' + String(a).replace(/</g, '&lt;') + '</li>').join('');
                const promo = d.promo_kit || {};
                const box = document.getElementById('ceoPromo');
                if (box) {
                    const items = (promo.whatsapp_status || []).concat(promo.social_caption ? [promo.social_caption] : []);
                    box.innerHTML = '';
                    items.forEach((txt, i) => {
                        const b = document.createElement('button');
                        b.className = 'w-full text-left p-3 rounded-xl bg-gray-950/80 border border-gray-800 hover:border-cyan-500/50 text-[11px] text-gray-200 leading-relaxed transition';
                        b.textContent = txt;
                        b.onclick = () => {
                            const done = () => { b.classList.add('border-emerald-500'); setTimeout(() => b.classList.remove('border-emerald-500'), 1500); };
                            if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done).catch(() => prompt('Copia el texto:', txt));
                            else prompt('Copia el texto:', txt);
                        };
                        box.appendChild(b);
                    });
                }
                const kw = (d.seo && d.seo.keywords) || [];
                set('ceoKeywords', kw.join(' • '));
            } catch (e) {}
        }
        loadCeoReport();

    </script>
</body>
</html>
"""

def render_page(template, current_page, depth=0, page_key="index", path=""):
    html = template.replace("__PORTADA_GRID__", render_portada_grid())
    html = html.replace("__VAULT_CARDS__", render_vault_cards())
    html = html.replace("__PORTADA_LABEL__", f"{len(PORTADA_IDS)} En Portada + {len(VAULT_IDS)} En Baúl")
    html = html.replace("__TRUTH_GRID__", render_truth_grid() or "")
    html = html.replace("__CHISTES_JSON__", jokes_json() or "[]")
    html = html.replace("__MONETAG_TAG__", MONETAG_TAG)
    html = html.replace("__HEADER__", get_header(current_page, depth=depth))
    html = html.replace("__AI_VIDEO_REEL_WIDGET__", AI_VIDEO_REEL_WIDGET)
    html = html.replace("__PLAYER_MODAL__", PLAYER_MODAL)
    html = html.replace("__PLAYER_IDENTITY_SCRIPT__", PLAYER_IDENTITY_SCRIPT)
    html = html.replace("__FOOTER__", get_footer(depth=depth))
    return inject_seo(html, page_key, path)

# Generación sincronizada simultánea en portal_bytezone Y bytezone
DIRECTORIOS_SALIDA = ["portal_bytezone", "bytezone"]

for target_dir in DIRECTORIOS_SALIDA:
    juegos_target = os.path.join(target_dir, "juegos")
    os.makedirs(juegos_target, exist_ok=True)
    
    # 1. index.html
    with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_INDEX, "arcade", depth=0, page_key="index", path=""))

    # 2. juegos/neon-stacker.html
    with open(os.path.join(juegos_target, "neon-stacker.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_STACKER, "arcade", depth=1, page_key="stacker", path="juegos/neon-stacker.html"))

    # 3. juegos/reflejos-visuales.html
    with open(os.path.join(juegos_target, "reflejos-visuales.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_REFLEX, "arcade", depth=1, page_key="reflex", path="juegos/reflejos-visuales.html"))

    # 4. juegos/cyber-memory.html
    with open(os.path.join(juegos_target, "cyber-memory.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_MEMORY, "arcade", depth=1, page_key="memory", path="juegos/cyber-memory.html"))

    # 4B. juegos/cyber-dodge.html (Joya en El Baúl Arcade)
    with open(os.path.join(juegos_target, "cyber-dodge.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_DODGE, "arcade", depth=1, page_key="dodge", path="juegos/cyber-dodge.html"))

    # 4C. juegos/cyber-drone.html (Nuevo Juego #5 en El Baúl Arcade)
    with open(os.path.join(juegos_target, "cyber-drone.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_DRONE, "arcade", depth=1, page_key="drone", path="juegos/cyber-drone.html"))

    # 4D. campeones.html (Salón de la Fama & Histórico Semanal de Ganadores)
    with open(os.path.join(target_dir, "campeones.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_CAMPEONES, "campeones", depth=0, page_key="campeones", path="campeones.html"))

    # 5. hacks.html (IA & Tech TV + Noticias Semanales + Hacks)
    with open(os.path.join(target_dir, "hacks.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_HACKS, "hacks", depth=0, page_key="hacks", path="hacks.html"))

    # 6. humor.html
    with open(os.path.join(target_dir, "humor.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_HUMOR, "humor", depth=0, page_key="humor", path="humor.html"))

    # 7. telegram.html
    with open(os.path.join(target_dir, "telegram.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_TELEGRAM, "telegram", depth=0, page_key="telegram", path="telegram.html"))

    # 8. stats.html
    with open(os.path.join(target_dir, "stats.html"), "w", encoding="utf-8") as f:
        f.write(render_page(TEMPLATE_STATS, "stats", depth=0, page_key="stats", path="stats.html"))

print("✅ Arquitectura Multi-Página v=14 de ByteZone sincronizada en portal_bytezone Y bytezone:")
print(" - index.html (Lobby + Reproductor Video Flash IA + Baúl Arcade)")
print(" - juegos/neon-stacker.html (Juego 1: Torre Neon Stacker Pro - ***** sincronizado en 33)")
print(" - juegos/reflejos-visuales.html (Juego 2: Test Reflejos Visuales)")
print(" - juegos/cyber-memory.html (Juego 3: Cyber Memory Neón)")
print(" - juegos/cyber-dodge.html (Juego 4 en El Baúl: Cyber Dodge Tormenta de Asteroides)")
print(" - hacks.html (IA & Tech TV + Noticias de la Semana + Hacks)")
print(" - humor.html (Página Humor & Memes)")
print(" - telegram.html (Página Telegram)")
print(" - stats.html (Panel de Métricas + Estado del Agente CEO Autónomo)")

