import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import glob

st.title("📈 IPL Data Visualization")

# Find CSV automatically
csv_files = glob.glob("*.csv")

if not csv_files:
    st.error("CSV dataset not found in the project folder.")
    st.stop()

df = pd.read_csv(r"C:\Users\User\Desktop\IPL_streamlit_project\IPL_Matches_Data_2008_2026.csv")

# Create total runs
if "team1_runs" in df.columns and "team2_runs" in df.columns:

    df["total_runs"] = (
        pd.to_numeric(df["team1_runs"], errors="coerce").fillna(0)
        + pd.to_numeric(df["team2_runs"], errors="coerce").fillna(0)
    )

# Sidebar
st.sidebar.title("🎛️ Filters")

if "season" in df.columns:

    seasons = sorted(df["season"].dropna().unique())

    selected_season = st.sidebar.selectbox(
        "Season",
        ["All Seasons"] + list(seasons)
    )

else:
    selected_season = "All Seasons"

filtered_df = df.copy()

if selected_season != "All Seasons":
    filtered_df = filtered_df[
        filtered_df["season"] == selected_season
    ]

st.subheader(
    f"Analysis for Season: {selected_season}"
)

# KPI section
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Matches", len(filtered_df))

with col2:
    if "total_runs" in filtered_df.columns:
        st.metric(
            "Average Runs",
            round(filtered_df["total_runs"].mean(), 2)
        )

with col3:
    if "total_runs" in filtered_df.columns:
        st.metric(
            "Highest Score",
            int(filtered_df["total_runs"].max())
        )

# -----------------------------
# BAR CHART
# -----------------------------

st.subheader("🏆 Top Winning Teams")

if "winner" in filtered_df.columns:

    wins = (
        filtered_df["winner"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    wins.columns = ["Team", "Wins"]

    fig1 = px.bar(
        wins,
        x="Team",
        y="Wins",
        title="Top Winning Teams"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# -----------------------------
# LINE CHART
# -----------------------------

st.subheader("📅 Matches by Season")

if "season" in df.columns:

    season_matches = (
        df.groupby("season")
        .size()
        .reset_index(name="Matches")
    )

    fig2 = px.line(
        season_matches,
        x="season",
        y="Matches",
        markers=True,
        title="Matches by Season"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -----------------------------
# PIE CHART
# -----------------------------

st.subheader("🪙 Toss Decision Distribution")

if "toss_decision" in filtered_df.columns:

    toss_decision = (
        filtered_df["toss_decision"]
        .value_counts()
        .reset_index()
    )

    toss_decision.columns = ["Decision", "Count"]

    fig3 = px.pie(
        toss_decision,
        names="Decision",
        values="Count",
        title="Toss Decision Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# -----------------------------
# HISTOGRAM
# -----------------------------

st.subheader("📊 Distribution of Total Match Runs")

if "total_runs" in filtered_df.columns:

    fig4 = px.histogram(
        filtered_df,
        x="total_runs",
        nbins=30,
        title="Distribution of Total Match Runs"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# -----------------------------
# SCATTER PLOT
# -----------------------------

st.subheader("🔵 Team 1 Runs vs Team 2 Runs")

if "team1_runs" in filtered_df.columns and "team2_runs" in filtered_df.columns:

    fig5 = px.scatter(
        filtered_df,
        x="team1_runs",
        y="team2_runs",
        title="Team 1 Runs vs Team 2 Runs"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# -----------------------------
# MATPLOTLIB
# -----------------------------

st.subheader("📉 Match Run Distribution - Matplotlib")

if "total_runs" in filtered_df.columns:

    fig, ax = plt.subplots()

    ax.hist(
        filtered_df["total_runs"].dropna(),
        bins=30
    )

    ax.set_title("Distribution of Match Runs")
    ax.set_xlabel("Total Runs")
    ax.set_ylabel("Number of Matches")

    st.pyplot(fig)

# -----------------------------
# COMPLETE DATA
# -----------------------------

with st.expander("📋 View Complete Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )