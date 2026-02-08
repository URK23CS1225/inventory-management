# 🏪 Inventory Management AI Agent

An intelligent, autonomous inventory management system that uses AI-driven risk analysis to make smart restocking decisions.

## Features

### Dashboard Overview
- Real-time inventory metrics (Total Value, Products, Critical Stock, Low Stock)
- Weekly sales trend visualization
- Critical items alert system
- Top performing products analysis

### Inventory Management
- Complete inventory dashboard with risk-level filtering
- Color-coded risk indicators (High/Medium/Low)
- Real-time stock and demand tracking
- Days of stock remaining calculations

### 🔍 Product Details
- Individual product deep-dive analysis
- Risk factor breakdown
- Complete decision timeline for each product
- Historical decision tracking

### AI Agent
- **Autonomous Decision Making**: No human intervention required
- **Risk-Based Analysis**: Calculates risk factor = lead_time_days / days_of_stock_left
- **Smart Reorder Logic**: 
  - High Risk: Reorder to cover 1.5x lead time demand
  - Medium Risk: Reorder to cover 2x lead time demand
  - Low Risk: No action needed
- **Explainable AI**: Every decision includes detailed reasoning
- **Decision Timeline**: Complete audit trail of all decisions

### Custom Data Upload
- Upload your own inventory and demand CSV files
- Validation of required columns
- Works with any warehouse data
- Download sample templates
- Reset to default data option

## Getting Started

### Prerequisites
```bash
Python 3.8+
pip
```

### Installation

1. **Clone or navigate to the project directory**
```bash
cd /home/lizania-dew-k/workspace/inven_agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
inven_agent/
├── app.py                          # Main Streamlit application
├── agent.py                        # AI Agent logic and decision engine
├── prepare_data.py                 # Data preparation script
├── requirements.txt                # Python dependencies
├── inventory.csv.gz                # Compressed inventory data
├── demand.csv                      # Daily demand data
├── decisions.json                  # Agent decision log
├── retail_store_inventory.csv      # Original retail data
└── README.md                       # This file
```

## Data Format

### Inventory CSV Format
```csv
product_id,product_name,current_stock,max_capacity,lead_time_days
P001,Product A,100,500,5
P002,Product B,200,600,7
```

**Required Columns:**
- `product_id`: Unique product identifier
- `product_name`: Product name
- `current_stock`: Current inventory level
- `max_capacity`: Maximum storage capacity
- `lead_time_days`: Days required for restocking

### Demand CSV Format
```csv
product_id,daily_demand
P001,25.5
P002,40.2
```

**Required Columns:**
- `product_id`: Unique product identifier (must match inventory)
- `daily_demand`: Average daily demand in units

##  How the AI Agent Works

### Risk Factor Calculation
```
Risk Factor = Lead Time Days / Days of Stock Left
Days of Stock Left = Current Stock / Daily Demand
```

### Risk Classification
- **High Risk**: Risk Factor ≥ 1.0 (Stock will run out before reorder arrives)
- **Medium Risk**: Risk Factor ≥ 0.5 (Approaching critical levels)
- **Low Risk**: Risk Factor < 0.5 (Adequate stock levels)

### Decision Logic
1. **Observe**: Current stock, demand, and lead time
2. **Calculate**: Days of stock remaining and risk factor
3. **Classify**: Determine risk level
4. **Decide**: Calculate optimal reorder quantity
5. **Act**: Log decision with detailed reasoning
6. **Track**: Maintain complete decision timeline

##  UI Features

- **Modern Design**: Professional gradient header with clean navigation
- **Responsive Layout**: Adapts to different screen sizes
- **Interactive Cards**: Hover effects and smooth transitions
- **Color-Coded Alerts**: Visual indicators for risk levels
- **Real-time Updates**: Dynamic data loading and visualization

## 📈 Use Cases

- **Retail Stores**: Manage product inventory across multiple locations
- **Warehouses**: Track stock levels and automate reordering
- **E-commerce**: Prevent stockouts and optimize inventory
- **Manufacturing**: Manage raw materials and components
- **Distribution Centers**: Optimize stock allocation

## 🔧 Customization

### Using Your Own Data

1. Navigate to **Upload Data** tab
2. Download sample templates
3. Prepare your CSV files following the format
4. Upload both inventory and demand files
5. System automatically validates and loads your data
6. Run the AI agent with your custom data

### Modifying Risk Thresholds

Edit `agent.py` to adjust risk classification:
```python
if risk_factor >= 1.0:
    risk_level = 'High'
elif risk_factor >= 0.5:
    risk_level = 'Medium'
else:
    risk_level = 'Low'
```

## Decision Log

All agent decisions are stored in `decisions.json` with:
- Timestamp
- Product details
- Observed stock and demand
- Risk factor and level
- Action taken
- Detailed reasoning

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Altair**: Interactive visualizations
- **Python**: Core programming language

## Key Innovations

1. **Risk Factor-Based Decision Making**: Unlike simple threshold alerts, uses intelligent risk analysis
2. **Explainable AI**: Every decision includes human-readable reasoning
3. **Complete Audit Trail**: Full decision timeline for transparency
4. **Flexible Data Input**: Works with any warehouse data via CSV upload
5. **Autonomous Operation**: No human intervention required for decisions

## Support

For issues or questions, refer to the decision logs and agent reasoning panels for detailed explanations of all actions taken.

## License

This project is created for inventory management and AI agent demonstration purposes.

---


