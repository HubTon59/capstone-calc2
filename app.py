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
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

# --- Cabeçalho Principal ---
st.markdown("""
<h1 class='main-header'>
    <i class="bi bi-buildings-fill icon-blue"></i> Otimização de Tanque Industrial
</h1>
<p style='font-size: 1.1rem; opacity: 0.8;'>
    <b>Cálculo 2 Aplicado à Engenharia</b> — Sistema para determinação de geometria ideal.
</p>
""", unsafe_allow_html=True)

# --- Sidebar ---
# Usando a nova classe CSS 'sidebar-header' para alinhar ícone e texto perfeitamente
st.sidebar.markdown("""
<div class="sidebar-header">
    <i class='bi bi-sliders icon-blue'></i> &nbsp; Parâmetros de Projeto
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("Restrições do sistema:")

# Inputs (agora ficarão azuis nativamente devido ao config.toml)
target_volume = st.sidebar.number_input("Volume Alvo (m³)", min_value=10.0, value=1000.0, step=10.0)
cost_base = st.sidebar.number_input("Custo Base/Tampa (R$/m²)", min_value=1.0, value=20.0, step=1.0)
cost_side = st.sidebar.number_input("Custo Lateral (R$/m²)", min_value=1.0, value=10.0, step=1.0)

st.sidebar.markdown("---")

# --- Navegação Principal (CORRIGIDO PARA MODO ESCURO) ---
selected = option_menu(
    menu_title=None,
    options=["Otimização", "Massa & Volume", "Simulação Térmica"],
    icons=["calculator", "box-seam", "thermometer-sun"], 
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"}, # Transparente para aceitar tema
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "var(--secondary-background-color)"},
        "nav-link-selected": {"background-color": "#0d6efd"}, # Azul Bootstrap
    }
)

# ==================================================
# MÓDULO 1: OTIMIZAÇÃO
# ==================================================
if selected == "Otimização":
    st.markdown("<h3 class='sub-header'><i class='bi bi-rulers icon-blue'></i> Geometria de Custo Mínimo</h3>", unsafe_allow_html=True)
    st.markdown(r"Aplicação do método de **Lagrange** para minimizar a função custo $C(r,h)$ sujeita à restrição de volume $V(r,h)$.")
    
    # Backend Logic
    optimal_radius = ((target_volume * cost_side) / (2 * np.pi * cost_base))**(1/3)
    optimal_height = target_volume / (np.pi * optimal_radius**2)
    
    area_base_top = 2 * np.pi * optimal_radius**2
    area_side = 2 * np.pi * optimal_radius * optimal_height
    min_cost = (area_base_top * cost_base) + (area_side * cost_side)

    # Layout de Métricas
    c1, c2, c3 = st.columns(3)
    c1.metric("Raio Ótimo (r)", f"{optimal_radius:.2f} m")
    c2.metric("Altura Ótima (h)", f"{optimal_height:.2f} m")
    c3.metric("Custo Estimado", f"R$ {min_cost:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualização
    col_viz1, col_viz2 = st.columns([1, 1])

    with col_viz1:
        st.markdown("#### <i class='bi bi-box icon-gray'></i> Modelo 3D", unsafe_allow_html=True)
        
        z = np.linspace(0, optimal_height, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = optimal_radius * np.cos(theta_grid)
        y_grid = optimal_radius * np.sin(theta_grid)

        fig_3d = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Blues', showscale=False, opacity=0.9)])
        
        # Layout transparente para funcionar no modo escuro
        fig_3d.update_layout(
            scene=dict(
                xaxis_title='X (m)', yaxis_title='Y (m)', zaxis_title='Altura (m)',
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=0), height=400,
            paper_bgcolor='rgba(0,0,0,0)', # Transparente
            plot_bgcolor='rgba(0,0,0,0)'   # Transparente
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_viz2:
        st.markdown("#### <i class='bi bi-graph-up icon-gray'></i> Curva de Custo", unsafe_allow_html=True)
        
        r_range = np.linspace(optimal_radius * 0.5, optimal_radius * 1.5, 100)
        costs = (2 * np.pi * r_range**2 * cost_base) + (2 * target_volume * cost_side / r_range)
        
        fig_2d = go.Figure()
        fig_2d.add_trace(go.Scatter(x=r_range, y=costs, mode='lines', name='Custo', line=dict(color='#0d6efd')))
        fig_2d.add_trace(go.Scatter(x=[optimal_radius], y=[min_cost], mode='markers', name='Mínimo', marker=dict(color='red', size=10)))
        
        fig_2d.update_layout(
            xaxis_title="Raio (m)", yaxis_title="Custo (R$)",
            height=400, hovermode="x unified",
            margin=dict(l=0, r=0, b=0, t=20),
            paper_bgcolor='rgba(0,0,0,0)', # Transparente
            plot_bgcolor='rgba(0,0,0,0)',  # Transparente
            legend=dict(bgcolor='rgba(0,0,0,0)') # Legenda Transparente
        )
        st.plotly_chart(fig_2d, use_container_width=True)

    with st.expander("Detalhes Matemáticos (Lagrange)"):
        st.latex(r"\text{Minimizar } C(r, h) = 2\pi r^2 P_{base} + 2\pi r h P_{lateral}")
        st.latex(r"\frac{h}{r} = 2 \left( \frac{P_{base}}{P_{lateral}} \right)")

# ==================================================
# MÓDULO 2: MASSA
# ==================================================
if selected == "Massa & Volume":
    st.markdown("<h3 class='sub-header'><i class='bi bi-hdd-stack icon-blue'></i> Propriedades Físicas</h3>", unsafe_allow_html=True)
    st.warning("Módulo em desenvolvimento pela Equipe 2")
    
    st.markdown("#### Definição da Densidade")
    st.latex(r"\rho(x, y, z) = A - B \cdot z")
    st.markdown("#### Integral Tripla")
    st.latex(r"M = \int_{0}^{2\pi} \int_{0}^{R} \int_{0}^{H} (A - Bz) \cdot r \, dz \, dr \, d\theta")

# ==================================================
# MÓDULO 3: TÉRMICA
# ==================================================
if selected == "Simulação Térmica":
    st.markdown("<h3 class='sub-header'><i class='bi bi-thermometer-high icon-blue'></i> Termodinâmica</h3>", unsafe_allow_html=True)
    st.warning("Módulo em desenvolvimento pela Equipe 3")
    
    st.markdown("#### Lei de Resfriamento de Newton")
    st.latex(r"\frac{dT}{dt} = -k (T(t) - T_{amb})")