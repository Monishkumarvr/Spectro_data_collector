import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
from agstyler import draw_grid
import base64
#from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="My dashboard", layout="wide", initial_sidebar_state="expanded")
#st_autorefresh(interval=60, key="dataframerefresh")

sheet_id = "1-SJVJmE85vHo8EUP1MBDmrK-pK7dSAdfnsByKrfoCRE"
sheet_name = "Items"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url)
df.drop(['Yield', 'Price', 'Size'], axis = 1, inplace = True)
df.fillna(0, inplace = True)

df.insert(loc = 2, column = "Metal RR", value = 100)
df.insert(loc = 3, column = "Min", value = None)
df.insert(loc = 4, column = "Max", value = None)

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

note = '<p style="font-family:Courier; color:Blue; font-size: 20px;">Note : Ensure to enter the inoculant quantity incase of inoculant item selected</p>'
st.markdown(note, unsafe_allow_html = True)
#st.markdown("#### Note : Ensure to enter the inoculant quantity incase of inoculant item selected")
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

if not 'items' in st.session_state:
    st.session_state['items'] = False
    
is_download = st.download_button(
    label = "Download Items CSV",
    data = final_df.to_csv(index=False),
    file_name = f_name+"_item_sheet.csv",
    mime = "text/csv",
    key='download-csv2'
    )


if is_download:
    st.session_state['items'] = True

if st.session_state['items']:
    
    sheet_name = "Grades"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    grade_df = pd.read_csv(url)

    grade_df.insert(loc = 2, column = "pouring time", value = None)
    grade_df.insert(loc = 3, column = "temperature", value = None)
    grade_df.insert(loc = 4, column = "has_nodularization", value = None)
    grade_df.insert(loc = 5, column = "furnace size", value = None)
    grade_df.insert(loc = 5, column = "Mg RR", value = None)

    grades = ['DI', 'GCI', 'SS', 'MS', 'AS', 'Others']

    # formatter_grade = {
    #     'Grade': ('Grade', {'width': 90, 'editable': True}),
    #     'Grade Category': ('Grade Category', {'width': 90, 'editable': True, 'cellEditor': 'agSelectCellEditor', 'cellEditorParams': {'values': [''] + grades,}}),
    #     'pouring time': ('pouring time', {'width': 90, 'editable': True}),
    #     'temperature': ('temperature', {'width': 90, 'editable': True}),
    #     'has_nodularization': ('has_nodularization', {'width': 90, 'editable': True}),
    #     'furnace size': ('furnace size', {'width': 90, 'editable': True}),
    #     'Mg RR': ('Mg RR', {'width': 90, 'editable': True}),
    #     'C': ('C', {'width': 80, 'editable': True}),
    #     'Si': ('Si', {'width': 80, 'editable': True}),
    #     'Mn': ('Mn', {'width': 80, 'editable': True}),
    #     'S': ('S', {'width': 80, 'editable': True}),
    #     'P': ('P', {'width': 80, 'editable': True}),
    #     'Mg': ('Mg', {'width': 80, 'editable': True}),
    #     'Cr': ('Cr', {'width': 80, 'editable': True}),
    #     'Cu': ('Cu', {'width': 80, 'editable': True}),
    #     'Ni': ('Ni', {'width': 80, 'editable': True}),
    #     'Al': ('Al', {'width': 80, 'editable': True}),
    #     'Sn': ('Sn', {'width': 80, 'editable': True}),
    #     'Mo': ('Mo', {'width': 80, 'editable': True}),
    # }

    gb = GridOptionsBuilder.from_dataframe(grade_df)

    string_to_add_row = "\n\n function(e) { \n \
    let api = e.api; \n \
    let rowIndex = e.rowIndex + 1; \n \
    api.applyTransaction({addIndex: rowIndex, add: [{}]}); \n \
        }; \n \n"

    
    cell_button_add = JsCode('''
        class BtnAddCellRenderer {
            init(params) {
                this.params = params;
                this.eGui = document.createElement('div');
                this.eGui.innerHTML = `
                <span>
                    <style>
                    .btn_add {
                    background-color: limegreen;
                    border: none;
                    color: white;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 10px;
                    font-weight: bold;
                    height: 2.5em;
                    width: 8em;
                    cursor: pointer;
                    }

                    .btn_add :hover {
                    background-color: #05d588;
                    }
                    </style>
                    <button id='click-button' 
                        class="btn_add" 
                        >&CirclePlus; Add</button>
                </span>
            `;
            }

            getGui() {
                return this.eGui;
            }

        };
        ''')

    cellsytle_jscode_Name = JsCode("""
                            function(params){
                                if (params.value.includes('Violation of Rule')) {
                                    return {
                                        'color': 'red', 
                                        'backgroundColor': 'white',
                                    }
                                }
                            
                            
                            if (params.value.includes('Missing')) {
                                return {
                                    'color': 'red', 
                                    'backgroundColor': 'white',
                                }
                            }
                            
                                                                    
                                if (params.value.length>6) {
                                    return {
                                        'color': 'red', 
                                        'backgroundColor': 'white',
                                    }
                                }                                    
                                                                    
                            
                            
                                if (params.value.length<=6) {
                                    return {
                                        'color': 'red', 
                                        'backgroundColor': 'white',
                                    }
                                } 
                            
                            if (params.value=="") {
                                return {
                                    'color': 'black', 
                                    'backgroundColor': 'yellow',
                                }
                            }                                    
                            
                            
                            }
                            
                            """)

    gb.configure_column('', headerTooltip='Click on Button to add new row', editable=False, filter=False,
                            onCellClicked=JsCode(string_to_add_row), cellRenderer=cell_button_add,
                            autoHeight=True, wrapText=True, lockPosition='left')


    st.write('## Grade Selection list')
#     grid_table_grade = draw_grid(
#         grade_df,
#         formatter=formatter_grade,
# #        fit_columns=True,
#         selection='multiple',  # or 'single', or None
#         use_checkbox='True',  # or False by default
#         max_height=300
#     )

    gb.configure_default_column(editable=True)
    gb.configure_selection(use_checkbox=True,selection_mode="multiple")
    gb.configure_column("Grade Category", editable=True, cellEditor='agSelectCellEditor', cellEditorParams={'values': grades })
    grid_options = gb.build()
    grid_table_grade=AgGrid(grade_df, gridOptions=grid_options, allow_unsafe_jscode=True,theme="streamlit")
#    df=grid_table_grade["data"]

    st.write('## Final Items list')
    selected_row_grade = grid_table_grade["selected_rows"]

    for i in range(len(selected_row_grade)):
        if '_selectedRowNodeInfo' in selected_row_grade[i]:
            del selected_row_grade[i]['_selectedRowNodeInfo']
            # selected_row[i] = {k: v or 0 for (k, v) in selected_row[i].items()}
            # for key, value in selected_row[i].items():
            #     try:
            #         selected_row[i][key] = float(value)
            #     except ValueError:
            #         selected_row[i][key] = value

    
    final_grade_df = pd.DataFrame(selected_row_grade)

    st.dataframe(final_grade_df)

    st.download_button(
        label = "Download Grade CSV",
        data = final_grade_df.to_csv(index=False),
        file_name = f_name+"_grade_sheet.csv",
        mime = "text/csv",
        key='download-csv2'
        )