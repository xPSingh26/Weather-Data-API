from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def data(station, date):
    filename = "TG_STAID" + station.zfill(6)

    df = pd.read_csv(rf"Weather Data/Data/{filename}.txt", skiprows=20,
                     parse_dates=['    DATE'])

    df["TG0"] = df['   TG'].mask(df['   TG'] == -9999, np.nan) / 10

    temp = df.loc[df['    DATE'] == date]['TG0'].squeeze()
    return {"station": station,
            "date": date,
            "temperature": temp}


if __name__ == "__main__":
    app.run(debug=True)
