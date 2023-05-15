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

# Drop the specified columns
df_dropped = df_train.drop(['time_in_cycles', 'unit_ID'], axis=1)

# Calculate the standard deviation of each column
std_dev = df_dropped.std()

# Sort the columns by their standard deviation, in descending order
sorted_columns = std_dev.sort_values(ascending=False)

# Get the names of the first four columns
selected_columns = sorted_columns.index[:4]

myfunction.plot_selected_columns(df_test, selected_unit_id, selected_columns, selected_columns)

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
