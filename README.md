# ⚡ Fault Analyzer — Analizador de Fallas COMTRADE

App Streamlit para análisis de fallas en líneas de transmisión.
Sube archivos `.CFG` + `.DAT`, selecciona el tipo de línea y obtén el análisis completo en pantalla.

---

## 🚀 Cómo publicar en Streamlit Cloud (paso a paso)

### 1. Crear repositorio en GitHub

1. Ve a [github.com](https://github.com) → **New repository**
2. Nombre: `fault-analyzer` (o el que prefieras)
3. Visibilidad: **Public** (requerido para Streamlit Cloud gratuito)
4. Click en **Create repository**

### 2. Subir los archivos al repositorio

**Opción A — Desde GitHub (más fácil):**
1. En el repo → **Add file → Upload files**
2. Arrastra todos los archivos de esta carpeta:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
3. Click **Commit changes**

**Opción B — Desde Git (terminal):**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU_USUARIO/fault-analyzer.git
git branch -M main
git push -u origin main
```

### 3. Publicar en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub
3. Click en **New app**
4. Selecciona:
   - **Repository:** `TU_USUARIO/fault-analyzer`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **Deploy!**

En 2-3 minutos tendrás una URL pública tipo:
`https://fault-analyzer-XXXXX.streamlit.app`

---

## 📂 Archivos del proyecto

```
fault-analyzer/
├── app.py                 ← App completa (un solo archivo)
├── requirements.txt       ← Dependencias Python
└── .streamlit/
    └── config.toml        ← Tema visual
```

---

## Cómo usar la app

1. **Selecciona el tipo de línea:** 69 kV o 13.8 kV
2. **Ingresa la longitud** de la línea en km
3. **Sube los archivos** `.CFG` y `.DAT` del relé
4. El análisis aparece automáticamente en pantalla

---

## Líneas configuradas

| Línea | Cable | Z1 (Ω/km) | Z0 (Ω/km) |
|-------|-------|-----------|-----------|
| 69 kV | ACSR HAWK 477 kcmil | 0.0841 + j0.3932 | 0.2530 + j1.1796 |
| 13.8 kV | ACSR 266 kcmil | 0.1710 + j0.3812 | 0.3402 + j1.1436 |

---

## Lo que muestra el reporte

- **Tipo de falla** detectada automáticamente (AG, BG, CG, AB, BC, CA, ABG, BCG, 3PH…)
- **Localización** con 3 métodos (Reactancia, Takagi, Takagi Modificado) + consenso
- **Barra visual** de posición de la falla en la línea
- **Magnitudes eléctricas** de corriente y tensión por fase
- **Gráficas interactivas:** Formas de onda, Componentes simétricas, Trayectoria R-X
- **Tabla resumen** del evento completo
