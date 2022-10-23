import streamlit as st
import pandas as pd

@st.cache
def csv_to_dataframe(file, index="Date"):
    return pd.read_csv(file, index_col=index)

def main():
    st.title("Commitments of traders - Datas 📊")
    st.markdown(
        """
        Cette application a pour objectif de faciliter l'analyse des rapports "Commitments of traders", issues du site [cftc.gov](https://www.cftc.gov/).
        Les données récupérées sont des contrats à terme non commerciaux, tels que les devises forex majeures essentiellement.
        💵 💴 💶 💷  

        La finalité est de déduire **l'Orderflow de la Smart Money** de manière la plus probable en fonction de nos analyses.

        ### Applications
        - ⚖️ Comparateur d'actifs
        - 💸 Meilleures metriques (*en développement*)

        ### Contact
        Si vous observer quelconques bugs ou avez des idées d'améliorations, contactez moi via **Discord** 
    """ 
    )

if __name__ == "__main__":
    st.set_page_config(
        page_title="Rapports COT",
        page_icon="📊",
        layout="wide",
    )
    main()