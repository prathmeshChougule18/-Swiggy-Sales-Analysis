import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Swiggy Sales Dashboard",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# SWIGGY THEME CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Background */
    .stApp { background-color: #1a0a00; }
    section[data-testid="stSidebar"] { background-color: #120700 !important; border-right: 1px solid #ff6b00; }

    /* Sidebar text */
    section[data-testid="stSidebar"] * { color: #ffd4a8 !important; }

    /* KPI Card */
    .kpi-card {
        background: linear-gradient(145deg, #2d1200, #3d1a00);
        border: 1px solid #ff6b00;
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(255,107,0,0.15);
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(255,107,0,0.3); }
    .kpi-label { color: #ff9f52; font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
    .kpi-value { color: #ffffff; font-size: 28px; font-weight: 800; margin: 8px 0 4px 0; }
    .kpi-sub { color: #ffa06a; font-size: 12px; }

    /* Section Header */
    .sec-header {
        color: #ff6b00;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #ff6b00;
        padding-bottom: 6px;
        margin: 24px 0 14px 0;
    }

    /* Swiggy Logo Style Header */
    .swiggy-header {
        background: linear-gradient(135deg, #fc8019, #ff4500);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .swiggy-title { color: white; font-size: 32px; font-weight: 800; margin: 0; }
    .swiggy-sub { color: rgba(255,255,255,0.85); font-size: 14px; margin-top: 4px; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { background: #2d1200; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { color: #ffa06a !important; border-radius: 8px; }
    .stTabs [aria-selected="true"] { background: #fc8019 !important; color: white !important; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Plotly dark template matching Swiggy theme
SWIGGY_LAYOUT = dict(
    paper_bgcolor='#2d1200',
    plot_bgcolor='#2d1200',
    font=dict(color='#ffd4a8', family='Inter'),
    xaxis=dict(gridcolor='#4a2000', linecolor='#4a2000'),
    yaxis=dict(gridcolor='#4a2000', linecolor='#4a2000'),
    margin=dict(t=40, b=40, l=10, r=10)
)

ORANGE_PALETTE = ['#fc8019', '#ff6b00', '#ffaa5c', '#ff4500', '#ffd4a8', '#ff8c42', '#e65c00', '#ffbe7d']

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    for path in ['swiggy_data.csv', 'data/swiggy_data.csv']:
        try:
            df = pd.read_csv(path)
            break
        except:
            continue
    else:
        st.error("❌ swiggy_data.csv not found!")
        st.stop()

    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=False, errors='coerce')
    df['YearMonth']  = df['Order Date'].dt.to_period('M').astype(str)
    df['DayName']    = df['Order Date'].dt.day_name()
    df['Quarter']    = df['Order Date'].dt.to_period('Q').astype(str)
    df['Month']      = df['Order Date'].dt.strftime('%b %Y')

    non_veg_kw = ["chicken","egg","fish","mutton","prawns","biryani","kabab","kebab","non-veg","non veg"]
    df['Food Category'] = np.where(
        df['Dish Name'].str.lower().str.contains('|'.join(non_veg_kw), na=False),
        'Non-Veg', 'Veg')
    return df

df = load_data()

def fmt_inr(v):
    if v >= 1e7:   return f"₹{v/1e7:.2f}Cr"
    if v >= 1e5:   return f"₹{v/1e5:.1f}L"
    if v >= 1000:  return f"₹{v/1000:.1f}K"
    return f"₹{v:.0f}"

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🍊 Swiggy Dashboard")
    st.markdown("---")
    st.markdown("**🔍 Filters**")

    states   = sorted(df['State'].dropna().unique())
    sel_st   = st.multiselect("State", states, placeholder="All States")

    cities   = sorted(df['City'].dropna().unique())
    sel_ct   = st.multiselect("City", cities, placeholder="All Cities")

    food_f   = st.radio("Food Type", ["All 🍽️", "Veg 🥦", "Non-Veg 🍗"])
    rating_f = st.slider("Min Rating", 0.0, 5.0, 0.0, 0.1)

    st.markdown("---")
    st.markdown("**📌 Pages**")
    page = st.radio("", ["🏠 Overview", "📈 Sales Trends", "🗺️ Locations", "🍽️ Food & Dishes"],
                    label_visibility="collapsed")

# ─────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────
fdf = df.copy()
if sel_st: fdf = fdf[fdf['State'].isin(sel_st)]
if sel_ct: fdf = fdf[fdf['City'].isin(sel_ct)]
if "Veg 🥦" in food_f:     fdf = fdf[fdf['Food Category']=='Veg']
if "Non-Veg 🍗" in food_f: fdf = fdf[fdf['Food Category']=='Non-Veg']
fdf = fdf[fdf['Rating'] >= rating_f]


# ═══════════════════════════════════════════
# PAGE 1: OVERVIEW
# ═══════════════════════════════════════════
if page == "🏠 Overview":

    # Hero Header
    st.markdown(f"""
    <div class="swiggy-header">
        <div>
            <div class="swiggy-title">🍊 Swiggy Sales Dashboard</div>
            <div class="swiggy-sub">
                {len(fdf):,} orders &nbsp;·&nbsp; {fdf['City'].nunique()} cities &nbsp;·&nbsp;
                {fdf['Restaurant Name'].nunique()} restaurants &nbsp;·&nbsp; {fdf['State'].nunique()} states
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # KPI Row
    c1,c2,c3,c4,c5 = st.columns(5)
    kpis = [
        ("🧾 Total Sales",    fmt_inr(fdf['Price (INR)'].sum()),       "Revenue generated"),
        ("📦 Total Orders",   f"{len(fdf):,}",                         "Orders placed"),
        ("💰 Avg Order Value",fmt_inr(fdf['Price (INR)'].mean()),       "Per order"),
        ("⭐ Avg Rating",     f"{fdf['Rating'].mean():.2f} / 5",       "Customer rating"),
        ("🏪 Restaurants",    f"{fdf['Restaurant Name'].nunique():,}", "Active outlets"),
    ]
    for col,(label,val,sub) in zip([c1,c2,c3,c4,c5], kpis):
        with col:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Quarterly Summary
    with col1:
        st.markdown('<div class="sec-header">📅 Quarterly Performance</div>', unsafe_allow_html=True)
        q = (fdf.groupby('Quarter').agg(
                Sales=('Price (INR)','sum'),
                Orders=('Order Date','count'),
                Rating=('Rating','mean')).reset_index().sort_values('Quarter'))
        fig = go.Figure()
        fig.add_bar(x=q['Quarter'], y=q['Sales'], name='Sales (₹)',
                    marker_color='#fc8019')
        fig.add_scatter(x=q['Quarter'], y=q['Rating']*q['Sales'].max()/5,
                        name='Avg Rating (scaled)', line=dict(color='#ffd4a8', width=2),
                        mode='lines+markers', yaxis='y2')
        fig.update_layout(**SWIGGY_LAYOUT,
            yaxis2=dict(overlaying='y', side='right', showgrid=False,
                        tickvals=[], ticktext=[]),
            legend=dict(bgcolor='#2d1200', bordercolor='#fc8019'))
        st.plotly_chart(fig, use_container_width=True)

    # Veg vs Non Veg donut
    with col2:
        st.markdown('<div class="sec-header">🥦 Veg vs 🍗 Non-Veg Revenue</div>', unsafe_allow_html=True)
        frev = fdf.groupby('Food Category')['Price (INR)'].sum().reset_index()
        fig2 = px.pie(frev, values='Price (INR)', names='Food Category', hole=0.55,
                      color_discrete_sequence=['#4CAF50','#fc8019'])
        fig2.update_traces(textinfo='percent+label', pull=[0.05,0],
                           textfont=dict(size=13))
        fig2.update_layout(**SWIGGY_LAYOUT,
            annotations=[dict(text='Revenue', x=0.5, y=0.5, showarrow=False,
                              font=dict(size=14, color='white'))])
        st.plotly_chart(fig2, use_container_width=True)

    # Rating Distribution
    st.markdown('<div class="sec-header">⭐ Rating Distribution</div>', unsafe_allow_html=True)
    fig3 = px.histogram(fdf, x='Rating', nbins=25, color_discrete_sequence=['#fc8019'])
    fig3.update_layout(**SWIGGY_LAYOUT, bargap=0.1)
    fig3.add_vline(x=fdf['Rating'].mean(), line_color='#ffd4a8', line_dash='dash',
                   annotation_text=f"Avg: {fdf['Rating'].mean():.2f}",
                   annotation_font_color='#ffd4a8')
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════
# PAGE 2: SALES TRENDS
# ═══════════════════════════════════════════
elif page == "📈 Sales Trends":
    st.markdown('<h2 style="color:#fc8019;">📈 Sales Trends</h2>', unsafe_allow_html=True)
    st.markdown("---")

    # Monthly trend with area
    st.markdown('<div class="sec-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
    mon = fdf.groupby('YearMonth')['Price (INR)'].sum().reset_index().sort_values('YearMonth')
    fig = px.area(mon, x='YearMonth', y='Price (INR)', color_discrete_sequence=['#fc8019'])
    fig.update_traces(fill='tozeroy', fillcolor='rgba(252,128,25,0.15)', line_color='#fc8019')
    fig.update_layout(**SWIGGY_LAYOUT)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    # Daily trend
    with col1:
        st.markdown('<div class="sec-header">Daily Revenue (Mon–Sun)</div>', unsafe_allow_html=True)
        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        daily = fdf.groupby('DayName')['Price (INR)'].sum().reindex(day_order).reset_index()
        fig2 = px.bar(daily, x='DayName', y='Price (INR)',
                      color='Price (INR)', color_continuous_scale=['#4a1a00','#fc8019','#ffbe7d'])
        fig2.update_layout(**SWIGGY_LAYOUT, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Orders by day
    with col2:
        st.markdown('<div class="sec-header">Orders by Day</div>', unsafe_allow_html=True)
        daily_ord = fdf.groupby('DayName').size().reindex(day_order).reset_index()
        daily_ord.columns = ['DayName','Orders']
        fig3 = px.line(daily_ord, x='DayName', y='Orders',
                       markers=True, color_discrete_sequence=['#ffd4a8'])
        fig3.update_traces(line=dict(width=3), marker=dict(size=9, color='#fc8019'))
        fig3.update_layout(**SWIGGY_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True)

    # Top Categories
    st.markdown('<div class="sec-header">Top 10 Categories by Revenue</div>', unsafe_allow_html=True)
    cat = fdf.groupby('Category')['Price (INR)'].sum().nlargest(10).sort_values().reset_index()
    fig4 = px.bar(cat, x='Price (INR)', y='Category', orientation='h',
                  color='Price (INR)', color_continuous_scale=['#4a1a00','#fc8019'])
    fig4.update_layout(**SWIGGY_LAYOUT, coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)


# ═══════════════════════════════════════════
# PAGE 3: LOCATION
# ═══════════════════════════════════════════
elif page == "🗺️ Locations":
    st.markdown('<h2 style="color:#fc8019;">🗺️ Location Analysis</h2>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-header">Revenue by State</div>', unsafe_allow_html=True)
        st_rev = fdf.groupby('State')['Price (INR)'].sum().sort_values(ascending=True).reset_index()
        fig = px.bar(st_rev, x='Price (INR)', y='State', orientation='h',
                     color='Price (INR)', color_continuous_scale=['#4a1a00','#fc8019','#ffd4a8'])
        fig.update_layout(**SWIGGY_LAYOUT, height=500, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-header">Top 10 Cities by Orders</div>', unsafe_allow_html=True)
        ct_ord = fdf.groupby('City').size().nlargest(10).sort_values().reset_index()
        ct_ord.columns = ['City','Orders']
        fig2 = px.bar(ct_ord, x='Orders', y='City', orientation='h',
                      color='Orders', color_continuous_scale=['#4a1a00','#fc8019'])
        fig2.update_layout(**SWIGGY_LAYOUT, height=500, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Top Restaurants
    st.markdown('<div class="sec-header">🏪 Top 10 Restaurants by Revenue</div>', unsafe_allow_html=True)
    rest = fdf.groupby('Restaurant Name').agg(
        Revenue=('Price (INR)','sum'),
        Orders=('Price (INR)','count'),
        Avg_Rating=('Rating','mean')
    ).nlargest(10,'Revenue').reset_index().sort_values('Revenue')

    fig3 = px.bar(rest, x='Revenue', y='Restaurant Name', orientation='h',
                  color='Avg_Rating', color_continuous_scale=['#fc8019','#ffd4a8'],
                  hover_data=['Orders','Avg_Rating'])
    fig3.update_layout(**SWIGGY_LAYOUT, coloraxis_colorbar=dict(title='Rating'))
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════
# PAGE 4: FOOD & DISHES
# ═══════════════════════════════════════════
elif page == "🍽️ Food & Dishes":
    st.markdown('<h2 style="color:#fc8019;">🍽️ Food & Dishes Analysis</h2>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-header">Veg vs Non-Veg — Orders</div>', unsafe_allow_html=True)
        fo = fdf['Food Category'].value_counts().reset_index()
        fo.columns = ['Food Category','Orders']
        fig = px.pie(fo, values='Orders', names='Food Category', hole=0.55,
                     color_discrete_sequence=['#4CAF50','#fc8019'])
        fig.update_traces(textinfo='percent+label', pull=[0.05,0])
        fig.update_layout(**SWIGGY_LAYOUT,
            annotations=[dict(text='Orders', x=0.5, y=0.5, showarrow=False,
                              font=dict(size=14,color='white'))])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-header">Price Range Distribution</div>', unsafe_allow_html=True)
        fig2 = px.box(fdf, x='Food Category', y='Price (INR)',
                      color='Food Category',
                      color_discrete_map={'Veg':'#4CAF50','Non-Veg':'#fc8019'})
        fig2.update_layout(**SWIGGY_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

    # Top Dishes
    st.markdown('<div class="sec-header">🍛 Top 15 Best Selling Dishes by Revenue</div>', unsafe_allow_html=True)
    top_d = (fdf.groupby(['Dish Name','Food Category'])['Price (INR)'].sum()
             .nlargest(15).reset_index().sort_values('Price (INR)'))
    fig3 = px.bar(top_d, x='Price (INR)', y='Dish Name', orientation='h',
                  color='Food Category',
                  color_discrete_map={'Veg':'#4CAF50','Non-Veg':'#fc8019'})
    fig3.update_layout(**SWIGGY_LAYOUT, legend=dict(bgcolor='#2d1200'))
    st.plotly_chart(fig3, use_container_width=True)

    # Avg price per category
    st.markdown('<div class="sec-header">💰 Avg Order Value by Food Category</div>', unsafe_allow_html=True)
    cat_avg = (fdf.groupby('Category')['Price (INR)'].mean()
               .nlargest(12).sort_values().reset_index())
    fig4 = px.bar(cat_avg, x='Price (INR)', y='Category', orientation='h',
                  color='Price (INR)', color_continuous_scale=['#4a1a00','#fc8019','#ffd4a8'])
    fig4.update_layout(**SWIGGY_LAYOUT, coloraxis_showscale=False,
                       xaxis_title='Avg Price (INR)')
    st.plotly_chart(fig4, use_container_width=True)


# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding: 20px;'>
    <span style='color:#fc8019; font-size:20px;'>🍊</span>
    <span style='color:#ffd4a8; font-size:13px; margin: 0 12px;'>
        © 2026 <strong>Prathamesh Chougule</strong> · All Rights Reserved
    </span>
    <span style='color:#fc8019; font-size:20px;'>🍊</span>
    <br><span style='color:#ff6b00; font-size:11px;'>Built with ❤️ using Python & Streamlit</span>
</div>
""", unsafe_allow_html=True)
