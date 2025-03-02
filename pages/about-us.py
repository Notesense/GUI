import streamlit as st
import requests

#change the name of tabs in the sidebar
st.sidebar.page_link(page="home.py", label="Keyword Search")
#st.sidebar.page_link(page="pages/topics.py", label="Topic Search")
st.sidebar.page_link(page="pages/about-data.py", label="About Data")
st.sidebar.page_link(page="pages/about-us.py", label="About Us")



## Show in webpage
st.header("About Us")

st.markdown("""
We are Hannah Doyal and Narges Chinichian, two data enthusiasts who believe that making sense of information should be as easy as a well-structured dataset. <br><br>

**Notesense** was born during our time at the Data Science Bootcamp at Spiced Academy—where late-night debugging sessions, endless coffee, and a passion for extracting insights turned into something useful (and hopefully, a little bit brilliant). <br><br>

We built this tool because we love finding patterns in data and making complex things a little less complex. We hope you find it as handy as we do! <br><br>

Want to see the code or contribute? Check out our work on [GitHub](https://github.com/Notesense/CommunityNotes). <br><br>

Have feedback, questions, or just want to say hi? Feel free to reach out!
""", unsafe_allow_html=True)


st.header("Contact Us")


FORMSPREE_ENDPOINT = "https://formspree.io/f/myzkrdqn"

with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    submitted = st.form_submit_button("Send")

    if submitted:
        response = requests.post(
            FORMSPREE_ENDPOINT,
            json={"name": name, "email": email, "message": message},
        )

        if response.status_code == 200:
            st.success("Thank you! We'll get back to you soon.")
        else:
            st.error("Something went wrong. Please try again later.")