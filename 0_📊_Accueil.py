import streamlit as st

def main():
    st.title("Commitments of traders - Datas 📊")
    st.markdown(
        """
        Cette application a pour objectif de faciliter l'analyse des rapports "Commitments of traders", issues du site [cftc.gov](https://www.cftc.gov/).
        Les données récupérées sont des contrats à terme non commerciaux, tels que les devises forex majeures essentiellement.
        💵 💴 💶 💷  

        La finalité est de déduire **l'Orderflow de la Smart Money** de manière la plus probable en fonction de nos analyses.
    """
    )

if __name__ == "__main__":
    st.set_page_config(
        page_title="Rapports COT",
        page_icon="📊",
        layout="wide",
    )
    main()