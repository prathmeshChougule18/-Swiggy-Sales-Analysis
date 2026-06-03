import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Swiggy Sales Analysis",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .kpi-card {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border: 1px solid #2e3347;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    .kpi-label { color: #8b92a5; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { color: #ffffff; font-size: 26px; font-weight: 700; margin: 6px 0; }
    .section-header {
        color: #e2e8f0;
        font-size: 17px;
        font-weight: 600;
        border-left: 4px solid #fc8019;
        padding-left: 12px;
        margin: 20px 0 12px 0;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    possible_paths = ['swiggy_data.csv', 'data/swiggy_data.csv',
                      'swiggy_data_xlsx_-_swiggy_data.csv']
    df = None
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            break
        except:
            continue
    if df is None:
        st.error("❌ swiggy_data.csv not found! Upload it in your repo root.")
        st.stop()

    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=False, errors='coerce')
    df['YearMonth'] = df['Order Date'].dt.to_period('M').astype(str)
    df['DayName'] = df['Order Date'].dt.day_name()
    df['Quarter'] = df['Order Date'].dt.to_period('Q').astype(str)

    non_veg_keywords = ["chicken", "egg", "fish", "mutton", "prawns",
                        "biryani", "kabab", "kebab", "non-veg", "non veg"]
    df['Food Category'] = np.where(
        df['Dish Name'].str.lower().str.contains('|'.join(non_veg_keywords), na=False),
        'Non-Veg', 'Veg'
    )
    return df


df = load_data()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍕 Swiggy Dashboard")
    st.markdown("---")
    st.markdown("### 🔍 Filters")

    all_states = sorted(df['State'].dropna().unique().tolist())
    selected_states = st.multiselect("Select State(s)", options=all_states, default=[], placeholder="All States")

    all_cities = sorted(df['City'].dropna().unique().tolist())
    selected_cities = st.multiselect("Select City", options=all_cities, default=[], placeholder="All Cities")

    food_filter = st.radio("Food Type", ["All", "Veg", "Non-Veg"])

    st.markdown("---")
    st.markdown("### 📌 Navigation")
    page = st.radio("", ["📊 Overview", "📈 Sales Trends", "🗺️ Location Analysis", "🍽️ Food Analysis"],
                    label_visibility="collapsed")

# ─────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────
filtered_df = df.copy()
if selected_states:
    filtered_df = filtered_df[filtered_df['State'].isin(selected_states)]
if selected_cities:
    filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
if food_filter != "All":
    filtered_df = filtered_df[filtered_df['Food Category'] == food_filter]


def fmt_inr(val):
    if val >= 1_00_00_000:
        return f"₹{val/1_00_00_000:.2f}Cr"
    elif val >= 1_00_000:
        return f"₹{val/1_00_000:.1f}L"
    elif val >= 1_000:
        return f"₹{val/1_000:.1f}K"
    return f"₹{val:.0f}"


# ═══════════════════════════════════════════
# PAGE 1: OVERVIEW
# ═══════════════════════════════════════════
if page == "📊 Overview":
    st.markdown("# 🍕 Swiggy Sales Analysis Dashboard")
    st.markdown(f"Showing **{len(filtered_df):,} orders** · {filtered_df['City'].nunique()} cities · {filtered_df['State'].nunique()} states")
    st.markdown("---")

    # KPI CARDS
    c1, c2, c3, c4, c5 = st.columns(5)
    total_sales = filtered_df['Price (INR)'].sum()
    avg_order = filtered_df['Price (INR)'].mean()
    avg_rating = filtered_df['Rating'].mean()
    total_orders = len(filtered_df)
    total_ratings = filtered_df['Rating Count'].sum()

    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Sales</div>
            <div class="kpi-value">{fmt_inr(total_sales)}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Order Value</div>
            <div class="kpi-value">{fmt_inr(avg_order)}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Rating</div>
            <div class="kpi-value">⭐ {avg_rating:.1f}</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Rating Count</div>
            <div class="kpi-value">{total_ratings:,}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quarterly Summary
    st.markdown('<div class="section-header">📅 Quarterly Performance Summary</div>', unsafe_allow_html=True)
    quarterly = (
        filtered_df.groupby('Quarter', as_index=False)
        .agg(Total_Sales=('Price (INR)', 'sum'),
             Avg_Rating=('Rating', 'mean'),
             Total_Orders=('Order Date', 'count'))
        .sort_values('Quarter')
    )
    quarterly['Total_Sales'] = quarterly['Total_Sales'].round(0)
    quarterly['Avg_Rating'] = quarterly['Avg_Rating'].round(2)
    quarterly['Total_Sales_Fmt'] = quarterly['Total_Sales'].apply(fmt_inr)
    st.dataframe(quarterly[['Quarter', 'Total_Sales_Fmt', 'Avg_Rating', 'Total_Orders']]
                 .rename(columns={'Total_Sales_Fmt': 'Total Sales', 'Avg_Rating': 'Avg Rating',
                                  'Total_Orders': 'Total Orders'}),
                 use_container_width=True, hide_index=True)

    # Rating Distribution
    st.markdown('<div class="section-header">⭐ Rating Distribution</div>', unsafe_allow_html=True)
    fig = px.histogram(filtered_df, x='Rating', nbins=20,
                       color_discrete_sequence=['#fc8019'], title='')
    fig.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130',
                      font_color='#e2e8f0', xaxis_title='Rating', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════
