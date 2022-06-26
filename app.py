import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from streamlit_agraph import Config, Edge, Node, agraph

from module.get_finace import get_finance_df

if "ticker_l" not in st.session_state:
    st.session_state.ticker_l = ["BZ=F"]


def draw_cahrt(ticker):
    df_chart = get_finance_df(ticker)
    # 線グラフ描画
    fig = px.line(
        df_chart,
        markers=True,
    )
    return fig


if __name__ == "__main__":
    st.title("Market Chain")
    chart_container = st.container()
    chart_container.header("Chart")

    # graph
    st.header("Supply chain")

    nodes = []
    edges = []
    nodes.append(
        Node(
            id="BZ=F",
            label="Brent Crude Oil",
            size=400,
            svg="https://is4-ssl.mzstatic.com/image/thumb/Purple128/v4/b3/20/59/b3205997-0225-4dd2-686e-2e4216712c00/source/256x256bb.jpg",
        )
    )  # includes **kwargs
    nodes.append(
        Node(
            id="HG=F",
            label="Cooper",
            size=400,
            svg="https://pbs.twimg.com/profile_images/1011557713132826626/rgs1Rjtg_400x400.jpg",
        )
    )
    nodes.append(
        Node(
            id="GC=F",
            label="Gold",
            size=400,
            svg="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREvrWdr-3Bz23gSknR6C4C0fyYXVVKdOEiZ0I4QwKHssMeKKYdJooTvadrYEUvHhBTG8I&usqp=CAU",
        )
    )
    nodes.append(
        Node(
            id="TSM",
            label="TSMC",
            size=400,
            svg="https://companiesmarketcap.com/img/company-logos/256/TSM.png",
        )
    )
    edges.append(
        Edge(
            source="GC=F",
            # label="friend_of",
            target="TSM",
            type="CURVE_SMOOTH",
        )
    )  # includes **kwargs

    config = Config(
        width=480,
        height=360,
        directed=True,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",  # or "blue"
        collapsible=True,
        node={"labelProperty": "label"},
        link={"labelProperty": "label", "renderLabel": True},
        # **kwargs e.g. node_size=1000 or node_color="blue"
    )

    return_value = agraph(nodes=nodes, edges=edges, config=config)
    if return_value:
        st.session_state.ticker_l.append(return_value["node"])

    # 市況データ取得
    # st.subheader(st.session_state.ticker_l[-1])
    ticker = st.session_state.ticker_l.pop()
    fig = draw_cahrt(ticker)
    chart_container.plotly_chart(fig, use_container_width=True)

    st.write(return_value)
    st.write(st.session_state.ticker_l)
