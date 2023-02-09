# Dependencies
import streamlit as st
import pandas as pd

def pageconfig_timeprogressionpage():
    st.set_page_config(
        page_title='Progression over time'
        )

def content_timeprogressionpage():
    st.markdown(
    """
    # Gym climbing logging application
    ## Progression over time
    """
    )

def sidebar_timeprogressionpage():
    st.sidebar.header('Progression over time')

if __name__ == '__main__':
    pageconfig_timeprogressionpage()
    content_timeprogressionpage()
    sidebar_timeprogressionpage()