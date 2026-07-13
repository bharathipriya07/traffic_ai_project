from flask import Flask, render_template, request, url_for
from database import create_table, insert_challan, fetch_violations, fetch_totals

app = Flask(__name__)
app.config["SECRET_KEY"] = "traffic_ai_dashboard_secret"


def bootstrap_database():
    create_table()

    # Add sample record if empty
    rows = fetch_violations()
    if len(rows) == 0:
        insert_challan("KA01AB1234", "Over-speeding", 1000, "speeding.jpg")
        insert_challan("MH02CD5678", "Signal Jump", 1500, "signal_jump.jpg")
        insert_challan("DL05EF9012", "Helmet violation", 500, "helmet.jpg")


@app.route("/")
def dashboard():
    search_value = request.args.get("vehicle", "")

    data = fetch_violations(search_value.strip())
    totals = fetch_totals(search_value.strip())

    return render_template(
        "index.html",
        data=data,
        totals=totals,
        search_value=search_value,
    )


@app.route("/api/violations")
def api_violations():
    search_value = request.args.get("vehicle", "")
    data = fetch_violations(search_value.strip())
    totals = fetch_totals(search_value.strip())

    return {
        "data": data,
        "totals": totals,
    }


if __name__ == "__main__":
    bootstrap_database()
    app.run(debug=True, host="0.0.0.0", port=5000)

