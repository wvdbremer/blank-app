import re

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_page_config(page_title="Graphical Calculator", page_icon="🧮")

st.title("🧮 Graphical Calculator")

tab_calc, tab_graph = st.tabs(["Calculator", "Graph Plotter"])

# ---------- Calculator ----------
with tab_calc:
    if "expression" not in st.session_state:
        st.session_state.expression = ""

    def press(key):
        st.session_state.expression += key

    def clear():
        st.session_state.expression = ""

    def backspace():
        st.session_state.expression = st.session_state.expression[:-1]

    def evaluate():
        expr = st.session_state.expression
        if not expr or not re.fullmatch(r"[0-9+\-*/(). ]*", expr):
            st.session_state.expression = "Error"
            return
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            st.session_state.expression = str(result)
        except Exception:
            st.session_state.expression = "Error"

    st.text_input("Display", value=st.session_state.expression, disabled=True, label_visibility="collapsed")

    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "(", ")"],
        ["C", "⌫", "=", "+"],
    ]

    for row in buttons:
        cols = st.columns(4)
        for col, label in zip(cols, row):
            if label == "C":
                col.button(label, use_container_width=True, on_click=clear)
            elif label == "⌫":
                col.button(label, use_container_width=True, on_click=backspace)
            elif label == "=":
                col.button(label, use_container_width=True, on_click=evaluate)
            else:
                col.button(label, use_container_width=True, on_click=press, args=(label,))

# ---------- Graph Plotter ----------
with tab_graph:
    st.write("Plot a function of `x`, e.g. `x**2 - 3*x + 2`, `sin(x)`, `sqrt(x)`")
    func_str = st.text_input("f(x) =", value="x**2")

    col1, col2 = st.columns(2)
    x_min = col1.number_input("x min", value=-10.0)
    x_max = col2.number_input("x max", value=10.0)

    if x_min >= x_max:
        st.error("x min must be less than x max")
    else:
        allowed_names = {name: getattr(np, name) for name in dir(np) if not name.startswith("_")}
        x = np.linspace(x_min, x_max, 400)
        try:
            y = eval(func_str, {"__builtins__": {}}, {**allowed_names, "x": x})
            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.axhline(0, color="black", linewidth=0.5)
            ax.axvline(0, color="black", linewidth=0.5)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True, linestyle="--", alpha=0.5)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not evaluate function: {e}")
