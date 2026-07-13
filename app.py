import streamlit as st

from parser import parse_excel
from gantt import make_gantt

st.set_page_config(
    page_title="Intelliphage Gantt",
    layout="wide"
)

st.title("📅 Intelliphage Gantt Dashboard")

uploaded = st.file_uploader(
    "Upload Excel",
    type=["xlsx"]
)

if uploaded:

    df = parse_excel(uploaded)

    st.sidebar.header("Filters")

    phases = st.sidebar.multiselect(
        "Phase",
        sorted(df["Phase"].dropna().unique()),
        default=sorted(df["Phase"].dropna().unique())
    )

    people = st.sidebar.multiselect(
        "Assigned",
        sorted(df["Assigned"].dropna().unique()),
        default=sorted(df["Assigned"].dropna().unique())
    )

    df = df[
        df["Phase"].isin(phases)
    ]

    df = df[
        df["Assigned"].isin(people)
    ]

    color = st.sidebar.radio(
        "Color by",
        [
            "Assigned",
            "Phase",
        ]
    )

    fig = make_gantt(df)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(df)
