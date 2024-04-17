from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)
stations = pd.read_csv("Weather Data/Data/stations.txt", skiprows=17)
stations = stations[["STAID","STANAME                                 "]][0:100]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


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


@app.route("/api/v1/<station>")
def stat_data(station):
    filename = "TG_STAID" + station.zfill(6)

    df = pd.read_csv(rf"Weather Data/Data/{filename}.txt", skiprows=20,
                     parse_dates=['    DATE'])

    df["TG0"] = df['   TG'].mask(df['   TG'] == -9999, np.nan) / 10
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def year_data(station, year):
    filename = "TG_STAID" + station.zfill(6)
    df = pd.read_csv(rf"Weather Data/Data/{filename}.txt", skiprows=20,)
    df["    DATE"] = df["    DATE"].astype(str)
    df["TG0"] = df['   TG'].mask(df['   TG'] == -9999, np.nan) / 10
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")

    return result


if __name__ == "__main__":
    app.run(debug=True)
