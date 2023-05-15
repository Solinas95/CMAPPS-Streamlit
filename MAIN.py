import myfunction
import streamlit as st
#streamlit run ALB/MAIN.py

train_data_file = st.file_uploader("Upload Normal process Data (txt)", type="txt")
if test_data_file is not None:
    df_train = load_data(train_data_file)
    st.write("Normal Data:")


test_data_file = st.file_uploader("Upload Test Data (txt)", type="txt")
if test_data_file is not None:
    df_test = load_data(test_data_file)
    st.write("Test Data:")
    st.write(df_test.shape)
    st.write(df_test.describe())



    

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
df_dropped = test.drop(['time_in_cycles', 'unit_ID'], axis=1)

# Calculate the standard deviation of each column
std_dev = df_dropped.std()

# Sort the columns by their standard deviation, in descending order
sorted_columns = std_dev.sort_values(ascending=False)

# Get the names of the first four columns
selected_columns = sorted_columns.index[:4]

myfunction.plot_selected_columns(test, selected_unit_id, selected_columns)

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
#myfunction.plot_sensor_data(test, filtered_data)

#######################################################

# NORMALIZZAZIONE COLONNE DATASET DI TEST + CREAZIONE cycle_norm
cols_to_exclude = ['unit_ID','time_in_cycles']
df_test_normalized = myfunction.normalize_test_columns(test, cols_to_exclude)
#st.dataframe(df_test_normalized.head(10))
