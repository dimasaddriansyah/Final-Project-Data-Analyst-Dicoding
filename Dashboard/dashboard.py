import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_monthly(df):
    monthly_df = df.resample(rule='M', on='dteday').agg({
        "cnt": "sum"
    })

    monthly_df.index = monthly_df.index.strftime('%b %Y')
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={
        "cnt": "order_count"
    }, inplace=True)

    return monthly_df

def create_season_df(df):
    if df["season"].dtype != "object":
        df["season"] = df["season"].apply(lambda x: 
            "Springer" if x == 1 else
            "Summer" if x == 2 else
            "Fall" if x == 3 else 
            "Winter")

    season = df.groupby("season")["instant"].nunique().sort_values(ascending=False).reset_index()

    return season

def create_weathersit_df(df):
    if df["weathersit"].dtype != "object":
        df["weathersit"] = df["weathersit"].apply(lambda x: 
            "Clear, Few Clouds, Partly Cloudy, Partly Cloudy" if x == 1 else
            "Mist + Cloudy, Mist + Broken Clouds, Mist + Few Clouds, Mist" if x == 2 else
            "Light Snow, Light Rain + Thunderstorm + Scattered Clouds, Light Rain + Scattered Clouds" if x == 3 else 
            "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog")
    
    weathersit = df.groupby("weathersit")["instant"].nunique().sort_values(ascending=False).reset_index()
    
    return weathersit

df = pd.read_csv("main_data.csv")

df.head()

df.info()

df["dteday"] = pd.to_datetime(df["dteday"])

min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://marketplace.canva.com/EAE7g0N0S5Y/1/0/1600w/canva-bike-sport-store-logo-ywkEt_4j9Gc.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]

monthly_df = create_monthly(main_df)
season_df = create_season_df(main_df)
weathersit_df = create_weathersit_df(main_df)

st.header('Final Project Data Analysis:bike:')

## Monthly ##
st.subheader("Penyewaan Bulanan")

total_orders = monthly_df["order_count"].sum()
st.metric("Total orders", value=f"{total_orders:,}")

fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(monthly_df['dteday'], monthly_df['order_count'], marker='o', linestyle='-', linewidth=2, color='#72BCD4')

plt.xticks(rotation=45)

st.pyplot(fig)
## Monthly ##

## Musim ##
st.subheader("Penyewaan Paling Banyak dan Sedikit Berdasarkan Musim")
 
fig, ax = plt.subplots(
    nrows=1, 
    ncols=2, 
    figsize=(24, 6)
)
 
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(
    x="instant", 
    y="season", 
    data=season_df.head(5), 
    palette=colors, ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title(
    "Paling Banyak Penyewaan", 
    loc="center", 
    fontsize=15
)
ax[0].tick_params(axis ='y', labelsize=12)
 
sns.barplot(
    x="instant", 
    y="season", 
    data=season_df.sort_values(
        by="instant", 
        ascending=True).head(5), 
    palette=colors, 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title(
    "Paling Sedikit Penyewaan", 
    loc="center", 
    fontsize=15
)
ax[1].tick_params(axis='y', labelsize=12)
 
st.pyplot(fig)
## Musim ##

## Kondisi Cuaca ##
st.subheader("Penyewaan Paling Banyak dan Sedikit Berdasarkan Kondisi Cuaca")
 
fig, ax = plt.subplots(
    nrows=1, 
    ncols=2, 
    figsize=(24, 6)
)
 
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(
    x="instant", 
    y="weathersit", 
    data=weathersit_df.head(5), 
    palette=colors, ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title(
    "Paling Banyak Penyewaan", 
    loc="center", 
    fontsize=15
)
ax[0].tick_params(axis ='y', labelsize=12)
 
sns.barplot(
    x="instant", 
    y="weathersit", 
    data=weathersit_df.sort_values(
        by="instant", 
        ascending=True).head(5), 
    palette=colors, 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title(
    "Paling Sedikit Penyewaan", 
    loc="center", 
    fontsize=15
)
ax[1].tick_params(axis='y', labelsize=12)
 
st.pyplot(fig)
## Kondisi Cuaca ##


st.caption('Copyright © Dimas Addriansyah with Partner Dicoding 2024')
