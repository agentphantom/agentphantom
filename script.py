from datetime import datetime

import plotly.graph_objects as go
import requests


# 24 Hours API.
URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"


def main():

    # We request the data from the API.
    with requests.get(URL) as response:

        data = response.json()
        print("Data fetched.")

        earthquakes = list()

        # We iterate over all items and extract the values we are interested in.
        for item in data["features"]:

            magnitude = item["properties"]["mag"]
            place = item["properties"]["place"]
            url = item["properties"]["url"]
            time = datetime.fromtimestamp(item["properties"]["time"] / 1000)
            formatted_time = f"{time:%m-%d-%Y %H:%M:%S}"
            lon = item["geometry"]["coordinates"][0]
            lat = item["geometry"]["coordinates"][1]

            earthquakes.append(
                [magnitude, place, url, formatted_time, lon, lat])

        # We sort the earthquakes by their magnitude (first column).
        earthquakes.sort(reverse=True)

        # We initiate our Markdown text.
        markdown = "![Map](./map.png)\n\n# Top 20 Strongest Earthquakes in the Past 24 Hours\n\n| Location | Mag | Date and Time (UTC) |\n|:---|:---|:---|\n"

        # These lists will be used to feed the scatter map.
        longitudes = list()
        latitudes = list()

        # We only take the top 20 records using list indexing.
        for item in earthquakes[:20]:
            markdown += f"| [{item[1]}]({item[2]}) | {item[0]} | {item[3]} |\n"
            longitudes.append(item[4])
            latitudes.append(item[5])

        # Save Markdown to file.
        open("./README.md", "w", encoding="utf-8").write(markdown)

        fig = go.Figure()

        # We create the scatter map, it is really simple to do as most
        # of the parameters are just visual customizations.
        fig.add_traces(go.Scattergeo(lon=longitudes, lat=latitudes,
                                     mode="markers", marker_color="gold", marker_size=10))

        fig.update_geos(showocean=True, oceancolor="#263238", showlakes=False,
                        showcountries=True, countrycolor="#FFFFFF", countrywidth=0.5,
                        framecolor="#FFFFFF", framewidth=1.5, coastlinewidth=0, landcolor="#1B2327")

        # Add final customizations.
        fig.update_layout(
            font_color="#FFFFFF",
            margin={"r": 20, "t": 20, "l": 20, "b": 0},
            width=1200,
            height=770,
            paper_bgcolor="#232b2b",
            annotations=[
                dict(
                    x=0.5,
                    y=-0.0,
                    yanchor="bottom",
                    text=f"Source: USGS API | Last updated: {datetime.now():%m-%d-%Y @ %H:%M:%S}",
                    font_size=26
                ),
                dict(
                    x=0.5,
                    y=0.91,
                    text="Top 20 Strongest Earthquakes in the Past 24 Hours",
                    font_size=32
                )
            ]
        )

        fig.write_image("./map.png")
        print("Map created.")


if __name__ == "__main__":

    main()
