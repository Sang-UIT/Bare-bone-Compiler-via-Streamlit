import streamlit as st
from parser import BareBoneParser
from execute import BareBoneCompiler
import tree
import json
import streamlit.components.v1 as components
def wide_space_default():
    st.set_page_config(layout='wide')
wide_space_default()
result = ''
st.markdown('''# :rainbow[**BAREBONE** COMPILER via **STREAMLIT**]''')
col1, col2 = st.columns(2)

with col1:
    st.markdown('### :orange[***INPUT:***]')
    text_input=st.text_area(label='Raw text',placeholder='Import your code here',height=250, label_visibility='collapsed')
    
    col11=st.columns(5)
    with col11[0]:
        run = st.button(':violet[COMPILE]')

    
if run:
    if text_input =='':
        st.warning(body='You import nothing', icon=None)
    else:
        parser = BareBoneParser()
        instr = parser.parse(text_input)
        if parser.get_errors():
            for error in parser.get_errors():
                st.error(f"Error at line {error[0]}: {error[1]}")
        else:
            html_code = tree.display_tree(instr)
            components.html(html_code, height=600)
            compiler = BareBoneCompiler(instr)
            st.write(instr)
            result = compiler.execute()
            
with col2:
    st.markdown('### :blue[***OUTPUT:***]')
    st.code(json.dumps(result, indent=4), language="json")