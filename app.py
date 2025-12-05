import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

<<<<<<< HEAD

=======
>>>>>>> develop
st.set_page_config(
    page_title="Projeto Tanque Ótimo",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("assets/style.css")

<<<<<<< HEAD

=======
>>>>>>> develop
st.markdown("""
<h1 class='main-header'>
    <i class="bi bi-buildings-fill icon-blue"></i> Otimização de Tanque Industrial
</h1>
<p style='font-size: 1.1rem; opacity: 0.8;'>
    <b>Cálculo 2 Aplicado à Engenharia</b> — Sistema para determinação de geometria ideal minimizando custos.
</p>
""", unsafe_allow_html=True)

<<<<<<< HEAD

=======
>>>>>>> develop
st.sidebar.markdown("""
<div class="sidebar-header">
    <i class='bi bi-sliders icon-blue'></i> &nbsp; Parâmetros de Projeto
</div>
""", unsafe_allow_html=True)

<<<<<<< HEAD

=======
>>>>>>> develop
st.sidebar.markdown("**Forma do Recipiente:**")
geometry_type = st.sidebar.selectbox(
    "Selecione o formato:",
    ["Cilindro (Padrão)", "Prisma Regular (Polígono)"],
    label_visibility="collapsed"
)

<<<<<<< HEAD

=======
>>>>>>> develop
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

<<<<<<< HEAD

=======
>>>>>>> develop
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


<<<<<<< HEAD
# MÓDULO 1: OTIMIZAÇÃO
=======
>>>>>>> develop
if selected == "Otimização":
    st.markdown("<h3 class='sub-header'><i class='bi bi-rulers icon-blue'></i> Geometria de Custo Mínimo</h3>", unsafe_allow_html=True)
    
    opt_dimension = 0
    opt_height = 0
    min_cost = 0
    dim_name = ""

    if geometry_type == "Cilindro (Padrão)":
        dim_name = "Raio (r)"
        st.markdown(r"Aplicação de **Lagrange** para **Cilindro**. Minimizando custo sujeito a Volume $V = \pi r^2 h$.")
<<<<<<< HEAD
        
        opt_dimension = ((target_volume * cost_side) / (2 * np.pi * cost_base))**(1/3)
        opt_height = target_volume / (np.pi * opt_dimension**2)
        
=======

        opt_dimension = ((target_volume * cost_side) / (2 * np.pi * cost_base))**(1/3)
        opt_height = target_volume / (np.pi * opt_dimension**2)
        

>>>>>>> develop
        area_base = np.pi * opt_dimension**2
        area_side = 2 * np.pi * opt_dimension * opt_height
        min_cost = (2 * area_base * cost_base) + (area_side * cost_side)
        
    else:
        dim_name = "Lado da Base (L)"
        n = num_sides
        st.markdown(f"Aplicação de **Lagrange** para **Prisma de {n} lados**. Minimizando custo sujeito a Volume $V = Area_{{base}} \cdot h$.")
        
        k_area = n / (4 * np.tan(np.pi / n))
        
        numerator = n * target_volume * cost_side
        denominator = 4 * (k_area**2) * cost_base
        opt_dimension = (numerator / denominator)**(1/3)
        
        opt_height = target_volume / (k_area * opt_dimension**2)
        
        area_base = k_area * opt_dimension**2
        area_side = (n * opt_dimension) * opt_height
        min_cost = (2 * area_base * cost_base) + (area_side * cost_side)

    c1, c2, c3 = st.columns(3)
    c1.metric(f"{dim_name} Ótimo", f"{opt_dimension:.2f} m")
    c2.metric("Altura Ótima (h)", f"{opt_height:.2f} m")
    c3.metric("Custo Mínimo", f"R$ {min_cost:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    col_viz1, col_viz2 = st.columns([1, 1])

    with col_viz1:
        st.markdown(f"#### <i class='bi bi-box icon-gray'></i> Modelo 3D ({'Cilindro' if geometry_type.startswith('Cil') else f'Prisma {num_sides} lados'})", unsafe_allow_html=True)
        
        z = np.linspace(0, opt_height, 2)
        
        if geometry_type == "Cilindro (Padrão)":
            theta = np.linspace(0, 2*np.pi, 60)
            radius_viz = opt_dimension
        else:
            theta = np.linspace(0, 2*np.pi, num_sides + 1)
            radius_viz = opt_dimension / (2 * np.sin(np.pi / num_sides))

        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = radius_viz * np.cos(theta_grid)
        y_grid = radius_viz * np.sin(theta_grid)

        fig_3d = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Blues', showscale=False, opacity=0.8)])
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
        
        dim_range = np.linspace(opt_dimension * 0.5, opt_dimension * 1.5, 100)
        
        if geometry_type.startswith("Cil"):
            c_curve = (2 * np.pi * dim_range**2 * cost_base) + (2 * target_volume * cost_side / dim_range)
        else:
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

    with st.expander("Ver Memória de Cálculo (Derivada)"):
        if geometry_type.startswith("Cil"):
            st.latex(r"C(r) = 2\pi r^2 C_{base} + \frac{2 V C_{lat}}{r}")
            st.latex(r"\frac{dC}{dr} = 4\pi r C_{base} - \frac{2 V C_{lat}}{r^2} = 0")
        else:
            st.write(f"Para um prisma regular de {num_sides} lados com lado $L$:")
            st.latex(r"Area_{base} = \frac{n L^2}{4 \tan(\pi/n)}")
            st.latex(r"C(L) = 2 A_{base} C_{base} + \frac{n V C_{lat}}{Area_{base}}")

<<<<<<< HEAD

# MÓDULO 2: MASSA
if selected == "Massa & Volume":
    st.markdown("<h3 class='sub-header'><i class='bi bi-hdd-stack icon-blue'></i> Propriedades Físicas</h3>", unsafe_allow_html=True)
    st.warning("Módulo em desenvolvimento...")
    st.markdown("Cálculo de integrais ajustado para a geometria selecionada.")

=======

if selected == "Massa & Volume":
    st.markdown("<h3 class='sub-header'><i class='bi bi-hdd-stack icon-blue'></i> Propriedades Físicas e Massa</h3>", unsafe_allow_html=True)

    opt_dim = 0
    opt_h = 0
    k_area = 0
    
    if geometry_type.startswith("Cil"):
        opt_dim = ((target_volume * cost_side) / (2 * np.pi * cost_base))**(1/3)
        opt_h = target_volume / (np.pi * opt_dim**2)
        k_area = np.pi
        geo_name = "Cilindro"
    else:
        n = num_sides
        k_area = n / (4 * np.tan(np.pi / n))
        num = n * target_volume * cost_side
        den = 4 * (k_area**2) * cost_base
        opt_dim = (num / den)**(1/3)
        opt_h = target_volume / (k_area * opt_dim**2)
        geo_name = f"Prisma ({n} lados)"

    area_base = k_area * opt_dim**2

    st.markdown(f"**Configuração do Material ({geo_name}):**")
    st.info(f"Dimensões Otimizadas importadas: Base (r/L) = {opt_dim:.2f}m | Altura = {opt_h:.2f}m | Área Base = {area_base:.2f}m²")

    col_mat1, col_mat2 = st.columns(2)
    with col_mat1:
        rho_base = st.number_input("Densidade na Base (kg/m³)", value=8000.0, step=100.0, help="Ex: Aço reforçado na base")
    with col_mat2:
        rho_top = st.number_input("Densidade no Topo (kg/m³)", value=7500.0, step=100.0, help="Ex: Aço mais leve no topo")

    if rho_top > rho_base:
        st.error("A densidade no topo geralmente é menor ou igual à da base.")

    density_gradient_B = (rho_base - rho_top) / opt_h

    st.markdown("---")

    col_result, col_code = st.columns([1, 1])

    with col_result:
        st.markdown("#### <i class='bi bi-calculator'></i> Resultados", unsafe_allow_html=True)
        
        total_mass = area_base * (rho_base * opt_h - (density_gradient_B * opt_h**2) / 2)

        moment_xy = area_base * ((rho_base * opt_h**2)/2 - (density_gradient_B * opt_h**3)/3)
        z_cm = moment_xy / total_mass

        st.metric("Massa Total Estimada", f"{total_mass:,.2f} kg")
        st.metric("Centro de Massa (Altura Z)", f"{z_cm:.2f} m")
        st.caption(f"O centro de massa está a {(z_cm/opt_h)*100:.1f}% da altura total.")

        z_vals = np.linspace(0, opt_h, 100)
        rho_vals = rho_base - density_gradient_B * z_vals
        
        fig_rho = go.Figure()
        fig_rho.add_trace(go.Scatter(x=rho_vals, y=z_vals, mode='lines', fill='tozeroy', name='Densidade'))
        fig_rho.update_layout(
            title="Perfil de Densidade (Parede do Tanque)",
            xaxis_title="Densidade (kg/m³)",
            yaxis_title="Altura Z (m)",
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_rho, use_container_width=True)

    with col_code:
        st.markdown("#### <i class='bi bi-code-slash'></i> Conexão Cálculo-Código", unsafe_allow_html=True)
        
        st.markdown("**1. O Problema Matemático**")
        st.write("A massa não é constante. Usamos uma integral definida para somar as 'fatias' infinitesimais de massa ao longo da altura $z$.")
        st.latex(r"M = \int_{0}^{H} Area_{base} \cdot \rho(z) \, dz")
        st.latex(r"\text{Onde } \rho(z) = \rho_{base} - \frac{\Delta \rho}{H} \cdot z")

        st.markdown("**2. A Implementação em Python**")
        st.write("O código abaixo resolve a integral definida analiticamente:")
        code_snippet = f'''
# Parâmetros
area = {area_base:.2f}
h = {opt_h:.2f}
rho_b = {rho_base}
B = {density_gradient_B:.4f}

# Resolução da Integral Definida
# Int(A - Bz) dz  =>  Az - (Bz^2)/2
termo1 = rho_b * h
termo2 = (B * h**2) / 2

massa = area * (termo1 - termo2)
# Resultado: {total_mass:.2f} kg
'''
        st.code(code_snippet, language="python")
        st.success("Nota: Em projetos complexos, usaríamos `scipy.integrate.quad` para resolver numericamente, mas como a função densidade é linear, a solução exata é mais rápida.")

>>>>>>> develop

# MÓDULO 3: TÉRMICA
if selected == "Simulação Térmica":
    st.markdown("<h3 class='sub-header'><i class='bi bi-thermometer-high icon-blue'></i> Termodinâmica</h3>", unsafe_allow_html=True)
    st.warning("Módulo em desenvolvimento...")