import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.controllers import optimization_logic

def render(geo_type, num_sides, vol, c_base, c_lat):
    st.markdown("<h3 class='sub-header'><i class='bi bi-rulers icon-blue'></i> Geometria de Custo Mínimo</h3>", unsafe_allow_html=True)
    
    # 1. Chama o Controller
    opt_dim, opt_h, min_cost, k_area, dim_name = optimization_logic.calculate_optimal_geometry(
        geo_type, num_sides, vol, c_base, c_lat
    )

    # 2. Métricas
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{dim_name} Ótimo", f"{opt_dim:.2f} m")
    c2.metric("Altura Ótima (h)", f"{opt_h:.2f} m")
    c3.metric("Custo Mínimo", f"R$ {min_cost:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Gráficos
    col_viz1, col_viz2 = st.columns([1, 1])

    with col_viz1:
        st.markdown(f"#### <i class='bi bi-box icon-gray'></i> Modelo 3D", unsafe_allow_html=True)
        # Lógica de plotagem 3D (simplificada para brevidade, use a completa aqui)
        z = np.linspace(0, opt_h, 2)
        if geo_type.startswith("Cil"):
            theta = np.linspace(0, 2*np.pi, 60)
            radius_viz = opt_dim
        else:
            theta = np.linspace(0, 2*np.pi, num_sides + 1)
            radius_viz = opt_dim / (2 * np.sin(np.pi / num_sides))
        
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = radius_viz * np.cos(theta_grid)
        y_grid = radius_viz * np.sin(theta_grid)
        
        fig_3d = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Blues', showscale=False, opacity=0.8)])
        fig_3d.add_trace(go.Scatter3d(x=x_grid[0], y=y_grid[0], z=z_grid[0], mode='lines', line=dict(color='black', width=2), name='Base'))
        fig_3d.add_trace(go.Scatter3d(x=x_grid[1], y=y_grid[1], z=z_grid[1], mode='lines', line=dict(color='black', width=2), name='Topo'))
        fig_3d.update_layout(
            scene=dict(xaxis_title='X (m)', yaxis_title='Y (m)', zaxis_title='Altura (m)', aspectmode='data'),
            margin=dict(l=0, r=0, b=0, t=0), height=400,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_viz2:
        st.markdown("#### <i class='bi bi-graph-up icon-gray'></i> Curva de Otimização", unsafe_allow_html=True)
        st.markdown("Observe como o Custo Total (curva azul) atinge o ponto mais baixo exatamente na dimensão calculada.", unsafe_allow_html=True)
        # Chama Controller para dados do gráfico
        dim_range, c_curve = optimization_logic.generate_cost_curve_data(opt_dim, vol, c_base, c_lat, geo_type, num_sides, k_area)
        
        fig_2d = go.Figure()
        fig_2d.add_trace(go.Scatter(x=dim_range, y=c_curve, mode='lines', name='Custo', line=dict(color='#0d6efd')))
        fig_2d.add_trace(go.Scatter(x=[opt_dim], y=[min_cost], mode='markers', name='Mínimo', marker=dict(color='red', size=10)))
        fig_2d.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_2d, use_container_width=True)

    # 4. Área Educacional
    render_education(geo_type, num_sides, k_area, vol, c_lat, c_base)

def render_education(geo_type, num_sides, k_area, vol, c_lat, c_base):
    st.markdown("---")
    st.markdown("#### <i class='bi bi-journal-text icon-gray'></i> A Otimização", unsafe_allow_html=True)
    
    # Usamos Expander para não poluir a tela, mas permitindo profundidade total
    with st.expander("Derivação", expanded=True):
        
        tab_prob, tab_lagrange, tab_algebra = st.tabs([
            "1. O Problema", "2. Lagrange", "3. Solução Algébrica"
        ])
        
        with tab_prob:
            st.markdown("##### Definição das Variáveis e Funções")
            st.write("Queremos minimizar o **Custo ($C$)** mantendo o **Volume ($V$)** constante.")
            
            col_vars, col_funcs = st.columns(2)
            with col_vars:
                st.markdown("**Variáveis:**")
                st.latex(r"r \text{ (Raio)}, h \text{ (Altura)}")
                st.markdown("**Constantes:**")
                st.latex(r"V_{alvo}, C_{base}, C_{lateral}")
            
            with col_funcs:
                st.markdown("**Função Objetivo (Custo):**")
                if geo_type.startswith("Cil"):
                    st.latex(r"C(r, h) = \underbrace{2\pi r^2 \cdot C_{base}}_{\text{Tampas}} + \underbrace{2\pi r h \cdot C_{lat}}_{\text{Lateral}}")
                else:
                    st.latex(r"C(L, h) = 2 \cdot A_{base}(L) \cdot C_{base} + \text{Perimetro} \cdot h \cdot C_{lat}")
                
                st.markdown("**Restrição (Volume):**")
                st.latex(r"V(r, h) = Area_{base} \cdot h = \text{constante}")

        with tab_lagrange:
            st.markdown("##### O Método dos Multiplicadores de Lagrange")
            st.write("A condição para otimização com restrição é que os vetores gradientes sejam paralelos:")
            st.latex(r"\nabla C = \lambda \nabla V")
            
            st.write("Isso gera um sistema de equações parciais. Para o cilindro, derivamos em relação a $r$ e $h$:")
            
            c_eq1, c_eq2 = st.columns(2)
            with c_eq1:
                st.markdown("**Eq. 1 (Derivada em $r$):**")
                st.latex(r"4\pi r C_{base} + 2\pi h C_{lat} = \lambda (2\pi r h)")
            with c_eq2:
                st.markdown("**Eq. 2 (Derivada em $h$):**")
                st.latex(r"2\pi r C_{lat} = \lambda (\pi r^2)")

        with tab_algebra:
            st.markdown("##### Solução")
            st.write("Isolamos $\lambda$ na Eq. 2 e substituímos na Eq. 1. Após simplificar, encontramos a **Relação Geométrica Ótima** (independente do volume!):")
            
            st.latex(r"h = 2r \cdot \left(\frac{C_{base}}{C_{lat}}\right)")
            st.caption("Interpretação: Se a base for cara, o tanque estica (h aumenta) para reduzir a área da base.")
            
            st.write("Substituindo esse $h$ na fórmula do Volume ($V = \pi r^2 h$), isolamos finalmente o raio ideal:")
            
            if geo_type.startswith("Cil"):
                st.latex(r"r = \sqrt[3]{ \frac{V \cdot C_{lat}}{2\pi \cdot C_{base}} }")
            else:
                st.latex(r"L = \sqrt[3]{ \frac{n \cdot V \cdot C_{lat}}{4 \cdot K_{area}^2 \cdot C_{base}} }")

#         with tab_code:
#             st.markdown("##### Tradução para Código")
#             st.write("O Python não resolve o sistema linear. Nós programamos a **fórmula final isolada**.")
            
#             if geo_type.startswith("Cil"):
#                 st.code(f"""
# # 1. Cálculo da Base (Fórmula Final)
# raio = (( {vol} * {c_lat} ) / ( 2 * np.pi * {c_base} ))**(1/3)

# # 2. Cálculo da Altura (Consequência do Volume)
# # h = V / Area
# h = {vol} / (np.pi * raio**2)
# """, language="python")
#             else:
#                 st.code(f"""
# # 1. Cálculo do Lado (Lagrange Generalizado)
# K = {k_area:.4f}
# numerador = {num_sides} * {vol} * {c_lat}
# denominador = 4 * (K**2) * {c_base}
# lado = (numerador / denominador)**(1/3)

# # 2. Altura
# h = {vol} / (K * lado**2)
# """, language="python")