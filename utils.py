import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import numpy as np
import pandas as pd

def fn(x):
    return int(x) if float(x).is_integer() else np.round(x, 2)

def card_button(key, icon, title, subtitle):
    active = "active" if st.session_state.risk_attitude == key else ""
    html = f"""
    <div class="risk-card {active}" id="card-{key}">
      <span class="card-icon">{icon}</span>
      <span class="card-title">{title}</span>
      <span class="card-subtitle">{subtitle}</span>
    </div>"""
    return html

def metric_card(self, title, value, icon, bg_color, accent_color, subtext="_"):
    self.html(f"""
        <div style='
            background: {bg_color};
            border: 1px solid rgba(255,255,255,0.65);
            border-radius: 22px;
            padding: 10px 20px;
            min-height: 125px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            overflow: hidden;
        '>
            <div style='
                width: 64px;
                height: 64px;
                border-radius: 64px;
                background: rgba(255,255,255,0.75);
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                box-shadow: 0 6px 18px rgba(0,0,0,0.06);
                color: {accent_color};
            '>
                {icon}
            </div>

            <div style='
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                min-width: 0;
            '>
                <div style='
                    font-size: 20px;
                    font-weight: 700;
                    color: #334155;
                    margin-bottom: 6px;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                '>{title}</div>

                <div style='
                    font-size: 35px;
                    font-weight: 800;
                    line-height: 1;
                    color: #0f172a;
                    margin-bottom: 6px;
                '>{value}</div>

                <div style='
                    font-size: 20px;
                    font-weight: 750;
                    color: {accent_color};
                '>{subtext}</div>
            </div>
        </div>
        """
    )

def recommendation_card(self, rank, title, score, color, status): 
    self.html(f"""
    <div style="
        background:white;
        border-radius:16px;
        padding:1px;
        margin-bottom:1px;
    ">

        <div style="
            display:flex;
            align-items:center;
            gap:12px;
        ">

            <div style="
                width:64px;
                height:64px;
                border-radius:50%;
                background:{color}20;
                color:{color};
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:30px;
            ">
                {rank}
            </div>

            <div style="flex:1;">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    margin-bottom:8px;
                ">
                    <span style="
                        font-weight:700;
                        font-size:18px;
                    ">
                        {title}
                    </span>

                    <span style="
                        font-weight:700;
                        font-size:15px;
                    ">
                        {score:.1f}%
                    </span>
                </div>

                <div style="
                    width:100%;
                    height:10px;
                    background:#e5e7eb;
                    border-radius:999px;
                    overflow:hidden;
                ">
                    <div style="
                        width:{score}%;
                        height:100%;
                        background:{color};
                        border-radius:999px;
                    ">
                    </div>
                </div>

                <div style="margin-top:10px;">
                    <span style="
                        background:{color}20;
                        color:{color};
                        padding:4px 10px;
                        border-radius:999px;
                        font-size:13px;
                        font-weight:600;
                    ">
                        {status}
                    </span>
                </div>
            </div>
        </div>
    </div>
    """)

DeltaGenerator.metric_card = metric_card
DeltaGenerator.recommendation_card = recommendation_card



# EV
def calculate_ev(payoff_matrix, probabilities):
    ev_values = payoff_matrix.to_numpy() @ np.array(probabilities)

    ranking = (
        pd.Series(ev_values, index=payoff_matrix.index)
        .rank(ascending=False, method="dense")
        .astype(int)
    )

    return ev_values, ranking

def create_ev_formula(payoff_matrix, probabilities, ev_values):

    formulas = []
    for row in payoff_matrix.index:
        terms = [f"({fn(payoff_matrix.loc[row, col])}×{fn(probabilities[i])})"
                 for i, col in enumerate(payoff_matrix.columns)]

        formula = (" + ".join(terms))
        formulas.append(formula)

    return formulas

# EU
def utility(x, risk_attitude="Risk Neutral"):
    if risk_attitude == "Risk Neutral":
        return x
    elif risk_attitude == "Risk Averse":
        return np.sqrt(x)
    elif risk_attitude == "Risk Seeking":
        return np.square(x)

def calculate_eu(payoff_matrix, probabilities,risk_attitude="Risk Neutral"):
    utility_matrix = utility(payoff_matrix.to_numpy(),risk_attitude)

    eu_values = (utility_matrix@ np.array(probabilities))

    ranking = (
        pd.Series(
            eu_values,
            index=payoff_matrix.index
        )
        .rank(
            ascending=False,
            method="dense"
        )
        .astype(int)
    )

    return utility_matrix, eu_values, ranking

def create_eu_formula(utility_matrix,probabilities):
    formulas = []
    for idx in range(4):
        terms = [
            f"({fn(utility_matrix[idx,i])}×{fn(probabilities[i])})"
            for i in range(len(probabilities))
        ]

        formulas.append(" + ".join(terms))

    return formulas