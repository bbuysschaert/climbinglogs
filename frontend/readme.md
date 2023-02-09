# Streamlit front-end to interact with the climbing logs

The front-end of the climbing logging app will be developed with streamlit.  This is because it has a fast learning curve and provides most of the functionality that you need.  The app will go somewhat further than a single-page streamlit application.  You will also need to use caching (or the more [experimental cache primitives](https://docs.streamlit.io/library/advanced-features/experimental-cache-primitives) to pass information in the app).


## Goals:
- [X] Have a multi-page streamlit application
- [ ] Have a page to upload your data to the database / back-end
- [ ] Have a page to receive the aggregated results to create the progression over time diagrams
- [ ] Have a page to receive the aggregated results to create the grade pyramids
- [ ] Have a page to receive the aggregated route results to create a style preference radar chart


## Beware:
- Using streamlit might learn you anti-patterns that will be hard to break later on.