import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    dongsi_data = pd.read_csv('data/PRSA_Data_Dongsi_20130301-20170228.csv')
    dingling_data = pd.read_csv('data/PRSA_Data_Dingling_20130301-20170228.csv')
    dongsi_data['date'] = pd.to_datetime(dongsi_data[['year', 'month', 'day', 'hour']])
    dingling_data['date'] = pd.to_datetime(dingling_data[['year', 'month', 'day', 'hour']])
    return dongsi_data, dingling_data

# Main dashboard
def main():
    st.title("Dashboard Analisis Kualitas Udara")

    # Introduction
    st.markdown("""
    ### Pertanyaan Bisnis:
    1. Apakah ada perbedaan yang signifikan dalam distribusi PM2.5 antara wilayah Dongsi dan Dingling?
    2. Bagaimana pola musiman konsentrasi PM2.5 di wilayah Dongsi dan Dingling?
    3. Bagaimana pengaruh suhu (TEMP), curah hujan (RAIN), kecepatan angin (WSPM), dan tekanan udara (PRES) terhadap konsentrasi PM2.5?
    """)

    # Load the data
    dongsi_data, dingling_data = load_data()

    # Sidebar filters
    st.sidebar.header("Filter Data")
    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        [dongsi_data['date'].min(), dongsi_data['date'].max()],
        min_value=dongsi_data['date'].min(),
        max_value=dongsi_data['date'].max()
    )

    selected_region = st.sidebar.multiselect(
        "Pilih Wilayah", ['Dongsi', 'Dingling'], default=['Dongsi', 'Dingling']
    )

    # Filter data based on selections
    filtered_dongsi = dongsi_data[(dongsi_data['date'] >= pd.to_datetime(date_range[0])) &
                                  (dongsi_data['date'] <= pd.to_datetime(date_range[1]))]
    filtered_dingling = dingling_data[(dingling_data['date'] >= pd.to_datetime(date_range[0])) &
                                      (dingling_data['date'] <= pd.to_datetime(date_range[1]))]

    # Question 1: Distribution of PM2.5
    if 'Dongsi' in selected_region and 'Dingling' in selected_region:
        st.subheader("Distribusi PM2.5 di Dongsi dan Dingling")
        plt.figure(figsize=(10, 5))
        sns.histplot(filtered_dongsi['PM2.5'], bins=30, color='blue', label='Dongsi', kde=True)
        sns.histplot(filtered_dingling['PM2.5'], bins=30, color='red', label='Dingling', kde=True)
        plt.title('Distribusi PM2.5 di Dongsi dan Dingling')
        plt.xlabel('Konsentrasi PM2.5')
        plt.ylabel('Frekuensi')
        plt.legend()
        st.pyplot(plt)

    # Question 2: Seasonal Trends of PM2.5
    st.subheader("Pola Musiman PM2.5")
    dongsi_monthly = filtered_dongsi.groupby(filtered_dongsi['date'].dt.month)['PM2.5'].mean()
    dingling_monthly = filtered_dingling.groupby(filtered_dingling['date'].dt.month)['PM2.5'].mean()

    plt.figure(figsize=(10, 5))
    plt.plot(dongsi_monthly.index, dongsi_monthly.values, marker='o', label='Dongsi', color='blue')
    plt.plot(dingling_monthly.index, dingling_monthly.values, marker='o', label='Dingling', color='red')
    plt.title('Rata-rata Bulanan PM2.5')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata PM2.5')
    plt.xticks(range(1, 13))
    plt.legend()
    plt.grid()
    st.pyplot(plt)

    # Question 3: Weather Factors and PM2.5
    st.subheader("Pengaruh Faktor Cuaca terhadap PM2.5")
    factor = st.selectbox("Pilih Faktor Cuaca", ['TEMP', 'RAIN', 'WSPM', 'PRES'])

    plt.figure(figsize=(10, 5))
    sns.scatterplot(data=filtered_dongsi, x=factor, y='PM2.5', color='blue', label='Dongsi')
    sns.scatterplot(data=filtered_dingling, x=factor, y='PM2.5', color='red', label='Dingling')
    plt.title(f'Pengaruh {factor} terhadap PM2.5 di Dongsi dan Dingling')
    plt.xlabel(factor)
    plt.ylabel('Konsentrasi PM2.5')
    plt.legend()
    plt.grid()
    st.pyplot(plt)

if __name__ == "__main__":
    main()