import myfunction
import streamlit as st
#streamlit run ALB/MAIN.py

# IMPORTO DATASET
url_TRAIN = "https://raw.githubusercontent.com/ashfu96/ALB/main/train_FD001.txt"
url_TEST = "https://raw.githubusercontent.com/ashfu96/ALB/main/test_FD001.txt"
url_RUL = "https://raw.githubusercontent.com/ashfu96/ALB/main/RUL_FD001.txt"

df_train, df_test, df_rul = myfunction.read_data_from_github(url_TRAIN, url_TEST, url_RUL)

# RIMUOVO NaN
df_train, df_test, df_rul = myfunction.remove_nan_columns(df_train, df_test, df_rul)

# RINOMINO COLONNE CON LABELS
columns = ['unit_ID','time_in_cycles','setting_1', 'setting_2','setting_3','T2','T24','T30','T50','P2','P15','P30','Nf','Nc','epr','Ps30','phi','NRf','NRc','BPR','farB','htBleed','Nf_dmd','PCNfR_dmd','W31','W32' ]

sensors = ['T2', 'T24', 'T30', 'T50', 'P2', 'P15', 'P30', 'Nf', 'Nc', 'epr','Ps30', 'phi', 'NRf', 'NRc', 'BPR', 'farB', 'htBleed', 'Nf_dmd','PCNfR_dmd', 'W31', 'W32']

settings = ['setting_1', 'setting_2','setting_3']

df_train, df_test = myfunction.rename_columns(df_train, df_test, columns)

# RIMOZIONE SENSORI CON DEVIAZIONE STANDARD = 0
train = myfunction.remove_zero_std_columns(df_train)
test = myfunction.remove_zero_std_columns(df_test)

# RIMOZIONE COLONNE CHE NON MI SERVONO ORA
columns_to_remove = ['setting_1', 'setting_2']
train, test = myfunction.remove_columns(train, test, columns_to_remove)

# PLOT DEI SENSORI CON STANDARD DEVIATION PIU' ELEVATA

# Ask the user for the unit_id
selected_unit_id = st.number_input('Please enter a unit ID', min_value=1, value=1)

import matplotlib.pyplot as plt
import numpy as np


def plot_selected_columns(df_train, selected_unit_id, selected_columns, sensors):
    # Filter the DataFrame for the selected unit ID
    df_selected_unit = df_train[df_train['unit_ID'] == selected_unit_id]
    
    # Define a list of colors
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    
    # Calculate the number of rows and columns for the grid
    num_plots = len(selected_columns)
    num_cols = int(np.ceil(np.sqrt(num_plots)))
    num_rows = int(np.ceil(num_plots / num_cols))
    
    # Create a figure and a grid of subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(6*num_cols, 6*num_rows))
    
    # Flatten the array of axes, for easier indexing
    axs = axs.flatten()
    
    # Plot each column
    for i, column in enumerate(selected_columns):
        axs[i].plot(df_selected_unit[column].values, color=colors[i % len(colors)], label=column)
        axs[i].set_title('Values of column "{}" for unit ID "{}"'.format(column, selected_unit_id))
        axs[i].set_xlabel('Count')
        axs[i].set_ylabel('Value')
        axs[i].legend()
    
    # Remove unused subplots
    for i in range(num_plots, num_rows*num_cols):
        fig.delaxes(axs[i])
    
    # Adjust the layout so that plots do not overlap
    plt.tight_layout()
    
    # Show the plot
    plt.show()

plot_selected_columns(df_test, selected_unit_id, sensors, sensors)

############################# PROVA PRINT TEST PREPROCESS #########################################
st.write("Preprocessed Test Data:")
st.write(test.head())

####### STREAMLIT #######

st.title("Visualizzazione dati sensori per unit_ID")
st.write("Analisi dati delle unità")

# Filtra il DataFrame in base all'unità selezionata
filtered_data = myfunction.filter_by_unit(test)

# Mostra il conteggio dei cicli per l'unità selezionata
results = myfunction.count_cycles_by_unit(filtered_data)
for result in results:
           st.write(result)

# Mostra il plot dell'andamento dei sensori per l'unità selezionata
myfunction.plot_sensor_data(test, filtered_data)

#######################################################

# NORMALIZZAZIONE COLONNE DATASET DI TEST + CREAZIONE cycle_norm
cols_to_exclude = ['unit_ID','time_in_cycles']
df_test_normalized = myfunction.normalize_test_columns(test, cols_to_exclude)
#st.dataframe(df_test_normalized.head(10))
