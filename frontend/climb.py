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

    This app can be used to log your climbing progress and use it for subsequent analyses.

    This app is currently still under active development.
    """
    )
def sidebar_mainpage():
    st.sidebar.header('Main page')
    
    file = st.sidebar.file_uploader('Upload your climbing logs here',
                            type='xlsx',
                            accept_multiple_files=False,
                            key='inputfile'#,
                            # on_change=<some_function_to_retrigger_stuff>
                            )                                
    uploadmode = st.sidebar.selectbox('Please select data upload mode',
                                    options=['Overwrite', 'Incremental'],
                                    index=0
                                    )
    upload = st.sidebar.button('Upload the climbing logs',
                        key='data upload'
                        )
    st.sidebar.text(f'{upload}')
    st.sidebar.text(f'{uploadmode}')
    import time
    my_bar = st.sidebar.progress(0)
    for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
    return file


if __name__ == '__main__':
    # Run the application itself
    pageconfig_mainpage()
    content_mainpage()
    sidebar_mainpage()