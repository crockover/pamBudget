import pandas as pd
import plotly.express as px
import os

# Load the financial data
df = pd.read_csv('financial_data.csv')

# Create a static directory if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

# Define colors for each category
category_colors = {
    'Income': '#a7e69e',  # Pastel green
    'Necessary': '#ff6961',  # Pastel red
    'Nice2Have': '#ffb347',  # Pastel orange
    'Savings': '#aec6cf'  # Pastel blue
}

# Create tree maps for each main category
for category, color in category_colors.items():
    category_df = df[df['Category'] == category]
    num_rows = len(category_df)
    
    # Calculate the number of unique subcategories
    num_subcategories = category_df['Sub Category'].nunique()
    
    # Total nodes = root node + subcategories + rows
    total_nodes = 1 + num_subcategories + num_rows
    
    # Create the treemap
    fig = px.treemap(category_df, path=['Sub Category', 'Description'], values='Amount', title=f'{category} Overview')
    fig.update_traces(marker=dict(colors=[color] * total_nodes, line=dict(color='white')), root_color=color)
    fig.update_traces(textinfo="label+value+percent parent+percent entry", textfont=dict(color='white'))
    
    # Update layout to include the category label for the root node
    fig.update_layout(
        annotations=[dict(
            text=category,
            x=0,
            y=1.02,
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            font=dict(size=12, color='white'),
            xref="paper",
            yref="paper"
        )],
        margin=dict(t=50, l=25, r=25, b=25)
    )
    fig.write_html(f'static/{category.lower()}_overview.html')

# Create an index.html that includes all four tree maps
index_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Dashboard</title>
</head>
<body>
    <h1>Financial Dashboard</h1>
    <h2>Income</h2>
    <iframe src="{{ url_for('static', filename='income_overview.html') }}" width="100%" height="600px" frameborder="0"></iframe>
    <h2>Necessary</h2>
    <iframe src="{{ url_for('static', filename='necessary_overview.html') }}" width="100%" height="600px" frameborder="0"></iframe>
    <h2>Nice2Have</h2>
    <iframe src="{{ url_for('static', filename='nice2have_overview.html') }}" width="100%" height="600px" frameborder="0"></iframe>
    <h2>Savings</h2>
    <iframe src="{{ url_for('static', filename='savings_overview.html') }}" width="100%" height="600px" frameborder="0"></iframe>
</body>
</html>
"""

# Write the index.html content to the templates directory
with open('templates/index.html', 'w') as f:
    f.write(index_html_content)