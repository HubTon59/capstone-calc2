import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# --- Configurações da Página ---
st.set_page_config(
    page_title="Projeto Tanque Ótimo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNÇÃO UTILITÁRIA DE CARREGAMENTO DE CSS ---
def local_css(file_name):
    # Tenta carregar, se não existir (deploy inicial), não quebra
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("assets/style.css")

# --- Cabeçalho Principal ---
st.markdown("""
<h1 class='main-header'>
    <i class="bi bi-buildings-fill icon-blue"></i> Otimização de Tanque Industrial
</h1>
<p style='font-size: 1.1rem; opacity: 0.8;'>
    <b>Cálculo 2 Aplicado à Engenharia</b> — Sistema para determinação de geometria ideal minimizando custos.
</p>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("""
<div class="sidebar-header">
    <i class='bi bi-sliders icon-blue'></i> &nbsp; Parâmetros de Projeto
</div>
""", unsafe_allow_html=True)

# 1. SELEÇÃO DE GEOMETRIA
st.sidebar.markdown("**Forma do Recipiente:**")
geometry_type = st.sidebar.selectbox(
    "Selecione o formato:",
    ["Cilindro (Padrão)", "Prisma Regular (Polígono)"],
    label_visibility="collapsed"
)

# Se for polígono, pergunta o número de lados
num_sides = 0
if geometry_type == "Prisma Regular (Polígono)":
    num_sides = st.sidebar.slider("Número de Lados da Base (n)", min_value=3, max_value=12, value=4, help="3=Triângulo, 4=Quadrado/Retângulo, 6=Hexágono...")

st.sidebar.markdown("---")
st.sidebar.markdown("**Restrições:**")

target_volume = st.sidebar.number_input("Volume Alvo (m³)", min_value=10.0, value=1000.0, step=10.0)
cost_base = st.sidebar.number_input("Custo Base/Tampa (R$/m²)", min_value=1.0, value=20.0, step=1.0)
cost_side = st.sidebar.number_input("Custo Lateral (R$/m²)", min_value=1.0, value=10.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.caption("v2.2 - Multi-Geometry Update")

# --- Navegação Principal ---
selected = option_menu(
    menu_title=None,
    options=["Otimização", "Massa & Volume", "Simulação Térmica"],
    icons=["calculator", "box-seam", "thermometer-sun"], 
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "var(--secondary-background-color)"},
        "nav-link-selected": {"background-color": "#0d6efd"},
    }
)

# ==================================================
# MÓDULO 1: OTIMIZAÇÃO
# ==================================================
if selected == "Otimização":
    st.markdown("<h3 class='sub-header'><i class='bi bi-rulers icon-blue'></i> Geometria de Custo Mínimo</h3>", unsafe_allow_html=True)
    
    # --- LOGICA MATEMÁTICA GENERALIZADA ---
    # Variáveis para resultados
    opt_dimension = 0 # Pode ser Raio ou Lado
    opt_height = 0
    min_cost = 0
    dim_name = "" # Nome da dimensão (Raio ou Lado)

    if geometry_type == "Cilindro (Padrão)":
        dim_name = "Raio (r)"
        st.markdown(r"Aplicação de **Lagrange** para **Cilindro**. Minimizando custo sujeito a Volume $V = \pi r^2 h$.")
        
        # Matemática Cilindro
        # r_otimo = cuberoot( (V * C_lat) / (2 * pi * C_base) )
        opt_dimension = ((target_volume * cost_side) / (2 * np.pi * cost_base))**(1/3)
        opt_height = target_volume / (np.pi * opt_dimension**2)
        
        # Custo
        area_base = np.pi * opt_dimension**2
        area_side = 2 * np.pi * opt_dimension * opt_height
        min_cost = (2 * area_base * cost_base) + (area_side * cost_side)
        
    else:
        # Prisma Regular (n lados)
        # Otimização para base quadrada (n=4), triangular (n=3), etc.
        dim_name = "Lado da Base (L)"
        n = num_sides
        st.markdown(f"Aplicação de **Lagrange** para **Prisma de {n} lados**. Minimizando custo sujeito a Volume $V = Area_{{base}} \cdot h$.")
        
        # Fórmulas Polígono Regular
        # Area Base = (n * L^2) / (4 * tan(pi/n))
        # Perimetro = n * L
        
        # Constante geométrica "K" da área: Area = K * L^2
        k_area = n / (4 * np.tan(np.pi / n))
        
        # Derivada do Custo em relação a L (Lagrange simplificado):
        # L_otimo = cuberoot( (V * C_side * Perimetro_unitario) / (2 * C_base * K_area) ) ?
        # Derivando C(L): L = cuberoot( (2 * V * C_side) / (2 * k_area * C_base / (Perim_unit/K_area) ) ) ...
        # Simplificando a álgebra para o código:
        # L_opt = cuberoot( (V * C_side * n) / (2 * k_area * C_base) )  <-- ERRADO
        
        # Vamos usar a formula exata derivada:
        # Custo = 2 * (K_area * L^2) * C_base  +  (n * L) * (V / (K_area * L^2)) * C_side
        # dC/dL = 4 * K_area * L * C_base  -  (n * V * C_side) / (K_area * L^2) = 0
        # L^3 = (n * V * C_side) / (4 * K_area^2 * C_base)
        
        numerator = n * target_volume * cost_side
        denominator = 4 * (k_area**2) * cost_base
        opt_dimension = (numerator / denominator)**(1/3)
        
        opt_height = target_volume / (k_area * opt_dimension**2)
        
        # Custo
        area_base = k_area * opt_dimension**2
        area_side = (n * opt_dimension) * opt_height
        min_cost = (2 * area_base * cost_base) + (area_side * cost_side)

    # --- MÉTRICAS ---
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{dim_name} Ótimo", f"{opt_dimension:.2f} m")
    c2.metric("Altura Ótima (h)", f"{opt_height:.2f} m")
    c3.metric("Custo Mínimo", f"R$ {min_cost:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- VISUALIZAÇÃO ---
    col_viz1, col_viz2 = st.columns([1, 1])

    with col_viz1:
        st.markdown(f"#### <i class='bi bi-box icon-gray'></i> Modelo 3D ({'Cilindro' if geometry_type.startswith('Cil') else f'Prisma {num_sides} lados'})", unsafe_allow_html=True)
        
        # Geração da Malha 3D
        z = np.linspace(0, opt_height, 2) # Altura (apenas topo e base para ficar leve)
        
        if geometry_type == "Cilindro (Padrão)":
            # Resolução alta para parecer redondo
            theta = np.linspace(0, 2*np.pi, 60)
            radius_viz = opt_dimension
        else:
            # Resolução exata para criar arestas (TRUQUE DO PLOTLY)
            # Para desenhar um quadrado, precisamos de 5 pontos (0, 90, 180, 270, 360 graus)
            theta = np.linspace(0, 2*np.pi, num_sides + 1)
            # Correção matemática: opt_dimension no prisma é o LADO (L).
            # Mas o Plotly desenha baseado no RAIO (distância centro-vértice).
            # R = L / (2 * sin(pi/n))
            radius_viz = opt_dimension / (2 * np.sin(np.pi / num_sides))

        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = radius_viz * np.cos(theta_grid)
        y_grid = radius_viz * np.sin(theta_grid)

        fig_3d = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Blues', showscale=False, opacity=0.8)])
        
        # Adicionar tampas (base e topo) visualmente
        fig_3d.add_trace(go.Scatter3d(x=x_grid[0], y=y_grid[0], z=z_grid[0], mode='lines', line=dict(color='black', width=2), name='Base'))
        fig_3d.add_trace(go.Scatter3d(x=x_grid[1], y=y_grid[1], z=z_grid[1], mode='lines', line=dict(color='black', width=2), name='Topo'))

        fig_3d.update_layout(
            scene=dict(
                xaxis_title='X (m)', yaxis_title='Y (m)', zaxis_title='Altura (m)',
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=0), height=400,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_viz2:
        st.markdown("#### <i class='bi bi-graph-up icon-gray'></i> Curva de Otimização", unsafe_allow_html=True)
        
        # Gráfico 2D: Custo vs Dimensão
        dim_range = np.linspace(opt_dimension * 0.5, opt_dimension * 1.5, 100)
        
        # Recalcular custo para o array dim_range
        if geometry_type.startswith("Cil"):
            # Custo Cilindro
            c_curve = (2 * np.pi * dim_range**2 * cost_base) + (2 * target_volume * cost_side / dim_range)
        else:
            # Custo Prisma
            # C(L) = 2 * K_area * L^2 * Cb  +  n * L * (V / (K_area * L^2)) * Cs
            # Simplificando: A * L^2 + B / L
            term_area = 2 * k_area * (dim_range**2) * cost_base
            term_side = (n * dim_range) * (target_volume / (k_area * dim_range**2)) * cost_side
            c_curve = term_area + term_side

        fig_2d = go.Figure()
        fig_2d.add_trace(go.Scatter(x=dim_range, y=c_curve, mode='lines', name='Custo Total', line=dict(color='#0d6efd')))
        fig_2d.add_trace(go.Scatter(x=[opt_dimension], y=[min_cost], mode='markers', name='Mínimo Global', marker=dict(color='red', size=10)))
        
        fig_2d.update_layout(
            xaxis_title=f"{dim_name} (m)", yaxis_title="Custo (R$)",
            height=400, hovermode="x unified",
            margin=dict(l=0, r=0, b=0, t=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_2d, use_container_width=True)

    # Detalhes Matemáticos Dinâmicos
    with st.expander("Ver Memória de Cálculo (Derivada)"):
        if geometry_type.startswith("Cil"):
            st.latex(r"C(r) = 2\pi r^2 C_{base} + \frac{2 V C_{lat}}{r}")
            st.latex(r"\frac{dC}{dr} = 4\pi r C_{base} - \frac{2 V C_{lat}}{r^2} = 0")
        else:
            st.write(f"Para um prisma regular de {num_sides} lados com lado $L$:")
            st.latex(r"Area_{base} = \frac{n L^2}{4 \tan(\pi/n)}")
            st.latex(r"C(L) = 2 A_{base} C_{base} + \frac{n V C_{lat}}{Area_{base}}")

# ==================================================
# MÓDULO 2: MASSA
# ==================================================
if selected == "Massa & Volume":
    st.markdown("<h3 class='sub-header'><i class='bi bi-hdd-stack icon-blue'></i> Propriedades Físicas</h3>", unsafe_allow_html=True)
    st.warning("Módulo em desenvolvimento pela Equipe 2")
    st.markdown("Cálculo de integrais ajustado para a geometria selecionada.")

# ==================================================
# MÓDULO 3: TÉRMICA
# ==================================================
if selected == "Simulação Térmica":
    st.markdown("<h3 class='sub-header'><i class='bi bi-thermometer-high icon-blue'></i> Termodinâmica</h3>", unsafe_allow_html=True)
    st.warning("Módulo em desenvolvimento pela Equipe 3")