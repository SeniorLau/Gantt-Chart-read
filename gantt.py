import plotly.express as px
import pandas as pd


def make_gantt(df):

    df = df.copy()

    # Convert progress to numeric %
    df["Progress_num"] = (
        df["Progress"]
        .astype(str)
        .str.replace("%", "")
        .astype(float)
    )

    # Create display finish date
    # One-day tasks get a small visible width
    df["Display_Finish"] = df["Finish"]

    one_day = df["Start"] == df["Finish"]

    df.loc[one_day, "Display_Finish"] = (
        df.loc[one_day, "Finish"]
        + pd.Timedelta(hours=12)
    )


    # Create status category
    def status(x):
        if x >= 100:
            return "Completed"
        elif x > 0:
            return "In progress"
        else:
            return "Not started"


    df["Status"] = df["Progress_num"].apply(status)


    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Display_Finish",
        y="Task",
        color="Status",
        hover_data=[
            "Phase",
            "Assigned",
            "Progress",
            "Start",
            "Finish"
        ],
        category_orders={
            "Status": [
                "Completed",
                "In progress",
                "Not started"
            ]
        }
    )


    fig.update_yaxes(
        autorange="reversed",
        tickfont=dict(size=10)
    )


    fig.update_layout(
        height=max(350, len(df)*30),

        margin=dict(
            l=150,
            r=10,
            t=25,
            b=30
        ),

        xaxis=dict(
            tickformat="%d/%m",
            tickfont=dict(size=10)
        ),

        bargap=0.25,

        legend_title_text="Status",

        showlegend=True
    )


    return fig
