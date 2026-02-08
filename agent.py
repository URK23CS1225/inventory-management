import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class InventoryAgent:
    def __init__(self, inventory_file, demand_file, decision_log_file='decisions.json'):
        # Handle both compressed and regular CSV files
        if inventory_file.endswith('.gz'):
            self.inventory = pd.read_csv(inventory_file, compression='gzip')
        else:
            self.inventory = pd.read_csv(inventory_file)
        
        self.demand = pd.read_csv(demand_file)
        self.decision_log_file = decision_log_file
        self.decisions = []
        self._load_decisions()
        
    def _load_decisions(self):
        if os.path.exists(self.decision_log_file):
            with open(self.decision_log_file, 'r') as f:
                self.decisions = json.load(f)
    
    def _save_decisions(self):
        with open(self.decision_log_file, 'w') as f:
            json.dump(self.decisions, f, indent=2)
    
    def calculate_risk(self, product_id):
        inv = self.inventory[self.inventory['product_id'] == product_id].iloc[0]
        dem = self.demand[self.demand['product_id'] == product_id].iloc[0]
        
        daily_demand = dem['daily_demand']
        current_stock = inv['current_stock']
        lead_time = inv['lead_time_days']
        
        if daily_demand == 0:
            days_of_stock = 999
            risk_factor = 0
        else:
            days_of_stock = current_stock / daily_demand
            risk_factor = lead_time / days_of_stock if days_of_stock > 0 else 999
        
        if risk_factor >= 1.0:
            risk_level = 'High'
        elif risk_factor >= 0.5:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'days_of_stock': round(days_of_stock, 2),
            'risk_factor': round(risk_factor, 2),
            'risk_level': risk_level,
            'current_stock': current_stock,
            'daily_demand': daily_demand,
            'lead_time': lead_time
        }
    
    def make_decision(self, product_id):
        risk_info = self.calculate_risk(product_id)
        inv = self.inventory[self.inventory['product_id'] == product_id].iloc[0]
        
        action = 'No Action'
        reorder_qty = 0
        reason = ''
        
        if risk_info['risk_level'] == 'High':
            # Calculate optimal reorder: cover lead time + safety buffer
            safety_stock = risk_info['daily_demand'] * risk_info['lead_time'] * 1.5
            reorder_qty = max(0, int(safety_stock - inv['current_stock']))
            
            # If still 0, at least reorder to max capacity
            if reorder_qty == 0:
                reorder_qty = int((inv['max_capacity'] - inv['current_stock']) * 0.8)
            
            action = f'Reorder {reorder_qty} units' if reorder_qty > 0 else 'No Action'
            reason = f"Critical: Stock will run out in {risk_info['days_of_stock']} days, but lead time is {risk_info['lead_time']} days. Risk factor {risk_info['risk_factor']} indicates imminent stockout. Recommended reorder: {reorder_qty} units to cover demand during lead time."
        elif risk_info['risk_level'] == 'Medium':
            # Reorder to reach optimal level
            optimal_stock = risk_info['daily_demand'] * risk_info['lead_time'] * 2
            reorder_qty = max(0, int(optimal_stock - inv['current_stock']))
            
            if reorder_qty == 0:
                reorder_qty = int((inv['max_capacity'] - inv['current_stock']) * 0.5)
            
            action = f'Reorder {reorder_qty} units' if reorder_qty > 0 else 'No Action'
            reason = f"Moderate risk: {risk_info['days_of_stock']} days of stock with {risk_info['lead_time']} day lead time. Risk factor {risk_info['risk_factor']} suggests proactive restocking of {reorder_qty} units."
        else:
            reason = f"Low risk: {risk_info['days_of_stock']} days of stock available, well above {risk_info['lead_time']} day lead time. Risk factor {risk_info['risk_factor']} is acceptable."
        
        decision = {
            'product_id': product_id,
            'product_name': inv['product_name'],
            'timestamp': datetime.now().isoformat(),
            'observed_stock': int(risk_info['current_stock']),
            'daily_demand': float(risk_info['daily_demand']),
            'days_of_stock': risk_info['days_of_stock'],
            'lead_time_days': int(risk_info['lead_time']),
            'risk_factor': risk_info['risk_factor'],
            'risk_level': risk_info['risk_level'],
            'action': action,
            'reorder_qty': reorder_qty,
            'reason': reason
        }
        
        self.decisions.append(decision)
        self._save_decisions()
        
        # Update inventory if reordering
        if reorder_qty > 0:
            self.inventory.loc[self.inventory['product_id'] == product_id, 'current_stock'] += reorder_qty
        
        return decision
    
    def run_all_products(self):
        results = []
        for product_id in self.inventory['product_id']:
            decision = self.make_decision(product_id)
            results.append(decision)
        return results
    
    def get_product_timeline(self, product_id):
        return [d for d in self.decisions if d['product_id'] == product_id]
    
    def get_current_status(self):
        status = []
        for _, inv in self.inventory.iterrows():
            risk_info = self.calculate_risk(inv['product_id'])
            recent_decisions = [d for d in self.decisions if d['product_id'] == inv['product_id']]
            last_action = recent_decisions[-1]['action'] if recent_decisions else 'No Action'
            
            status.append({
                'product_id': inv['product_id'],
                'product_name': inv['product_name'],
                'current_stock': int(inv['current_stock']),
                'daily_demand': risk_info['daily_demand'],
                'risk_level': risk_info['risk_level'],
                'risk_factor': risk_info['risk_factor'],
                'days_of_stock': risk_info['days_of_stock'],
                'last_action': last_action
            })
        return pd.DataFrame(status)
