import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io, datetime, struct, re
import pandas as pd

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analizador de Fallas · Líneas de Transmisión",
    page_icon="⚡",
    layout="wide",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
AER_LOGO_B64 = "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"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@400;500;600;700;800&display=swap');

* {{ font-family: 'Inter', sans-serif; }}

[data-testid="stAppViewContainer"] {{
    background: #f0f2f5;
}}
[data-testid="stSidebar"] {{
    background: #ffffff;
    border-right: 1px solid #e0e4ea;
}}
[data-testid="stHeader"] {{ background: transparent; }}

/* Top navbar */
.aer-navbar {{
    background: #ffffff;
    border-bottom: 3px solid #2e7d32;
    padding: 0.9rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}
.aer-navbar-left {{ display: flex; align-items: center; gap: 16px; }}
.aer-navbar-title {{
    font-size: 1.4rem; font-weight: 800; color: #1a2535; letter-spacing: -0.5px;
}}
.aer-navbar-title span {{ color: #2e7d32; }}
.aer-navbar-sub {{ font-size: 0.75rem; color: #6b7a8d; margin-top: 1px; }}
.aer-navbar-badge {{
    background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7;
    border-radius: 20px; padding: 3px 12px; font-size: 0.7rem; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase;
}}

/* Metric cards */
.metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 1.2rem 0; }}
.mcard {{
    background: #ffffff;
    border: 1px solid #e0e4ea;
    border-top: 3px solid #2e7d32;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}}
.mcard-label {{ font-size: 0.65rem; color: #6b7a8d; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; font-weight: 600; }}
.mcard-value {{ font-family: 'Share Tech Mono', monospace; font-size: 1.7rem; color: #1a2535; line-height: 1; }}
.mcard-unit {{ font-size: 0.7rem; color: #6b7a8d; margin-top: 3px; }}

/* Fault badge */
.fault-badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 8px 24px; border-radius: 6px;
    font-family: 'Share Tech Mono', monospace; font-size: 1.7rem; letter-spacing: 3px; font-weight: 700; }}
.badge-ground  {{ background: #fff3f3; border: 2px solid #e53935; color: #c62828; }}
.badge-phase   {{ background: #fff8e1; border: 2px solid #f9a825; color: #e65100; }}
.badge-3ph     {{ background: #f3e5f5; border: 2px solid #8e24aa; color: #6a1b9a; }}
.badge-unknown {{ background: #f5f5f5; border: 2px solid #9e9e9e; color: #616161; }}

/* Location bar */
.loc-bar-track {{
    height: 14px; background: #e8eaed; border-radius: 7px; position: relative;
    border: 1px solid #d0d4da; margin: 8px 0;
}}
.loc-bar-fill {{
    height: 100%; border-radius: 7px;
    background: linear-gradient(90deg, #43a047, #2e7d32);
    position: absolute;
}}
.loc-bar-marker {{
    width: 14px; height: 24px; background: #e53935; border-radius: 4px;
    position: absolute; top: -5px; transform: translateX(-50%);
    box-shadow: 0 2px 6px rgba(229,57,53,0.5);
}}
.loc-bar-labels {{
    display: flex; justify-content: space-between;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68rem; color: #6b7a8d; margin-top: 4px;
}}

/* Consensus box */
.consensus-box {{
    background: #e8f5e9;
    border: 1px solid #a5d6a7;
    border-left: 5px solid #2e7d32;
    border-radius: 8px;
    padding: 1.2rem 1.8rem;
    margin: 1rem 0;
}}
.consensus-km {{ font-family: 'Share Tech Mono', monospace; font-size: 3rem; color: #2e7d32; line-height: 1; }}

/* Section title */
.section-title {{
    font-size: 0.7rem; color: #2e7d32; letter-spacing: 3px; text-transform: uppercase;
    font-weight: 700; border-left: 3px solid #2e7d32; padding-left: 10px; margin: 1.8rem 0 0.8rem;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; background: transparent; }}
.stTabs [data-baseweb="tab"] {{
    background: #ffffff; border: 1px solid #e0e4ea;
    border-radius: 6px; color: #6b7a8d; padding: 8px 20px;
    font-weight: 500;
}}
.stTabs [aria-selected="true"] {{
    background: #e8f5e9 !important;
    border-color: #2e7d32 !important;
    color: #2e7d32 !important;
    font-weight: 700 !important;
}}

/* General text readability */
h1, h2, h3 {{ color: #1a2535; }}
p, label, div {{ color: #2c3e50; }}
.stRadio label {{ color: #1a2535 !important; font-weight: 500; }}
.stNumberInput label {{ color: #1a2535 !important; font-weight: 500; }}
[data-testid="stMetricValue"] {{ color: #1a2535 !important; }}
[data-testid="stMetricLabel"] {{ color: #6b7a8d !important; }}
</style>
""", unsafe_allow_html=True)

# ─── Line parameters ──────────────────────────────────────────────────────────
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

# ═══════════════════════════════════════════════════════════════════════════════
# COMTRADE PARSER (sin librería externa)
# ═══════════════════════════════════════════════════════════════════════════════
def parse_cfg(cfg_bytes: bytes):
    """Parse .CFG file, returns metadata dict."""
    text = cfg_bytes.decode("latin-1", errors="replace")
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Line 1: station, device, year
    header = lines[0].split(",")
    station = header[0] if len(header) > 0 else ""

    # Line 2: total channels, nA analog, nD digital
    ch_line = lines[1].split(",")
    total_ch = int(ch_line[0])
    n_analog = int(re.findall(r"\d+", ch_line[1])[0]) if len(ch_line) > 1 else 0

    # Analog channel definitions
    channels = []
    for i in range(2, 2 + n_analog):
        if i >= len(lines):
            break
        parts = lines[i].split(",")
        # idx, name, phase, circuit, unit, a, b, skew, min, max, primary, secondary, PS
        name  = parts[1].strip() if len(parts) > 1 else f"ch{i}"
        unit  = parts[4].strip() if len(parts) > 4 else ""
        a_mlt = float(parts[5]) if len(parts) > 5 else 1.0
        b_off = float(parts[6]) if len(parts) > 6 else 0.0
        channels.append({"name": name, "unit": unit, "a": a_mlt, "b": b_off})

    # Find frequency and sample rate
    freq = 60.0
    n_rates = 1
    sample_rate = 3840.0
    n_samples = 0
    timestamp = "N/A"

    idx = 2 + n_analog
    # Skip digital channels
    n_digital = total_ch - n_analog
    idx += n_digital

    try:
        freq = float(lines[idx]); idx += 1
        n_rates = int(lines[idx]); idx += 1
        for _ in range(n_rates):
            rate_parts = lines[idx].split(",")
            sample_rate = float(rate_parts[0])
            n_samples   = int(rate_parts[1])
            idx += 1
        timestamp = lines[idx] if idx < len(lines) else "N/A"; idx += 1
        idx += 1  # end timestamp
        file_type = lines[idx].strip().upper() if idx < len(lines) else "ASCII"
    except Exception:
        file_type = "ASCII"

    return dict(
        station=station, n_analog=n_analog, channels=channels,
        freq=freq, sample_rate=sample_rate, n_samples=n_samples,
        timestamp=timestamp, file_type=file_type,
    )


def parse_dat_ascii(dat_bytes: bytes, n_analog: int, channels: list):
    """Parse ASCII .DAT file."""
    text = dat_bytes.decode("latin-1", errors="replace")
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    times, signals = [], [[] for _ in range(n_analog)]

    for line in lines:
        parts = line.split(",")
        if len(parts) < 2 + n_analog:
            continue
        try:
            t_us = float(parts[1])
            times.append(t_us * 1e-6)
            for k in range(n_analog):
                raw = float(parts[2 + k])
                a   = channels[k]["a"]
                b   = channels[k]["b"]
                signals[k].append(raw * a + b)
        except (ValueError, IndexError):
            continue

    return np.array(times), [np.array(s) for s in signals]


def parse_dat_binary(dat_bytes: bytes, n_analog: int, n_samples: int, channels: list):
    """Parse binary .DAT file (16-bit integers)."""
    # Each record: sample_num (4 bytes) + timestamp (4 bytes) + n_analog*2 bytes
    record_size = 8 + n_analog * 2
    times, signals = [], [[] for _ in range(n_analog)]

    for i in range(n_samples):
        offset = i * record_size
        if offset + record_size > len(dat_bytes):
            break
        try:
            _samp = struct.unpack_from("<I", dat_bytes, offset)[0]
            t_us  = struct.unpack_from("<I", dat_bytes, offset + 4)[0]
            times.append(t_us * 1e-6)
            for k in range(n_analog):
                raw = struct.unpack_from("<h", dat_bytes, offset + 8 + k * 2)[0]
                signals[k].append(raw * channels[k]["a"] + channels[k]["b"])
        except struct.error:
            break

    return np.array(times), [np.array(s) for s in signals]


def load_comtrade(cfg_bytes, dat_bytes):
    """Main entry: parse CFG + DAT, return dict with Va,Vb,Vc,Ia,Ib,Ic,time,fs."""
    meta = parse_cfg(cfg_bytes)
    ch   = meta["channels"]

    if meta.get("file_type", "ASCII").upper() in ("BINARY", "BINARY32"):
        t_arr, sigs = parse_dat_binary(dat_bytes, meta["n_analog"], meta["n_samples"], ch)
    else:
        t_arr, sigs = parse_dat_ascii(dat_bytes, meta["n_analog"], ch)

    if len(t_arr) < 2:
        raise ValueError("El archivo DAT no contiene suficientes muestras.")

    # Use sample_rate from CFG first (most reliable), fallback to diff(t)
    fs_cfg = float(meta.get("sample_rate", 0))
    if fs_cfg > 0:
        fs = fs_cfg
    else:
        diffs = np.diff(t_arr)
        diffs = diffs[diffs > 0]   # remove zeros / negatives
        if len(diffs) == 0:
            fs = 3840.0
        else:
            dt = float(np.median(diffs))
            fs = 1.0 / dt if dt > 0 else 3840.0
    # Sanity clamp: realistic range 100 – 100000 Hz
    fs = float(np.clip(fs, 100.0, 100_000.0))

    # Map channels by name
    names = [c["name"].lower().strip() for c in ch]

    def find(patterns):
        for i, n in enumerate(names):
            for p in patterns:
                if p in n:
                    return i
        return None

    def get(idx):
        return sigs[idx].copy() if idx is not None and idx < len(sigs) else np.zeros(len(t_arr))

    Va = get(find(["va","v_a","ua","vpha","u1","ea","an1"]))
    Vb = get(find(["vb","v_b","ub","vphb","u2","eb","an2"]))
    Vc = get(find(["vc","v_c","uc","vphc","u3","ec","an3"]))
    Ia = get(find(["ia","i_a","ifa","ipha","an4"]))
    Ib = get(find(["ib","i_b","ifb","iphb","an5"]))
    Ic = get(find(["ic","i_c","ifc","iphc","an6"]))

    return dict(Va=Va, Vb=Vb, Vc=Vc, Ia=Ia, Ib=Ib, Ic=Ic,
                time=t_arr, fs=fs, timestamp=meta["timestamp"],
                channel_names=[c["name"] for c in ch])


# ═══════════════════════════════════════════════════════════════════════════════
# UI — HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="aer-navbar">
    <div class="aer-navbar-left">
        <img src="data:image/png;base64,{AER_LOGO_B64}" height="52" style="border-radius:4px;">
        <div>
            <div class="aer-navbar-title">⚡ FAULT <span>ANALYZER</span></div>
            <div class="aer-navbar-sub">Alternativa de Energía Renovable, S.A. · Análisis de fallas en líneas de transmisión</div>
        </div>
    </div>
    <span class="aer-navbar-badge">COMTRADE</span>
</div>
""", unsafe_allow_html=True)

# ─── Step 1: Line type ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Paso 1 · Tipo de línea</div>', unsafe_allow_html=True)

line_name = st.radio("", options=list(LINE_PARAMS.keys()), horizontal=True,
                     label_visibility="collapsed")
cfg_line = LINE_PARAMS[line_name]

col1, col2, col3 = st.columns(3)
line_length = col1.number_input("Longitud de la línea (km)", min_value=1.0, max_value=500.0,
                                 value=50.0 if "69" in line_name else 15.0, step=0.5)
col2.metric("Tensión nominal", f"{cfg_line['vkv']} kV")
col3.metric("Corriente nominal", f"{cfg_line['I_rated']} A")

# ─── Step 2: Upload ───────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Paso 2 · Cargar archivo COMTRADE</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
cfg_file = col_a.file_uploader("Archivo .CFG", type=["cfg", "CFG"])
dat_file = col_b.file_uploader("Archivo .DAT", type=["dat", "DAT"])

if not (cfg_file and dat_file):
    st.info("📂 Sube los archivos .CFG y .DAT del relé de protección para comenzar el análisis.")
    st.stop()

# ─── Parse ────────────────────────────────────────────────────────────────────
with st.spinner("⚙️ Procesando COMTRADE…"):
    try:
        cfg_file.seek(0); dat_file.seek(0)
        data = load_comtrade(cfg_file.read(), dat_file.read())
    except Exception as e:
        st.error(f"❌ Error al leer COMTRADE: {e}")
        st.stop()

Va, Vb, Vc = data["Va"], data["Vb"], data["Vc"]
Ia, Ib, Ic = data["Ia"], data["Ib"], data["Ic"]
t_arr = data["time"]
fs    = data["fs"]
ts    = data["timestamp"]

# ─── Analysis helpers ─────────────────────────────────────────────────────────
def rms_w(x, fs, cyc=1):
    N = max(2, min(int(fs / 60 * cyc), len(x) // 4))
    return np.sqrt(np.convolve(x**2, np.ones(N)/N, mode="same"))

def phasor(x, idx, fs, f0=60.0):
    n = max(2, min(int(fs / f0), len(x) - idx))
    seg = x[idx:idx+n]
    if len(seg) < n: seg = np.pad(seg, (0, n-len(seg)))
    return np.dot(seg, np.exp(-1j*2*np.pi*np.arange(n)/n)) * 2/n

# Onset detection
n_samples_total = len(t_arr)
# n_pre = 3 cycles, but never more than 25% of the signal
n_pre = min(max(4, int(3 * fs / 60)), n_samples_total // 4)
Irms = rms_w(Ia+Ib+Ic, fs)
thresh = np.mean(Irms[:n_pre]) + 5*np.std(Irms[:n_pre])
cands = np.where(Irms > thresh)[0]
onset = int(cands[0]) if len(cands) else n_pre

# Phasors
pf0   = max(0, onset - int(fs/60))
Va_pf = phasor(Va,pf0,fs); Vb_pf = phasor(Vb,pf0,fs); Vc_pf = phasor(Vc,pf0,fs)
Ia_pf = phasor(Ia,pf0,fs); Ib_pf = phasor(Ib,pf0,fs); Ic_pf = phasor(Ic,pf0,fs)
Va_f  = phasor(Va,onset,fs); Vb_f = phasor(Vb,onset,fs); Vc_f = phasor(Vc,onset,fs)
Ia_f  = phasor(Ia,onset,fs); Ib_f = phasor(Ib,onset,fs); Ic_f = phasor(Ic,onset,fs)

# Fault type
fa = (abs(Ia_f)>1.5*max(abs(Ia_pf),1e-9)) or (abs(Va_f)<0.7*max(abs(Va_pf),1e-9))
fb = (abs(Ib_f)>1.5*max(abs(Ib_pf),1e-9)) or (abs(Vb_f)<0.7*max(abs(Vb_pf),1e-9))
fc = (abs(Ic_f)>1.5*max(abs(Ic_pf),1e-9)) or (abs(Vc_f)<0.7*max(abs(Vc_pf),1e-9))
I0_ph = (Ia_f+Ib_f+Ic_f)/3
has_gnd = abs(I0_ph) > 0.1*max(abs(Ia_f),abs(Ib_f),abs(Ic_f),1e-9)
n_f = sum([fa,fb,fc])

if n_f>=3:      ft = "3PH"  + ("G" if has_gnd else "")
elif n_f==2:
    if fa and fb:   ft = "ABG" if has_gnd else "AB"
    elif fb and fc: ft = "BCG" if has_gnd else "BC"
    else:           ft = "CAG" if has_gnd else "CA"
elif n_f==1:    ft = "AG" if fa else ("BG" if fb else "CG")
else:           ft = "DESCONOCIDA"

# Clear time
Irms_a=rms_w(Ia,fs); Irms_b=rms_w(Ib,fs); Irms_c=rms_w(Ic,fs)
I0a=max(np.mean(Irms_a[:n_pre]),1e-6); I0b=max(np.mean(Irms_b[:n_pre]),1e-6); I0c=max(np.mean(Irms_c[:n_pre]),1e-6)
clear = len(Ia)-1
for i in range(onset+int(fs/60), len(Irms_a)):
    if Irms_a[i]<1.2*I0a and Irms_b[i]<1.2*I0b and Irms_c[i]<1.2*I0c:
        clear=i; break
dur_ms = (clear-onset)/fs*1000

# Localization
Z1=cfg_line["Z1"]; Z0=cfg_line["Z0"]
k0=(Z0-Z1)/(3*Z1)
Ir_ph=Ia_f+Ib_f+Ic_f
dIa=Ia_f-Ia_pf; dIb=Ib_f-Ib_pf; dIc=Ic_f-Ic_pf

if ft in ("AG","ABG","CAG"):   V,I,dI = Va_f, Ia_f+k0*Ir_ph, dIa
elif ft in ("BG","BCG"):        V,I,dI = Vb_f, Ib_f+k0*Ir_ph, dIb
elif ft in ("CG",):             V,I,dI = Vc_f, Ic_f+k0*Ir_ph, dIc
elif "AB" in ft:                V,I,dI = Va_f-Vb_f, Ia_f-Ib_f, dIa-dIb
elif "BC" in ft:                V,I,dI = Vb_f-Vc_f, Ib_f-Ic_f, dIb-dIc
elif "CA" in ft:                V,I,dI = Vc_f-Va_f, Ic_f-Ia_f, dIc-dIa
else:                           V,I,dI = Va_f, Ia_f, dIa

def clip_km(m): return float(np.clip(m*line_length, 0, line_length*1.5))

loc = {}
if abs(I)>1e-9:
    Zm = V/I
    loc["Reactancia"]   = clip_km(Zm.imag/Z1.imag)
    den=(Z1*I*np.conj(dI)).real
    if abs(den)>1e-12: loc["Takagi"] = clip_km((V*np.conj(dI)).real/den)
    den2=(Z1*dI*np.conj(dI)).real
    if abs(den2)>1e-12:
        dV = V - (Va_pf if "A" in ft else Vb_pf if "B" in ft else Vc_pf)
        loc["Takagi Mod."] = clip_km((dV*np.conj(dI)).real/den2)

consensus = float(np.median(list(loc.values()))) if loc else None

# Symmetrical components
A_op=np.exp(1j*2*np.pi/3); A2=A_op**2
V0=(Va_f+Vb_f+Vc_f)/3; V1=(Va_f+A_op*Vb_f+A2*Vc_f)/3; V2=(Va_f+A2*Vb_f+A_op*Vc_f)/3
I0_s=(Ia_f+Ib_f+Ic_f)/3; I1_s=(Ia_f+A_op*Ib_f+A2*Ic_f)/3; I2_s=(Ia_f+A2*Ib_f+A_op*Ic_f)/3

onset_ms = t_arr[onset]*1000 if onset<len(t_arr) else 0
dVa=(1-abs(Va_f)/max(abs(Va_pf),1e-9))*100
dVb=(1-abs(Vb_f)/max(abs(Vb_pf),1e-9))*100
dVc=(1-abs(Vc_f)/max(abs(Vc_pf),1e-9))*100

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown('<div class="section-title">Resultado del análisis</div>', unsafe_allow_html=True)

badge_cls = ("badge-3ph" if "3PH" in ft else
             "badge-ground" if "G" in ft else
             "badge-phase" if ft!="DESCONOCIDA" else "badge-unknown")

col_b1, col_b2 = st.columns([2,3])
with col_b1:
    st.markdown(f"""
    <div style="margin-bottom:8px;">
        <div class="mcard-label">TIPO DE FALLA DETECTADA</div>
        <span class="fault-badge {badge_cls}">{ft}</span>
    </div>
    """, unsafe_allow_html=True)
with col_b2:
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="mcard">
            <div class="mcard-label">Timestamp</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:0.8rem;color:#00b4ff;">{ts}</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Inicio falla</div>
            <div class="mcard-value">{onset_ms:.1f}</div>
            <div class="mcard-unit">ms</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Duración</div>
            <div class="mcard-value">{dur_ms:.0f}</div>
            <div class="mcard-unit">ms</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Fs</div>
            <div class="mcard-value">{int(fs)}</div>
            <div class="mcard-unit">Hz</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Location ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Localización de falla</div>', unsafe_allow_html=True)

if consensus is not None:
    pct = consensus/line_length*100
    bar_w = min(max(pct,1),100)
    st.markdown(f"""
    <div class="consensus-box">
        <div class="mcard-label">DISTANCIA ESTIMADA (CONSENSO)</div>
        <div style="display:flex;align-items:baseline;gap:12px;margin-top:4px;">
            <span class="consensus-km">{consensus:.2f}</span>
            <span style="color:#4a6080;">km</span>
            <span style="color:#fff;font-size:1.4rem;font-weight:700;">{pct:.1f}%</span>
            <span style="color:#4a6080;font-size:0.85rem;">de la línea</span>
        </div>
    </div>
    <div style="margin:12px 0 4px;font-size:0.7rem;color:#4a6080;font-family:'Share Tech Mono',monospace;">POSICIÓN EN LA LÍNEA</div>
    <div class="loc-bar-track">
        <div class="loc-bar-fill" style="width:{bar_w}%;"></div>
        <div class="loc-bar-marker" style="left:{bar_w}%;"></div>
    </div>
    <div class="loc-bar-labels">
        <span>🔴 ORIGEN — 0 km</span>
        <span>⚡ FALLA: {consensus:.2f} km</span>
        <span>{line_length:.0f} km — DESTINO 🔴</span>
    </div>
    """, unsafe_allow_html=True)

    cols_loc = st.columns(len(loc))
    for col, (method, d_km) in zip(cols_loc, loc.items()):
        col.markdown(f"""
        <div class="mcard" style="margin-top:12px;">
            <div class="mcard-label">{method}</div>
            <div class="mcard-value">{d_km:.2f}</div>
            <div class="mcard-unit">km · {d_km/line_length*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Electrical magnitudes ────────────────────────────────────────────────────
st.markdown('<div class="section-title">Magnitudes eléctricas</div>', unsafe_allow_html=True)
Ia_pk = float(np.max(np.abs(Ia[onset:clear+1]))) if clear>onset else 0
Ib_pk = float(np.max(np.abs(Ib[onset:clear+1]))) if clear>onset else 0
Ic_pk = float(np.max(np.abs(Ic[onset:clear+1]))) if clear>onset else 0

st.markdown(f"""
<div class="metrics-grid">
    <div class="mcard"><div class="mcard-label">Ia pico</div>
        <div class="mcard-value">{Ia_pk:.1f}</div><div class="mcard-unit">A</div></div>
    <div class="mcard"><div class="mcard-label">Ib pico</div>
        <div class="mcard-value">{Ib_pk:.1f}</div><div class="mcard-unit">A</div></div>
    <div class="mcard"><div class="mcard-label">Ic pico</div>
        <div class="mcard-value">{Ic_pk:.1f}</div><div class="mcard-unit">A</div></div>
    <div class="mcard"><div class="mcard-label">I0 seq. cero</div>
        <div class="mcard-value">{abs(I0_s):.3f}</div><div class="mcard-unit">A</div></div>
    <div class="mcard"><div class="mcard-label">ΔV Fase A</div>
        <div class="mcard-value">{dVa:.1f}</div><div class="mcard-unit">%</div></div>
    <div class="mcard"><div class="mcard-label">ΔV Fase B</div>
        <div class="mcard-value">{dVb:.1f}</div><div class="mcard-unit">A</div></div>
    <div class="mcard"><div class="mcard-label">ΔV Fase C</div>
        <div class="mcard-value">{dVc:.1f}</div><div class="mcard-unit">%</div></div>
    <div class="mcard"><div class="mcard-label">Muestras</div>
        <div class="mcard-value">{len(t_arr)}</div><div class="mcard-unit">total</div></div>
</div>
""", unsafe_allow_html=True)

# ─── Charts ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Gráficas</div>', unsafe_allow_html=True)

DARK="rgba(255,255,255,1)"; CARD="rgba(248,250,252,1)"; GRID="rgba(0,0,0,0.06)"
t_ms = t_arr*1000
onset_ms_v = t_ms[onset] if onset<len(t_ms) else 0
clear_ms_v = t_ms[clear] if clear<len(t_ms) else t_ms[-1]

tab1, tab2, tab3 = st.tabs(["🌊  Formas de Onda", "⚖️  Componentes Simétricas", "📐  Trayectoria R-X"])

with tab1:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=["Tensiones (V)", "Corrientes (A)"], vertical_spacing=0.1)
    for sig,name,clr in [(Va,"Va","#f0a500"),(Vb,"Vb","#00b4ff"),(Vc,"Vc","#44dd88")]:
        fig.add_trace(go.Scatter(x=t_ms,y=sig,name=name,line=dict(color=clr,width=1.5)),row=1,col=1)
    for sig,name,clr in [(Ia,"Ia","#f0a500"),(Ib,"Ib","#00b4ff"),(Ic,"Ic","#44dd88")]:
        fig.add_trace(go.Scatter(x=t_ms,y=sig,name=name,line=dict(color=clr,width=1.5)),row=2,col=1)
    for row in [1,2]:
        fig.add_vline(x=onset_ms_v,line=dict(color="#ff4444",width=1.5,dash="dash"),
                      annotation_text="Onset",annotation_font_color="#ff4444",row=row,col=1)
        fig.add_vline(x=clear_ms_v,line=dict(color="#44dd88",width=1,dash="dot"),
                      annotation_text="Clear",annotation_font_color="#44dd88",row=row,col=1)
    fig.update_layout(height=520,paper_bgcolor=DARK,plot_bgcolor=CARD,
                      font=dict(color="#2c3e50",size=10),margin=dict(l=50,r=20,t=35,b=40))
    for ax in ["xaxis","xaxis2","yaxis","yaxis2"]:
        fig.layout[ax].update(gridcolor=GRID, zeroline=False)
    fig.update_xaxes(title_text="Tiempo (ms)",row=2,col=1)
    st.plotly_chart(fig,use_container_width=True)

with tab2:
    seq_labels=["Seq-0 (Cero)","Seq-1 (Pos.)","Seq-2 (Neg.)"]
    V_m=[abs(V0),abs(V1),abs(V2)]
    I_m=[abs(I0_s),abs(I1_s),abs(I2_s)]
    V0_pf=(Va_pf+Vb_pf+Vc_pf)/3; V1_pf=(Va_pf+A_op*Vb_pf+A2*Vc_pf)/3
    V_pf_m=[abs(V0_pf),abs(V1_pf),abs((Va_pf+A2*Vb_pf+A_op*Vc_pf)/3)]
    I0_pf_s=(Ia_pf+Ib_pf+Ic_pf)/3
    I_pf_m=[abs(I0_pf_s),abs((Ia_pf+A_op*Ib_pf+A2*Ic_pf)/3),abs((Ia_pf+A2*Ib_pf+A_op*Ic_pf)/3)]

    fig2=make_subplots(rows=1,cols=2,subplot_titles=["Tensiones de Secuencia (V)","Corrientes de Secuencia (A)"])
    clrs     = ["#ff4444","#f0a500","#00b4ff"]
    clrs_dim = ["rgba(255,68,68,0.3)","rgba(240,165,0,0.3)","rgba(0,180,255,0.3)"]
    for i,(lbl,clr,clr_dim) in enumerate(zip(seq_labels,clrs,clrs_dim)):
        fig2.add_trace(go.Bar(x=[lbl],y=[V_m[i]],name=f"{lbl}",marker_color=clr),row=1,col=1)
        fig2.add_trace(go.Bar(x=[lbl],y=[V_pf_m[i]],name=f"{lbl} pre",marker_color=clr_dim,showlegend=False),row=1,col=1)
        fig2.add_trace(go.Bar(x=[lbl],y=[I_m[i]],name=lbl,marker_color=clr,showlegend=False),row=1,col=2)
        fig2.add_trace(go.Bar(x=[lbl],y=[I_pf_m[i]],name=f"{lbl} pre",marker_color=clr_dim,showlegend=False),row=1,col=2)
    fig2.update_layout(height=400,barmode="group",paper_bgcolor=DARK,plot_bgcolor=CARD,
                       font=dict(color="#2c3e50",size=10),margin=dict(l=50,r=20,t=35,b=40))
    for ax in ["xaxis","xaxis2","yaxis","yaxis2"]: fig2.layout[ax].update(gridcolor=GRID,zeroline=False)
    st.plotly_chart(fig2,use_container_width=True)

with tab3:
    Ir_a=Ia+Ib+Ic
    if ft in ("AG","ABG","CAG"):   Vl,Il=Va,Ia+k0.real*Ir_a
    elif ft in ("BG","BCG"):        Vl,Il=Vb,Ib+k0.real*Ir_a
    elif ft in ("CG",):             Vl,Il=Vc,Ic+k0.real*Ir_a
    elif "AB" in ft:                Vl,Il=Va-Vb,Ia-Ib
    elif "BC" in ft:                Vl,Il=Vb-Vc,Ib-Ic
    elif "CA" in ft:                Vl,Il=Vc-Va,Ic-Ia
    else:                           Vl,Il=Va,Ia

    with np.errstate(divide="ignore",invalid="ignore"):
        Z_a=np.where(np.abs(Il)>1e-3,Vl/Il,np.nan+0j)
    R_a,X_a=Z_a.real,Z_a.imag
    theta=np.linspace(0,2*np.pi,300)
    Zc=Z1*line_length/2; Rm=abs(Z1*line_length)/2*1.1

    fig3=go.Figure()
    fig3.add_trace(go.Scatter(x=R_a[:onset],y=X_a[:onset],mode="lines",
                               line=dict(color="rgba(0,180,255,0.2)",width=1),name="Pre-falla"))
    fig3.add_trace(go.Scatter(x=R_a[onset:clear],y=X_a[onset:clear],mode="lines+markers",
                               line=dict(color="#ff4444",width=2),marker=dict(size=3,color="#ff4444"),name="Falla"))
    fig3.add_trace(go.Scatter(x=[0,Z1.real*line_length],y=[0,Z1.imag*line_length],
                               mode="lines+markers",line=dict(color="#f0a500",width=3),
                               marker=dict(size=[8,14],symbol=["circle","x"],color="#f0a500"),
                               name=f"Z1 línea ({line_length:.0f}km)"))
    fig3.add_trace(go.Scatter(x=Zc.real+Rm*np.cos(theta),y=Zc.imag+Rm*np.sin(theta),
                               mode="lines",line=dict(color="rgba(240,165,0,0.3)",width=1.5,dash="dot"),
                               name="Zona MHO"))
    fig3.update_layout(height=480,paper_bgcolor=DARK,plot_bgcolor=CARD,
                       font=dict(color="#2c3e50",size=10),margin=dict(l=50,r=20,t=35,b=40),
                       xaxis=dict(gridcolor=GRID,zeroline=True,zerolinecolor="#b0bec5",title="R (Ω)"),
                       yaxis=dict(gridcolor=GRID,zeroline=True,zerolinecolor="#b0bec5",title="X (Ω)"))
    st.plotly_chart(fig3,use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DIAGNÓSTICO PARA EQUIPO DE CAMPO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🔎 Diagnóstico para equipo de campo</div>', unsafe_allow_html=True)

# ── Lógica de diagnóstico ──────────────────────────────────────────────────────
causas     = []   # (emoji, título, descripción, prioridad: "alta"/"media"/"baja")
acciones   = []   # strings de qué revisar en campo
descartar  = []   # qué probablemente NO es

I_rated    = cfg_line["I_rated"]
I_falla_max = max(Ia_pk, Ib_pk, Ic_pk)
factor_I   = I_falla_max / max(I_rated, 1)
pct_linea  = (consensus / line_length * 100) if consensus else 50

# ── Reglas de diagnóstico ──────────────────────────────────────────────────────

# 1. TIPO DE FALLA → causa principal
if ft in ("AG", "BG", "CG"):
    causas.append(("⚡", "Falla fase-tierra (monofásica)",
        f"Solo una fase ({ft[0]}) tocó tierra. Causa más común: aislador flashover, rama de árbol, pararrayos dañado o conductor caído.",
        "alta"))
    acciones += [
        f"Inspeccionar aisladores de fase {ft[0]} en el tramo identificado",
        "Buscar marcas de arco eléctrico (quemaduras negras) en aisladores",
        "Revisar pararrayos de fase — medir con medidor de fuga",
        "Verificar vegetación cercana a la línea (ramas quemadas)",
        "Buscar conductor caído o dañado en el suelo",
    ]
    descartar += ["Falla en transformador (la falla es en línea)", "Problema trifásico de equipo"]

elif ft in ("AB", "BC", "CA"):
    causas.append(("⚡⚡", "Falla entre dos fases (sin tierra)",
        "Dos fases se tocaron entre sí sin llegar a tierra. Probable causa: balanceo de conductores por viento fuerte, objeto extraño (cometa, rama) o distancia entre conductores reducida.",
        "alta"))
    acciones += [
        "Inspeccionar separadores/espaciadores entre conductores",
        "Buscar objetos atrapados entre fases (cometas, alambres)",
        "Verificar flecha de conductores — posible elongación",
        "Revisar estructuras/crucetas por daño mecánico",
    ]
    descartar += ["Problema de aisladores a tierra", "Falla de pararrayos"]

elif ft in ("ABG", "BCG", "CAG"):
    causas.append(("⚡⚡", "Falla doble fase-tierra",
        "Dos fases tocaron tierra simultáneamente. Probable: caída de estructura, impacto de rayo que afectó dos fases, o falla de aisladores múltiples.",
        "alta"))
    acciones += [
        "Verificar integridad de estructura (poste/torre) — posible volteo",
        "Buscar evidencia de impacto de rayo (marcas en estructura)",
        "Revisar aisladores de ambas fases afectadas",
        "Inspeccionar puesta a tierra de estructura",
    ]

elif "3PH" in ft:
    causas.append(("🔴", "Falla trifásica",
        "Las tres fases fallaron simultáneamente. Causas: rayo directo sobre la línea, colapso de estructura, o cortocircuito en equipo conectado (transformador, banco de capacitores).",
        "alta"))
    acciones += [
        "Buscar estructura colapsada (poste caído) en el tramo",
        "Verificar si hay equipo conectado en el punto de falla (transformadores)",
        "Revisar evidencia de rayo directo",
        "Inspeccionar seccionadores y equipos de maniobra en la zona",
    ]

# 2. DURACIÓN → transitoria vs permanente
if dur_ms < 200:
    causas.append(("🌿", "Falla transitoria (auto-eliminada)",
        f"Duración muy corta ({dur_ms:.0f} ms) — el relé reconectó exitosamente. Causa probable: contacto momentáneo por vegetación, animal, o flashover por contaminación. La línea puede estar operando normalmente.",
        "media"))
    acciones += ["Revisar vegetación en el tramo — probable contacto de rama con conductor",
                 "Inspeccionar aisladores por contaminación (sales, polvo industrial)"]
    descartar += ["Daño físico permanente del conductor"]
elif dur_ms < 500:
    causas.append(("⏱️", "Falla semipermanente",
        f"Duración de {dur_ms:.0f} ms — posiblemente el relé intentó reconectar sin éxito. El objeto causante puede seguir presente.",
        "media"))
    acciones += ["La falla persiste — probable objeto físico en la línea",
                 "Patrullaje urgente del tramo antes de reconectar manualmente"]
else:
    causas.append(("🔴", "Falla permanente",
        f"Duración larga ({dur_ms:.0f} ms) — daño físico permanente. No intentar reconectar sin inspección visual.",
        "alta"))
    acciones += ["NO reconectar sin inspección visual previa",
                 "Movilizar cuadrilla de mantenimiento inmediatamente"]

# 3. MAGNITUD DE CORRIENTE → tipo de falla
if factor_I > 8:
    causas.append(("💥", "Corriente de cortocircuito muy alta",
        f"Corriente de falla {I_falla_max:.0f} A ({factor_I:.1f}x la nominal). Falla de baja impedancia — contacto directo conductor-tierra o conductor-conductor. Probable daño severo.",
        "alta"))
    acciones += ["Inspeccionar conductor por ruptura o empalme fallido",
                 "Verificar que no haya conductor caído energizado en suelo"]
elif factor_I > 3:
    causas.append(("⚠️", "Corriente de falla moderada-alta",
        f"Corriente de falla {I_falla_max:.0f} A ({factor_I:.1f}x la nominal). Puede indicar flashover de aislador con arco sostenido o contacto con vegetación.",
        "media"))
    acciones += ["Revisar aisladores por flashover — buscar marcas de arco"]
else:
    causas.append(("🔍", "Corriente de falla baja",
        f"Corriente de falla {I_falla_max:.0f} A ({factor_I:.1f}x la nominal). Falla de alta impedancia — posible contacto con árbol húmedo, conductor sobre tierra, o aislador muy contaminado.",
        "baja"))
    acciones += ["Revisar aisladores por contaminación severa (falla de alta impedancia)",
                 "Buscar conductor apoyado sobre vegetación densa húmeda",
                 "Inspeccionar puesta a tierra de estructuras"]

# 4. POSICIÓN EN LA LÍNEA → qué infraestructura hay ahí
if consensus:
    if pct_linea < 15:
        causas.append(("🏗️", "Falla cercana al origen (subestación)",
            f"Falla a {consensus:.1f} km del origen ({pct_linea:.0f}%). Revisar equipos en cabecera: seccionadores, transformadores de medida, pararrayos de salida.",
            "media"))
        acciones += ["Inspeccionar equipos de patio en subestación origen",
                     "Revisar pararrayos de salida de línea",
                     "Verificar seccionadores de línea"]
    elif pct_linea > 85:
        causas.append(("🏗️", "Falla cercana al destino (subestación remota)",
            f"Falla a {consensus:.1f} km ({pct_linea:.0f}% de la línea). Revisar equipos en subestación destino o transformadores de distribución al final de la línea.",
            "media"))
        acciones += ["Inspeccionar equipos en subestación destino",
                     "Revisar transformadores de distribución en el extremo final"]
    else:
        acciones += [f"Concentrar patrullaje en zona de {max(0,consensus-2):.1f} km a {min(line_length,consensus+2):.1f} km desde el origen"]

# 5. COMPONENTE I0 → pararrayos
if abs(I0_s) > 0.3 * I_rated and has_gnd:
    causas.append(("⛈️", "Alta corriente de secuencia cero — posible pararrayos operado",
        f"I0 = {abs(I0_s):.2f} A. Corriente de secuencia cero elevada indica falla a tierra con buena conducción. Puede ser pararrayos que operó por sobretensión de rayo y quedó dañado (en corto).",
        "media"))
    acciones += ["Medir resistencia de pararrayos en el tramo con medidor de fuga",
                 "Reemplazar pararrayos sospechosos — son económicos, cambiar preventivamente",
                 "Verificar contador de operaciones de pararrayos si tienen"]
    descartar += []

# ── RENDER ──────────────────────────────────────────────────────────────────────
# Causas probables
st.markdown("""
<div style="background:#fffbf0;border:1px solid #f9a825;border-left:5px solid #f9a825;
border-radius:8px;padding:1rem 1.5rem;margin-bottom:1rem;">
<div style="font-weight:700;color:#e65100;font-size:0.85rem;letter-spacing:1px;
text-transform:uppercase;margin-bottom:8px;">⚠️ Causas más probables</div>
""", unsafe_allow_html=True)

for emoji, titulo, desc, prioridad in causas:
    bdr = {"alta":"#e53935","media":"#f9a825","baja":"#43a047"}[prioridad]
    bg  = {"alta":"#fff3f3","media":"#fffbf0","baja":"#f1f8e9"}[prioridad]
    st.markdown(f"""
    <div style="background:{bg};border-left:4px solid {bdr};border-radius:6px;
    padding:0.8rem 1.2rem;margin:6px 0;">
        <div style="font-weight:700;color:#1a2535;font-size:0.95rem;">{emoji} {titulo}</div>
        <div style="color:#4a5568;font-size:0.85rem;margin-top:4px;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Acciones en campo
st.markdown("""
<div style="background:#e8f5e9;border:1px solid #a5d6a7;border-left:5px solid #2e7d32;
border-radius:8px;padding:1rem 1.5rem;margin-bottom:1rem;">
<div style="font-weight:700;color:#1b5e20;font-size:0.85rem;letter-spacing:1px;
text-transform:uppercase;margin-bottom:10px;">🛠️ Qué revisar en campo (en orden de prioridad)</div>
""", unsafe_allow_html=True)

acciones_unicas = list(dict.fromkeys(acciones))  # quitar duplicados
for i, accion in enumerate(acciones_unicas, 1):
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:10px;padding:5px 0;
    border-bottom:1px solid rgba(0,0,0,0.06);">
        <span style="background:#2e7d32;color:white;border-radius:50%;width:22px;height:22px;
        display:flex;align-items:center;justify-content:center;font-size:0.7rem;
        font-weight:700;flex-shrink:0;margin-top:1px;">{i}</span>
        <span style="color:#1a2535;font-size:0.88rem;">{accion}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Qué descartar
if descartar:
    st.markdown("""
    <div style="background:#f5f5f5;border:1px solid #e0e0e0;border-left:5px solid #9e9e9e;
    border-radius:8px;padding:1rem 1.5rem;margin-bottom:1rem;">
    <div style="font-weight:700;color:#616161;font-size:0.85rem;letter-spacing:1px;
    text-transform:uppercase;margin-bottom:8px;">✅ Qué probablemente NO es</div>
    """, unsafe_allow_html=True)
    for d in descartar:
        st.markdown(f'<div style="color:#757575;font-size:0.85rem;padding:3px 0;">❌ {d}</div>',
                    unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─── Summary table ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Resumen del evento</div>', unsafe_allow_html=True)

summary_data = {
    "Parámetro": [
        "Línea analizada","Longitud","Tipo de falla","Falla a tierra",
        "Inicio de falla","Duración estimada","Distancia estimada",
        "Ia pico (falla)","Ib pico (falla)","Ic pico (falla)",
        "I0 (seq. cero)","ΔV Fase A","ΔV Fase B","ΔV Fase C","Timestamp",
    ],
    "Valor": [
        line_name, f"{line_length:.1f} km", ft, "Sí" if has_gnd else "No",
        f"{onset_ms:.2f} ms", f"{dur_ms:.0f} ms",
        f"{consensus:.2f} km ({consensus/line_length*100:.1f}%)" if consensus else "N/D",
        f"{Ia_pk:.1f} A", f"{Ib_pk:.1f} A", f"{Ic_pk:.1f} A",
        f"{abs(I0_s):.3f} A", f"{dVa:.1f}%", f"{dVb:.1f}%", f"{dVc:.1f}%", ts,
    ]
}

df_summary = pd.DataFrame(summary_data)
col_s1, col_s2 = st.columns(2)
half = len(df_summary)//2
col_s1.dataframe(df_summary.iloc[:half].reset_index(drop=True), hide_index=True, use_container_width=True)
col_s2.dataframe(df_summary.iloc[half:].reset_index(drop=True), hide_index=True, use_container_width=True)

st.divider()
st.caption(f"⚡ Fault Analyzer · {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · {line_name}")
