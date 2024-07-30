import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read the data from the CSV file
data = pd.read_csv('financial_data.csv')

# Calculate total income
total_income = data[data['Category'] == 'Income']['Amount'].sum()

# Filter the data to exclude income
expense_data = data[data['Category'] != 'Income'].copy()

# Create a formatted amount column for display purposes
expense_data['Formatted Amount'] = expense_data['Amount'].apply(lambda x: f"${x:,.2f}")

# Create labels for the tree map
expense_data['Label'] = expense_data['Description'] + '<br>' + expense_data['Formatted Amount']

# Create a tree map for expenses
fig = px.treemap(
    expense_data,
    path=['Category', 'Sub Category', 'Label'],
    values='Amount',
    title='Expense Overview Tree Map',
    hover_data={'Amount': True, 'Label': False}
)

# Update layout to accommodate the annotation and prevent overlapping
fig.update_layout(
    title={
        'text': "Expense Overview Tree Map",
        'x': 0.5,
        'xanchor': 'center'
    },
    margin=dict(t=120)  # Increase the top margin to make space for the annotation
)

# Add annotation for total income below the title
fig.add_annotation(
    text=f"Total Income: ${total_income:,.2f}",
    x=0.5, y=1.05,
    xref='paper', yref='paper',
    showarrow=False,
    font=dict(size=20)
)

# Show the tree map
fig.show()