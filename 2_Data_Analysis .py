import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("IPL Data Visualization")

df = pd.read_csv(r"C:\Users\User\Desktop\IPL_streamlit_project\IPL_Matches_Data_2008_2026.csv")

df["total_runs"] = (
    df["team1_runs"] +
    df["team2_runs"]
)

# Bar Chart

season_matches = (
    df.groupby("season")
    .size()
    .reset_index(name="matches")
)

st.bar_chart(
    season_matches.set_index("season")
)

# Line Chart

season_runs = (
    df.groupby("season")["total_runs"]
    .sum()
    .reset_index()
)

st.line_chart(
    season_runs.set_index("season")
)

# Interactive Plotly Chart
# Top Winning Teams

wins = (
    df["winner"]
    .value_counts()
    .head(10)
    .reset_index()
)

wins.columns = [
    "Team",
    "Wins"
]

fig = px.bar(
    wins,
    x="Team",
    y="Wins",
    title="Top Winning Teams"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Pie Chart

toss_decision = (
    df["toss_decision"]
    .value_counts()
    .reset_index()
)

toss_decision.columns = [
    "Decision",
    "Count"
]

fig = px.pie(
    toss_decision,
    names="Decision",
    values="Count",
    title="Toss Decision Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Histogram

fig = px.histogram(
    df,
    x="total_runs",
    nbins=30,
    title="Distribution of Total Match Runs"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Scatter Plot

fig = px.scatter(
    df,
    x="team1_runs",
    y="team2_runs",
    title="Team 1 Runs vs Team 2 Runs"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Matplotlib

fig, ax = plt.subplots()

ax.hist(
    df["total_runs"].dropna(),
    bins=30
)

ax.set_title(
    "Distribution of Match Runs"
)

ax.set_xlabel(
    "Total Runs"
)

ax.set_ylabel(
    "Number of Matches"
)

st.pyplot(fig)

# Layout Control

col1, col2 = st.columns(2)

with col1:

    st.subheader("Season Analysis")

    st.bar_chart(
        season_matches.set_index("season")
    )

with col2:

    st.subheader("Run Analysis")

    st.line_chart(
        season_runs.set_index("season")
    )

# Three Columns

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Matches",
        len(df)
    )

with col2:

    st.metric(
        "Seasons",
        df["season"].nunique()
    )

with col3:

    st.metric(
        "Venues",
        df["venue"].nunique()
    )

# Expanders

with st.expander("View Complete Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )

with st.expander("View Statistical Summary"):

    st.dataframe(
        df.describe()
    )