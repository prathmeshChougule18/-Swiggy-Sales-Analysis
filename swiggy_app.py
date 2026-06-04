import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════ SWIGGY LOGO (base64 embedded) ═══════════════════
SWIGGY_LOGO_B64 = "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"
SWIGGY_LOGO_IMG = f'<img src="data:image/webp;base64,{SWIGGY_LOGO_B64}' + '" style="height:36px;object-fit:contain;">'
SWIGGY_LOGO_SIDEBAR = f'<img src="data:image/webp;base64,{SWIGGY_LOGO_B64}' + '" style="height:44px;object-fit:contain;">'

st.set_page_config(page_title="Swiggy Sales Dashboard", page_icon="🍊", layout="wide")

# ═══════════════════ CSS - EXACT SWIGGY DARK NAVY THEME ═══════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif !important; }

/* Dark navy background */
.stApp { background-color: #0a1929 !important; }
.main .block-container { padding: 1rem 1.5rem !important; max-width: 100% !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111f 0%, #0a1929 100%) !important;
    border-right: 1px solid #1e3a5f !important; width: 220px !important;
}
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
section[data-testid="stSidebar"] .stRadio label { padding: 8px 12px !important; border-radius: 8px !important; display: block !important; }

/* Header */
.swiggy-topbar {
    background: #07111f;
    border-bottom: 1px solid #1e3a5f;
    padding: 12px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: -1rem -1.5rem 1rem -1.5rem;
    border-radius: 0;
}
.swiggy-brand { display: flex; align-items: center; gap: 12px; }
.swiggy-logo-circle {
    width: 40px; height: 40px; border-radius: 50%;
    background: #fc8019; display: flex; align-items: center;
    justify-content: center; font-size: 20px;
}
.swiggy-title-text { font-size: 22px; font-weight: 900; }
.swiggy-title-text span:first-child { color: white; }
.swiggy-title-text span:last-child { color: #fc8019; margin-left: 6px; }
.swiggy-date { color: #94a3b8; font-size: 13px; font-weight: 600; }

/* KPI Cards */
.kpi-wrap {
    background: linear-gradient(135deg, #0d2137, #0f2840);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 16px;
    display: flex; align-items: center; gap: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.kpi-icon-circle {
    width: 48px; height: 48px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
}
.kpi-info { flex: 1; }
.kpi-label { color: #64748b; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.kpi-value { color: white; font-size: 22px; font-weight: 900; margin: 2px 0; }
.kpi-delta { font-size: 11px; font-weight: 700; }
.kpi-delta.up { color: #22c55e; }
.kpi-delta.down { color: #ef4444; }

/* Chart Cards */
.chart-card {
    background: #0d2137;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}
.chart-title {
    color: #e2e8f0; font-size: 13px; font-weight: 700;
    margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px;
}

/* Quarterly table */
.q-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.q-table th { color: #64748b; font-weight: 700; padding: 8px 6px; border-bottom: 1px solid #1e3a5f; text-align: left; }
.q-table td { color: #e2e8f0; padding: 8px 6px; border-bottom: 1px solid #1e3a5f; }
.q-badge { background: #1a3a1a; color: #22c55e; padding: 2px 8px; border-radius: 4px; font-weight: 700; }
.q-dash { color: #475569; }

/* City bar */
.city-row { margin: 6px 0; }
.city-name { color: #94a3b8; font-size: 12px; margin-bottom: 3px; display: flex; justify-content: space-between; }
.city-bar-bg { background: #1e3a5f; border-radius: 4px; height: 8px; }
.city-bar-fill { background: linear-gradient(90deg, #fc8019, #ff9f52); border-radius: 4px; height: 8px; }

/* Delivery guy card */
.delivery-card {
    background: linear-gradient(135deg, #0d2137, #1a3a5f);
    border: 1px solid #fc8019;
    border-radius: 12px; padding: 16px; text-align: center;
    margin: 12px 0;
}
.delivery-tagline { color: white; font-weight: 800; font-size: 13px; line-height: 1.4; }
.delivery-sub { color: #fc8019; font-size: 11px; margin-top: 4px; }

/* Data source footer */
.ds-info { color: #475569; font-size: 11px; margin-top: 8px; padding: 8px 0; border-top: 1px solid #1e3a5f; }

/* Filters */
.filter-card {
    background: #0d2137; border: 1px solid #1e3a5f;
    border-radius: 12px; padding: 14px; margin-bottom: 10px;
}
.filter-title { color: #fc8019; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }

#MainMenu {visibility:hidden;} footer {visibility:hidden;}
.stSelectbox > div > div { background: #0d2137 !important; border-color: #1e3a5f !important; color: white !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════ DATA LOADING ═══════════════════
@st.cache_data
def load_data():
    for p in ['swiggy_data.csv', 'data/swiggy_data.csv']:
        try: df = pd.read_csv(p); break
        except: continue
    else:
        st.error("❌ swiggy_data.csv not found!"); st.stop()

    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=False, errors='coerce')
    df['YearMonth']  = df['Order Date'].dt.to_period('M').astype(str)
    df['DayName']    = df['Order Date'].dt.day_name()
    df['Quarter']    = df['Order Date'].dt.to_period('Q').astype(str)
    df['Week']       = 'W' + df['Order Date'].dt.isocalendar().week.astype(str).str.zfill(2)
    df['Month_n']    = df['Order Date'].dt.month

    kw = ["chicken","egg","fish","mutton","prawns","biryani","kabab","kebab","non-veg","non veg"]
    df['Food Category'] = np.where(df['Dish Name'].str.lower().str.contains('|'.join(kw),na=False),'Non-Veg','Veg')
    return df

@st.cache_data
def get_india_geojson():
    try:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        return requests.get(url, timeout=10).json()
    except: return None

def fmt_inr(v):
    if v>=1e7:  return f"₹{v/1e7:.2f}Cr"
    if v>=1e5:  return f"₹{v/1e5:.1f}L"
    if v>=1000: return f"₹{v/1000:.1f}K"
    return f"₹{v:.0f}"

def fmt_M(v):
    if v>=1e6: return f"₹{v/1e6:.2f}M"
    return fmt_inr(v)

def delta_pct(curr, prev):
    if prev==0: return 0
    return (curr - prev) / prev * 100

LAYOUT = dict(paper_bgcolor='#0d2137', plot_bgcolor='#0d2137',
              font=dict(color='#94a3b8', family='Nunito', size=11),
              margin=dict(t=10,b=10,l=10,r=10),
              xaxis=dict(gridcolor='#1e3a5f', linecolor='#1e3a5f', showgrid=True),
              yaxis=dict(gridcolor='#1e3a5f', linecolor='#1e3a5f', showgrid=True))

df = load_data()
india_geojson = get_india_geojson()

state_name_map = {'Jammu and Kashmir': 'Jammu & Kashmir', 'Delhi': 'Delhi'}

# ═══════════════════ SIDEBAR ═══════════════════
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 12px 0 8px;'>
        {SWIGGY_LOGO_SIDEBAR}
        <div style='color:#64748b; font-size:10px; letter-spacing:2px; margin-top:6px;'>ANALYTICS DASHBOARD</div>
    </div>
    <hr style='border-color:#1e3a5f; margin: 8px 0;'>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "🏠 Overview", "📈 Sales Trends", "📊 KPI's",
        "🏪 Restaurants", "📦 Orders", "⭐ Ratings", "🗺️ Locations"
    ], label_visibility="collapsed")

    st.markdown("""
    <hr style='border-color:#1e3a5f; margin: 12px 0 8px;'>
    <div class='delivery-card'>
        <div style='font-size:40px;'>🛵</div>
        <div class='delivery-tagline'>Delicious food,<br>delivered fast!</div>
        <div class='delivery-sub'>🍕 🍔 🍜 🍣</div>
    </div>
    <div class='ds-info'>
        📊 Data Source: Swiggy<br>
        🕐 Last Updated: Aug 2025
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════ FILTERS (top bar) ═══════════════════
states  = ['All'] + sorted(df['State'].dropna().unique())
cities  = ['All'] + sorted(df['City'].dropna().unique())
months  = ['All'] + sorted(df['YearMonth'].dropna().unique())

fc1, fc2, fc3, fc4 = st.columns([2,2,2,2])
with fc1: sel_month = st.selectbox("📅 Month", months, key='m')
with fc2: sel_state = st.selectbox("🗺️ State", states, key='s')
with fc3: sel_city  = st.selectbox("🏙️ City", cities, key='c')
with fc4: sel_food  = st.selectbox("🍽️ Food Type", ["All","Veg","Non-Veg"], key='f')

# Apply filters
fdf = df.copy()
if sel_month != 'All': fdf = fdf[fdf['YearMonth']==sel_month]
if sel_state != 'All': fdf = fdf[fdf['State']==sel_state]
if sel_city  != 'All': fdf = fdf[fdf['City']==sel_city]
if sel_food  != 'All': fdf = fdf[fdf['Food Category']==sel_food]

# KPI deltas (vs previous period)
monthly_sales = df.groupby('YearMonth')['Price (INR)'].sum().sort_index()
if len(monthly_sales) >= 2:
    curr_s, prev_s = monthly_sales.iloc[-1], monthly_sales.iloc[-2]
else:
    curr_s = prev_s = monthly_sales.iloc[-1] if len(monthly_sales) else 1

monthly_stats = df.groupby('YearMonth').agg(
    Rating=('Rating','mean'), AvgOrder=('Price (INR)','mean'),
    RatingCount=('Rating Count','sum'), Orders=('Price (INR)','count')).sort_index()

d_rating = delta_pct(monthly_stats['Rating'].iloc[-1], monthly_stats['Rating'].iloc[-2]) if len(monthly_stats)>=2 else 0
d_avg    = delta_pct(monthly_stats['AvgOrder'].iloc[-1], monthly_stats['AvgOrder'].iloc[-2]) if len(monthly_stats)>=2 else 0
d_rc     = delta_pct(monthly_stats['RatingCount'].iloc[-1], monthly_stats['RatingCount'].iloc[-2]) if len(monthly_stats)>=2 else 0
d_ord    = delta_pct(monthly_stats['Orders'].iloc[-1], monthly_stats['Orders'].iloc[-2]) if len(monthly_stats)>=2 else 0
d_sales  = delta_pct(curr_s, prev_s)
prev_m   = monthly_stats.index[-2] if len(monthly_stats)>=2 else "Prev"


# ═══════════════════ OVERVIEW PAGE ═══════════════════
if page == "🏠 Overview":

    # Top Bar
    date_label = f"{fdf['Order Date'].min().strftime('%d %b %Y')} – {fdf['Order Date'].max().strftime('%d %b %Y')}" if not fdf.empty else ""
    st.markdown(f"""
    <div class="swiggy-topbar">
        <div class="swiggy-brand">
            {SWIGGY_LOGO_IMG}
            <div class="swiggy-title-text"><span style='color:#94a3b8;font-size:14px;font-weight:600;letter-spacing:2px;'>SALES DASHBOARD</span></div>
        </div>
        <div class="swiggy-date">📅 {date_label}</div>
    </div>""", unsafe_allow_html=True)

    # ── KPI CARDS ──
    k1,k2,k3,k4,k5 = st.columns(5)
    total_sales = fdf['Price (INR)'].sum()
    avg_rating  = fdf['Rating'].mean()
    avg_order   = fdf['Price (INR)'].mean()
    total_rc    = fdf['Rating Count'].sum()
    total_orders= len(fdf)

    kpis = [
        (k1, "₹", "#fc8019", "#3d1a00", "Total Sales (₹)", fmt_M(total_sales), d_sales, prev_m),
        (k2, "⭐", "#f59e0b", "#3d2e00", "Average Rating",  f"{avg_rating:.2f}", d_rating, prev_m),
        (k3, "🛍️", "#3b82f6", "#0a1f3d", "Avg Order Value", fmt_inr(avg_order), d_avg, prev_m),
        (k4, "👥", "#8b5cf6", "#1e0a3d", "Ratings Count",  f"{total_rc/1000:.1f}K", d_rc, prev_m),
        (k5, "📋", "#10b981", "#0a2d1f", "Total Orders",   f"{total_orders/1000:.1f}K", d_ord, prev_m),
    ]
    for col, icon, color, bg, label, val, delta, pm in kpis:
        with col:
            d_class = "up" if delta >= 0 else "down"
            d_arrow = "▲" if delta >= 0 else "▼"
            st.markdown(f"""
            <div class="kpi-wrap">
                <div class="kpi-icon-circle" style="background:{bg}; color:{color};">{icon}</div>
                <div class="kpi-info">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{val}</div>
                    <div class="kpi-delta {d_class}">{d_arrow} {abs(delta):.1f}% &nbsp;<span style="color:#475569;font-weight:400;">vs {pm}</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:12px 0'></div>", unsafe_allow_html=True)

    # ── ROW 1: Monthly | Daily | Donut | India Map ──
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)

    with r1c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Monthly Sales Trend</div>', unsafe_allow_html=True)
        mon = fdf.groupby('YearMonth')['Price (INR)'].sum().reset_index().sort_values('YearMonth')
        mon['Label'] = mon['YearMonth'].str[-2:].map({'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'})
        fig = go.Figure(go.Scatter(x=mon['Label'], y=mon['Price (INR)'],
            mode='lines+markers', line=dict(color='#fc8019',width=2.5),
            marker=dict(color='#fc8019',size=7,line=dict(color='white',width=1.5)),
            fill='tozeroy', fillcolor='rgba(252,128,25,0.08)'))
        fig.update_layout(**LAYOUT, height=200)
        fig.update_yaxes(tickprefix='₹', tickformat='.1s')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    with r1c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Daily Sales Trend</div>', unsafe_allow_html=True)
        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        day_labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        daily = fdf.groupby('DayName')['Price (INR)'].sum().reindex(day_order).reset_index()
        fig2 = go.Figure(go.Scatter(x=day_labels, y=daily['Price (INR)'],
            mode='lines+markers', line=dict(color='#fc8019',width=2.5),
            marker=dict(color='#fc8019',size=7,line=dict(color='white',width=1.5)),
            fill='tozeroy', fillcolor='rgba(252,128,25,0.08)'))
        fig2.update_layout(**LAYOUT, height=200)
        fig2.update_yaxes(tickprefix='₹', tickformat='.1s')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    with r1c3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Total Sales by Food Type</div>', unsafe_allow_html=True)
        frev = fdf.groupby('Food Category')['Price (INR)'].sum().reset_index()
        total_for_donut = frev['Price (INR)'].sum()
        fig3 = go.Figure(go.Pie(
            values=frev['Price (INR)'], labels=frev['Food Category'],
            hole=0.62, marker_colors=['#fc8019','#22c55e'],
            textinfo='percent', textfont=dict(size=12),
            pull=[0.03,0]))
        fig3.update_layout(**LAYOUT, height=200,
            annotations=[dict(text=f"<b>{fmt_M(total_for_donut)}</b><br><span style='font-size:9px'>Total Sales</span>",
                x=0.5, y=0.5, showarrow=False, font=dict(size=12,color='white'))],
            legend=dict(orientation='h', y=-0.1, x=0.5, xanchor='center',
                        font=dict(color='#94a3b8',size=11), bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    with r1c4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Total Sales by State</div>', unsafe_allow_html=True)
        state_rev = fdf.groupby('State')['Price (INR)'].sum().reset_index()
        state_rev['State_GJ'] = state_rev['State'].replace(state_name_map)
        if india_geojson:
            fig4 = px.choropleth(state_rev, geojson=india_geojson,
                featureidkey='properties.ST_NM', locations='State_GJ',
                color='Price (INR)', color_continuous_scale=['#0d2137','#fc8019','#ffd4a8'],
                projection='mercator')
            fig4.update_geos(fitbounds='locations', visible=False)
            fig4.update_layout(paper_bgcolor='#0d2137', geo_bgcolor='#0d2137',
                height=200, margin=dict(t=0,b=0,l=0,r=0),
                coloraxis_showscale=False)
        else:
            top_s = state_rev.nlargest(6,'Price (INR)')
            fig4 = px.bar(top_s, x='Price (INR)', y='State', orientation='h',
                color_discrete_sequence=['#fc8019'])
            fig4.update_layout(**LAYOUT, height=200)
        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 2: Food Bar | India Map | Quarterly | Top 5 Cities ──
    r2c1, r2c2, r2c3, r2c4 = st.columns(4)

    with r2c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Sales by Food Type (Veg vs Non-Veg)</div>', unsafe_allow_html=True)
        fbar = fdf.groupby('Food Category')['Price (INR)'].sum().reset_index()
        fig5 = go.Figure()
        colors = {'Veg':'#22c55e', 'Non-Veg':'#fc8019'}
        for _, row in fbar.iterrows():
            fig5.add_bar(x=[row['Food Category']], y=[row['Price (INR)']],
                name=row['Food Category'], marker_color=colors.get(row['Food Category'],'#fc8019'),
                text=[fmt_M(row['Price (INR)'])], textposition='outside',
                textfont=dict(color='white',size=11,family='Nunito'))
        fig5.update_layout(**LAYOUT, height=220, showlegend=False, bargap=0.4)
        fig5.update_yaxes(tickprefix='₹', tickformat='.1s')
        st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    with r2c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">State Revenue Map</div>', unsafe_allow_html=True)
        if india_geojson:
            fig6 = px.choropleth(state_rev, geojson=india_geojson,
                featureidkey='properties.ST_NM', locations='State_GJ',
                color='Price (INR)', color_continuous_scale=['#0a1929','#fc4500','#ff9f52'],
                projection='mercator', hover_data={'State_GJ':True,'Price (INR)':True})
            fig6.update_geos(fitbounds='locations', visible=False)
            fig6.update_layout(paper_bgcolor='#0d2137', geo_bgcolor='#0d2137',
                height=220, margin=dict(t=0,b=0,l=0,r=0), coloraxis_showscale=False)
        else:
            fig6 = px.bar(state_rev.nlargest(8,'Price (INR)').sort_values('Price (INR)'),
                x='Price (INR)', y='State', orientation='h', color_discrete_sequence=['#fc8019'])
            fig6.update_layout(**LAYOUT, height=220)
        st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    with r2c3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Quarterly Performance Summary</div>', unsafe_allow_html=True)
        qdf = fdf.groupby('Quarter').agg(
            Sales=('Price (INR)','sum'), Rating=('Rating','mean'),
            Orders=('Price (INR)','count')).reset_index().sort_values('Quarter')

        rows = ""
        for _, r in qdf.iterrows():
            q_label = r['Quarter'].replace('2025Q','Q').replace('2024Q','Q')
            rows += f"""<tr>
                <td>{q_label}</td>
                <td><span class='q-badge'>{fmt_M(r['Sales'])}</span></td>
                <td>{r['Rating']:.1f}</td>
                <td>{r['Orders']/1000:.1f}K</td>
            </tr>"""
        if qdf.empty:
            rows = "<tr><td colspan='4' style='color:#475569;text-align:center'>No data</td></tr>"

        st.markdown(f"""
        <table class='q-table'>
            <thead><tr>
                <th>Quarter</th><th>Sales (₹)</th><th>Rating</th><th>Orders</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2c4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top 5 Cities by Sales</div>', unsafe_allow_html=True)
        top5 = fdf.groupby('City')['Price (INR)'].sum().nlargest(5).sort_values(ascending=False).reset_index()
        max_val = top5['Price (INR)'].max()
        html = ""
        for _, r in top5.iterrows():
            pct = int(r['Price (INR)'] / max_val * 100)
            html += f"""
            <div class="city-row">
                <div class="city-name"><span>{r['City']}</span><span style='color:#fc8019;font-weight:700;'>{fmt_inr(r['Price (INR)'])}</span></div>
                <div class="city-bar-bg"><div class="city-bar-fill" style="width:{pct}%;"></div></div>
            </div>"""
        st.markdown(html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 3: Weekly Trend ──
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Weekly Trend Analysis (Sales + Orders)</div>', unsafe_allow_html=True)
    weekly = fdf.groupby('Week').agg(Sales=('Price (INR)','sum'), Orders=('Price (INR)','count')).reset_index().sort_values('Week').head(20)
    fig7 = go.Figure()
    fig7.add_bar(x=weekly['Week'], y=weekly['Sales'], name='Sales (₹)',
        marker_color='#fc8019', opacity=0.85, yaxis='y')
    fig7.add_scatter(x=weekly['Week'], y=weekly['Orders'], name='Orders',
        mode='lines+markers', line=dict(color='#ffd4a8',width=2,dash='dot'),
        marker=dict(color='#ffd4a8',size=7,symbol='circle'),
        yaxis='y2')
    fig7.update_layout(**LAYOUT, height=220,
        legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', y=1.1, x=0.5, xanchor='center',
                    font=dict(color='#94a3b8')),
        bargap=0.2)
    fig7.update_layout(
        yaxis=dict(gridcolor='#1e3a5f',linecolor='#1e3a5f',tickprefix='₹',tickformat='.1s'),
        yaxis2=dict(overlaying='y', side='right', showgrid=False, tickformat='.1s',
                    title=dict(text='Orders', font=dict(color='#ffd4a8')),
                    tickfont=dict(color='#ffd4a8')))
    st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════ SALES TRENDS PAGE ═══════════════════
elif page == "📈 Sales Trends":
    st.markdown("<h2 style='color:#fc8019;'>📈 Sales Trends</h2>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card"><div class="chart-title">Monthly Revenue</div>', unsafe_allow_html=True)
        mon = fdf.groupby('YearMonth')['Price (INR)'].sum().reset_index().sort_values('YearMonth')
        fig = px.area(mon, x='YearMonth', y='Price (INR)', color_discrete_sequence=['#fc8019'])
        fig.update_traces(fillcolor='rgba(252,128,25,0.1)', line_color='#fc8019')
        fig.update_layout(**LAYOUT, height=250); fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card"><div class="chart-title">Daily Revenue (Mon–Sun)</div>', unsafe_allow_html=True)
        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        daily = fdf.groupby('DayName')['Price (INR)'].sum().reindex(day_order).reset_index()
        fig2 = px.bar(daily, x='DayName', y='Price (INR)', color_discrete_sequence=['#fc8019'])
        fig2.update_layout(**LAYOUT, height=250)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card"><div class="chart-title">Top 10 Categories by Revenue</div>', unsafe_allow_html=True)
    cat = fdf.groupby('Category')['Price (INR)'].sum().nlargest(10).sort_values().reset_index()
    fig3 = px.bar(cat, x='Price (INR)', y='Category', orientation='h',
                  color='Price (INR)', color_continuous_scale=['#0d2137','#fc8019'])
    fig3.update_layout(**LAYOUT, height=300, coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════ KPI's PAGE ═══════════════════
elif page == "📊 KPI's":
    st.markdown("""
    <div style='margin-bottom:16px;'>
        <span style='color:#fc8019;font-size:22px;font-weight:900;letter-spacing:1px;'>📊 KPI SUMMARY</span>
        <span style='color:#475569;font-size:12px;margin-left:12px;'>Performance at a glance</span>
    </div>""", unsafe_allow_html=True)

    total_sales  = fdf['Price (INR)'].sum()
    avg_rating   = fdf['Rating'].mean()
    avg_order    = fdf['Price (INR)'].mean()
    total_orders = len(fdf)
    total_rc     = fdf['Rating Count'].sum()
    unique_rest  = fdf['Restaurant Name'].nunique()

    kpi_data = [
        ("💰", "#fc8019", "#3d1a00", "Total Revenue",      fmt_M(total_sales),         f"₹{total_sales/1e7:.2f} Crore total",     d_sales),
        ("⭐", "#f59e0b", "#3d2e00", "Average Rating",     f"{avg_rating:.2f} / 5.0",  "Customer satisfaction score",              d_rating),
        ("🛍️", "#3b82f6", "#0a1f3d", "Avg Order Value",   fmt_inr(avg_order),          "Per transaction average",                 d_avg),
        ("📋", "#10b981", "#0a2d1f", "Total Orders",       f"{total_orders:,}",         f"{total_orders/1000:.1f}K orders placed", d_ord),
        ("👥", "#8b5cf6", "#1e0a3d", "Total Rating Count", f"{total_rc/1e6:.2f}M",     "Cumulative ratings received",              d_rc),
        ("🏪", "#ec4899", "#3d0a24", "Unique Restaurants", f"{unique_rest:,}",          "Active restaurant partners",              0),
    ]

    c1, c2, c3 = st.columns(3)
    cols_cycle = [c1, c2, c3, c1, c2, c3]
    for i, (icon, color, bg, label, val, sub, delta) in enumerate(kpi_data):
        d_class = "up" if delta >= 0 else "down"
        d_arrow = "▲" if delta >= 0 else "▼"
        delta_html = f"<div class='kpi-delta {d_class}'>{d_arrow} {abs(delta):.1f}% vs prev month</div>" if delta != 0 else "<div style='color:#475569;font-size:11px;'>—</div>"
        with cols_cycle[i]:
            st.markdown(f"""
            <div class="kpi-wrap" style="margin-bottom:12px;position:relative;overflow:hidden;">
                <div style="position:absolute;right:-10px;top:-10px;font-size:60px;opacity:0.06;">{icon}</div>
                <div class="kpi-icon-circle" style="background:{bg};color:{color};font-size:24px;width:52px;height:52px;">{icon}</div>
                <div class="kpi-info">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value" style="font-size:26px;color:{color};">{val}</div>
                    <div style="color:#475569;font-size:10px;margin:2px 0 4px;">{sub}</div>
                    {delta_html}
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)

    qa, qb, qc = st.columns([2, 1, 1])

    with qa:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📅 Quarterly Revenue Breakdown</div>', unsafe_allow_html=True)
        qdf = fdf.groupby('Quarter').agg(Sales=('Price (INR)','sum'), Rating=('Rating','mean'), Orders=('Price (INR)','count')).reset_index().sort_values('Quarter')
        q_colors = ['#fc8019','#ff9f52','#ffc088','#ffd4a8']
        fig_q = go.Figure()
        for idx, (_, row) in enumerate(qdf.iterrows()):
            fig_q.add_bar(x=[row['Quarter']], y=[row['Sales']],
                marker_color=q_colors[idx % len(q_colors)],
                text=[fmt_M(row['Sales'])], textposition='outside',
                textfont=dict(color='white', size=12), name=row['Quarter'])
        fig_q.update_layout(**LAYOUT, height=280, showlegend=False, bargap=0.35)
        fig_q.update_yaxes(tickprefix='₹', tickformat='.1s')
        fig_q.update_xaxes(tickfont=dict(size=12, color='#94a3b8'))
        st.plotly_chart(fig_q, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    with qb:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">⭐ Rating Gauge</div>', unsafe_allow_html=True)
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_rating,
            delta={'reference': 4.0, 'increasing': {'color': '#22c55e'}, 'decreasing': {'color': '#ef4444'}},
            gauge={
                'axis': {'range': [0, 5], 'tickcolor': '#94a3b8', 'tickfont': {'color': '#94a3b8', 'size': 10}},
                'bar': {'color': '#fc8019', 'thickness': 0.25},
                'bgcolor': '#0d2137', 'bordercolor': '#1e3a5f',
                'steps': [
                    {'range': [0, 2.5], 'color': '#1a0a00'},
                    {'range': [2.5, 4.0], 'color': '#3d1a00'},
                    {'range': [4.0, 5.0], 'color': '#5a2e00'},
                ],
                'threshold': {'line': {'color': '#ffd4a8', 'width': 3}, 'thickness': 0.75, 'value': 4.5}
            },
            number={'font': {'color': 'white', 'size': 30, 'family': 'Nunito'}, 'suffix': '/5'}
        ))
        fig_g.update_layout(paper_bgcolor='#0d2137', plot_bgcolor='#0d2137',
            font=dict(color='#94a3b8', family='Nunito'), height=280,
            margin=dict(t=30, b=10, l=20, r=20))
        st.plotly_chart(fig_g, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    with qc:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🥗 Veg vs Non-Veg</div>', unsafe_allow_html=True)
        frev = fdf.groupby('Food Category')['Price (INR)'].sum().reset_index()
        fig_d = go.Figure(go.Pie(
            values=frev['Price (INR)'], labels=frev['Food Category'],
            hole=0.58, marker_colors=['#22c55e','#fc8019'],
            textinfo='label+percent', textfont=dict(size=11, color='white'), pull=[0.04, 0]))
        fig_d.update_layout(**LAYOUT, height=280,
            legend=dict(orientation='h', y=-0.1, x=0.5, xanchor='center',
                        font=dict(color='#94a3b8', size=10), bgcolor='rgba(0,0,0,0)'),
            annotations=[dict(text=f"<b>{fmt_M(frev['Price (INR)'].sum())}</b>",
                x=0.5, y=0.5, showarrow=False, font=dict(size=13, color='white'))])
        st.plotly_chart(fig_d, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    ra, rb = st.columns([3, 2])

    with ra:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Monthly Revenue Trend</div>', unsafe_allow_html=True)
        mon = fdf.groupby('YearMonth')['Price (INR)'].sum().reset_index().sort_values('YearMonth')
        fig_m = go.Figure(go.Scatter(x=mon['YearMonth'], y=mon['Price (INR)'],
            mode='lines+markers', line=dict(color='#fc8019', width=2.5),
            marker=dict(color='#fc8019', size=7, line=dict(color='white', width=1.5)),
            fill='tozeroy', fillcolor='rgba(252,128,25,0.1)',
            hovertemplate='%{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>'))
        fig_m.update_layout(**LAYOUT, height=220)
        fig_m.update_yaxes(tickprefix='₹', tickformat='.1s')
        fig_m.update_xaxes(tickangle=30, tickfont=dict(size=10))
        st.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)

    with rb:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🍽️ Top 5 Categories</div>', unsafe_allow_html=True)
        cat5 = fdf.groupby('Category')['Price (INR)'].sum().nlargest(5).sort_values().reset_index()
        max_c = cat5['Price (INR)'].max()
        html_c = ""
        for _, row in cat5.iterrows():
            pct = int(row['Price (INR)'] / max_c * 100)
            html_c += f"""
            <div style="margin:10px 0;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="color:#e2e8f0;font-size:12px;font-weight:600;">{row['Category']}</span>
                    <span style="color:#fc8019;font-size:12px;font-weight:700;">{fmt_M(row['Price (INR)'])}</span>
                </div>
                <div style="background:#1e3a5f;border-radius:6px;height:10px;">
                    <div style="width:{pct}%;background:linear-gradient(90deg,#fc8019,#ffd4a8);border-radius:6px;height:10px;"></div>
                </div>
            </div>"""
        st.markdown(html_c, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════ RESTAURANTS PAGE ═══════════════════
elif page == "🏪 Restaurants":
    st.markdown("<h2 style='color:#fc8019;'>🏪 Restaurant Analysis</h2>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card"><div class="chart-title">Top 10 Restaurants by Revenue</div>', unsafe_allow_html=True)
        rest = fdf.groupby('Restaurant Name')['Price (INR)'].sum().nlargest(10).sort_values().reset_index()
        fig = px.bar(rest, x='Price (INR)', y='Restaurant Name', orientation='h',
                     color_discrete_sequence=['#fc8019'])
        fig.update_layout(**LAYOUT, height=320)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card"><div class="chart-title">Top 10 Restaurants by Rating</div>', unsafe_allow_html=True)
        rest_r = fdf.groupby('Restaurant Name').agg(Rating=('Rating','mean'), Orders=('Rating','count')).query('Orders>10').nlargest(10,'Rating').sort_values('Rating').reset_index()
        fig2 = px.bar(rest_r, x='Rating', y='Restaurant Name', orientation='h', color_discrete_sequence=['#22c55e'])
        fig2.update_layout(**LAYOUT, height=320)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════ ORDERS PAGE ═══════════════════
elif page == "📦 Orders":
    st.markdown("<h2 style='color:#fc8019;'>📦 Orders Analysis</h2>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card"><div class="chart-title">Orders by Day</div>', unsafe_allow_html=True)
        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        daily_o = fdf.groupby('DayName').size().reindex(day_order).reset_index()
        daily_o.columns = ['Day','Orders']
        fig = px.bar(daily_o, x='Day', y='Orders', color_discrete_sequence=['#fc8019'])
        fig.update_layout(**LAYOUT, height=280)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card"><div class="chart-title">Price Distribution</div>', unsafe_allow_html=True)
        fig2 = px.histogram(fdf[fdf['Price (INR)']<1000], x='Price (INR)', nbins=40, color_discrete_sequence=['#fc8019'])
        fig2.update_layout(**LAYOUT, height=280)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════ RATINGS PAGE ═══════════════════
elif page == "⭐ Ratings":
    st.markdown("<h2 style='color:#fc8019;'>⭐ Ratings Analysis</h2>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card"><div class="chart-title">Rating Distribution</div>', unsafe_allow_html=True)
        fig = px.histogram(fdf, x='Rating', nbins=25, color_discrete_sequence=['#fc8019'])
        fig.add_vline(x=fdf['Rating'].mean(), line_color='white', line_dash='dash',
                      annotation_text=f"Avg: {fdf['Rating'].mean():.2f}", annotation_font_color='white')
        fig.update_layout(**LAYOUT, height=280)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card"><div class="chart-title">Rating by Food Category</div>', unsafe_allow_html=True)
        fig2 = px.box(fdf, x='Food Category', y='Rating',
                      color='Food Category', color_discrete_map={'Veg':'#22c55e','Non-Veg':'#fc8019'})
        fig2.update_layout(**LAYOUT, height=280, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════ LOCATIONS PAGE ═══════════════════
elif page == "🗺️ Locations":
    st.markdown("<h2 style='color:#fc8019;'>🗺️ Location Analysis</h2>", unsafe_allow_html=True)
    state_rev = fdf.groupby('State')['Price (INR)'].sum().reset_index()
    state_rev['State_GJ'] = state_rev['State'].replace(state_name_map)
    if india_geojson:
        st.markdown('<div class="chart-card"><div class="chart-title">India State Revenue Map</div>', unsafe_allow_html=True)
        fig = px.choropleth(state_rev, geojson=india_geojson, featureidkey='properties.ST_NM',
            locations='State_GJ', color='Price (INR)',
            color_continuous_scale=['#0a1929','#fc4500','#ffd4a8'], projection='mercator',
            hover_data={'State':True,'Price (INR)':True})
        fig.update_geos(fitbounds='locations', visible=False)
        fig.update_layout(paper_bgcolor='#0d2137', geo_bgcolor='#0d2137',
            height=400, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card"><div class="chart-title">Revenue by State</div>', unsafe_allow_html=True)
        fig2 = px.bar(state_rev.sort_values('Price (INR)',ascending=True), x='Price (INR)', y='State',
                      orientation='h', color='Price (INR)', color_continuous_scale=['#0d2137','#fc8019'])
        fig2.update_layout(**LAYOUT, height=500, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="chart-card"><div class="chart-title">Top 10 Cities</div>', unsafe_allow_html=True)
        city_r = fdf.groupby('City')['Price (INR)'].sum().nlargest(10).sort_values().reset_index()
        fig3 = px.bar(city_r, x='Price (INR)', y='City', orientation='h', color_discrete_sequence=['#fc8019'])
        fig3.update_layout(**LAYOUT, height=500)
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar':False})
        st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ──
st.markdown("""
<div style='text-align:center;padding:20px 0;margin-top:20px;border-top:1px solid #1e3a5f;'>
    <span style='font-size:22px;'>🍊</span>
    <span style='color:#94a3b8;font-size:12px;margin:0 12px;'>
        © 2026 <strong style='color:white;'>Prathamesh Chougule</strong> · All Rights Reserved
    </span>
    <span style='font-size:22px;'>🍊</span>
    <br><span style='color:#475569;font-size:10px;'>Built with ❤️ using Python & Streamlit</span>
</div>""", unsafe_allow_html=True)
