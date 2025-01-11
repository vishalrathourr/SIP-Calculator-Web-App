import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.io import to_html
import plotly.graph_objects as go
import plotly.io as pio
import json
import io
import base64

def calculate_sip(investment_amount, annual_interest_rate, time_period_years):
    """
    Calculate the maturity value of a Systematic Investment Plan (SIP) and return the results and graph as base64.

    Parameters:
    - investment_amount (float): The amount invested at regular intervals.
    - annual_interest_rate (float): The annual interest rate in percentage (e.g., 10 for 10%).
    - time_period_years (int): The total investment duration in years.

    Returns:
    - tuple: A tuple containing the total investment, estimated returns, total maturity value, and graph as base64.
    """
    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = (annual_interest_rate / 100) / 12

    # Total number of monthly payments
    total_payments = 12 * time_period_years

    # SIP maturity formula
    maturity_value = investment_amount * (
        ((1 + monthly_interest_rate) ** total_payments - 1) / monthly_interest_rate
    ) * (1 + monthly_interest_rate)

    # Round maturity value to the nearest integer
    total_value = round(maturity_value)

    # Calculate total investment (investment amount * number of payments)
    total_investment = investment_amount * total_payments

    # Calculate estimated returns
    est_returns = total_value - total_investment

    # Create a pie plot to visualize the total investment and estimated returns
    investment_return = [est_returns, total_investment]
    labels = ['Estimated Returns', 'Total Investment']

    # Create the pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(investment_return, startangle=90, colors=['royalblue', 'lavender'])
    
    # Add a circle at the center to transform it into a donut chart
    my_circle = plt.Circle((0, 0), 0.65, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    # Add a legend and adjust position
    plt.legend(labels, loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=10, frameon=False)

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    # Encode the plot as base64
    plot_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    plt.close()

    # Return total investment, estimated returns, total maturity value, and base64-encoded graph
    return total_investment, est_returns, total_value, plot_data



def calculate_year_on_year_maturity_interactive(investment_amount, annual_interest_rate, total_years):
    """
    Calculate the Year-on-Year maturity amount for a SIP investment and plot it interactively as a stacked bar plot.
    Also, show the maturity value slightly above the top of the last bar with INR format.

    Parameters:
    - investment_amount (float): The amount invested at regular intervals.
    - annual_interest_rate (float): The annual interest rate in percentage (e.g., 10 for 10%).
    - total_years (int): The total investment duration in years.

    Returns:
    - str: The HTML string to embed the Plotly graph in the web page.
    """
    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    
    # Lists to store year-wise invested amounts and maturity values
    invested_amounts = []
    maturity_values = []
    profits = []

    # Calculate invested amount and maturity value for each year
    for year in range(1, total_years + 1):
        # Total number of monthly payments for the current year
        total_payments = 12 * year
        
        # SIP maturity formula for the current year
        maturity_value = investment_amount * (
            ((1 + monthly_interest_rate) ** total_payments - 1) / monthly_interest_rate
        ) * (1 + monthly_interest_rate)
        
        # Calculate invested amount (Total amount invested by the end of the year)
        invested_amount = investment_amount * total_payments
        
        # Round the maturity value to the nearest integer
        maturity_value_rounded = round(maturity_value)
        profit = maturity_value_rounded - invested_amount
        
        # Append invested amount and maturity value to the lists
        invested_amounts.append(invested_amount)
        maturity_values.append(maturity_value_rounded)
        profits.append(profit)

    # Extract years for plotting
    years = [year for year in range(1, total_years + 1)]

    # Create an interactive stacked bar plot using Plotly
    fig = go.Figure()

    # Add bar for invested amount
    fig.add_trace(go.Bar(
        x=years, 
        y=invested_amounts,
        name="Amount Invested",
        marker=dict(color='royalblue'),  
    ))

    # Add bar for maturity value
    fig.add_trace(go.Bar(
        x=years, 
        y=profits,
        name="Profit Earned",
        marker=dict(color='turquoise'), 
    ))

    # Add style to plot
    fig.update_layout(
        title=f"Year-on-Year Investment and Maturity Amount for SIP",
        xaxis_title="Year",
        yaxis_title="Amount (INR)",
        template='plotly',  # Default light theme for a clean, modern look
        plot_bgcolor='white',  # White background for a clean, minimal look
        font=dict(color='black'),  # Black font for labels and title
        hovermode="closest",  # Hover effect to show closest data point
        barmode='stack',  # Stack the bars
        width=1200,  # Set width to 1000px (10 inches approx.)
        height=600,  # Set height to 1000px (10 inches approx.)
        xaxis=dict(
            tickvals=years,  # Specify the x-axis values
            ticktext=[f"{int(year):,}" for year in years],  # Format each year value with commas
        ),
        legend=dict(
            x=0.05,  # Position the legend on the left
            y=0.95,  # Position the legend at the top
            traceorder='normal',
            orientation='v',  # Horizontal legend
            bgcolor='rgba(255, 255, 255, 0)',  # Transparent background for the legend box
            bordercolor='rgba(255, 255, 255, 0)',  # No border around the legend
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="black"
            )
        )
    )

    # Add annotation for the maturity value slightly above the last bar (last year)
    last_year = total_years
    last_year_maturity_value = maturity_values[-1]  # Get maturity value for the last year
    formatted_maturity_value = f"₹ {last_year_maturity_value:,}"  # Format with commas
    
    fig.add_annotation(
        x=last_year,  # Position annotation at the last year
        y=maturity_values[-1] + 0.05 * maturity_values[-1],  # Position it slightly above the last bar
        text=formatted_maturity_value,  # Display the formatted maturity value
        showarrow=False,  # No arrow for this annotation
        font=dict(size=14, color='black', weight='bold'),  # Font style for the annotation text
        bgcolor='white',  # Background color for the annotation
    )

    # Generate the HTML to embed the plot
    plot_html = pio.to_html(fig, full_html=False)

    return plot_html
