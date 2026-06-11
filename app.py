import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import joblib

# ═══════════════════════════════════════════════════════════
# 1. KONFIGURASI HALAMAN
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Smart Retail — Project Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS Global (Dark Theme) ───────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0a0a0f !important;
        color: #e2e8f0 !important;
    }

    /* Sidebar — dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #0a0a0f 100%) !important;
        border-right: 0.5px solid #1e1e2e !important;
    }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #475569 !important;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background: #111118 !important;
        border-color: #2a2a3e !important;
    }
    [data-testid="stSidebar"] .stRadio label { color: #94a3b8 !important; }

    /* Main background */
    .stApp { background-color: #0a0a0f !important; }
    .block-container { background-color: #0a0a0f !important; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #111118;
        padding: 6px;
        border-radius: 10px;
        border: 0.5px solid #1e1e2e;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 7px;
        padding: 9px 18px;
        font-weight: 500;
        font-size: 13px;
        color: #475569;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        background: #1a1a2e !important;
        color: #e2e8f0 !important;
        border: 0.5px solid #2a2a3e !important;
    }

    /* Dataframe */
    .stDataFrame {
        background: #111118 !important;
        border: 0.5px solid #1e1e2e !important;
        border-radius: 10px !important;
    }

    /* KPI Cards */
    .kpi-box {
        background: #111118;
        border: 0.5px solid #1e1e2e;
        border-left: 3px solid #3b82f6;
        padding: 16px 18px;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    .kpi-box-danger {
        background: #110e0e;
        border: 0.5px solid #2a1a1a;
        border-left: 3px solid #ef4444;
        padding: 16px 18px;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    .kpi-box-success {
        background: #0a110e;
        border: 0.5px solid #1a2e1e;
        border-left: 3px solid #22c55e;
        padding: 16px 18px;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    .kpi-box-warning {
        background: #110f08;
        border: 0.5px solid #2e2414;
        border-left: 3px solid #f59e0b;
        padding: 16px 18px;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    .kpi-title {
        font-size: 10px;
        color: #475569;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #f1f5f9;
        font-family: 'DM Mono', monospace;
    }
    .kpi-sub { font-size: 11px; color: #475569; margin-top: 3px; }

    /* Section Header */
    .section-header {
        font-size: 13px;
        font-weight: 700;
        color: #94a3b8;
        margin-bottom: 12px;
        padding-bottom: 7px;
        border-bottom: 0.5px solid #1e1e2e;
    }

    /* Risk Cards */
    .risk-card {
        background: #111118;
        border: 0.5px solid #1e1e2e;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 10px;
    }
    .risk-tag-high {
        display: inline-block;
        background: #1f0a0a;
        color: #f87171;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 7px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 0.5px solid #3d1a1a;
    }
    .risk-tag-med {
        display: inline-block;
        background: #1a1306;
        color: #fbbf24;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 7px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 0.5px solid #3d2e0a;
    }

    /* Info / Success box */
    .info-box {
        background: #0d1526;
        border: 0.5px solid #1e3a5f;
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 13px;
        color: #93c5fd;
        line-height: 1.6;
    }
    .success-box {
        background: #0a1a0f;
        border: 0.5px solid #1a3d27;
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 13px;
        color: #86efac;
        line-height: 1.6;
    }

    /* Team card */
    .team-card {
        background: #111118;
        border: 0.5px solid #1e1e2e;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 8px;
    }
    .team-role { font-size: 13px; font-weight: 700; color: #f1f5f9; margin-bottom: 3px; }
    .team-acc { font-size: 12px; color: #60a5fa; font-weight: 500; margin-bottom: 5px; }
    .team-desc { font-size: 12px; color: #64748b; line-height: 1.5; }

    /* Deployment step */
    .deploy-step {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 0;
        border-bottom: 0.5px solid #15151f;
    }
    .deploy-num {
        width: 30px;
        height: 30px;
        background: #1e1e2e;
        color: #e2e8f0;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        flex-shrink: 0;
        border: 0.5px solid #2a2a3e;
    }
    .deploy-content { flex: 1; }
    .deploy-title { font-size: 13px; font-weight: 700; color: #f1f5f9; margin-bottom: 2px; }
    .deploy-desc { font-size: 12px; color: #64748b; }

    /* Metric chip */
    .metric-chip {
        display: inline-block;
        background: #111118;
        border: 0.5px solid #1e1e2e;
        border-radius: 8px;
        padding: 9px 14px;
        font-size: 13px;
        color: #94a3b8;
        margin: 4px;
    }
    .metric-chip strong {
        color: #f1f5f9;
        display: block;
        font-size: 18px;
        font-family: 'DM Mono', monospace;
    }

    /* Divider */
    hr { border: none; border-top: 0.5px solid #1e1e2e; margin: 18px 0; }

    /* Selectbox & radio override */
    div[data-baseweb="select"] > div {
        background-color: #111118 !important;
        border-color: #2a2a3e !important;
        color: #e2e8f0 !important;
    }
    div[data-baseweb="popover"] { background-color: #111118 !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# 2. LOAD DATA & MODEL
# ═══════════════════════════════════════════════════════════
@st.cache_data
def load_data_and_models():
    df_clean = pd.read_csv('retail_clean.csv')
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])
    model = joblib.load('rf_model_inventory.pkl')
    scaler = joblib.load('scaler_inventory.pkl')
    feature_cols = joblib.load('feature_columns.pkl')
    return df_clean, model, scaler, feature_cols

try:
    df, rf_model, scaler, feature_columns = load_data_and_models()
except Exception as e:
    st.error(f"Gagal memuat file komponen AI. Pastikan semua file berada di folder yang sama.\n\nError: {e}")
    st.stop()


# ═══════════════════════════════════════════════════════════
# 3. SIDEBAR CONTROL
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📦 AI Smart Retail")
    st.markdown("<p style='font-size:12px;color:#475569;'>Inventory Demand Forecasting System</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ⚙️ Pusat Kontrol")
    st.markdown("<p style='font-size:11px;color:#475569;'>Atur parameter analisis di bawah ini</p>", unsafe_allow_html=True)

    pilihan_produk = st.selectbox("📦 ID Produk:", sorted(df['Product ID'].unique()))
    df_filtered_prod = df[df['Product ID'] == pilihan_produk]
    pilihan_toko = st.selectbox("🏪 ID Cabang Toko:", sorted(df_filtered_prod['Store ID'].unique()))

    st.markdown("---")
    st.markdown("### 📅 Periode Prediksi")
    periode_pilihan = st.radio(
        "Horizon Peramalan:",
        options=["1 Minggu (7 Hari)", "1 Bulan (30 Hari)"],
        index=0
    )
    forecast_days = 7 if "Minggu" in periode_pilihan else 30

    st.markdown("---")
    mask_info = (df['Product ID'] == pilihan_produk) & (df['Store ID'] == pilihan_toko)
    df_info = df[mask_info]
    if not df_info.empty:
        cat = df_info['Category'].iloc[0]
        region = df_info['Region'].iloc[0]
        st.markdown(f"**Kategori:** {cat}")
        st.markdown(f"**Region:** {region}")
        st.markdown(f"**Total Record:** {len(df_info):,} hari")

    st.markdown("---")
    st.markdown("<p style='font-size:10px;color:#475569;'>Kelompok 5 · 4PDS1<br>Universitas Bunda Mulia · 2026</p>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# 4. FILTER DATA & PREDIKSI
# ═══════════════════════════════════════════════════════════
mask = (df['Product ID'] == pilihan_produk) & (df['Store ID'] == pilihan_toko)
df_hist = df[mask].sort_values('Date').tail(30).reset_index(drop=True)

if df_hist.empty:
    st.warning("⚠️ Tidak ada data historis untuk kombinasi tersebut.")
    st.stop()

last_row = df_hist.iloc[-1]
last_date = df_hist['Date'].iloc[-1]
safety_stock_val = last_row['Safety_Stock']
stok_sekarang = int(last_row.get('Inventory Level', df_hist['Inventory Level'].mean()))

tanggal_prediksi = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days)

fitur_statis = {
    'Inventory Level': stok_sekarang,
    'Units Ordered': df_hist['Units Ordered'].mean(),
    'Demand Forecast': df_hist['Demand Forecast'].mean() if 'Demand Forecast' in df.columns else 0,
    'Price': last_row.get('Price', df_hist['Price'].mean()) if 'Price' in df.columns else 0,
    'Discount': last_row.get('Discount', 0) if 'Discount' in df.columns else 0,
    'Safety_Stock': safety_stock_val,
}

rows_future = []
for tgl in tanggal_prediksi:
    row = fitur_statis.copy()
    row['Month'] = tgl.month
    row['Day_of_Week'] = tgl.dayofweek
    row['Is_Weekend'] = 1 if tgl.dayofweek >= 5 else 0
    rows_future.append(row)

df_future = pd.DataFrame(rows_future)
for col in feature_columns:
    if col not in df_future.columns:
        df_future[col] = 0
df_future = df_future[feature_columns]
df_future_scaled = scaler.transform(df_future)
prediksi_hasil = rf_model.predict(df_future_scaled).round().astype(int)

total_prediksi = prediksi_hasil.sum()
safety_stock_int = int(safety_stock_val)
rekomendasi_order = max(0, total_prediksi + safety_stock_int - stok_sekarang)
avg_harian = df_hist['Units Sold'].mean()
stok_coverage_days = round(stok_sekarang / max(avg_harian, 1), 1)
label_prediksi = "7H" if forecast_days == 7 else "30H"


# ═══════════════════════════════════════════════════════════
# 5. HEADER UTAMA
# ═══════════════════════════════════════════════════════════
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"## 🚀 AI Smart Retail Inventory Dashboard")
    st.markdown(f"<p style='color:#64748b;font-size:14px;'>Produk <strong style='color:#94a3b8;'>{pilihan_produk}</strong> &nbsp;·&nbsp; Cabang <strong style='color:#94a3b8;'>{pilihan_toko}</strong> &nbsp;·&nbsp; Kategori <strong style='color:#94a3b8;'>{df_hist['Category'].iloc[0]}</strong> &nbsp;·&nbsp; Region <strong style='color:#94a3b8;'>{df_hist['Region'].iloc[0]}</strong></p>", unsafe_allow_html=True)
with col_h2:
    status_color = "#ef4444" if rekomendasi_order > 0 else "#22c55e"
    status_bg = "#110e0e" if rekomendasi_order > 0 else "#0a110e"
    status_border = "#2a1a1a" if rekomendasi_order > 0 else "#1a2e1e"
    status_text = "⚠️ PERLU REORDER" if rekomendasi_order > 0 else "✅ STOK AMAN"
    st.markdown(f"""
    <div style='background:{status_bg};border:1px solid {status_border};border-radius:10px;padding:12px 16px;text-align:center;margin-top:8px;'>
        <div style='font-size:11px;font-weight:700;color:{status_color};letter-spacing:0.06em;'>{status_text}</div>
        <div style='font-size:22px;font-weight:800;color:{status_color};font-family:DM Mono,monospace;'>
            {'+ ' + str(rekomendasi_order) + ' Unit' if rekomendasi_order > 0 else '0 Unit'}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# 6. TAB LAYOUT
# ═══════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard Operasional",
    "🧠 Pemahaman Bisnis & Data",
    "👥 Tim & Timeline Proyek",
    "⚠️ Manajemen Risiko",
    "🚀 Deployment & Monitoring"
])


# ══════════════════════════════════════════
# TAB 1 — DASHBOARD OPERASIONAL
# ══════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f'<div class="kpi-box"><div class="kpi-title">📦 Stok Saat Ini</div><div class="kpi-value">{stok_sekarang}</div><div class="kpi-sub">Unit tersedia</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-box" style="border-left-color:#8b5cf6;"><div class="kpi-title">📈 Prediksi Terjual ({label_prediksi})</div><div class="kpi-value" style="color:#a78bfa;">{total_prediksi}</div><div class="kpi-sub">Proyeksi AI</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-box-warning"><div class="kpi-title">🛡️ Safety Stock</div><div class="kpi-value" style="color:#fbbf24;">{safety_stock_int}</div><div class="kpi-sub">Buffer minimum</div></div>', unsafe_allow_html=True)
    with c4:
        if rekomendasi_order > 0:
            st.markdown(f'<div class="kpi-box-danger"><div class="kpi-title">🛒 Reorder Diperlukan</div><div class="kpi-value" style="color:#f87171;">+{rekomendasi_order}</div><div class="kpi-sub">Unit harus dipesan</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="kpi-box-success"><div class="kpi-title">🛒 Status Reorder</div><div class="kpi-value" style="color:#4ade80;">Aman</div><div class="kpi-sub">Stok mencukupi</div></div>', unsafe_allow_html=True)
    with c5:
        coverage_color = "#f87171" if stok_coverage_days < 7 else "#4ade80"
        coverage_bg = "#110e0e" if stok_coverage_days < 7 else "#0a110e"
        coverage_border = "#2a1a1a" if stok_coverage_days < 7 else "#1a2e1e"
        st.markdown(f'<div class="kpi-box" style="border-left-color:{coverage_color};background:{coverage_bg};border-color:{coverage_border};"><div class="kpi-title">📅 Coverage Stok</div><div class="kpi-value" style="color:{coverage_color};">{stok_coverage_days}H</div><div class="kpi-sub">Hari hingga habis</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown(f'<div class="section-header">📉 Proyeksi Tren Penjualan & Ambang Stok ({label_prediksi})</div>', unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_hist['Date'], y=df_hist['Units Sold'],
            name='Historis (30 Hari)', line=dict(color='#334155', width=2),
            fill='tozeroy', fillcolor='rgba(51,65,85,0.15)'
        ))
        fig.add_trace(go.Scatter(
            x=tanggal_prediksi, y=prediksi_hasil,
            name=f'Proyeksi AI ({label_prediksi})', mode='lines+markers',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=9, color='#3b82f6', line=dict(width=2, color='#0a0a0f')),
            fill='tozeroy', fillcolor='rgba(59,130,246,0.08)'
        ))
        fig.add_trace(go.Scatter(
            x=list(df_hist['Date']) + list(tanggal_prediksi),
            y=[safety_stock_int] * (len(df_hist) + forecast_days),
            name='Batas Safety Stock', line=dict(color='#ef4444', width=1.5, dash='dot')
        ))
        fig.update_layout(
            template='plotly_dark',
            margin=dict(l=10, r=10, t=10, b=10), height=340,
            hovermode="x unified", legend=dict(orientation="h", y=-0.15),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,17,24,0.8)',
            font=dict(family='DM Sans', color='#94a3b8')
        )
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='#1e1e2e', showline=False, color='#64748b')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='#1e1e2e', title="Unit Terjual", zeroline=False, color='#64748b')
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown(f'<div class="section-header">📋 Jadwal Rencana Distribusi ({label_prediksi})</div>', unsafe_allow_html=True)
        df_output = pd.DataFrame({
            'Hari': tanggal_prediksi.strftime('%a, %d %b'),
            'Estimasi': prediksi_hasil,
            'Status': ['🚨 RISIKO' if prediksi_hasil[i] > stok_sekarang * 0.4 else '🟢 AMAN' for i in range(forecast_days)]
        }, index=range(1, forecast_days + 1))
        df_output.index.name = 'H'

        def color_status(val):
            if '🚨' in str(val):
                return 'background:#1f0a0a;color:#f87171;font-weight:600;'
            return 'background:#0a1a0f;color:#4ade80;'

        st.dataframe(
            df_output.style.map(color_status, subset=['Status']),
            use_container_width=True, height=min(340 + (forecast_days - 7) * 20, 700)
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Analisis Pola Historis</div>', unsafe_allow_html=True)
    ca, cb, cc = st.columns(3)

    with ca:
        dow_map = {0: 'Sen', 1: 'Sel', 2: 'Rab', 3: 'Kam', 4: 'Jum', 5: 'Sab', 6: 'Min'}
        df_hist['DayName'] = df_hist['Day_of_Week'].map(dow_map)
        dow_avg = df_hist.groupby('Day_of_Week')['Units Sold'].mean().reset_index()
        dow_avg['DayName'] = dow_avg['Day_of_Week'].map(dow_map)
        dow_avg = dow_avg.sort_values('Day_of_Week')
        fig_dow = px.bar(dow_avg, x='DayName', y='Units Sold', title='Rata-rata Penjualan per Hari',
                         color='Units Sold', color_continuous_scale='Blues')
        fig_dow.update_layout(template='plotly_dark', height=240, margin=dict(l=0, r=0, t=40, b=0),
                               paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,17,24,0.8)',
                               showlegend=False, coloraxis_showscale=False,
                               title_font_size=13, font=dict(color='#94a3b8'))
        fig_dow.update_xaxes(showgrid=False, color='#64748b')
        fig_dow.update_yaxes(showgrid=True, gridcolor='#1e1e2e', color='#64748b')
        st.plotly_chart(fig_dow, use_container_width=True)

    with cb:
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=df_hist['Units Sold'], nbinsx=12,
                                        marker_color='#3b82f6', opacity=0.8))
        fig_hist.update_layout(template='plotly_dark', title='Distribusi Units Sold (30H)', height=240,
                                margin=dict(l=0, r=0, t=40, b=0),
                                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,17,24,0.8)',
                                title_font_size=13, font=dict(color='#94a3b8'))
        fig_hist.update_xaxes(showgrid=False, color='#64748b')
        fig_hist.update_yaxes(showgrid=True, gridcolor='#1e1e2e', title='Frekuensi', color='#64748b')
        st.plotly_chart(fig_hist, use_container_width=True)

    with cc:
        fig_sc = px.scatter(df_hist, x='Inventory Level', y='Units Sold',
                            color='Is_Weekend', color_discrete_map={0: '#3b82f6', 1: '#f59e0b'},
                            title='Stok vs Penjualan (Weekday/Weekend)',
                            labels={'color': 'Weekend'})
        fig_sc.update_layout(template='plotly_dark', height=240, margin=dict(l=0, r=0, t=40, b=0),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,17,24,0.8)',
                              title_font_size=13, font=dict(color='#94a3b8'))
        fig_sc.update_xaxes(showgrid=True, gridcolor='#1e1e2e', color='#64748b')
        fig_sc.update_yaxes(showgrid=True, gridcolor='#1e1e2e', color='#64748b')
        st.plotly_chart(fig_sc, use_container_width=True)


# ══════════════════════════════════════════
# TAB 2 — PEMAHAMAN BISNIS & DATA
# ══════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    col2a, col2b = st.columns([1, 1])

    with col2a:
        st.markdown('<div class="section-header">🎯 Bagian 1 — Pemahaman Bisnis & Pendefinisian Masalah</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
        <strong>Problem Statement</strong><br>
        Jaringan ritel multi-cabang menghadapi inefisiensi rantai pasok akibat pola permintaan
        yang tidak terprediksi — menyebabkan <em>overstock</em> (pemborosan holding cost)
        dan <em>stockout</em> (kehilangan penjualan). Secara Data Science, masalah ini
        diterjemahkan sebagai <strong>regresi time-series multivariat</strong>: memprediksi
        <em>Units Sold</em> 7 hari ke depan berdasarkan fitur historis stok, harga,
        diskon, cuaca, dan musim.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("**📌 Business Objectives & Success Criteria**")
        biz_data = {
            'Dimensi': ['Bisnis', 'Bisnis', 'Teknis (Model)', 'Teknis (Model)'],
            'Metrik': ['Holding Cost', 'Lost Sales', 'MAPE', 'R² Score'],
            'Target': ['↓ 15%', '↓ 20%', '< 15%', '> 85%'],
            'Status Saat Ini': ['Baseline', 'Baseline', '14.32% ✅', '99.41% ✅']
        }
        df_biz = pd.DataFrame(biz_data)
        st.dataframe(df_biz, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("**👥 Stakeholder Mapping**")
        stakeholders = [
            ("🏢 Project Sponsor (COO)", "Mendanai proyek & menetapkan KPI bisnis. Ekspektasi: ROI terukur dari efisiensi stok."),
            ("🔬 Data Science Team", "Membangun & memvalidasi model ML. Ekspektasi: data berkualitas & infrastruktur cloud."),
            ("🏪 Manajer Toko (End-User)", "Menggunakan dashboard harian. Ekspektasi: antarmuka intuitif tanpa perlu skill teknis."),
            ("📦 Tim Procurement", "Merencanakan pemesanan. Ekspektasi: rekomendasi reorder akurat & tepat waktu."),
            ("🗄️ IT / Data Owner", "Mengelola akses ERP/POS. Ekspektasi: kepatuhan data governance & keamanan data."),
        ]
        for title, desc in stakeholders:
            st.markdown(f"""
            <div class="team-card">
                <div class="team-role">{title}</div>
                <div class="team-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2b:
        st.markdown('<div class="section-header">🗂️ Bagian 2 — Strategi Data & Arsitektur</div>', unsafe_allow_html=True)

        st.markdown("**📋 Daftar Fitur / Variabel Data**")
        feat_data = {
            'Variabel': ['Units Sold', 'Inventory Level', 'Units Ordered', 'Demand Forecast',
                         'Price', 'Discount', 'Weather Condition', 'Holiday/Promotion',
                         'Competitor Pricing', 'Seasonality', 'Safety_Stock',
                         'Month', 'Day_of_Week', 'Is_Weekend'],
            'Tipe': ['Target', 'Fitur', 'Fitur', 'Fitur', 'Fitur', 'Fitur',
                     'Fitur', 'Fitur', 'Fitur', 'Fitur', 'Fitur', 'Temporal', 'Temporal', 'Temporal'],
            'Sumber': ['POS', 'ERP', 'ERP', 'Internal', 'ERP', 'ERP',
                       'API Cuaca', 'Kalender', 'Web Scraping', 'Kalender',
                       'Kebijakan', 'Derived', 'Derived', 'Derived']
        }
        df_feat = pd.DataFrame(feat_data)

        def color_tipe(val):
            if val == 'Target':
                return 'background:#0d1526;color:#60a5fa;font-weight:600;'
            elif val == 'Temporal':
                return 'background:#0a1a0f;color:#4ade80;'
            return ''

        st.dataframe(df_feat.style.map(color_tipe, subset=['Tipe']),
                     use_container_width=True, height=290, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("**🔒 Data Governance & Privacy**")
        st.markdown("""
        <div class="info-box">
        <strong>Kebijakan Penanganan Data:</strong><br>
        • <strong>Anonimisasi:</strong> Data pelanggan di-hash (SHA-256) sebelum disimpan di Data Lake<br>
        • <strong>Akses Berlapis:</strong> Role-Based Access Control (RBAC) di AWS IAM<br>
        • <strong>Enkripsi:</strong> Data at-rest (AES-256) & in-transit (TLS 1.3)<br>
        • <strong>Audit Trail:</strong> Setiap akses dilog di AWS CloudTrail<br>
        • <strong>Retensi:</strong> Data historis disimpan maksimal 3 tahun sesuai kebijakan perusahaan
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("**⚙️ Alur Infrastruktur Data**")
        pipeline_steps = [
            ("1", "Akuisisi", "ERP/POS System → AWS DMS / Azure Data Factory → Raw Storage (S3)"),
            ("2", "Processing", "AWS Glue / Databricks → Cleaning, Hashing, Feature Engineering → Parquet"),
            ("3", "Serving", "Data Lake → Feature Store → Model Training (SageMaker) → API Endpoint"),
            ("4", "Visualisasi", "API Endpoint → Streamlit Dashboard → Manajer Toko / Procurement"),
        ]
        for num, title, desc in pipeline_steps:
            st.markdown(f"""
            <div class="deploy-step">
                <div class="deploy-num">{num}</div>
                <div class="deploy-content">
                    <div class="deploy-title">{title}</div>
                    <div class="deploy-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("**🔄 Kerangka Metodologi CRISP-DM**")
        crisp_phases = [
            ("Business Understanding", "#3b82f6", "KPI: Holding cost ↓15%, Lost sales ↓20%"),
            ("Data Understanding", "#8b5cf6", "Eksplorasi 73.100 record dari 5 toko, 20 produk"),
            ("Data Preparation", "#06b6d4", "ETL, cleaning, feature engineering lag/rolling"),
            ("Modeling", "#10b981", "Random Forest vs XGBoost vs GRU — RF terbaik"),
            ("Evaluation", "#f59e0b", "MAPE 14.32% < 15% ✅, R² 99.41% ✅"),
            ("Deployment", "#ef4444", "Streamlit Dashboard + API Endpoint production"),
        ]
        for i, (phase, color, note) in enumerate(crisp_phases):
            st.markdown(f"""
            <div style='display:flex;align-items:center;margin-bottom:6px;'>
                <div style='background:{color}18;border:1px solid {color}35;border-radius:8px;padding:8px 12px;flex:1;'>
                    <div style='font-size:12px;font-weight:700;color:{color};'>{phase}</div>
                    <div style='font-size:11px;color:#64748b;'>{note}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 3 — TIM & TIMELINE
# ══════════════════════════════════════════
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)

    col3a, col3b = st.columns([1, 1])

    with col3a:
        st.markdown('<div class="section-header">👥 Struktur Organisasi Tim Proyek</div>', unsafe_allow_html=True)

        team_members = [
            ("🎯 Project Manager / Scrum Master", "Tata kelola, risiko & linimasa",
             "#3b82f6", "Jembatan teknis-bisnis, mengawal CRISP-DM, memastikan proyek on-time & on-budget"),
            ("🔧 Data Engineer", "Keandalan data pipeline hulu",
             "#8b5cf6", "ETL dari ERP/POS, membangun Ingestion & Processing Layer, hashing data sensitif"),
            ("🧠 Data Scientist", "Akurasi & kualitas model prediktif",
             "#06b6d4", "Feature engineering (lag, rolling window), eksplorasi algoritma, target MAPE < 15%"),
            ("⚙️ ML Engineer (MLE)", "Operasionalisasi & MLOps",
             "#10b981", "Packaging model ke API endpoint (SageMaker/Azure ML), sistem monitoring model drift"),
            ("📊 Data Analyst / BI Developer", "Aksesibilitas visualisasi end-user",
             "#f59e0b", "Desain & bangun dashboard Streamlit/Tableau, integrasikan ke API prediksi"),
            ("💼 SME / Business Analyst", "Validasi logika bisnis & operasional",
             "#ef4444", "Konteks produk ritel, validasi fitur model vs realitas lapangan"),
        ]
        for role, acc, color, desc in team_members:
            st.markdown(f"""
            <div class="team-card" style="border-left:3px solid {color};">
                <div class="team-role" style="color:{color};">{role}</div>
                <div class="team-acc">⚡ {acc}</div>
                <div class="team-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**📋 Hierarki Struktur Tim**")
        fig_org = go.Figure()
        nodes = [
            (0.5, 0.95, "Project Sponsor\n(COO)", "#1e3a5f", "#93c5fd"),
            (0.5, 0.78, "Project Manager\n/ Scrum Master", "#1e3a5f", "#60a5fa"),
            (0.15, 0.60, "Data\nEngineer", "#1e1a3e", "#a78bfa"),
            (0.38, 0.60, "Data\nScientist", "#0d2a2a", "#67e8f9"),
            (0.62, 0.60, "ML\nEngineer", "#0a2218", "#6ee7b7"),
            (0.85, 0.60, "SME /\nBiz Analyst", "#1f0a0a", "#fca5a5"),
            (0.38, 0.42, "Data Analyst\n/ BI Developer", "#1a1306", "#fcd34d"),
        ]
        edges = [(0.5, 0.95, 0.5, 0.78), (0.5, 0.78, 0.15, 0.60), (0.5, 0.78, 0.38, 0.60),
                 (0.5, 0.78, 0.62, 0.60), (0.5, 0.78, 0.85, 0.60), (0.38, 0.60, 0.38, 0.42)]
        for x0, y0, x1, y1 in edges:
            fig_org.add_shape(type='line', x0=x0, y0=y0, x1=x1, y1=y1,
                              line=dict(color='#2a2a3e', width=2))
        for x, y, label, bg, fg in nodes:
            fig_org.add_annotation(x=x, y=y, text=label.replace('\n', '<br>'),
                                   showarrow=False, font=dict(size=11, color=fg, family='DM Sans'),
                                   bgcolor=bg, bordercolor=fg, borderwidth=1,
                                   borderpad=8, align='center')
        fig_org.update_layout(
            template='plotly_dark',
            height=340, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0.3, 1.1]),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_org, use_container_width=True)

    with col3b:
        st.markdown('<div class="section-header">📅 Timeline & Gantt Chart (12 Minggu)</div>', unsafe_allow_html=True)

        gantt_data = [
            ("Fase 1: Business & Data Understanding", 1, 2, "#3b82f6", "Project Charter, BRD"),
            ("Fase 2: Data Preparation & Ingestion", 3, 4, "#8b5cf6", "ETL Pipeline, Dataset Parquet"),
            ("Fase 3: Feature Engineering & Baseline", 5, 6, "#06b6d4", "Kode Fitur, Baseline Report"),
            ("Fase 4: Advanced Modeling & Tuning", 7, 8, "#10b981", "Model ML Terbaik (RF)"),
            ("Fase 5: Model Evaluation & Validation", 9, 9, "#f59e0b", "Validasi MAPE < 15%"),
            ("Fase 6: Serving & BI Dashboarding", 10, 11, "#f97316", "API Endpoint, Dashboard"),
            ("Fase 7: UAT & Project Handover", 12, 12, "#ef4444", "Berita Acara UAT, Closure"),
        ]

        fig_gantt = go.Figure()
        for i, (task, start, end, color, deliverable) in enumerate(gantt_data):
            fig_gantt.add_trace(go.Bar(
                x=[end - start + 1], y=[task], orientation='h',
                base=[start - 1], marker_color=color,
                marker_line_width=0, opacity=0.8,
                hovertemplate=f"<b>{task}</b><br>Minggu {start}–{end}<br>Deliverable: {deliverable}<extra></extra>",
                showlegend=False
            ))
            fig_gantt.add_annotation(
                x=end - 0.1, y=task,
                text=f"  {deliverable}",
                showarrow=False, xanchor='left',
                font=dict(size=9, color='#64748b')
            )

        fig_gantt.update_layout(
            template='plotly_dark',
            height=380, margin=dict(l=10, r=10, t=10, b=30),
            xaxis=dict(title='Minggu', range=[0, 14], tickvals=list(range(1, 13)),
                       ticktext=[f'M{i}' for i in range(1, 13)], showgrid=True, gridcolor='#1e1e2e', color='#64748b'),
            yaxis=dict(autorange='reversed', showgrid=False, color='#94a3b8'),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,17,24,0.8)',
            bargap=0.35, font=dict(family='DM Sans', size=11, color='#94a3b8')
        )
        st.plotly_chart(fig_gantt, use_container_width=True)

        st.markdown("**🏁 Milestone & Deliverables**")
        milestone_df = pd.DataFrame({
            'Periode': ['Minggu 1–2', 'Minggu 3–4', 'Minggu 5–6', 'Minggu 7–8',
                        'Minggu 9', 'Minggu 10–11', 'Minggu 12'],
            'Fase': ['Business Understanding', 'Data Preparation', 'Feature Engineering',
                     'Advanced Modeling', 'Evaluation', 'Serving & BI', 'UAT & Handover'],
            'Deliverable Utama': ['Project Charter + BRD', 'ETL Pipeline + Dataset Parquet',
                                  'Repositori Fitur + Baseline', 'Model ML Terbaik',
                                  'Dokumen Validasi (MAPE<15%)', 'API Endpoint + Dashboard', 'Berita Acara + Closure']
        })
        st.dataframe(milestone_df, use_container_width=True, hide_index=True, height=270)


# ══════════════════════════════════════════
# TAB 4 — MANAJEMEN RISIKO
# ══════════════════════════════════════════
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)

    col4a, col4b = st.columns([1, 1])

    with col4a:
        st.markdown('<div class="section-header">🗺️ Risk Matrix (Probabilitas × Dampak)</div>', unsafe_allow_html=True)

        risks = {
            'Risiko': ['User Adoption Risk', 'Concept Drift Risk', 'Data Quality Risk',
                       'Infrastructure Failure', 'Regulatory/Privacy Risk'],
            'Probabilitas': [4, 3, 3, 2, 2],
            'Dampak': [5, 5, 4, 4, 3],
        }
        df_risk = pd.DataFrame(risks)
        df_risk['Skor'] = df_risk['Probabilitas'] * df_risk['Dampak']
        df_risk['Level'] = df_risk['Skor'].apply(
            lambda x: '🔴 TINGGI' if x >= 15 else ('🟡 SEDANG' if x >= 8 else '🟢 RENDAH')
        )

        fig_risk = px.scatter(df_risk, x='Probabilitas', y='Dampak',
                              size='Skor', color='Level', text='Risiko',
                              color_discrete_map={'🔴 TINGGI': '#ef4444', '🟡 SEDANG': '#f59e0b', '🟢 RENDAH': '#22c55e'},
                              size_max=50)
        fig_risk.update_traces(textposition='top center', textfont_size=11)
        fig_risk.update_layout(
            template='plotly_dark',
            height=340, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title='Probabilitas (1-5)', range=[0, 6], showgrid=True, gridcolor='#1e1e2e', color='#64748b'),
            yaxis=dict(title='Dampak (1-5)', range=[0, 6], showgrid=True, gridcolor='#1e1e2e', color='#64748b'),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,17,24,0.8)',
            font=dict(family='DM Sans', color='#94a3b8')
        )
        fig_risk.add_shape(type='rect', x0=0, y0=0, x1=2.5, y1=2.5,
                           fillcolor='rgba(34,197,94,0.04)', line_width=0)
        fig_risk.add_shape(type='rect', x0=2.5, y0=2.5, x1=6, y1=6,
                           fillcolor='rgba(239,68,68,0.04)', line_width=0)
        st.plotly_chart(fig_risk, use_container_width=True)

        st.dataframe(
            df_risk[['Risiko', 'Probabilitas', 'Dampak', 'Skor', 'Level']],
            use_container_width=True, hide_index=True
        )

    with col4b:
        st.markdown('<div class="section-header">📋 Rencana Mitigasi Detail</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="risk-card">
            <span class="risk-tag-high">🔴 TINGGI — Skor 20</span>
            <div class="team-role">Risiko 1: Resistensi Pengguna (User Adoption Risk)</div>
            <div class="team-desc" style="margin-top:6px;">
                <strong style="color:#94a3b8;">Deskripsi:</strong> Manajer Toko/Procurement menolak hasil prediksi AI dan
                tetap memesan secara manual (black-box syndrome).<br><br>
                <strong style="color:#94a3b8;">Dampak:</strong> Model underutilization → target holding cost ↓15% tidak tercapai.<br><br>
                <strong style="color:#94a3b8;">Mitigasi:</strong><br>
                ① <em>Shadow Running (2–4 minggu):</em> Sistem lama & baru berjalan paralel sebagai proof of accuracy.<br>
                ② <em>Edukasi Inklusif:</em> Manajer Toko dilibatkan sebagai SME sejak fase Business Understanding.<br>
                ③ <em>KPI Digitalisasi:</em> Tingkat adopsi dashboard dimasukkan ke KPI cabang toko.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="risk-card">
            <span class="risk-tag-high">🔴 TINGGI — Skor 15</span>
            <div class="team-role">Risiko 2: Degradasi Model (Concept Drift Risk)</div>
            <div class="team-desc" style="margin-top:6px;">
                <strong style="color:#94a3b8;">Deskripsi:</strong> Perubahan mendadak pada pola demand akibat inflasi,
                regulasi baru, atau kompetitor baru menyebabkan akurasi model turun drastis.<br><br>
                <strong style="color:#94a3b8;">Dampak:</strong> MAPE > 15% → prediksi tidak reliable → stockout/overstock massal.<br><br>
                <strong style="color:#94a3b8;">Mitigasi:</strong><br>
                ① <em>Automated Monitoring:</em> SageMaker Model Monitor / Azure ML melacak performa real-time.<br>
                ② <em>Retraining Pipeline:</em> Model auto-retrain jika MAPE > 20% selama 3 minggu berturut-turut.<br>
                ③ <em>Fallback Mechanism:</em> Otomatis beralih ke moving average jika anomali terdeteksi.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="risk-card">
            <span class="risk-tag-med">🟡 SEDANG — Skor 12</span>
            <div class="team-role">Risiko 3: Kualitas Data Historis Buruk</div>
            <div class="team-desc" style="margin-top:6px;">
                <strong style="color:#94a3b8;">Deskripsi:</strong> Data ERP/POS memiliki nilai hilang, duplikat, atau
                kesalahan entry yang signifikan pada periode tertentu.<br><br>
                <strong style="color:#94a3b8;">Dampak:</strong> Hasil rekayasa fitur bias → model tidak bisa mencapai target MAPE.<br><br>
                <strong style="color:#94a3b8;">Mitigasi:</strong><br>
                ① <em>Data Quality Dashboard:</em> Monitor completeness, consistency & accuracy secara otomatis.<br>
                ② <em>Validasi SME:</em> Data Scientist & SME melakukan validasi manual per anomali terdeteksi.<br>
                ③ <em>Data Contract:</em> SLA kualitas data ditandatangani bersama tim IT/Data Owner.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 5 — DEPLOYMENT & MONITORING
# ══════════════════════════════════════════
with tab5:
    st.markdown("<br>", unsafe_allow_html=True)

    col5a, col5b = st.columns([1, 1])

    with col5a:
        st.markdown('<div class="section-header">🚀 Deployment Plan</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="success-box">
        <strong>Strategi Integrasi Operasional Harian</strong><br>
        Model RF ini dideploy dalam bentuk <strong>Streamlit Dashboard</strong> yang diakses
        langsung oleh Manajer Toko dan Tim Procurement. Prediksi diperbarui setiap hari
        secara otomatis melalui scheduled job di cloud.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        deploy_steps = [
            ("1", "Model Packaging", "Model RF disimpan sebagai .pkl + scaler + feature_columns → dikemas ke Docker container"),
            ("2", "API Endpoint", "Container dideploy ke Amazon SageMaker / Azure ML sebagai REST API (/predict)"),
            ("3", "Scheduler", "AWS EventBridge / Azure Logic Apps memicu prediksi harian pukul 06.00 otomatis"),
            ("4", "Streamlit Dashboard", "Dashboard ini mengkonsumsi API endpoint → ditampilkan ke Manajer Toko via browser"),
            ("5", "Alert System", "Jika reorder_qty > 0, email/WhatsApp otomatis ke Tim Procurement"),
        ]
        st.markdown('<div class="section-header" style="margin-top:16px;">⚙️ Alur Deployment (End-to-End)</div>', unsafe_allow_html=True)
        for num, title, desc in deploy_steps:
            st.markdown(f"""
            <div class="deploy-step">
                <div class="deploy-num">{num}</div>
                <div class="deploy-content">
                    <div class="deploy-title">{title}</div>
                    <div class="deploy-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">🔄 Change Management</div>', unsafe_allow_html=True)
        change_items = [
            ("📋 Versioning", "Setiap perubahan model diberi versi semantik (v1.0.0) di Git & model registry"),
            ("🧪 Staging Environment", "Perubahan diuji di environment staging sebelum merge ke production"),
            ("✅ Sign-off Protocol", "Setiap update model memerlukan persetujuan DS + PM sebelum deploy"),
            ("📢 User Communication", "Changelog dikirim ke Manajer Toko setiap kali ada update sistem"),
            ("↩️ Rollback Plan", "Versi model sebelumnya selalu tersimpan — rollback < 15 menit jika error"),
        ]
        for icon_title, desc in change_items:
            st.markdown(f"""
            <div style="display:flex;gap:10px;padding:8px 0;border-bottom:0.5px solid #15151f;align-items:flex-start;">
                <div style="min-width:120px;font-size:12px;font-weight:600;color:#94a3b8;">{icon_title}</div>
                <div style="font-size:12px;color:#64748b;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    with col5b:
        st.markdown('<div class="section-header">📡 Model Monitoring (Post-Deployment)</div>', unsafe_allow_html=True)

        monitoring_kpis = [
            ("R² Score", "99.41%", "#22c55e", "LULUS"),
            ("sMAPE", "14.32%", "#22c55e", "Di bawah 15%"),
            ("MAE", "7.16 unit", "#f59e0b", "Acceptable"),
            ("Model Version", "v1.0.0", "#3b82f6", "Production"),
        ]
        cols_m = st.columns(2)
        for i, (label, val, color, status) in enumerate(monitoring_kpis):
            with cols_m[i % 2]:
                st.markdown(f"""
                <div class="kpi-box" style="border-left-color:{color};">
                    <div class="kpi-title">{label}</div>
                    <div class="kpi-value" style="font-size:22px;color:{color};">{val}</div>
                    <div class="kpi-sub">{status}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("**📊 Metrik yang Dipantau Post-Deployment**")
        monitor_data = {
            'Metrik': ['MAPE', 'MAE', 'Prediction Drift', 'Data Freshness', 'API Latency', 'Reorder Accuracy'],
            'Threshold': ['< 15%', '< 10 unit', '< 5%/minggu', '< 24 jam', '< 500ms', '> 80%'],
            'Frekuensi': ['Harian', 'Harian', 'Mingguan', 'Real-time', 'Real-time', 'Mingguan'],
            'Action': ['Retrain jika > 20%', 'Alert DS', 'Investigasi fitur', 'Alert DE', 'Scale API', 'Review model'],
        }
        st.dataframe(pd.DataFrame(monitor_data), use_container_width=True, hide_index=True, height=240)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("**📈 Simulasi Tren Performa Model (Post-Deploy)**")
        weeks = list(range(1, 13))
        mape_trend = [14.32, 14.1, 13.9, 14.5, 14.8, 15.2, 14.6, 14.1, 13.8, 14.0, 13.5, 13.7]
        threshold_line = [15.0] * 12

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=weeks, y=mape_trend, name='MAPE Aktual',
                                       line=dict(color='#3b82f6', width=2.5),
                                       marker=dict(size=7),
                                       fill='tozeroy', fillcolor='rgba(59,130,246,0.06)'))
        fig_trend.add_trace(go.Scatter(x=weeks, y=threshold_line, name='Batas MAPE (15%)',
                                       line=dict(color='#ef4444', width=1.5, dash='dot')))
        fig_trend.add_annotation(x=6, y=15.2, text="⚠️ Near Threshold",
                                  showarrow=True, arrowhead=2, arrowcolor='#f59e0b',
                                  font=dict(size=10, color='#fbbf24'))
        fig_trend.update_layout(
            template='plotly_dark',
            height=250, margin=dict(l=0, r=0, t=10, b=10),
            hovermode="x unified",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,17,24,0.8)',
            legend=dict(orientation='h', y=-0.2), font=dict(family='DM Sans', color='#94a3b8')
        )
        fig_trend.update_xaxes(title='Minggu ke-', showgrid=True, gridcolor='#1e1e2e',
                                tickvals=weeks, ticktext=[f'W{w}' for w in weeks], color='#64748b')
        fig_trend.update_yaxes(title='MAPE (%)', showgrid=True, gridcolor='#1e1e2e', color='#64748b')
        st.plotly_chart(fig_trend, use_container_width=True)

        st.markdown("""
        <div class="info-box" style="margin-top:8px;">
        <strong>Catatan:</strong> Pada Minggu ke-6, MAPE mendekati threshold 15% —
        sistem secara otomatis memicu <em>retraining pipeline</em> menggunakan
        data 3 bulan terakhir. Hasilnya performa kembali stabil di bawah 14.5%.
        </div>
        """, unsafe_allow_html=True)