import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
from agstyler import draw_grid


sheet_id = "1-SJVJmE85vHo8EUP1MBDmrK-pK7dSAdfnsByKrfoCRE"
sheet_name = "Items"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url)
df.drop(['Yield', 'Price', 'Size'], axis = 1, inplace = True)
df.fillna(0, inplace = True)

df.insert(loc = 2, column = "Metal RR", value = 100)
df.insert(loc = 3, column = "Min", value = None)
df.insert(loc = 4, column = "Max", value = None)

st.set_page_config(page_title="My dashboard", layout="wide", initial_sidebar_state="expanded")

f_name = st.text_input("Enter the foundry name")
f_name = f_name.split()
f_name = '_'.join(f_name)

if not f_name:
    st.stop()

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='multiple', use_checkbox=True)
gd.configure_default_column(editable = True, groupable = True)
gridoptions = gd.build()

formatter = {
    'Item Name': ('Item Name', {'width': 80, 'editable': True}),
    'Type': ('Type', {'width': 50, 'editable': True}),
    'Metal RR': ('Metal RR', {'width': 40, 'editable': True}),
    'Min': ('Min', {'width': 30, 'editable': True}),
    'Max': ('Max', {'width': 30, 'editable': True}),
    'C': ('C', {'width': 30, 'editable': True}),
    'Si': ('Si', {'width': 30, 'editable': True}),
    'Mn': ('Mn', {'width': 30, 'editable': True}),
    'S': ('S', {'width': 30, 'editable': True}),
    'P': ('P', {'width': 30, 'editable': True}),
    'Mg': ('Mg', {'width': 30, 'editable': True}),
    'Cr': ('Cr', {'width': 30, 'editable': True}),
    'Cu': ('Cu', {'width': 30, 'editable': True}),
    'Ni': ('Ni', {'width': 30, 'editable': True}),
    'Al': ('Al', {'width': 30, 'editable': True}),
    'Ti': ('Ti', {'width': 30, 'editable': True}),
    'Mo': ('Mo', {'width': 30, 'editable': True}),
}

st.write('## Items Selection list')
grid_table = draw_grid(
    df,
    formatter=formatter,
    fit_columns=True,
    selection='multiple',  # or 'single', or None
    use_checkbox='True',  # or False by default
    max_height=300
)


#st.write('## Items Selection list')
#grid_table = AgGrid(df, height=400, gridOptions=gridoptions, width = '100%', update_mode=GridUpdateMode.SELECTION_CHANGED, fit_columns_on_grid_load=True)

st.write('## Final Items list')
selected_row = grid_table["selected_rows"]

for i in range(len(selected_row)):
    if '_selectedRowNodeInfo' in selected_row[i]:
        del selected_row[i]['_selectedRowNodeInfo']
        selected_row[i] = {k: v or 0 for (k, v) in selected_row[i].items()}
        for key, value in selected_row[i].items():
            try:
                selected_row[i][key] = float(value)
            except ValueError:
                selected_row[i][key] = value


#st.dataframe(selected_row)

final_df = pd.DataFrame(selected_row)

try:
    final_df['Min'] = final_df['Min'].replace([0.0000], [None])
    final_df['Max'] = final_df['Max'].replace([0.0000], [None])
except:
    pass


st.dataframe(final_df)

st.download_button(
    label = "Download Items CSV",
    data = final_df.to_csv(index=False),
    file_name = f_name+"_item_sheet.csv",
    mime = "text/csv",
    key='download-csv2'
    )



