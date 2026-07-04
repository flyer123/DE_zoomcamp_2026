"""
# NYC Taxi Data Analysis

This marimo notebook analyzes NYC taxi trip data loaded via dlt pipeline.
"""

import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import duckdb
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    return duckdb, go, mo, pd, px


@app.cell
def __(mo):
    # Title - always visible
    return mo.md("# NYC Taxi Data Analysis")


@app.cell
def __(duckdb):
    conn = duckdb.connect('taxi_pipeline.duckdb')
    return (conn,)


@app.cell
def __(conn, mo):
    df = conn.execute("SELECT * FROM taxi_data.taxi_data").df()
    return mo.md(f"**Loaded {len(df):,} trips** from DuckDB."), df


@app.cell
def __(mo):
    return mo.md("## Dataset overview")


@app.cell
def __(df, mo):
    start = df['trip_pickup_date_time'].min()
    end = df['trip_pickup_date_time'].max()
    return mo.vstack([
        mo.md(f"- **Total trips:** {len(df):,}"),
        mo.md(f"- **Date range:** {start} to {end}"),
        mo.md("- **Columns:** " + ", ".join(df.columns.astype(str))),
    ]), end, start


@app.cell
def __(mo):
    return mo.md("## Payment type distribution")


@app.cell
def __(df):
    payment_counts = df['payment_type'].value_counts()
    return (payment_counts,)


@app.cell
def __(payment_counts):
    payment_counts
    return


@app.cell
def __(df, px):
    fig_payment_pie = px.pie(
        values=df['payment_type'].value_counts().values,
        names=df['payment_type'].value_counts().index,
        title="Payment Type Distribution",
    )
    fig_payment_pie
    return (fig_payment_pie,)


@app.cell
def __(df, mo):
    total_tips = df['tip_amt'].sum()
    return mo.md(f"## Tips — **Total: ${total_tips:,.2f}**"), total_tips


@app.cell
def __(df):
    tips_by_payment = df.groupby('payment_type')['tip_amt'].agg(['sum', 'mean', 'count'])
    tips_by_payment.columns = ['Total Tips', 'Average Tip', 'Trip Count']
    tips_by_payment
    return (tips_by_payment,)


@app.cell
def __(df, px):
    tips_avg = df.groupby('payment_type')['tip_amt'].mean().sort_values(ascending=False)
    fig_tips_bar = px.bar(
        x=tips_avg.index,
        y=tips_avg.values,
        title="Average Tip by Payment Type",
        labels={'x': 'Payment Type', 'y': 'Average Tip ($)'},
    )
    fig_tips_bar
    return (fig_tips_bar, tips_avg)


@app.cell
def __(df, pd):
    df['pickup_date'] = pd.to_datetime(df['trip_pickup_date_time'])
    df['day_of_week'] = df['pickup_date'].dt.day_name()
    df['hour'] = df['pickup_date'].dt.hour
    return (df,)


@app.cell
def __(mo):
    return mo.md("## Trips by day of week")


@app.cell
def __(df, px):
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    by_day = df['day_of_week'].value_counts().reindex(day_order, fill_value=0)
    fig_day = px.bar(
        x=by_day.index,
        y=by_day.values,
        title="Trips by Day of Week",
        labels={'x': 'Day', 'y': 'Trips'},
    )
    fig_day
    return (by_day, day_order, fig_day)


@app.cell
def __(mo):
    return mo.md("## Trips by hour of day")


@app.cell
def __(df, px):
    by_hour = df['hour'].value_counts().sort_index()
    fig_hour = px.line(
        x=by_hour.index,
        y=by_hour.values,
        title="Trips by Hour",
        labels={'x': 'Hour', 'y': 'Trips'},
        markers=True,
    )
    fig_hour
    return (by_hour, fig_hour)


@app.cell
def __(df, mo):
    total_revenue = df['total_amt'].sum()
    return mo.md(f"## Revenue — **Total: ${total_revenue:,.2f}**"), total_revenue


@app.cell
def __(df, px):
    fig_dist = px.histogram(
        df,
        x='trip_distance',
        nbins=50,
        title="Trip distance distribution",
        labels={'trip_distance': 'Distance (miles)', 'count': 'Trips'},
    )
    fig_dist
    return (fig_dist,)


@app.cell
def __(df, px):
    sample = df.sample(min(1000, len(df)))
    fig_scatter = px.scatter(
        sample,
        x='trip_distance',
        y='total_amt',
        color='payment_type',
        title="Trip distance vs total amount",
        labels={'trip_distance': 'Distance (miles)', 'total_amt': 'Total ($)'},
        hover_data=['passenger_count'],
    )
    fig_scatter
    return (fig_scatter, sample)


@app.cell
def __(mo):
    return mo.md("## Daily revenue (SQL)")


@app.cell
def __(conn):
    daily_revenue = conn.execute("""
        SELECT
            DATE(trip_pickup_date_time) as date,
            COUNT(*) as trip_count,
            SUM(total_amt) as daily_revenue,
            SUM(tip_amt) as daily_tips
        FROM taxi_data.taxi_data
        GROUP BY DATE(trip_pickup_date_time)
        ORDER BY date
    """).df()
    daily_revenue
    return (daily_revenue,)


@app.cell
def __(daily_revenue, px):
    fig_daily = px.line(
        daily_revenue,
        x='date',
        y='daily_revenue',
        title="Daily revenue over time",
        labels={'date': 'Date', 'daily_revenue': 'Revenue ($)'},
        markers=True,
    )
    fig_daily
    return (fig_daily,)


@app.cell
def __(mo):
    return mo.md("## Summary statistics")


@app.cell
def __(df):
    summary = df[['fare_amt', 'tip_amt', 'tolls_amt', 'total_amt', 'trip_distance']].describe()
    summary
    return (summary,)


@app.cell
def __(conn):
    conn.close()
    return


if __name__ == "__main__":
    app.run()