# PAGE 2: SALES TRENDS
# ═══════════════════════════════════════════
elif page == "📈 Sales Trends":
    st.markdown("# 📈 Sales Trends")
    st.markdown("---")

    # Monthly Trend
    st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
    monthly = filtered_df.groupby('YearMonth')['Price (INR)'].sum().reset_index()
    monthly = monthly.sort_values('YearMonth')
    fig = px.line(monthly, x='YearMonth', y='Price (INR)',
                  markers=True, color_discrete_sequence=['#fc8019'])
    fig.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130',
                      font_color='#e2e8f0', xaxis_title='Month', yaxis_title='Revenue (INR)')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    # Daily Trend
    st.markdown('<div class="section-header">Daily Revenue Trend (Mon–Sun)</div>', unsafe_allow_html=True)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily = (filtered_df.groupby('DayName')['Price (INR)'].sum()
             .reindex(day_order).reset_index())
    fig2 = px.bar(daily, x='DayName', y='Price (INR)',
                  color_discrete_sequence=['#fc8019'])
    fig2.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130',
                       font_color='#e2e8f0', xaxis_title='Day', yaxis_title='Revenue (INR)')
    st.plotly_chart(fig2, use_container_width=True)

    # Top Categories
    st.markdown('<div class="section-header">Top 10 Categories by Revenue</div>', unsafe_allow_html=True)
    cat_rev = (filtered_df.groupby('Category')['Price (INR)'].sum()
               .nlargest(10).sort_values().reset_index())
    fig3 = px.bar(cat_rev, x='Price (INR)', y='Category', orientation='h',
                  color_discrete_sequence=['#fc8019'])
    fig3.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130',
                       font_color='#e2e8f0', xaxis_title='Revenue (INR)', yaxis_title='')
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════
# PAGE 3: LOCATION ANALYSIS
# ═══════════════════════════════════════════
elif page == "🗺️ Location Analysis":
    st.markdown("# 🗺️ Location Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)

    # Revenue by State
    with col1:
        st.markdown('<div class="section-header">Revenue by State</div>', unsafe_allow_html=True)
        state_rev = (filtered_df.groupby('State')['Price (INR)'].sum()
                     .sort_values(ascending=False).reset_index())
        fig = px.bar(state_rev, x='Price (INR)', y='State', orientation='h',
                     color_discrete_sequence=['#6366f1'])
        fig.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130',
                          font_color='#e2e8f0', height=500,
                          yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig, use_container_width=True)

    # Top 5 Cities
    with col2:
        st.markdown('<div class="section-header">Top 10 Cities by Sales</div>', unsafe_allow_html=True)
        city_rev = (filtered_df.groupby('City')['Price (INR)'].sum()
                    .nlargest(10).sort_values().reset_index())
        fig2 = px.bar(city_rev, x='Price (INR)', y='City', orientation='h',
                      color_discrete_sequence=['#fc8019'])
        fig2.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130',
                           font_color='#e2e8f0', height=500)
        st.plotly_chart(fig2, use_container_width=True)

    # Top Restaurants
    st.markdown('<div class="section-header">Top 10 Restaurants by Revenue</div>', unsafe_allow_html=True)
    rest_rev = (filtered_df.groupby('Restaurant Name')['Price (INR)'].sum()
                .nlargest(10).sort_values().reset_index())
    fig3 = px.bar(rest_rev, x='Price (INR)', y='Restaurant Name', orientation='h',
                  color_discrete_sequence=['#10b981'])
    fig3.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130',
                       font_color='#e2e8f0')
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════
# PAGE 4: FOOD ANALYSIS
# ═══════════════════════════════════════════
elif page == "🍽️ Food Analysis":
    st.markdown("# 🍽️ Food Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)

    # Veg vs Non-Veg
    with col1:
        st.markdown('<div class="section-header">Revenue: Veg vs Non-Veg</div>', unsafe_allow_html=True)
        food_rev = filtered_df.groupby('Food Category')['Price (INR)'].sum().reset_index()
        fig = px.pie(food_rev, values='Price (INR)', names='Food Category',
                     hole=0.5, color_discrete_sequence=['#10b981', '#fc8019'])
        fig.update_traces(textinfo='percent+label', pull=[0.05, 0])
        fig.update_layout(paper_bgcolor='#1e2130', font_color='#e2e8f0', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Orders: Veg vs Non-Veg
    with col2:
        st.markdown('<div class="section-header">Orders: Veg vs Non-Veg</div>', unsafe_allow_html=True)
        food_orders = filtered_df['Food Category'].value_counts().reset_index()
        food_orders.columns = ['Food Category', 'Orders']
        fig2 = px.pie(food_orders, values='Orders', names='Food Category',
                      hole=0.5, color_discrete_sequence=['#6366f1', '#f59e0b'])
        fig2.update_traces(textinfo='percent+label', pull=[0.05, 0])
        fig2.update_layout(paper_bgcolor='#1e2130', font_color='#e2e8f0', height=400)
        st.plotly_chart(fig2, use_container_width=True)

    # Top 10 Dishes
    st.markdown('<div class="section-header">Top 10 Best Selling Dishes</div>', unsafe_allow_html=True)
    top_dishes = (filtered_df.groupby('Dish Name')['Price (INR)'].sum()
                  .nlargest(10).sort_values().reset_index())
    fig3 = px.bar(top_dishes, x='Price (INR)', y='Dish Name', orientation='h',
                  color_discrete_sequence=['#fc8019'])
    fig3.update_layout(paper_bgcolor='#1e2130', plot_bgcolor='#1e2130',
                       font_color='#e2e8f0')
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #8b92a5; padding: 20px;'>
    <p>© 2026 <strong style='color: #e2e8f0;'>Prathamesh Chougule</strong> · All Rights Reserved</p>
    <p style='font-size: 12px;'>Built with ❤️ using Python & Streamlit</p>
</div>
""", unsafe_allow_html=True)
