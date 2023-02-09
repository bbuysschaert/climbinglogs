# Dependencies
import streamlit as st
import pandas as pd

def pageconfig_pyramidpage():
    st.set_page_config(
        page_title='Climbing pyramid'
        )

def content_pyramidpage():
    st.markdown(
    """
    # Gym climbing logging application
    ## Climbing pyramid
    """
    )

def sidebar_pyramidpage():
    st.sidebar.header('Climbing pyramid')

if __name__ == '__main__':
    pageconfig_pyramidpage()
    content_pyramidpage()
    sidebar_pyramidpage()