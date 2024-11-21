import pandas as pd

def load_and_prepare_data(file_path):
    data = pd.read_csv(file_path, encoding='Windows-1252', sep=';', skiprows=1)
    data.columns = [col.strip() for col in data.columns]
    data.rename(columns={'Megnevezés': 'Jövedelem_típus', 'Ország összesen': 'Ország összesen'}, inplace=True)

    # Évszámok azonosítása
    year_rows = data.iloc[:, 0].str.isdigit()
    data['Év'] = None
    data.loc[year_rows, 'Év'] = data.loc[year_rows, data.columns[0]]
    data['Év'] = data['Év'].ffill()

    # Csak releváns sorok megtartása
    data = data[~year_rows]
    data = data[data['Jövedelem_típus'].isin(['Bruttó jövedelem', 'Nettó jövedelem'])]

    # Numerikus oszlopok konvertálása
    numeric_columns = [col for col in data.columns if col not in ['Jövedelem_típus', 'Év']]
    for col in numeric_columns:
        data[col] = data[col].replace({' ': '', '…': '0'}, regex=True).str.replace(',', '').astype(float)

    # Év oszlop numerikussá alakítása
    data['Év'] = pd.to_numeric(data['Év'], errors='coerce')

    # Hiányzó évek pótlása
    all_years = pd.Series(range(int(data['Év'].min()), int(data['Év'].max()) + 1))
    missing_years = all_years[~all_years.isin(data['Év'])]

    # Üres sorok létrehozása
    empty_rows = []
    for year in missing_years:
        for income_type in ['Bruttó jövedelem', 'Nettó jövedelem']:
            empty_rows.append({'Jövedelem_típus': income_type, 'Év': year})

    empty_df = pd.DataFrame(empty_rows)
    data = pd.concat([data, empty_df], ignore_index=True)
    data = data.sort_values(by='Év').reset_index(drop=True)

    return data
