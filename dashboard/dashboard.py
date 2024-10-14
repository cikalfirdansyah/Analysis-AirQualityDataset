import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    data_dongsi = pd.read_csv('data/data_1.csv')
    data_dingling = pd.read_csv('data/data_2.csv')
    return data_dongsi, data_dingling

# Main dashboard
def main():
    st.title("Analisis Data Kualitas Udara")
    
    # Load the data
    data_dongsi, data_dingling = load_data()
    
    # Display dataset info
    st.header("Informasi Dataset Dongsi")
    st.write(data_dongsi.info())
    
    st.header("Informasi Dataset Dingling")
    st.write(data_dingling.info())

    # Visualisasi Distribusi PM2.5
    st.header("Distribusi Konsentrasi PM2.5")
    plt.figure(figsize=(10, 5))
    sns.histplot(data_dongsi['PM2.5'], bins=50, color='blue', kde=True, label='Dongsi')
    sns.histplot(data_dingling['PM2.5'], bins=50, color='orange', kde=True, label='Dingling')
    plt.title('Distribusi PM2.5 di Dongsi dan Dingling')
    plt.xlabel('Konsentrasi PM2.5')
    plt.ylabel('Frekuensi')
    plt.legend()
    st.pyplot(plt)

    # Visualisasi Musiman PM2.5
    st.header("Musiman dari PM2.5")
    data_dongsi['month'] = pd.to_datetime(data_dongsi[['year', 'month', 'day']]).dt.month
    data_dingling['month'] = pd.to_datetime(data_dingling[['year', 'month', 'day']]).dt.month
    monthly_dongsi = data_dongsi.groupby('month')['PM2.5'].mean()
    monthly_dingling = data_dingling.groupby('month')['PM2.5'].mean()

    plt.figure(figsize=(10, 5))
    monthly_dongsi.plot(kind='bar', color='blue', label='Dongsi', alpha=0.6)
    monthly_dingling.plot(kind='bar', color='orange', label='Dingling', alpha=0.6)
    plt.title('Rata-rata Bulanan PM2.5')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata PM2.5')
    plt.xticks(rotation=0)
    plt.legend()
    st.pyplot(plt)

if __name__ == "__main__":
    main()