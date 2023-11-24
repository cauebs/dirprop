from itertools import count

import pandas as pd
import streamlit as st

st.title("Diretoria proporcional")

total_cadeiras = int(st.number_input("Cadeiras da diretoria", min_value=0))

votação = {}
for i in count(start=1):
    left, right = st.columns(2)
    with left:
        chapa = st.text_input(f"Chapa {i}")
    with right:
        votos = int(st.number_input(f"Votos da chapa {i}", min_value=0))

    if chapa in votação:
        st.error("Chapa repetida")
        st.stop()

    if not chapa:
        break
    votação[chapa] = votos

with right:
    total_de_votos = sum(votação.values())
    st.write(f"Total de votos: {total_de_votos}")

if not (total_cadeiras and votação and total_de_votos):
    st.stop()


def cadeiras_ocupadas(chapa: str) -> int:
    return sum(1 for cadeira in diretoria if cadeira == chapa)


def pontuação(chapa: str) -> float:
    return votação[chapa] / (cadeiras_ocupadas(chapa) + 1)


diretoria: list[str] = []
for _ in range(total_cadeiras):
    chapas = votação.keys()
    chapa_selecionada = max(chapas, key=pontuação)
    diretoria.append(chapa_selecionada)

st.table(
    [
        {
            "Chapa": chapa,
            "Cadeiras ocupadas": cadeiras_ocupadas(chapa),
        }
        for chapa in votação.keys()
    ]
)

filler = {chapa: "" for chapa in votação.keys()}
cadeiras = pd.DataFrame([{**filler, chapa: chapa} for chapa in diretoria])
st.table(cadeiras.style.highlight_max(axis='columns', color="gray"))
