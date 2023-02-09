# Dependencies
import streamlit as st

def pageconfig_mainpage():
    st.set_page_config(
        page_title='Main page'
        )

def content_mainpage():
    st.markdown(
    """
    # Gym climbing logging application

    Describe what you can find on this page
    """
    )

def sidebar_mainpage():
    st.sidebar.header('Main page')

if __name__ == '__main__':
    # Run the application itself
    pageconfig_mainpage()
    content_mainpage()
    sidebar_mainpage()