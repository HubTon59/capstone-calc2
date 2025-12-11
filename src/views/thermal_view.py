import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.controllers import thermal_logic

def render():
    st.markdown("<h3 class='sub-header'><i class='bi bi-thermometer-high icon-blue'></i> Termodinâmica e EDO</h3>", unsafe_allow_html=True)
    st.markdown("Previsão de temperatura baseada na **Lei de Resfriamento de Newton**.")

    # 1. Inputs Específicos (Temperatura, k, tempo)
    col_param1, col_param2, col_param3 = st.columns(3)
    with col_param1:
        t_amb = st.number_input("Temp. Ambiente (°C)", value=35.0, step=1.0)
        t_critical = st.number_input("Temp. Crítica (°C)", value=25.0, step=1.0)
    with col_param2:
        t_initial = st.number_input("Temp. Inicial (°C)", value=5.0, step=1.0)
        time_span = st.slider("Simulação (horas)", 1, 48, 24)
    with col_param3:
        k_const = st.number_input("Condutividade (k)", value=0.15, step=0.01)

    st.markdown("---")

    # 2. Chama o Controller
    t_values, temp_values, time_to_fail = thermal_logic.simulate_cooling(
        t_amb, t_initial, t_critical, time_span, k_const
    )

    # 3. Visualização
    col_viz, col_alert = st.columns([2, 1])

    with col_viz:
        st.markdown("#### <i class='bi bi-graph-up-arrow icon-gray'></i> Curva de Aquecimento", unsafe_allow_html=True)
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=t_values, y=temp_values, mode='lines', name='Temperatura', line=dict(color='#fd7e14', width=3)))
        fig_temp.add_trace(go.Scatter(x=[0, time_span], y=[t_critical, t_critical], mode='lines', name='Limite Crítico', line=dict(color='red', dash='dash')))
        fig_temp.update_layout(
            xaxis_title="Tempo (h)", yaxis_title="Temp (°C)", height=350,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified", margin=dict(t=10, b=0, l=0, r=0),
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    with col_alert:
        st.markdown("#### <i class='bi bi-shield-check icon-gray'></i> Status", unsafe_allow_html=True)
        if time_to_fail is not None:
            st.error(f"**CRÍTICO**")
            st.metric("Tempo até Falha", f"{time_to_fail:.1f} horas", delta="Risco Iminente", delta_color="inverse")
        else:
            st.success(f"**SEGURO**")
            st.metric("Margem", "Estável", delta="OK")
        
        st.markdown("---")
        st.code(f"k = {k_const}\nT_amb = {t_amb}°C", language="text")

    # 4. Educação
    render_education(t_amb, t_initial, k_const)

def render_education(t_amb, t_ini, k):
    st.markdown("---")
    st.markdown("#### <i class='bi bi-journal-text icon-gray'></i> Da Teoria à Prática", unsafe_allow_html=True)
    
    col_math, col_code = st.columns([1, 1])
    
    with col_math:
        st.markdown("**1. A Modelagem (Equações Diferenciais)**")
        st.write("""
        A Lei de Resfriamento de Newton afirma que a **velocidade** com que a temperatura muda é proporcional à diferença entre o corpo e o ambiente.
        """)
        
        st.latex(r"\frac{dT}{dt} = -k \cdot (T(t) - T_{amb})")
        
        st.info("""
                **Interpretação:**
                Quando a diferença de temperatura é grande, o resfriamento é rápido (inclinação alta). Conforme se aproxima do equilíbrio, o processo desacelera.
        """)
        
        st.write("Integrando esta EDO de 1ª ordem, chegamos à solução exponencial:")
        st.latex(r"T(t) = T_{amb} + (T_{0} - T_{amb}) \cdot e^{-k \cdot t}")

    with col_code:
        st.markdown("**2. O Algoritmo (Python)**")
        st.write("Em vez de simular passo a passo (loop), usamos a **solução analítica vetorizada** do NumPy, que calcula todos os pontos de tempo de uma vez.")
        
        st.code(f"""
# Parâmetros Físicos
k = {k}
t_amb = {t_amb}
delta_T = {t_ini} - {t_amb}

# Aplicação da Solução da EDO
# np.exp() calcula e^(-kt) para cada instante 't'
temp_final = t_amb + delta_T * np.exp(-k * t)
""", language="python")