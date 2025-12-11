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
    st.markdown("#### <i class='bi bi-journal-text icon-gray'></i>A Física por Trás da Integral", unsafe_allow_html=True)
    
    with st.expander("Derivação", expanded=True):
        
        tab_model, tab_step = st.tabs(["1. Modelagem Física", "2. Resolvendo a Integral"])
        
        with tab_model:
            st.markdown("##### O Problema da Densidade Variável")
            st.write("Não podemos usar a fórmula simples $Massa = Volume \\times Densidade$ porque a densidade muda com a altura $z$.")
            
            st.markdown("**Função Densidade Linear:**")
            st.write("Assumimos que a densidade decresce linearmente da base para o topo:")
            st.latex(r"\rho(z) = \rho_{base} - B \cdot z")
            st.latex(rf"\text{{Onde }} B = \frac{{\rho_{{base}} - \rho_{{topo}}}}{{H}} = {B:.4f}")

            st.markdown("##### O Método do Fatiamento (Riemann)")
            st.write("Para calcular a massa total, 'fatiamos' o tanque em discos horizontais infinitesimais de espessura $dz$.")
            st.latex(r"dM = \text{Area} \cdot \rho(z) \cdot dz")
            st.latex(r"M = \int_{0}^{H} \text{Area} \cdot (\rho_{base} - B z) \, dz")

        with tab_step:
            st.markdown("##### Passo a Passo da Integração")
            st.write("Vamos resolver $\int (\rho_{base} - B z) dz$ usando as regras de cálculo:")
            
            st.markdown("**Passo 1: Separar (Linearidade)**")
            st.latex(r"\int \rho_{base} \, dz - \int B z \, dz")
            
            st.markdown(r"**Passo 2: Regra da Potência ($\int z^n dz = \frac{z^{n+1}}{n+1}$)**")
            st.write(r"A integral de uma constante é $z$. A integral de $z$ (que é $z^1$) vira $z^2/2$.")
            st.latex(r"\left[ \rho_{base} \cdot z - B \cdot \frac{z^2}{2} \right]_0^H")
            
            st.markdown("**Passo 3: Aplicar Limites (Teorema Fundamental)**")
            st.write("Calculamos no Topo ($H$) e subtraímos a Base ($0$).")
            st.latex(r"M = \text{Area} \cdot \left[ (\rho_{base} H - \frac{B H^2}{2}) - (0 - 0) \right]")
            
            st.success("Esta é a fórmula final utilizada.")

#         with tab_code:
#             st.markdown("##### Tradução para Código")
#             st.write("O código apenas calcula o valor numérico do polinômio resultante da integração.")
            
#             st.code(f"""
# # Variáveis Físicas
# Area = ... # Calculada na aba 1
# h = {h:.2f}
# rho_base = {rho}
# B = {B:.4f} # Gradiente calculado

# # Aplicação do Resultado da Integral:
# # Termo 1 (Retângulo): rho * h
# # Termo 2 (Triângulo): (B * h^2) / 2
# massa = Area * (rho_base * h - (B * h**2) / 2)
# """, language="python")