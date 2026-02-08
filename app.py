import streamlit as st
import pandas as pd
from agent import InventoryAgent
import time
import altair as alt

st.set_page_config(page_title="Inventory AI Agent", layout="wide", initial_sidebar_state="collapsed")

# Professional CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 100%;
    }
    
    /* Professional Header */
    .pro-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px 40px;
        margin: -2rem -3rem 2rem -3rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-text {
        font-size: 32px;
        font-weight: 700;
        color: white;
        letter-spacing: -0.5px;
    }
    
    /* Navigation Pills */
    .stRadio > div {
        background: rgba(255,255,255,0.15);
        padding: 8px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .stRadio [role="radiogroup"] {
        gap: 8px;
    }
    
    .stRadio label {
        background: transparent !important;
        color: white !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        border: 1px solid transparent !important;
    }
    
    .stRadio label:hover {
        background: rgba(255,255,255,0.2) !important;
        transform: translateY(-1px);
    }
    
    .stRadio label[data-checked="true"] {
        background: white !important;
        color: #667eea !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 36px !important;
        font-weight: 700 !important;
        color: #1a202c;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #718096 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="metric-container"] {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Headings */
    h1 {
        font-size: 36px !important;
        font-weight: 700 !important;
        color: #1a202c !important;
        margin-bottom: 8px !important;
    }
    
    h2 {
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #2d3748 !important;
        margin-top: 32px !important;
    }
    
    h3 {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #4a5568 !important;
    }
    
    /* Cards for sections */
    .card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    
    /* Tables */
    .dataframe {
        font-size: 14px !important;
        border: none !important;
    }
    
    .dataframe thead tr th {
        background: #f7fafc !important;
        color: #2d3748 !important;
        font-weight: 600 !important;
        padding: 16px !important;
        border: none !important;
    }
    
    .dataframe tbody tr td {
        padding: 14px !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    
    .dataframe tbody tr:hover {
        background: #f7fafc !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 12px 32px;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Success/Warning/Error boxes */
    .stSuccess, .stWarning, .stError {
        border-radius: 12px;
        padding: 16px;
        font-weight: 500;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f7fafc;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize agent
@st.cache_resource
def load_agent(_inventory_file=None, _demand_file=None):
    if _inventory_file and _demand_file:
        return InventoryAgent(_inventory_file, _demand_file)
    return InventoryAgent('inventory.csv.gz', 'demand.csv')

# Check if custom data is uploaded
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = None
if 'demand_data' not in st.session_state:
    st.session_state.demand_data = None

# Professional Header
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown('<div class="logo-text">🏪 Home.cash</div>', unsafe_allow_html=True)
with col2:
    subcol1, subcol2 = st.columns([4, 1])
    with subcol1:
        action = st.radio(
            "",
            ["📊 Overview", "📦 Inventory", "🔍 Product Details", "🤖 Run Agent", "📤 Upload Data"],
            horizontal=True,
            label_visibility="collapsed"
        )
    with subcol2:
        if st.session_state.inventory_data is not None:
            st.markdown('<span style="color: #48bb78; font-size: 14px; margin-top: 10px; display: block;">✅ Custom Data</span>', unsafe_allow_html=True)

# Load agent with appropriate data
if st.session_state.inventory_data is not None and st.session_state.demand_data is not None:
    agent = load_agent(st.session_state.inventory_data, st.session_state.demand_data)
else:
    agent = load_agent()

if action == "📤 Upload Data":
    st.title("📤 Upload Custom Data")
    st.markdown("Upload your warehouse inventory and demand data to use the AI agent")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload section in single row
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📦 Inventory Data")
        st.markdown("**Required:** `product_id`, `product_name`, `current_stock`, `max_capacity`, `lead_time_days`")
        inventory_file = st.file_uploader("", type=['csv'], key='inv_upload', label_visibility="collapsed")
        
        if inventory_file:
            try:
                inv_df = pd.read_csv(inventory_file)
                required_cols = ['product_id', 'product_name', 'current_stock', 'max_capacity', 'lead_time_days']
                
                if all(col in inv_df.columns for col in required_cols):
                    st.success(f"✅ {len(inv_df)} products loaded")
                    with st.expander("Preview Data"):
                        st.dataframe(inv_df.head(3), use_container_width=True)
                    
                    inv_df.to_csv('/tmp/uploaded_inventory.csv', index=False)
                    st.session_state.inventory_data = '/tmp/uploaded_inventory.csv'
                else:
                    st.error(f"❌ Missing columns")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Demand Data")
        st.markdown("**Required:** `product_id`, `daily_demand`")
        demand_file = st.file_uploader("", type=['csv'], key='dem_upload', label_visibility="collapsed")
        
        if demand_file:
            try:
                dem_df = pd.read_csv(demand_file)
                required_cols = ['product_id', 'daily_demand']
                
                if all(col in dem_df.columns for col in required_cols):
                    st.success(f"✅ {len(dem_df)} products loaded")
                    with st.expander("Preview Data"):
                        st.dataframe(dem_df.head(3), use_container_width=True)
                    
                    dem_df.to_csv('/tmp/uploaded_demand.csv', index=False)
                    st.session_state.demand_data = '/tmp/uploaded_demand.csv'
                else:
                    st.error(f"❌ Missing columns")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.inventory_data and st.session_state.demand_data:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%); padding: 20px; border-radius: 12px; text-align: center;'>
            <h3 style='margin: 0; color: #22543d;'>✅ Data Successfully Loaded!</h3>
            <p style='margin: 8px 0 0 0; color: #2f855a;'>You can now use the AI agent with your custom warehouse data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Reset to Default Data", use_container_width=True):
                st.session_state.inventory_data = None
                st.session_state.demand_data = None
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sample data download
    st.markdown("### 📥 Download Sample Templates")
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        sample_inv = pd.DataFrame({
            'product_id': ['P001', 'P002', 'P003'],
            'product_name': ['Product A', 'Product B', 'Product C'],
            'current_stock': [100, 200, 150],
            'max_capacity': [500, 600, 400],
            'lead_time_days': [5, 7, 10]
        })
        st.download_button(
            "📦 Download Inventory Template",
            sample_inv.to_csv(index=False),
            "inventory_template.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col2:
        sample_dem = pd.DataFrame({
            'product_id': ['P001', 'P002', 'P003'],
            'daily_demand': [25.5, 40.2, 30.0]
        })
        st.download_button(
            "📊 Download Demand Template",
            sample_dem.to_csv(index=False),
            "demand_template.csv",
            "text/csv",
            use_container_width=True
        )

elif action == "📊 Overview":
    st.title("📊 Dashboard Overview")
    st.markdown("Real-time insights into your inventory performance")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Load data
    status_df = agent.get_current_status()
    inventory = agent.inventory
    
    # Calculate metrics
    total_stock_value = (inventory['current_stock'] * 50).sum()
    total_products = len(inventory)
    out_of_stock_count = len(status_df[status_df['risk_level'] == 'High'])
    low_stock = len(status_df[status_df['risk_level'] == 'Medium'])
    
    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Value", f"₹{total_stock_value:,.0f}", delta="-20%")
    with col2:
        st.metric("📦 Total Products", f"{total_products}", delta="+5")
    with col3:
        st.metric("🚨 Critical Stock", out_of_stock_count, delta=f"-{out_of_stock_count}")
    with col4:
        st.metric("⚠️ Low Stock", low_stock, delta=f"-{low_stock}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 Weekly Sales Trend")
        sales_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Sales': [120, 190, 150, 180, 160, 200, 170]
        })
        
        # Create altair chart with proper ordering
        chart = alt.Chart(sales_data).mark_bar(color='#1e88e5').encode(
            x=alt.X('Day:N', sort=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Sales:Q', title='Sales')
        ).properties(height=350)
        
        st.altair_chart(chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚨 Critical Items")
        out_of_stock = status_df[status_df['risk_level'] == 'High'][['product_name', 'current_stock', 'daily_demand']].head(8)
        if len(out_of_stock) > 0:
            for idx, row in out_of_stock.iterrows():
                st.markdown(f"""
                <div style='padding: 10px; margin: 8px 0; background: #fff5f5; border-left: 4px solid #fc8181; border-radius: 6px;'>
                    <strong>{row['product_name']}</strong><br>
                    <span style='color: #718096; font-size: 13px;'>Stock: {row['current_stock']} | Demand: {row['daily_demand']}/day</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ All products adequately stocked!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Top Products Table
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏆 Top Performing Products")
    top_products = status_df.nlargest(10, 'daily_demand')[['product_name', 'daily_demand', 'current_stock', 'risk_level', 'days_of_stock']]
    top_products.columns = ['Product Name', 'Daily Demand', 'Current Stock', 'Risk Level', 'Days Left']
    top_products['Daily Demand'] = top_products['Daily Demand'].round(1)
    top_products['Days Left'] = top_products['Days Left'].round(1)
    
    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    st.markdown('</div>', unsafe_allow_html=True)

elif action == "📦 Inventory":
    st.title("📦 Inventory Dashboard")
    
    status_df = agent.get_current_status()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", len(status_df))
    with col2:
        high_risk = len(status_df[status_df['risk_level'] == 'High'])
        st.metric("High Risk", high_risk, delta=None, delta_color="inverse")
    with col3:
        medium_risk = len(status_df[status_df['risk_level'] == 'Medium'])
        st.metric("Medium Risk", medium_risk)
    with col4:
        low_risk = len(status_df[status_df['risk_level'] == 'Low'])
        st.metric("Low Risk", low_risk)
    
    # Filter
    risk_filter = st.multiselect("Filter by Risk Level", ['High', 'Medium', 'Low'], default=['High', 'Medium', 'Low'])
    filtered_df = status_df[status_df['risk_level'].isin(risk_filter)]
    
    # Color coding
    def color_risk(val):
        if val == 'High':
            return 'background-color: #ff4444; color: white'
        elif val == 'Medium':
            return 'background-color: #ffaa00; color: white'
        else:
            return 'background-color: #44ff44; color: black'
    
    st.dataframe(
        filtered_df.style.applymap(color_risk, subset=['risk_level']),
        use_container_width=True,
        height=500
    )

elif action == "🔍 Product Details":
    st.title("🔍 Product Detail View")
    
    product_ids = agent.inventory['product_id'].tolist()
    selected_product = st.selectbox("Select Product", product_ids)
    
    if selected_product:
        risk_info = agent.calculate_risk(selected_product)
        inv = agent.inventory[agent.inventory['product_id'] == selected_product].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Current Status")
            st.metric("Product", inv['product_name'])
            st.metric("Current Stock", int(inv['current_stock']))
            st.metric("Max Capacity", int(inv['max_capacity']))
            st.metric("Daily Demand", risk_info['daily_demand'])
            st.metric("Lead Time", f"{risk_info['lead_time']} days")
        
        with col2:
            st.subheader("Risk Analysis")
            st.metric("Days of Stock Left", risk_info['days_of_stock'])
            st.metric("Risk Factor", risk_info['risk_factor'])
            
            risk_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
            st.metric("Risk Level", f"{risk_color[risk_info['risk_level']]} {risk_info['risk_level']}")
        
        st.subheader("📜 Decision Timeline")
        timeline = agent.get_product_timeline(selected_product)
        
        if timeline:
            for decision in reversed(timeline[-10:]):  # Show last 10
                with st.expander(f"{decision['timestamp'][:19]} - {decision['action']}"):
                    st.write(f"**Stock:** {decision['observed_stock']} units")
                    st.write(f"**Demand:** {decision['daily_demand']} units/day")
                    st.write(f"**Risk Factor:** {decision['risk_factor']}")
                    st.write(f"**Risk Level:** {decision['risk_level']}")
                    st.write(f"**Reason:** {decision['reason']}")
        else:
            st.info("No decisions recorded yet. Run the agent first.")

elif action == "🤖 Run Agent":
    st.title("🤖 AI Agent Execution")
    st.markdown("Let the AI agent analyze inventory and make autonomous decisions")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("▶️ Execute Agent Analysis", type="primary"):
        with st.spinner("🔄 Agent analyzing inventory..."):
            progress_bar = st.progress(0)
            results = []
            
            products = agent.inventory['product_id'].tolist()
            for i, product_id in enumerate(products):
                decision = agent.make_decision(product_id)
                results.append(decision)
                progress_bar.progress((i + 1) / len(products))
                time.sleep(0.01)
            
            st.success(f"✅ Agent completed analysis of {len(results)} products")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Categorize results
            high_risk_actions = [r for r in results if r['risk_level'] == 'High']
            medium_risk_actions = [r for r in results if r['risk_level'] == 'Medium']
            low_risk = len(results) - len(high_risk_actions) - len(medium_risk_actions)
            
            # Summary Cards
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fc8181 0%, #f56565 100%); padding: 24px; border-radius: 12px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0; font-size: 48px;'>{len(high_risk_actions)}</h2>
                    <p style='margin: 8px 0 0 0; font-size: 16px; opacity: 0.9;'>🚨 Critical Actions</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%); padding: 24px; border-radius: 12px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0; font-size: 48px;'>{len(medium_risk_actions)}</h2>
                    <p style='margin: 8px 0 0 0; font-size: 16px; opacity: 0.9;'>⚠️ Medium Priority</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #68d391 0%, #48bb78 100%); padding: 24px; border-radius: 12px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0; font-size: 48px;'>{low_risk}</h2>
                    <p style='margin: 8px 0 0 0; font-size: 16px; opacity: 0.9;'>✅ Healthy Stock</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # High Risk Products - Card Format
            if high_risk_actions:
                st.markdown("## 🚨 Critical Actions Required")
                for action in high_risk_actions[:10]:
                    st.markdown(f"""
                    <div style='background: white; border-left: 5px solid #fc8181; padding: 20px; margin: 16px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                        <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
                            <div>
                                <h3 style='margin: 0; color: #1a202c; font-size: 20px;'>{action['product_name']}</h3>
                                <span style='background: #fed7d7; color: #c53030; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-top: 8px; display: inline-block;'>CRITICAL</span>
                            </div>
                            <div style='text-align: right;'>
                                <div style='font-size: 24px; font-weight: 700; color: #fc8181;'>{action['action']}</div>
                            </div>
                        </div>
                        <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 16px 0; padding: 16px; background: #f7fafc; border-radius: 6px;'>
                            <div>
                                <div style='font-size: 12px; color: #718096; font-weight: 600;'>CURRENT STOCK</div>
                                <div style='font-size: 18px; font-weight: 600; color: #2d3748;'>{action['observed_stock']} units</div>
                            </div>
                            <div>
                                <div style='font-size: 12px; color: #718096; font-weight: 600;'>DAILY DEMAND</div>
                                <div style='font-size: 18px; font-weight: 600; color: #2d3748;'>{action['daily_demand']:.1f} units</div>
                            </div>
                            <div>
                                <div style='font-size: 12px; color: #718096; font-weight: 600;'>DAYS LEFT</div>
                                <div style='font-size: 18px; font-weight: 600; color: #e53e3e;'>{action['days_of_stock']:.1f} days</div>
                            </div>
                            <div>
                                <div style='font-size: 12px; color: #718096; font-weight: 600;'>RISK FACTOR</div>
                                <div style='font-size: 18px; font-weight: 600; color: #e53e3e;'>{action['risk_factor']:.2f}</div>
                            </div>
                        </div>
                        <div style='background: #fff5f5; padding: 12px; border-radius: 6px; border-left: 3px solid #fc8181;'>
                            <strong style='color: #c53030;'>AI Reasoning:</strong>
                            <p style='margin: 8px 0 0 0; color: #4a5568; line-height: 1.6;'>{action['reason']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Medium Risk Products - Compact Cards
            if medium_risk_actions:
                st.markdown("## ⚠️ Medium Priority Actions")
                for action in medium_risk_actions[:10]:
                    st.markdown(f"""
                    <div style='background: white; border-left: 5px solid #f6ad55; padding: 16px; margin: 12px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <h4 style='margin: 0; color: #1a202c; font-size: 18px;'>{action['product_name']}</h4>
                                <span style='color: #718096; font-size: 14px;'>Stock: {action['observed_stock']} | Demand: {action['daily_demand']:.1f}/day | Risk: {action['risk_factor']:.2f}</span>
                            </div>
                            <div style='background: #feebc8; color: #c05621; padding: 8px 16px; border-radius: 6px; font-weight: 600;'>
                                {action['action']}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Low Risk Summary
            if low_risk > 0:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%); padding: 20px; border-radius: 12px; margin-top: 24px;'>
                    <h3 style='margin: 0; color: #22543d;'>✅ {low_risk} Products with Healthy Stock Levels</h3>
                    <p style='margin: 8px 0 0 0; color: #2f855a;'>These products have adequate inventory and don't require immediate action.</p>
                </div>
                """, unsafe_allow_html=True)
