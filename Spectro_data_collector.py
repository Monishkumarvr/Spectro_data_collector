import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd

sheet_id = "1-SJVJmE85vHo8EUP1MBDmrK-pK7dSAdfnsByKrfoCRE"
sheet_name = "Items"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url)
df.drop(['Yield', 'Price', 'Size'], axis = 1, inplace = True)
df.fillna(0, inplace = True)

f_name = st.text_input("Enter the foundry name")
#st.dataframe(data=df2, width=None, height=None)

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='multiple', use_checkbox=True)
gd.configure_default_column(editable = True, groupable = True)
gridoptions = gd.build()

st.write('## Items Selection list')
grid_table = AgGrid(df, height=250, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

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


st.dataframe(selected_row)

final_df = pd.DataFrame(selected_row)

st.download_button(
   label = "Download Items CSV",
   data = final_df.to_csv(index=False),
   file_name = f_name+"_item_sheet.csv",
   mime = "text/csv",
   key='download-csv'
)

# if st.button('Download Items CSV'):
#     final_df.to_csv(f_name+"_item_sheet.csv", index=False)


