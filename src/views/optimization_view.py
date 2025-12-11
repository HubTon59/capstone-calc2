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
    st.markdown("#### <i class='bi bi-journal-text icon-gray'></i> Análise Matemática Detalhada", unsafe_allow_html=True)
    
    # Abas internas para organizar a teoria densa
    tab_math, tab_code = st.columns([1, 1])
    
    with tab_math:
        st.markdown("##### 1. O Problema de Otimização Condicionada")
        st.write("""
        Nosso objetivo não é apenas encontrar o mínimo de uma função, mas encontrar o mínimo que respeite uma regra física: 
        o volume deve ser constante. É aqui que entra o **Multiplicador de Lagrange**.
        """)
        
        st.latex(r"\nabla C(r, h) = \lambda \nabla V(r, h)")
        
        st.info("""
        **Interpretação Geométrica:**
        Os vetores gradientes da função Custo ($\nabla C$) e da função Volume ($\nabla V$) devem ser **paralelos**.
        Isso significa que a curva de nível do custo tangencia a curva de nível do volume. Não há como mover-se na superfície de volume constante para reduzir mais o custo.
        """)
        
        st.markdown("##### 2. A Solução Analítica")
        if geo_type.startswith("Cil"):
            st.write("Resolvendo o sistema de equações parciais para o cilindro, isolamos o raio:")
            st.latex(r"r_{ótimo} = \sqrt[3]{\frac{V \cdot C_{lateral}}{2\pi \cdot C_{base}}}")
            st.caption("Observe: Se o Custo Lateral aumenta (numerador), o raio aumenta (o tanque fica mais baixo e largo) para usar menos parede.")
        else:
            st.write(f"Para um prisma de {num_sides} lados, a área da base depende do fator geométrico $K_{{area}}$. A fórmula generalizada é:")
            st.latex(r"L_{ótimo} = \sqrt[3]{\frac{n \cdot V \cdot C_{lateral}}{4 \cdot K_{area}^2 \cdot C_{base}}}")

    with tab_code:
        st.markdown("##### O Algoritmo (Python)")
        st.write("""
        Computacionalmente, não precisamos refazer as derivadas a cada execução. 
        Nós programamos a **solução algébrica final** (a fórmula isolada à esquerda).
        """)
        
        if geo_type.startswith("Cil"):
            code_snippet = f"""
# Variáveis vindas dos Inputs
V = {vol}        # Volume Alvo
C_lat = {c_lat}  # Custo Lateral
C_base = {c_base} # Custo Base

# Fórmula derivada de Lagrange aplicada diretamente:
# np.pi é a constante pi (3.1415...)
raio_otimo = ((V * C_lat) / (2 * np.pi * C_base))**(1/3)
"""
        else:
            code_snippet = f"""
# Para Prismas, calculamos o fator K primeiro
n = {num_sides}
K_area = {k_area:.4f} # Fator geométrico da base

# Fórmula Generalizada derivada via Lagrange:
numerador = n * V * C_lat
denominador = 4 * (K_area**2) * C_base
lado_otimo = (numerador / denominador)**(1/3)
"""
        st.code(code_snippet, language="python")
