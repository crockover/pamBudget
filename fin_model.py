import pandas as pd
import plotly.express as px
import os

# Load the financial data
df = pd.read_csv('financial_data.csv')

# Create a function to categorize the data
def categorize_data(df):
    categories = {
        'Income': df[df['Category'] == 'Income'],
        'Necessary': df[df['Category'] == 'Necessary'],
        'Nice2Have': df[df['Category'] == 'Nice2Have'],
        'Savings': df[df['Category'] == 'Savings']
    }
    return categories

# Categorize the data
categories = categorize_data(df)

# Calculate the totals for each category
totals = {key: data['Amount'].sum() for key, data in categories.items()}

# Calculate savings
totals['Savings'] = totals['Income'] - totals['Necessary'] - totals['Nice2Have']

# Create a static directory if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

# Create a tree map for the financial overview
tree_map_data = []
for category, data in categories.items():
    for subcat, amount, description in zip(data['Sub Category'], data['Amount'], data['Description']):
        tree_map_data.append({'Overview': 'Overview', 'Category': category, 'Sub Category': subcat, 'Amount': amount, 'Description': description})

tree_map_df = pd.DataFrame(tree_map_data)

# Define colors for each category
category_colors = {
    'Income': '#87ba80',  # Pastel green
    'Necessary': '#ff6961',  # Pastel red
    'Nice2Have': '#e88c2a',  # Pastel orange
    'Savings': '#7ba7b0',  # Pastel blue
    'Overview': '#777e80'  # Light gray for the root node
}

# Assign colors to each category
color_sequence = [category_colors['Overview'], category_colors['Necessary'], category_colors['Income'], category_colors['Savings'], category_colors['Nice2Have']]

# Create the treemap with the specified colors
fig = px.treemap(tree_map_df, path=['Overview', 'Category', 'Sub Category', 'Description'], values='Amount', title='Financial Overview', color='Category', color_discrete_map=category_colors, color_discrete_sequence=color_sequence)
fig.update_traces(root_color=category_colors['Overview'])
fig.update_traces(textinfo="label+value+percent parent+percent entry", textfont=dict(color='white'))
fig.write_html('static/financial_overview.html')