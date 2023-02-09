# Dependencies
import streamlit as st
import pandas as pd

def pageconfig_routepage():
    st.set_page_config(
        page_title='Route information'
        )

def content_routepage():
    st.markdown(
    """
    # Gym climbing logging application
    ## Route information
    """
    )

def sidebar_routepage():
    st.sidebar.header('Route information')
    
if __name__ == '__main__':
    pageconfig_routepage()
    content_routepage()
    sidebar_routepage()