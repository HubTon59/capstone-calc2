import streamlit as st
from streamlit_option_menu import option_menu

# Importando nossos novos módulos
from src.utils import ui_helper
from src.views import optimization_view, physics_view, thermal_view

# 1. Configuração Global
st.set_page_config(
    page_title="Projeto Tanque Ótimo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Carregar Recursos
ui_helper.load_css("assets/style.css")
ui_helper.render_header()

# 3. Sidebar (Inputs Globais)
st.sidebar.markdown("""
<div class="sidebar-header">
    <i class='bi bi-sliders icon-blue'></i> &nbsp; Parâmetros de Projeto
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("**Forma do Recipiente:**")
geometry_type = st.sidebar.selectbox("Selecione:", ["Cilindro (Padrão)", "Prisma Regular (Polígono)"], label_visibility="collapsed")

num_sides = 0
if geometry_type == "Prisma Regular (Polígono)":
    num_sides = st.sidebar.slider("Lados (n)", 3, 12, 4)

st.sidebar.markdown("---")
target_volume = st.sidebar.number_input("Volume Alvo (m³)", min_value=10.0, value=1000.0)
cost_base = st.sidebar.number_input("Custo Base (R$/m²)", min_value=1.0, value=20.0)
cost_side = st.sidebar.number_input("Custo Lateral (R$/m²)", min_value=1.0, value=10.0)

st.sidebar.markdown("---")
st.sidebar.caption("v5.0 - Modular MVC Architecture")

# 4. Navegação
selected = option_menu(
    menu_title=None,
    options=["Otimização", "Massa & Volume", "Simulação Térmica"],
    icons=["calculator", "box-seam", "thermometer-sun"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "transparent"},
        "nav-link-selected": {"background-color": "#0d6efd"},
    }
)

# 5. Roteamento (Controller Principal)
if selected == "Otimização":
    optimization_view.render(geometry_type, num_sides, target_volume, cost_base, cost_side)

elif selected == "Massa & Volume":
    physics_view.render(geometry_type, num_sides, target_volume, cost_base, cost_side)

elif selected == "Simulação Térmica":
    thermal_view.render()