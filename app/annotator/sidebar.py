import streamlit as st

def setup_sidebar():
    """Set up the sidebar input UI"""
    st.sidebar.header("Input")
    
    grc = st.sidebar.selectbox(
        "Select Genome",
        options=["hg38", "hg19"],
        index=0
    )
    
    variant = st.sidebar.text_input(
        "Variant (e.g., NM_000546.6:c.524G>A)",
        value="NM_000546.6:c.524G>A"
    )
    st.sidebar.markdown(
        """
        ### Example Input (GRCh38)
        - chrX:153803771:1:A
        - 22 28695868 AG A
        - 22-28695869--G
        - 22-28695869-G-
        - NM_000277.2:c.1A>G
        - TERT c.-124C>T
        - MLH1:p.Arg217Cys
        - TP53:c.524G>A
        - AGT M259T
        - rs1228544607
        ### Example Input (GRCh37)
        - 22-28695869-G-A
        """
    )
    return grc, variant