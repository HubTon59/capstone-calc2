import streamlit as st
import plotly.graph_objects as go
from src.controllers import physics_logic

def render(geo_type, num_sides, vol, c_base, c_lat):
    st.markdown("<h3 class='sub-header'><i class='bi bi-hdd-stack icon-blue'></i> Propriedades Físicas e Massa</h3>", unsafe_allow_html=True)
    
    # 1. Inputs Específicos desta View
    st.markdown(f"**Configuração do Material:**")
    col_mat1, col_mat2 = st.columns(2)
    with col_mat1:
        rho_base = st.number_input("Densidade na Base (kg/m³)", value=8000.0, step=100.0, key="rho_base")
    with col_mat2:
        rho_top = st.number_input("Densidade no Topo (kg/m³)", value=7500.0, step=100.0, key="rho_top")

    # 2. Chama o Controller (Lógica)
    # Note que passamos os inputs globais (vol, c_base...) e os locais (rho_base...)
    total_mass, z_cm, opt_h, rho_b, B = physics_logic.calculate_mass_properties(
        geo_type, num_sides, vol, c_base, c_lat, rho_base, rho_top
    )

    # 3. Exibição dos Resultados (Metrics)
    st.markdown("---")
    col_metrics, col_graph = st.columns([1, 2])
    
    with col_metrics:
        st.markdown("#### <i class='bi bi-calculator icon-gray'></i> Resultados", unsafe_allow_html=True)
        st.metric("Massa Total", f"{total_mass:,.2f} kg")
        st.metric("Centro de Massa (Z)", f"{z_cm:.2f} m")
        st.caption(f"Ponto de equilíbrio a {(z_cm/opt_h)*100:.1f}% da altura.")

    # 4. Gráfico de Densidade
    with col_graph:
        # Pede os dados XY para o controller
        z_vals, rho_vals = physics_logic.generate_density_profile(opt_h, rho_b, B)
        
        fig_rho = go.Figure()
        fig_rho.add_trace(go.Scatter(x=rho_vals, y=z_vals, mode='lines', fill='tozeroy', name='Densidade', line=dict(color='#198754')))
        fig_rho.update_layout(
            title="Variação da Densidade com a Altura",
            xaxis_title="Densidade (kg/m³)", yaxis_title="Altura (m)",
            height=300, margin=dict(t=30, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_rho, use_container_width=True)

    # 5. Área Educacional
    render_education(total_mass, z_cm, opt_h, rho_b, B)

def render_education(mass, z_cm, h, rho, B):
    st.markdown("---")
    st.markdown("#### <i class='bi bi-journal-text icon-gray'></i> Da Teoria à Prática", unsafe_allow_html=True)
    
    col_math, col_code = st.columns([1, 1])
    
    with col_math:
        st.markdown("**1. A Modelagem (Integrais)**")
        st.write("""
        **Por que usamos Integrais?**
        Não podemos simplesmente multiplicar $Volume \\times Densidade$ porque a densidade muda com a altura (é mais densa na base).
        Precisamos **fatiar** o tanque em discos infinitesimais de altura $dz$.
        """)
        
        st.latex(r"dM = \text{Area} \cdot \rho(z) \cdot dz")
        st.latex(r"M = \int_{0}^{H} Area \cdot (\rho_{base} - B \cdot z) \, dz")
        
        st.markdown("**Centro de Massa:**")
        st.write("Calculado pela razão entre o Momento de 1ª Ordem e a Massa Total:")
        st.latex(r"\bar{z} = \frac{\int z \cdot \rho(z) \, dV}{\int \rho(z) \, dV}")

    with col_code:
        st.markdown("**2. O Algoritmo (Python)**")
        st.write("O código implementa o resultado analítico da integral definida:")
        st.latex(r"\int (A - Bz)dz = Az - \frac{Bz^2}{2}")
        
        st.code(f"""
# Dados Físicos
Area_base = ... 
h = {h:.2f}
rho_base = {rho}
B = {B:.4f} # Gradiente de densidade

# Cálculo da Massa (Resultado da Integral)
# Termo 1: rho_base * h
# Termo 2: (B * h^2) / 2
massa = Area_base * (rho_base * h - (B * h**2) / 2)
""", language="python")