from flask import Flask, request, jsonify, render_template
from formulas import calculate_sip, calculate_year_on_year_maturity_interactive

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculate():
    if request.method == "GET":
        # Render the HTML form on GET request
        return render_template("index.html")
    
    if request.method == "POST":
        # Traditional form submission (if still needed)
        data = request.form
        investment_amount = data["investment_amount"]
        annual_interest_rate = data["annual_interest_rate"]
        time_period_years = data["time_period_years"]
        
        # Generate the interactive plot
        plot_html = calculate_year_on_year_maturity_interactive(investment_amount, annual_interest_rate, time_period_years)
        
        # Return the page with plot
        return render_template("index.html", plot_html=plot_html)
    
    return render_template("index.html", plot_html=None)


@app.route("/update_plot", methods=["POST"])
def update_plot():
    # Handle the AJAX request to update the plot without reloading the page
    data = request.get_json()  # Get JSON data sent from the front-end
    
    investment_amount = float(data.get("investment_amount"))
    annual_interest_rate = float(data.get("annual_interest_rate"))
    time_period_years = int(data.get("time_period_years"))
    
    # Generate the plot based on the data
    plot_html = calculate_year_on_year_maturity_interactive(investment_amount, annual_interest_rate, time_period_years)
    
    # Send the plot HTML back as a JSON response
    return jsonify({"plot_html": plot_html})


if __name__ == "__main__":
    app.run(debug=True)
