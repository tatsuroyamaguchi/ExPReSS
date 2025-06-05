import streamlit as st

from config import NORMAL_SAMPLES, DEFAULT_EP_INSTITUTION, EP_DEPARTMENTS, EP_RESPONSIBLES, DEFAULT_EP_CONTACT, DEFAULT_EP_TEL

def render_sidebar_inputs():
    """
    Render sidebar inputs and store them in st.session_state.
    Returns the input values as a dictionary.
    """
    st.sidebar.header("⚙️ Settings")
    st.sidebar.markdown("---")
    # Initialize session state if not already set
    if 'date' not in st.session_state:
        st.session_state.date = None
    if 'normal_sample' not in st.session_state:
        st.session_state.normal_sample = NORMAL_SAMPLES[0]
    if 'ep_institution' not in st.session_state:
        st.session_state.ep_institution = DEFAULT_EP_INSTITUTION
    if 'ep_department' not in st.session_state:
        st.session_state.ep_department = EP_DEPARTMENTS
    if 'ep_responsible' not in st.session_state:
        st.session_state.ep_responsible = EP_RESPONSIBLES
    if 'ep_contact' not in st.session_state:
        st.session_state.ep_contact = DEFAULT_EP_CONTACT
    if 'ep_tel' not in st.session_state:
        st.session_state.ep_tel = DEFAULT_EP_TEL

    # Date input
    st.session_state.date = st.sidebar.date_input(
        "エキスパートパネル開催日"
    )

    # Normal sample selection
    st.session_state.normal_sample = st.sidebar.selectbox(
        "正常サンプル（HemeSight）",
        NORMAL_SAMPLES,
        index=NORMAL_SAMPLES.index(st.session_state.normal_sample) if st.session_state.normal_sample in NORMAL_SAMPLES else 0
    )

    # EP institution
    st.session_state.ep_institution = st.sidebar.text_input(
        label='EP実施医療機関',
        value=st.session_state.ep_institution
    )

    # EP department
    st.session_state.ep_department = st.sidebar.text_input(
        label="診療科",
        value=st.session_state.ep_department
    )

    # EP responsible
    st.session_state.ep_responsible = st.sidebar.text_input(
        label="EP責任者",
        value=st.session_state.ep_responsible
    )

    # Contact information
    st.session_state.ep_contact = st.sidebar.text_input(
        label='問い合わせ窓口（住所）',
        value=st.session_state.ep_contact
    )
    
    # Contact phone number
    st.session_state.ep_tel = st.sidebar.text_input(
        label='問い合わせ窓口（電話番号）',
        value=st.session_state.ep_tel
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
                #### Visualization with ProteinPaint for HemeSight
                - https://proteinpaint.stjude.org/
                """)
    
    # License information
    st.sidebar.markdown(
        """
        License: CC BY-NC-SA 4.0
        
        [![CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)
        """,
        unsafe_allow_html=True  # Allow HTML to render the license button
    )

    return {
        'date': st.session_state.date,
        'normal_sample': st.session_state.normal_sample,
        'ep_institution': st.session_state.ep_institution,
        'ep_department': st.session_state.ep_department,
        'ep_responsible': st.session_state.ep_responsible,
        'ep_contact': st.session_state.ep_contact,
        'ep_tel': st.session_state.ep_tel
    }