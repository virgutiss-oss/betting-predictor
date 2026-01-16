@app.route("/", methods=["GET", "POST"])
def index():
    home_prob = None
    away_prob = None

    if request.method == "POST":
        sport = request.form["sport"]
        home = request.form["home"]
        away = request.form["away"]

        home_prob, away_prob = predict(sport, home, away)

    return render_template(
        "index.html",
        home_prob=home_prob,
        away_prob=away_prob
    )
