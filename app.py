import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import comtrade
import tempfile, os, io, datetime

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analizador de Fallas · Líneas de Transmisión",
    page_icon="⚡",
    layout="wide",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow:wght@400;600;700;800&display=swap');

* { font-family: 'Barlow', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: #080c14;
    background-image:
        radial-gradient(ellipse at 20% 0%, rgba(0,180,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 100%, rgba(255,140,0,0.05) 0%, transparent 60%);
}
[data-testid="stSidebar"] {
    background: #0d1220;
    border-right: 1px solid rgba(0,180,255,0.12);
}

/* Hide default header */
[data-testid="stHeader"] { background: transparent; }

.hero {
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid rgba(0,180,255,0.12);
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 2.4rem; font-weight: 800; letter-spacing: -1px;
    color: #ffffff; line-height: 1;
}
.hero-title span { color: #00b4ff; }
.hero-sub { color: #4a6080; font-size: 0.9rem; margin-top: 6px; font-weight: 400; }

.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,180,255,0.1);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    transition: border-color 0.2s;
}
.step-card:hover { border-color: rgba(0,180,255,0.3); }
.step-num {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem; color: #00b4ff; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 4px;
}
.step-title { font-size: 1.1rem; font-weight: 700; color: #e8f0ff; }

/* Metric cards */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin: 1.5rem 0;
}
.mcard {
    background: #0d1220;
    border: 1px solid rgba(0,180,255,0.15);
    border-radius: 10px;
    padding: 1.1rem 1rem;
    text-align: center;
}
.mcard-label {
    font-size: 0.68rem; color: #4a6080; text-transform: uppercase;
    letter-spacing: 1.5px; margin-bottom: 6px;
}
.mcard-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.6rem; color: #00b4ff; font-weight: 400;
    line-height: 1;
}
.mcard-unit { font-size: 0.72rem; color: #4a6080; margin-top: 4px; }

/* Fault type badge */
.fault-badge {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 20px; border-radius: 6px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.5rem; letter-spacing: 3px;
    font-weight: 400;
}
.badge-ground  { background: rgba(255,60,60,0.1);  border: 1px solid rgba(255,60,60,0.4);  color: #ff4444; }
.badge-phase   { background: rgba(255,165,0,0.1);  border: 1px solid rgba(255,165,0,0.4);  color: #ffa500; }
.badge-3ph     { background: rgba(180,0,255,0.1);  border: 1px solid rgba(180,0,255,0.4);  color: #cc44ff; }
.badge-unknown { background: rgba(100,100,100,0.1);border: 1px solid rgba(100,100,100,0.4);color: #888; }

/* Location bar */
.loc-bar-wrap { margin: 1.2rem 0; }
.loc-bar-track {
    height: 12px; background: rgba(255,255,255,0.06);
    border-radius: 6px; position: relative; overflow: visible;
    border: 1px solid rgba(0,180,255,0.1);
}
.loc-bar-fill {
    height: 100%; border-radius: 6px;
    background: linear-gradient(90deg, #00b4ff, #0070cc);
    position: absolute; left: 0; top: 0;
}
.loc-bar-marker {
    width: 14px; height: 22px;
    background: #ff4444;
    border-radius: 3px;
    position: absolute; top: -5px;
    transform: translateX(-50%);
}
.loc-bar-labels {
    display: flex; justify-content: space-between;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem; color: #4a6080; margin-top: 6px;
}

.section-title {
    font-size: 0.72rem; color: #00b4ff; letter-spacing: 3px;
    text-transform: uppercase; font-weight: 600;
    border-left: 3px solid #00b4ff; padding-left: 10px;
    margin: 2rem 0 1rem;
}

.consensus-box {
    background: rgba(0,180,255,0.06);
    border: 1px solid rgba(0,180,255,0.25);
    border-radius: 10px;
    padding: 1.2rem 1.8rem;
    margin: 1rem 0;
    display: flex; align-items: center; gap: 16px;
}
.consensus-km {
    font-family: 'Share Tech Mono', monospace;
    font-size: 3rem; color: #00b4ff; line-height: 1;
}
.consensus-sub { color: #4a6080; font-size: 0.85rem; }
.consensus-pct { color: #ffffff; font-size: 1.4rem; font-weight: 700; }

/* Plotly chart background fix */
.js-plotly-plot .plotly { border-radius: 10px; overflow: hidden; }

.stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,180,255,0.08);
    border-radius: 6px;
    color: #4a6080; padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,180,255,0.1) !important;
    border-color: rgba(0,180,255,0.4) !important;
    color: #00b4ff !important;
}

hr { border-color: rgba(0,180,255,0.08); }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
LINE_PARAMS = {
    "69 kV — ACSR HAWK 477 kcmil": {
        "vkv": 69.0, "Z1": complex(0.0841, 0.3932), "Z0": complex(0.2530, 1.1796),
        "CTR": 400, "VTR": 600, "I_rated": 659,
    },
    "13.8 kV — ACSR 266 kcmil": {
        "vkv": 13.8, "Z1": complex(0.1710, 0.3812), "Z0": complex(0.3402, 1.1436),
        "CTR": 200, "VTR": 120, "I_rated": 460,
    },
}

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">⚡ FAULT <span>ANALYZER</span></div>
  <div class="hero-sub">Análisis de fallas en líneas de transmisión · Archivos COMTRADE</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PASO 1 — Selección de línea
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Paso 1 · Tipo de línea</div>', unsafe_allow_html=True)

line_name = st.radio(
    "",
    options=list(LINE_PARAMS.keys()),
    horizontal=True,
    label_visibility="collapsed",
)
cfg_line = LINE_PARAMS[line_name]

col1, col2, col3 = st.columns(3)
line_length = col1.number_input("Longitud de la línea (km)", min_value=1.0, max_value=500.0,
                                 value=50.0 if "69" in line_name else 15.0, step=0.5)
col2.metric("Tensión nominal", f"{cfg_line['vkv']} kV")
col3.metric("Corriente nominal", f"{cfg_line['I_rated']} A")

# ═══════════════════════════════════════════════════════════════════════════════
# PASO 2 — Subir archivos
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Paso 2 · Cargar archivo COMTRADE</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
cfg_file = col_a.file_uploader("Archivo .CFG", type=["cfg", "CFG"])
dat_file = col_b.file_uploader("Archivo .DAT", type=["dat", "DAT"])

if not (cfg_file and dat_file):
    st.info("📂 Sube los archivos .CFG y .DAT del relé de protección para comenzar el análisis.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# CARGA Y ANÁLISIS
# ═══════════════════════════════════════════════════════════════════════════════
with st.spinner("⚙️ Procesando COMTRADE…"):
    try:
        rec = comtrade.Comtrade()
        with tempfile.TemporaryDirectory() as tmp:
            cp = os.path.join(tmp, "r.cfg")
            dp = os.path.join(tmp, "r.dat")
            cfg_file.seek(0); dat_file.seek(0)
            open(cp, "wb").write(cfg_file.read())
            open(dp, "wb").write(dat_file.read())
            rec.load(cp, dp)

        names  = [ch.name.lower().strip() for ch in rec.cfg.analog_channels]
        analog = np.array(rec.analog, dtype=np.float64)
        t_arr  = np.array(rec.time,   dtype=np.float64)
        fs     = 1.0 / np.median(np.diff(t_arr)) if len(t_arr) > 1 else 3840.0

        def find(patterns):
            for i, n in enumerate(names):
                for p in patterns:
                    if p in n: return i if i < analog.shape[0] else None
            return None

        def get(i):
            return analog[i].copy() if i is not None else np.zeros(len(t_arr))

        Va = get(find(["va","v_a","ua","vpha","ea"]))
        Vb = get(find(["vb","v_b","ub","vphb","eb"]))
        Vc = get(find(["vc","v_c","uc","vphc","ec"]))
        Ia = get(find(["ia","i_a","ifa","ipha"]))
        Ib = get(find(["ib","i_b","ifb","iphb"]))
        Ic = get(find(["ic","i_c","ifc","iphc"]))

    except Exception as e:
        st.error(f"❌ Error al leer COMTRADE: {e}")
        st.stop()

# ─── Signal analysis functions ─────────────────────────────────────────────────
def rms_window(x, fs, cycles=1):
    N = max(2, int(fs / 60 * cycles))
    return np.sqrt(np.convolve(x**2, np.ones(N)/N, mode="same"))

def phasor(x, idx, fs, f0=60.0):
    n = int(fs / f0)
    seg = x[idx:idx+n]
    if len(seg) < n: seg = np.pad(seg, (0, n-len(seg)))
    return np.dot(seg, np.exp(-1j*2*np.pi*np.arange(n)/n)) * 2/n

# Detect onset
n_pre = int(3 * fs / 60)
Ir_rms = rms_window(Ia+Ib+Ic, fs)
base   = np.mean(Ir_rms[:n_pre]) + 5*np.std(Ir_rms[:n_pre])
onset_candidates = np.where(Ir_rms > base)[0]
onset = int(onset_candidates[0]) if len(onset_candidates) > 0 else n_pre

# Pre-fault phasors
pf0 = max(0, onset - int(fs/60))
Va_pf = phasor(Va, pf0, fs); Vb_pf = phasor(Vb, pf0, fs); Vc_pf = phasor(Vc, pf0, fs)
Ia_pf = phasor(Ia, pf0, fs); Ib_pf = phasor(Ib, pf0, fs); Ic_pf = phasor(Ic, pf0, fs)

# Fault phasors
Va_f = phasor(Va, onset, fs); Vb_f = phasor(Vb, onset, fs); Vc_f = phasor(Vc, onset, fs)
Ia_f = phasor(Ia, onset, fs); Ib_f = phasor(Ib, onset, fs); Ic_f = phasor(Ic, onset, fs)

# Fault type detection
oc = lambda If, I0: abs(If) > 1.5 * max(abs(I0), 1e-9)
vd = lambda Vf, V0: abs(Vf) < 0.70 * max(abs(V0), 1e-9)
fa = oc(Ia_f, Ia_pf) or vd(Va_f, Va_pf)
fb = oc(Ib_f, Ib_pf) or vd(Vb_f, Vb_pf)
fc = oc(Ic_f, Ic_pf) or vd(Vc_f, Vc_pf)
I0_ph = (Ia_f+Ib_f+Ic_f)/3
has_gnd = abs(I0_ph) > 0.1 * max(abs(Ia_f), abs(Ib_f), abs(Ic_f), 1e-9)
n_f = sum([fa,fb,fc])

if n_f >= 3:   ft = "3PH" + ("G" if has_gnd else "")
elif n_f == 2:
    if fa and fb:   ft = "ABG" if has_gnd else "AB"
    elif fb and fc: ft = "BCG" if has_gnd else "BC"
    else:           ft = "CAG" if has_gnd else "CA"
elif n_f == 1:
    ft = ("AG" if fa else "BG" if fb else "CG")
else:
    ft = "DESCONOCIDA"

# Duration
Irms_a = rms_window(Ia, fs); Irms_b = rms_window(Ib, fs); Irms_c = rms_window(Ic, fs)
I0a = np.mean(Irms_a[:n_pre]) or 1e-6
I0b = np.mean(Irms_b[:n_pre]) or 1e-6
I0c = np.mean(Irms_c[:n_pre]) or 1e-6
clear = len(Ia)-1
for i in range(onset+int(fs/60), len(Irms_a)):
    if Irms_a[i]<1.2*I0a and Irms_b[i]<1.2*I0b and Irms_c[i]<1.2*I0c:
        clear = i; break
dur_ms = (clear - onset) / fs * 1000

# ─── Fault localization ────────────────────────────────────────────────────────
Z1 = cfg_line["Z1"]; Z0 = cfg_line["Z0"]
k0 = (Z0 - Z1) / (3 * Z1)
Ir_ph = Ia_f + Ib_f + Ic_f
dIa = Ia_f-Ia_pf; dIb = Ib_f-Ib_pf; dIc = Ic_f-Ic_pf

if ft in ("AG","ABG","CAG"):    V,I,dI = Va_f, Ia_f+k0*Ir_ph, dIa
elif ft in ("BG","BCG"):         V,I,dI = Vb_f, Ib_f+k0*Ir_ph, dIb
elif ft in ("CG",):              V,I,dI = Vc_f, Ic_f+k0*Ir_ph, dIc
elif ft in ("AB",):              V,I,dI = Va_f-Vb_f, Ia_f-Ib_f, dIa-dIb
elif ft in ("BC",):              V,I,dI = Vb_f-Vc_f, Ib_f-Ic_f, dIb-dIc
elif ft in ("CA",):              V,I,dI = Vc_f-Va_f, Ic_f-Ia_f, dIc-dIa
else:                            V,I,dI = Va_f, Ia_f, dIa

def clip_km(m):
    return float(np.clip(m * line_length, 0, line_length * 1.5))

loc = {}
if abs(I) > 1e-9:
    Zm = V/I
    loc["Reactancia"] = clip_km(Zm.imag / Z1.imag)
    den = (Z1*I*np.conj(dI)).real
    if abs(den)>1e-12: loc["Takagi"] = clip_km((V*np.conj(dI)).real/den)
    den2 = (Z1*dI*np.conj(dI)).real
    if abs(den2)>1e-12: loc["Takagi Mod."] = clip_km(((V-Va_pf if ft=="AG" else V)*np.conj(dI)).real/den2)

consensus = float(np.median(list(loc.values()))) if loc else None

# ─── Symmetrical components ────────────────────────────────────────────────────
A  = np.exp(1j*2*np.pi/3); A2 = A**2
V0 = (Va_f+Vb_f+Vc_f)/3
V1 = (Va_f+A*Vb_f+A2*Vc_f)/3
V2 = (Va_f+A2*Vb_f+A*Vc_f)/3
I0_s = (Ia_f+Ib_f+Ic_f)/3
I1_s = (Ia_f+A*Ib_f+A2*Ic_f)/3
I2_s = (Ia_f+A2*Ib_f+A*Ic_f)/3

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown('<div class="section-title">Resultado del análisis</div>', unsafe_allow_html=True)

# ── Fault type & timestamp ────────────────────────────────────────────────────
try: ts = str(rec.start_timestamp)
except: ts = "N/A"

onset_ms = t_arr[onset]*1000 if onset < len(t_arr) else 0

badge_cls = ("badge-3ph" if "3PH" in ft else
             "badge-ground" if "G" in ft else
             "badge-phase" if ft!="DESCONOCIDA" else "badge-unknown")

col_badge, col_ts = st.columns([2,3])
with col_badge:
    st.markdown(f"""
    <div style="margin-bottom:8px;">
        <div class="mcard-label">TIPO DE FALLA DETECTADA</div>
        <span class="fault-badge {badge_cls}">{ft}</span>
    </div>
    """, unsafe_allow_html=True)
with col_ts:
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="mcard">
            <div class="mcard-label">Timestamp</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:0.85rem;color:#00b4ff;">{ts}</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Inicio falla</div>
            <div class="mcard-value">{onset_ms:.1f}</div>
            <div class="mcard-unit">ms desde inicio</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Duración estimada</div>
            <div class="mcard-value">{dur_ms:.0f}</div>
            <div class="mcard-unit">ms</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Muestras / Fs</div>
            <div class="mcard-value">{int(fs)}</div>
            <div class="mcard-unit">Hz</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Location ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Localización de falla</div>', unsafe_allow_html=True)

if consensus is not None:
    pct = consensus / line_length * 100
    bar_width = min(max(pct, 1), 100)

    st.markdown(f"""
    <div class="consensus-box">
        <div>
            <div class="mcard-label">DISTANCIA ESTIMADA (CONSENSO)</div>
            <div style="display:flex;align-items:baseline;gap:12px;">
                <span class="consensus-km">{consensus:.2f}</span>
                <span style="color:#4a6080;font-size:1rem;">km</span>
                <span class="consensus-pct">{pct:.1f}%</span>
                <span style="color:#4a6080;font-size:0.85rem;">de la línea</span>
            </div>
        </div>
    </div>
    <div class="loc-bar-wrap">
        <div style="font-size:0.7rem;color:#4a6080;margin-bottom:4px;font-family:'Share Tech Mono',monospace;">
            POSICIÓN EN LA LÍNEA
        </div>
        <div class="loc-bar-track">
            <div class="loc-bar-fill" style="width:{bar_width}%;"></div>
            <div class="loc-bar-marker" style="left:{bar_width}%;"></div>
        </div>
        <div class="loc-bar-labels">
            <span>🔴 SUB. ORIGEN — 0 km</span>
            <span>FALLA: {consensus:.2f} km</span>
            <span>{line_length:.0f} km — SUB. DESTINO 🔴</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Method comparison table
    cols_loc = st.columns(len(loc))
    for col, (method, d_km) in zip(cols_loc, loc.items()):
        col.markdown(f"""
        <div class="mcard">
            <div class="mcard-label">{method}</div>
            <div class="mcard-value">{d_km:.2f}</div>
            <div class="mcard-unit">km &nbsp;·&nbsp; {d_km/line_length*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No se pudo calcular la distancia — revisar señales.")

# ── Electrical magnitudes ─────────────────────────────────────────────────────
st.markdown('<div class="section-title">Magnitudes eléctricas</div>', unsafe_allow_html=True)

dVa = (1 - abs(Va_f)/max(abs(Va_pf),1e-9))*100
dVb = (1 - abs(Vb_f)/max(abs(Vb_pf),1e-9))*100
dVc = (1 - abs(Vc_f)/max(abs(Vc_pf),1e-9))*100

st.markdown(f"""
<div class="metrics-grid">
    <div class="mcard">
        <div class="mcard-label">|Ia| falla pico</div>
        <div class="mcard-value">{np.max(np.abs(Ia[onset:clear+1])):.1f}</div>
        <div class="mcard-unit">A</div>
    </div>
    <div class="mcard">
        <div class="mcard-label">|Ib| falla pico</div>
        <div class="mcard-value">{np.max(np.abs(Ib[onset:clear+1])):.1f}</div>
        <div class="mcard-unit">A</div>
    </div>
    <div class="mcard">
        <div class="mcard-label">|Ic| falla pico</div>
        <div class="mcard-value">{np.max(np.abs(Ic[onset:clear+1])):.1f}</div>
        <div class="mcard-unit">A</div>
    </div>
    <div class="mcard">
        <div class="mcard-label">I0 (seq. cero)</div>
        <div class="mcard-value">{abs(I0_s):.2f}</div>
        <div class="mcard-unit">A</div>
    </div>
    <div class="mcard">
        <div class="mcard-label">ΔV Fase A</div>
        <div class="mcard-value">{dVa:.1f}</div>
        <div class="mcard-unit">%</div>
    </div>
    <div class="mcard">
        <div class="mcard-label">ΔV Fase B</div>
        <div class="mcard-value">{dVb:.1f}</div>
        <div class="mcard-unit">%</div>
    </div>
    <div class="mcard">
        <div class="mcard-label">ΔV Fase C</div>
        <div class="mcard-value">{dVc:.1f}</div>
        <div class="mcard-unit">%</div>
    </div>
    <div class="mcard">
        <div class="mcard-label">Impedancia Z1 total</div>
        <div class="mcard-value">{abs(Z1*line_length):.2f}</div>
        <div class="mcard-unit">Ω</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Charts ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Gráficas</div>', unsafe_allow_html=True)

DARK = "#080c14"; CARD = "#0d1220"; GRID = "rgba(0,180,255,0.08)"; TXT = "#4a6080"
LAYOUT = dict(paper_bgcolor=DARK, plot_bgcolor=CARD,
              font=dict(color="#8899bb", size=10),
              margin=dict(l=50,r=20,t=35,b=40),
              xaxis=dict(gridcolor=GRID, zeroline=False),
              yaxis=dict(gridcolor=GRID, zeroline=False))

tab1, tab2, tab3 = st.tabs(["🌊  Formas de Onda", "⚖️  Componentes Simétricas", "📐  Trayectoria R-X"])

t_ms = t_arr * 1000
onset_ms_v = t_ms[onset] if onset < len(t_ms) else 0

with tab1:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=["Tensiones (V)", "Corrientes (A)"],
                        vertical_spacing=0.1)
    for sig, name, clr in [(Va,"Va","#f0a500"),(Vb,"Vb","#00b4ff"),(Vc,"Vc","#44dd88")]:
        fig.add_trace(go.Scatter(x=t_ms, y=sig, name=name,
                                  line=dict(color=clr, width=1.5)), row=1, col=1)
    for sig, name, clr in [(Ia,"Ia","#f0a500"),(Ib,"Ib","#00b4ff"),(Ic,"Ic","#44dd88")]:
        fig.add_trace(go.Scatter(x=t_ms, y=sig, name=name,
                                  line=dict(color=clr, width=1.5)), row=2, col=1)
    for row in [1,2]:
        fig.add_vline(x=onset_ms_v, line=dict(color="#ff4444",width=1.5,dash="dash"),
                      annotation_text="Onset", annotation_font_color="#ff4444", row=row, col=1)
        fig.add_vline(x=t_ms[clear] if clear<len(t_ms) else t_ms[-1],
                      line=dict(color="#44dd88",width=1,dash="dot"),
                      annotation_text="Clear", annotation_font_color="#44dd88", row=row, col=1)
    L = dict(LAYOUT); L["height"] = 520
    for ax in ["xaxis","xaxis2","yaxis","yaxis2"]: L[ax]=dict(gridcolor=GRID, zeroline=False)
    L["xaxis2"] = dict(gridcolor=GRID, zeroline=False, title="Tiempo (ms)")
    fig.update_layout(**L)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    seq_labels = ["Seq-0 (Cero)", "Seq-1 (+)", "Seq-2 (-)"]
    V_mags = [abs(V0), abs(V1), abs(V2)]
    I_mags = [abs(I0_s), abs(I1_s), abs(I2_s)]
    V_pf_mags = [abs((Va_pf+Vb_pf+Vc_pf)/3),
                 abs((Va_pf+A*Vb_pf+A2*Vc_pf)/3),
                 abs((Va_pf+A2*Vb_pf+A*Vc_pf)/3)]
    I_pf_mags = [abs((Ia_pf+Ib_pf+Ic_pf)/3),
                 abs((Ia_pf+A*Ib_pf+A2*Ic_pf)/3),
                 abs((Ia_pf+A2*Ib_pf+A*Ic_pf)/3)]

    fig2 = make_subplots(rows=1, cols=2,
                         subplot_titles=["Tensiones de Secuencia (V)", "Corrientes de Secuencia (A)"])
    clrs = ["#ff4444","#f0a500","#00b4ff"]
    for i,(lbl,clr) in enumerate(zip(seq_labels, clrs)):
        fig2.add_trace(go.Bar(x=[lbl], y=[V_mags[i]], name=f"{lbl} falla",
                               marker_color=clr), row=1, col=1)
        fig2.add_trace(go.Bar(x=[lbl], y=[V_pf_mags[i]], name=f"{lbl} pre-falla",
                               marker_color=clr.replace(")", ",0.3)").replace("rgb","rgba") if "rgb" in clr else clr+"55"),
                               row=1, col=1)
        fig2.add_trace(go.Bar(x=[lbl], y=[I_mags[i]], name=f"{lbl}",
                               marker_color=clr, showlegend=False), row=1, col=2)
        fig2.add_trace(go.Bar(x=[lbl], y=[I_pf_mags[i]], name=f"{lbl} pre",
                               marker_color=clr+"55", showlegend=False), row=1, col=2)
    L2 = dict(LAYOUT); L2["height"]=400; L2["barmode"]="group"
    for ax in ["xaxis","xaxis2","yaxis","yaxis2"]: L2[ax]=dict(gridcolor=GRID,zeroline=False)
    fig2.update_layout(**L2)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    Ir_arr = Ia+Ib+Ic
    if ft in ("AG","ABG","CAG"):    Vl,Il = Va, Ia+k0.real*Ir_arr
    elif ft in ("BG","BCG"):         Vl,Il = Vb, Ib+k0.real*Ir_arr
    elif ft in ("CG",):              Vl,Il = Vc, Ic+k0.real*Ir_arr
    elif "AB" in ft:                 Vl,Il = Va-Vb, Ia-Ib
    elif "BC" in ft:                 Vl,Il = Vb-Vc, Ib-Ic
    elif "CA" in ft:                 Vl,Il = Vc-Va, Ic-Ia
    else:                            Vl,Il = Va, Ia

    with np.errstate(divide="ignore", invalid="ignore"):
        Z_arr = np.where(np.abs(Il)>1e-3, Vl/Il, np.nan+0j)
    R_arr, X_arr = Z_arr.real, Z_arr.imag

    theta = np.linspace(0, 2*np.pi, 300)
    Zc = Z1*line_length/2; Rmho = abs(Z1*line_length)/2*1.1

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=R_arr[:onset], y=X_arr[:onset], mode="lines",
                               line=dict(color="rgba(0,180,255,0.25)",width=1), name="Pre-falla"))
    fig3.add_trace(go.Scatter(x=R_arr[onset:clear], y=X_arr[onset:clear],
                               mode="lines+markers",
                               line=dict(color="#ff4444",width=2),
                               marker=dict(size=3,color="#ff4444"), name="Durante falla"))
    fig3.add_trace(go.Scatter(x=[0, Z1.real*line_length], y=[0, Z1.imag*line_length],
                               mode="lines+markers",
                               line=dict(color="#f0a500",width=3),
                               marker=dict(size=[8,14],symbol=["circle","x"],color="#f0a500"),
                               name=f"Línea Z1 ({line_length:.0f}km)"))
    fig3.add_trace(go.Scatter(x=Zc.real+Rmho*np.cos(theta),
                               y=Zc.imag+Rmho*np.sin(theta),
                               mode="lines", line=dict(color="rgba(240,165,0,0.3)",
                               width=1.5, dash="dot"), name="Zona MHO aprox."))
    L3 = dict(LAYOUT); L3["height"]=480
    L3["xaxis"] = dict(gridcolor=GRID, zeroline=True, zerolinecolor=GRID, title="R (Ω)")
    L3["yaxis"] = dict(gridcolor=GRID, zeroline=True, zerolinecolor=GRID, title="X (Ω)")
    fig3.update_layout(**L3)
    st.plotly_chart(fig3, use_container_width=True)

# ─── Summary table ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Resumen del evento</div>', unsafe_allow_html=True)

summary = {
    "Timestamp del registro": ts,
    "Línea analizada": line_name,
    "Longitud de línea": f"{line_length:.1f} km",
    "Tipo de falla": ft,
    "Falla a tierra": "Sí" if has_gnd else "No",
    "Inicio de falla": f"{onset_ms:.2f} ms",
    "Duración estimada": f"{dur_ms:.0f} ms",
    "Distancia estimada": f"{consensus:.2f} km ({consensus/line_length*100:.1f}%)" if consensus else "N/D",
    "Corriente pico Ia": f"{np.max(np.abs(Ia[onset:clear+1])):.1f} A",
    "Corriente pico Ib": f"{np.max(np.abs(Ib[onset:clear+1])):.1f} A",
    "Corriente pico Ic": f"{np.max(np.abs(Ic[onset:clear+1])):.1f} A",
    "Corriente I0 (seq. cero)": f"{abs(I0_s):.3f} A",
    "Depresión Va": f"{dVa:.1f}%",
    "Depresión Vb": f"{dVb:.1f}%",
    "Depresión Vc": f"{dVc:.1f}%",
    "Frecuencia de muestreo": f"{int(fs)} Hz",
    "Muestras totales": f"{len(t_arr)}",
}

cols_s = st.columns(2)
items = list(summary.items())
half = len(items)//2
for col, chunk in zip(cols_s, [items[:half], items[half:]]):
    rows = [["PARÁMETRO","VALOR"]] + [[k,v] for k,v in chunk]
    # Simple st.table
    import pandas as pd
    df = pd.DataFrame(chunk, columns=["Parámetro","Valor"])
    col.dataframe(df, hide_index=True, use_container_width=True)

st.divider()
st.caption(f"⚡ Fault Analyzer · {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · {line_name}")
