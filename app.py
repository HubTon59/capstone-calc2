import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Configurações da Página ---
st.set_page_config(page_title="Projeto Tanque Ótimo", layout="wide")

st.title("🏭 Otimização de Tanque Industrial")
st.markdown("""
**Cálculo 2 Aplicado à Engenharia:**
Este sistema determina as dimensões ideais de um tanque cilíndrico para minimizar custos de material, 
além de analisar propriedades físicas (massa) e termodinâmicas.
""")

# --- Sidebar: Entradas do Usuário ---
st.sidebar.header("📝 Parâmetros de Projeto")

target_volume = st.sidebar.number_input("Volume Desejado (m³)", min_value=10.0, value=1000.0, step=10.0)
cost_base = st.sidebar.number_input("Custo Material Base/Tampa (R$/m²)", min_value=1.0, value=20.0, step=1.0)
cost_side = st.sidebar.number_input("Custo Material Lateral (R$/m²)", min_value=1.0, value=10.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.caption("Grupo: Engenharia & Cálculo 2")

# --- Estrutura em Abas ---
tab1, tab2, tab3 = st.tabs(["1. Otimização (Lagrange)", "2. Massa (Integrais)", "3. Térmica (EDO)"])


# ABA 1: Otimização
with tab1:
    st.header("📐 Otimização Geométrica e de Custos")
    
    # 1. Cálculos Matemáticos (Backend)
    # Fórmula derivada via Multiplicadores de Lagrange:
    # r_otimo = raiz_cubica( (V * C_lateral) / (2 * pi * C_base) )
    optimal_radius = ((target_volume * cost_side) / (2 * np.pi * cost_base))**(1/3)
    optimal_height = target_volume / (np.pi * optimal_radius**2)
    
    # Cálculo do Custo Mínimo
    area_base_top = 2 * np.pi * optimal_radius**2 # Base + Tampa
    area_side = 2 * np.pi * optimal_radius * optimal_height
    min_cost = (area_base_top * cost_base) + (area_side * cost_side)

    # 2. Exibição dos Resultados
    col1, col2, col3 = st.columns(3)
    col1.metric("Raio Ótimo (r)", f"{optimal_radius:.2f} m")
    col2.metric("Altura Ótima (h)", f"{optimal_height:.2f} m")
    col3.metric("Custo Mínimo Total", f"R$ {min_cost:,.2f}")

    st.divider()

    # 3. Visualização Gráfica (Plotly)
    col_viz1, col_viz2 = st.columns([1, 1])

    with col_viz1:
        st.subheader("Visualização 3D do Tanque")
        
        # Gerar cilindro paramétrico
        z = np.linspace(0, optimal_height, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = optimal_radius * np.cos(theta_grid)
        y_grid = optimal_radius * np.sin(theta_grid)

        fig_3d = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Viridis', opacity=0.8, showscale=False)])
        
        # Adicionar tampas (visualmente simples usando Scatter3d para simular wireframe ou mesh)
        # (Simplificado para o cilindro principal para performance)
        
        fig_3d.update_layout(
            title="Geometria Otimizada",
            scene=dict(
                xaxis_title='X (m)',
                yaxis_title='Y (m)',
                zaxis_title='Altura (m)',
                aspectmode='data' # Mantém a proporção real
            ),
            margin=dict(l=0, r=0, b=0, t=30)
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_viz2:
        st.subheader("Análise de Custo vs Raio")
        st.caption("Prova visual de que encontramos o mínimo (derivada zero).")
        
        # Criar dados para o gráfico 2D (variando o raio ao redor do ótimo)
        r_range = np.linspace(optimal_radius * 0.5, optimal_radius * 1.5, 100)
        # Função Custo C(r) substituindo h por V/(pi*r^2)
        # C(r) = 2*pi*r^2*Cb + 2*V*Cl/r
        costs = (2 * np.pi * r_range**2 * cost_base) + (2 * target_volume * cost_side / r_range)
        
        fig_2d = go.Figure()
        fig_2d.add_trace(go.Scatter(x=r_range, y=costs, mode='lines', name='Curva de Custo'))
        fig_2d.add_trace(go.Scatter(x=[optimal_radius], y=[min_cost], mode='markers', name='Ponto Ótimo', marker=dict(color='red', size=12)))
        
        fig_2d.update_layout(
            xaxis_title="Raio (m)",
            yaxis_title="Custo Total (R$)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_2d, use_container_width=True)

    # 4. Explicação Teórica (Latex)
    with st.expander("📚 Ver Memória de Cálculo (Lagrange)"):
        st.markdown("O problema foi modelado minimizando a função Custo sujeita à restrição de Volume:")
        st.latex(r"C(r, h) = 2\pi r^2 \cdot P_{base} + 2\pi r h \cdot P_{lateral}")
        st.latex(r"V(r, h) = \pi r^2 h = " + str(target_volume))
        st.markdown("Pelo método dos Multiplicadores de Lagrange, resolvemos o sistema:")
        st.latex(r"\nabla C = \lambda \nabla V")
        st.write("Isso nos leva à relação ideal entre raio e altura para estes custos específicos.")


# ABA 2: Integrais - Placeholder
with tab2:
    st.header("⚖️ Cálculo de Massa e Centro de Gravidade")
    st.info("🚧 Módulo em desenvolvimento pela Equipe 2")
    
    st.write(f"Utilizando as dimensões calculadas na etapa anterior ($r={optimal_radius:.2f}, h={optimal_height:.2f}$)...")
    
    st.markdown("### Definição da Densidade Variável")
    st.latex(r"\rho(z) = A - B \cdot z")
    st.markdown("A massa será calculada via **Integral Tripla** em coordenadas cilíndricas:")
    st.latex(r"M = \int_{0}^{2\pi} \int_{0}^{R} \int_{0}^{H} \rho(z) \cdot r \, dz \, dr \, d\theta")


# ABA 3: EDO - Placeholder
with tab3:
    st.header("🌡️ Simulação Térmica")
    st.info("🚧 Módulo em desenvolvimento pela Equipe 3")
    
    st.markdown("### Lei de Resfriamento de Newton")
    st.write("Estimativa de tempo para o líquido atingir temperatura crítica.")
    st.latex(r"\frac{dT}{dt} = k(T - T_{amb})")
    
    st.button("Simular Aquecimento (Demo)")