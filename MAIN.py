import myfunction
import streamlit as st
#streamlit run ALB/MAIN.py
# RINOMINO COLONNE CON LABELS


test_data_file = st.file_uploader("Upload Test Data (txt)", type="txt")
if test_data_file is not None:
    df_test = myfunction.load_data(test_data_file)
    df_test.dropna(axis=1, inplace=True)
    st.write("Test Data:")
    st.write(df_test.shape)
    columns = ['unit_ID','time_in_cycles','setting_1', 'setting_2','setting_3','T2','T24','T30','T50','P2','P15','P30','Nf','Nc','epr','Ps30','phi','NRf','NRc','BPR','farB','htBleed','Nf_dmd','PCNfR_dmd','W31','W32' ]

    sensors = ['T2', 'T24', 'T30', 'T50', 'P2', 'P15', 'P30', 'Nf', 'Nc', 'epr','Ps30', 'phi', 'NRf', 'NRc', 'BPR', 'farB', 'htBleed', 'Nf_dmd','PCNfR_dmd', 'W31', 'W32']

    settings = ['setting_1', 'setting_2','setting_3']

    # IMPORTO DATASET
    url_TRAIN = "https://raw.githubusercontent.com/ashfu96/ALB/main/train_FD001.txt"
    url_TEST = "https://raw.githubusercontent.com/ashfu96/ALB/main/test_FD001.txt"
    url_RUL = "https://raw.githubusercontent.com/ashfu96/ALB/main/RUL_FD001.txt"
    
    df_train, comparison_test, df_rul = myfunction.read_data_from_github(url_TRAIN, url_TEST, url_RUL)
    df_train.dropna(axis=1, inplace=True)
    df_train, df_test = myfunction.rename_columns(df_train, df_test, columns)
    st.write(df_test.describe())

    # RIMOZIONE SENSORI CON DEVIAZIONE STANDARD = 0
    train = myfunction.remove_zero_std_columns(df_train)
    test = myfunction.remove_zero_std_columns(df_test)

    # RIMOZIONE COLONNE CHE NON MI SERVONO ORA
    columns_to_remove = ['setting_1', 'setting_2']
    train, test = myfunction.remove_columns(train, test, columns_to_remove)
    
    
    st.title("Visualizzazione dati sensori per unit_ID")
    st.write("Analisi dati delle unità")
    # PLOT DEI SENSORI CON STANDARD DEVIATION PIU' ELEVATA
    unit_ids = df_test['unit_ID'].unique()
    # Ask the user for the unit_id
    selected_unit_id = st.sidebar.selectbox('Seleziona unit_ID', unit_ids)
    # Filtra il DataFrame in base all'unità selezionata
    filtered_data = myfunction.filter_by_unit(test,selected_unit_id)

    # Mostra il conteggio dei cicli per l'unità selezionata
    results = myfunction.count_cycles_by_unit(filtered_data)
    for result in results:
            st.write(result)



    # Drop the specified columns
    df_dropped = test.drop(['time_in_cycles', 'unit_ID'], axis=1)

    # Calculate the standard deviation of each column
    std_dev = df_dropped.std()

    # Sort the columns by their standard deviation, in descending order
    sorted_columns = std_dev.sort_values(ascending=False)

    # Get the names of the first four columns
    selected_columns = sorted_columns.index[:4]

    myfunction.plot_selected_columns(test, selected_unit_id, selected_columns)



    # NORMALIZZAZIONE COLONNE DATASET DI TEST + CREAZIONE cycle_norm
    cols_to_exclude = ['unit_ID','time_in_cycles']
    df_test_normalized = myfunction.normalize_test_columns(test, cols_to_exclude)
    #st.dataframe(df_test_normalized.head(10))

    
    # Plot the Hotelling's T-square for the specified unit_id
    unit_T_square_test=myfunction.plot_hotelling_tsquare(df_test, selected_unit_id,sensors)
    unit_T_square_train=myfunction.plot_hotelling_tsquare(df_train, selected_unit_id,sensors)

    myfunction.plot_hotelling_tsquare_comparison(df_train, df_test, selected_unit_id, sensors)
