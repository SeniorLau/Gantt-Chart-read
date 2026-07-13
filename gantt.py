import plotly.express as px
import pandas as pd


def make_gantt(df):

    df = df.copy()

    # Convert progress to number
    df["Progress_num"] = (
        df["Progress"]
        .astype(str)
        .str.replace("%", "")
        .astype(float)
    )

    # Make one-day tasks visible
    df["Display_Finish"] = df["Finish"]

    one_day = df["Start"] == df["Finish"]

    df.loc[one_day, "Display_Finish"] = (
        df.loc[one_day, "Finish"]
        + pd.Timedelta(hours=12)
    )

    # Create color category
    df["Color"] = df["Assigned"].astype(str)

    # Completed tasks become green
    df.loc[
        df["Progress_num"] >= 100,
        "Color"
    ] = "✓ Completed"


    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Display_Finish",
        y="Task",
        color="Color",
        hover_data=[
            "Phase",
            "Assigned",
            "Progress",
            "Start",
            "Finish"
        ],
    )


    # Force completed color to green
    color_map = {
        "✓ Completed": "green"
    }

    fig.for_each_trace(
        lambda trace: trace.update(
            marker_color=color_map.get(
                trace.name,
                trace.marker.color
            )
        )
        if trace.name in color_map
        else None
    )


        fig.update_yaxes(
        autorange="reversed",
        tickfont=dict(size=10),
        showgrid=True,
        gridwidth=1
    )


    fig.update_xaxes(
        dtick="D1",                  # every day
        tickformat="%d\n%b",          # day + month
        tickfont=dict(size=9),

        showgrid=True,
        gridwidth=1,

        minor=dict(
            showgrid=True,
            dtick=12*60*60*1000
        )
    )


    fig.update_layout(

        height=max(400, len(df)*32),

        margin=dict(
            l=170,
            r=20,
            t=40,
            b=60
        ),

        bargap=0.25,

        plot_bgcolor="white",

        legend_title_text="Assigned",

        hovermode="closest"
    )


    return fig
