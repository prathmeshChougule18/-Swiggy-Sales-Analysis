import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import warnings
warnings.filterwarnings('ignore')

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
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 8px;'>
        <div style='font-size:32px;'>🍊</div>
        <div style='color:#fc8019; font-size:18px; font-weight:900;'>SWIGGY</div>
        <div style='color:#64748b; font-size:10px; letter-spacing:2px;'>ANALYTICS</div>
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
            <div class="swiggy-logo-circle">🍊</div>
            <div class="swiggy-title-text"><span>SWIGGY</span><span>SALES DASHBOARD</span></div>
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
    fig7.update_layout(
        paper_bgcolor='#0d2137', plot_bgcolor='#0d2137',
        font=dict(color='#94a3b8', family='Nunito', size=11),
        margin=dict(t=10,b=10,l=10,r=10),
        height=220,
        xaxis=dict(gridcolor='#1e3a5f', linecolor='#1e3a5f'),
        yaxis=dict(gridcolor='#1e3a5f', linecolor='#1e3a5f', tickprefix='₹', tickformat='.1s'),
        yaxis2=dict(overlaying='y', side='right', showgrid=False, tickformat='.1s',
                    title='Orders', titlefont=dict(color='#ffd4a8'), tickfont=dict(color='#ffd4a8')),
        legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', y=1.1, x=0.5, xanchor='center',
                    font=dict(color='#94a3b8')),
        bargap=0.2)
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
    st.markdown("<h2 style='color:#fc8019;'>📊 KPI Summary</h2>", unsafe_allow_html=True)
    k1,k2,k3 = st.columns(3)
    with k1: st.metric("Total Sales", fmt_M(fdf['Price (INR)'].sum()))
    with k2: st.metric("Avg Rating", f"{fdf['Rating'].mean():.2f}")
    with k3: st.metric("Avg Order Value", fmt_inr(fdf['Price (INR)'].mean()))
    k4,k5,k6 = st.columns(3)
    with k4: st.metric("Total Orders", f"{len(fdf):,}")
    with k5: st.metric("Total Rating Count", f"{fdf['Rating Count'].sum():,}")
    with k6: st.metric("Unique Restaurants", f"{fdf['Restaurant Name'].nunique():,}")
    st.markdown('<div class="chart-card"><div class="chart-title">Quarterly Performance</div>', unsafe_allow_html=True)
    qdf = fdf.groupby('Quarter').agg(Sales=('Price (INR)','sum'), Rating=('Rating','mean'), Orders=('Price (INR)','count')).reset_index()
    fig = px.bar(qdf, x='Quarter', y='Sales', color_discrete_sequence=['#fc8019'],
                 text=qdf['Sales'].apply(fmt_M))
    fig.update_layout(**LAYOUT, height=250)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
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
