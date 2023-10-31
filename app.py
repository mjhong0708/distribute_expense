import streamlit as st
import pandas  as pd



import numpy as np

def distribute(balance: list[float]):
    avg = sum(balance) / len(balance)
    residual = [n - avg for n in balance]

    history = []
    
    donors = [i for (i, n) in enumerate(residual) if n > 0]
    donors.sort(key=lambda i: residual[i])
    
    acceptors = [i for (i, n) in enumerate(residual) if n <= 0]
    acceptors.sort(key=lambda i: -residual[i])
    for i_d in donors:
        for i_a in acceptors:
            if residual[i_d] > -residual[i_a]:
                donate_val = -residual[i_a]
            else:
                donate_val = residual[i_d]
            residual[i_d] -= donate_val
            residual[i_a] += donate_val
            # print(f"{i_d} to {i_a}: {donate_val:.2f}")
            # print(residual)
            history.append(((i_d, i_a), donate_val))
    history = [h for h in history if h[1]]
    return history


st.title("출장비 정산하기")

def get_names():
    st.header("Step 1. 참가자 입력")
    names_raw = st.text_input(label="참가자를 콤마(`,`)로 구분해서 입력하세요", placeholder="ex) 홍길동, 김철수")
    names = [s.strip() for s in names_raw.split(",")]
    button = st.button("Submit", key="submit_1")
    return names, button


def get_data(names):
    data = pd.DataFrame(index=["예산", "지출"], columns=names, data=np.zeros((2, len(names))))
    st.header("Step 2. 예산 및 지출 입력")
    edited_data = st.data_editor(data)
    return edited_data
    

if __name__ == "__main__":
    names, button_1 = get_names()
    edited_data = get_data(names) 
    button = st.button("Done")
    if button:
        residual = edited_data.loc["예산"] - edited_data.loc["지출"]
        history = distribute(residual)
        edited_data.loc["잔액"] = residual

        result = [x for x in residual]
        for (i, j), val in history:
            st.markdown(f"- {names[i]} to {names[j]}: {val:.0f}")   
            result[i] -= val
            result[j] += val
        result = [round(x) for x in result]
        edited_data.loc["분배후금액"] = result
        st.dataframe(edited_data)
