# Dependencies
import streamlit as st
import pandas as pd

def pageconfig_dataentrypage():
    st.set_page_config(
        page_title='Date entry page'
        )

def content_dataentrypage():
    st.markdown(
    """
    # Gym climbing logging application
    ## Data entry page
    """
    )

def sidebar_mainpage():
    st.sidebar.header('Date entry page')

if __name__ == '__main__':
    pageconfig_dataentrypage()
    content_dataentrypage()
    sidebar_mainpage()