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
        tickfont=dict(size=10)
    )


    fig.update_layout(
        height=max(350, len(df)*30),

        margin=dict(
            l=160,
            r=10,
            t=25,
            b=30
        ),

        xaxis=dict(
            tickformat="%d/%m",
            tickfont=dict(size=10)
        ),

        bargap=0.25,

        legend_title_text="Assigned"
    )


    return fig
