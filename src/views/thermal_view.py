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
    st.markdown("#### <i class='bi bi-journal-text icon-gray'></i> Termodinâmica e EDOs", unsafe_allow_html=True)
    
    with st.expander("Derivação", expanded=True):
        
        tab_edo, tab_sol = st.tabs(["1. A Equação Diferencial", "2. Solução Analítica"])
        
        with tab_edo:
            st.markdown("##### Lei de Resfriamento de Newton")
            st.write("Newton estabeleceu que a **velocidade** de mudança da temperatura é proporcional à diferença entre o corpo e o ambiente.")
            
            col_eq, col_meaning = st.columns(2)
            with col_eq:
                st.latex(r"\frac{dT}{dt} = -k \cdot (T - T_{amb})")
            with col_meaning:
                st.caption("""
                - **dT/dt**: Taxa de variação (velocidade).
                - **k**: Condutividade térmica.
                - **Sinal negativo**: Indica que a temperatura tende ao equilíbrio (se está quente, esfria).
                """)

        with tab_sol:
            st.markdown("##### Resolvendo por Separação de Variáveis")
            st.write("1. Separamos tudo que é $T$ para um lado e $t$ para o outro:")
            st.latex(r"\frac{1}{T - T_{amb}} dT = -k \, dt")
            
            st.write("2. Integramos ambos os lados ($\int 1/x = \ln|x|$):")
            st.latex(r"\ln(T - T_{amb}) = -k t + C")
            
            st.write("3. Isolamos $T$ usando exponencial e aplicamos a condição inicial $T(0) = T_{inicial}$:")
            st.latex(r"T(t) = T_{amb} + (T_{inicial} - T_{amb}) \cdot e^{-kt}")
            st.success("Esta é a fórmula que prevê o futuro da temperatura")

#         with tab_code:
#             st.markdown("##### Tradução para Código")
#             st.write("Em vez de um loop `for` (método de Euler), usamos a **solução exata** vetorizada do NumPy, que é mais precisa e rápida.")
            
#             st.code(f"""
# # Parâmetros
# k = {k}
# t_amb = {t_amb}
# delta_T = {t_ini} - {t_amb}

# # Vetor de Tempo (0 a 48h)
# t = np.linspace(0, 48, 100)

# # Fórmula Exata da EDO:
# # np.exp() calcula e^(-kt)
# temp_final = t_amb + delta_T * np.exp(-k * t)
# """, language="python")