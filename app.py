import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

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

st.markdown("""
<h1 class='main-header'>
    <i class="bi bi-buildings-fill icon-blue"></i> Otimização de Tanque Industrial
</h1>
<p style='font-size: 1.1rem; opacity: 0.8;'>
    <b>Cálculo 2 Aplicado à Engenharia</b> — Modelagem matemática para maximização de eficiência e análise de fenômenos físicos.
</p>
""", unsafe_allow_html=True)

with st.expander("📘 Entenda o Problema de Engenharia (O Dilema Custo vs. Geometria)", expanded=False):
    st.markdown("""
    **O Desafio:** Projetar um reservatório que armazene um volume fixo $V$, mas que custe o mínimo possível.
    
    **A Tensão:** * Se fizermos o tanque muito **largo e baixo** (parece uma piscina), gastamos muito material na base e tampa (que são caros por serem reforçados).
    * Se fizermos o tanque muito **alto e fino** (parece um tubo), gastamos muito material na parede lateral.
    
    **A Solução via Cálculo:** Existe um "ponto ideal" entre esses dois extremos. Usamos **Derivadas Parciais** e **Multiplicadores de Lagrange** para encontrar exatamente onde a taxa de variação do custo se anula em relação à geometria.
    """)

st.sidebar.markdown("""
<div class="sidebar-header">
    <i class='bi bi-sliders icon-blue'></i> &nbsp; Parâmetros de Projeto
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("**Forma do Recipiente:**")
geometry_type = st.sidebar.selectbox(
    "Selecione o formato:",
    ["Cilindro (Padrão)", "Prisma Regular (Polígono)"],
    label_visibility="collapsed"
)

num_sides = 0
if geometry_type == "Prisma Regular (Polígono)":
    num_sides = st.sidebar.slider("Número de Lados da Base (n)", min_value=3, max_value=12, value=4, help="3=Triângulo, 4=Quadrado/Retângulo, 6=Hexágono...")

st.sidebar.markdown("---")
st.sidebar.markdown("**Restrições e Custos:**")

target_volume = st.sidebar.number_input("Volume Alvo (m³)", min_value=10.0, value=1000.0, step=10.0)
cost_base = st.sidebar.number_input("Custo Base/Tampa (R$/m²)", min_value=1.0, value=20.0, step=1.0, help="Geralmente mais caro devido à fundação/reforço.")
cost_side = st.sidebar.number_input("Custo Lateral (R$/m²)", min_value=1.0, value=10.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.caption("v4.0 - Master Edition")

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

if selected == "Otimização":
    st.markdown("<h3 class='sub-header'><i class='bi bi-rulers icon-blue'></i> Geometria de Custo Mínimo</h3>", unsafe_allow_html=True)
    
    opt_dimension = 0 
    opt_height = 0
    min_cost = 0
    dim_name = "" 
    k_area = 0

    if geometry_type == "Cilindro (Padrão)":
        dim_name = "Raio (r)"
        k_area = np.pi
        opt_dimension = ((target_volume * cost_side) / (2 * np.pi * cost_base))**(1/3)
        opt_height = target_volume / (np.pi * opt_dimension**2)
        area_base = np.pi * opt_dimension**2
        area_side = 2 * np.pi * opt_dimension * opt_height
        min_cost = (2 * area_base * cost_base) + (area_side * cost_side)
    else:
        dim_name = "Lado da Base (L)"
        n = num_sides
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
        st.markdown(f"#### <i class='bi bi-box icon-gray'></i> Modelo 3D Otimizado", unsafe_allow_html=True)
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
            scene=dict(xaxis_title='X (m)', yaxis_title='Y (m)', zaxis_title='Altura (m)', aspectmode='data'),
            margin=dict(l=0, r=0, b=0, t=0), height=400,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_viz2:
        st.markdown("#### <i class='bi bi-graph-up icon-gray'></i> Curva de Otimização", unsafe_allow_html=True)
        st.caption("Observe como o Custo Total (curva azul) atinge o ponto mais baixo exatamente na dimensão calculada.")
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
            height=380, hovermode="x unified",
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_2d, use_container_width=True)

    st.markdown("---")
    st.markdown("#### <i class='bi bi-journal-text icon-gray'></i> Da Teoria à Prática", unsafe_allow_html=True)
    
    col_math, col_code = st.columns([1, 1])
    
    with col_math:
        st.markdown("**1. A Modelagem (Cálculo 2)**")
        st.write("""
        Para otimizar o custo respeitando o volume fixo, utilizamos os **Multiplicadores de Lagrange**.
        O ponto ótimo ocorre quando o gradiente do Custo é paralelo ao gradiente do Volume:
        """)
        st.latex(r"\nabla C = \lambda \nabla V \implies \frac{\partial C}{\partial r} = \lambda \frac{\partial V}{\partial r}")
        
        st.write("Resolvendo esse sistema de equações parciais, isolamos a dimensão característica:")
        
        if geometry_type.startswith("Cil"):
            st.latex(r"r_{ótimo} = \sqrt[3]{\frac{V \cdot C_{lateral}}{2\pi \cdot C_{base}}}")
            st.caption("Observe: Se o Custo Lateral aumenta (numerador), o raio aumenta (tanque fica mais baixo e largo) para usar menos parede.")
        else:
            st.latex(r"L_{ótimo} = \sqrt[3]{\frac{n \cdot V \cdot C_{lateral}}{4 \cdot K_{area}^2 \cdot C_{base}}}")
            st.caption(f"Fórmula generalizada para polígono de {num_sides} lados. $K_{{area}}$ é a constante geométrica da base.")

    with col_code:
        st.markdown("**2. O Algoritmo (Python)**")
        st.write("""
        No código, não precisamos refazer as derivadas a cada execução. 
        Nós programamos a **solução algébrica final** (a fórmula isolada à esquerda).
        """)
        
        if geometry_type.startswith("Cil"):
            code_snippet = f"""
# Variáveis vindas dos Inputs
V = {target_volume}      # Volume Alvo
C_lat = {cost_side}    # Custo Lateral
C_base = {cost_base}   # Custo Base

# Tradução direta da fórmula matemática:
# np.pi é a constante pi (3.1415...)
# **(1/3) é a raiz cúbica
raio_otimo = ((V * C_lat) / (2 * np.pi * C_base))**(1/3)
"""
        else:
            code_snippet = f"""
# Para Prismas, calculamos o fator K primeiro
n = {num_sides}
# tan() vem da biblioteca numpy (np)
K_area = n / (4 * np.tan(np.pi / n)) 

# Fórmula Generalizada implementada:
numerador = n * V * C_lat
denominador = 4 * (K_area**2) * C_base
lado_otimo = (numerador / denominador)**(1/3)
"""
        st.code(code_snippet, language="python")
        st.info("💡 **Eficiência:** O Python apenas substitui os valores na fórmula derivada pelo Cálculo. Isso é instantâneo, diferentemente de métodos de 'tentativa e erro'.")

if selected == "Massa & Volume":
    st.markdown("<h3 class='sub-header'><i class='bi bi-hdd-stack icon-blue'></i> Propriedades Físicas e Massa</h3>", unsafe_allow_html=True)
    
    if geometry_type.startswith("Cil"):
        opt_dim = ((target_volume * cost_side) / (2 * np.pi * cost_base))**(1/3)
        opt_h = target_volume / (np.pi * opt_dim**2)
        k_area = np.pi
    else:
        n = num_sides
        k_area = n / (4 * np.tan(np.pi / n))
        num = n * target_volume * cost_side
        den = 4 * (k_area**2) * cost_base
        opt_dim = (num / den)**(1/3)
        opt_h = target_volume / (k_area * opt_dim**2)

    area_base = k_area * opt_dim**2

    col_mat1, col_mat2 = st.columns(2)
    with col_mat1:
        rho_base = st.number_input("Densidade na Base (kg/m³)", value=8000.0, step=100.0)
    with col_mat2:
        rho_top = st.number_input("Densidade no Topo (kg/m³)", value=7500.0, step=100.0)

    density_gradient_B = (rho_base - rho_top) / opt_h

    st.markdown("---")
    
    col_metrics, col_graph = st.columns([1, 2])
    
    with col_metrics:
        st.markdown("#### <i class='bi bi-calculator icon-gray'></i> Resultados", unsafe_allow_html=True)
        
        total_mass = area_base * (rho_base * opt_h - (density_gradient_B * opt_h**2) / 2)
        
        moment_xy = area_base * ((rho_base * opt_h**2)/2 - (density_gradient_B * opt_h**3)/3)
        z_cm = moment_xy / total_mass

        st.metric("Massa Total", f"{total_mass:,.2f} kg")
        st.metric("Centro de Massa (Z)", f"{z_cm:.2f} m")
        st.caption(f"Ponto de equilíbrio a {(z_cm/opt_h)*100:.1f}% da altura.")

    with col_graph:
        z_vals = np.linspace(0, opt_h, 100)
        rho_vals = rho_base - density_gradient_B * z_vals
        
        fig_rho = go.Figure()
        fig_rho.add_trace(go.Scatter(x=rho_vals, y=z_vals, mode='lines', fill='tozeroy', name='Densidade', line=dict(color='#198754'))) # Verde Engenharia
        fig_rho.update_layout(
            title="Variação da Densidade com a Altura",
            xaxis_title="Densidade (kg/m³)", 
            yaxis_title="Altura do Tanque (m)",
            height=300, 
            margin=dict(t=30, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_rho, use_container_width=True)

    st.markdown("---")
    st.markdown("#### <i class='bi bi-journal-text icon-gray'></i> Da Teoria à Prática", unsafe_allow_html=True)
    
    col_math, col_code = st.columns([1, 1])
    
    with col_math:
        st.markdown("**1. A Modelagem (Integrais)**")
        st.write("""
        A densidade não é constante, então não podemos usar multiplicação simples.
        Precisamos **fatiar** o tanque em discos infinitesimais de espessura $dz$.
        A massa de cada disco é $dM = Area \cdot \rho(z) \cdot dz$.
        """)
        
        st.latex(r"M = \int_{0}^{H} Area_{base} \cdot (\rho_{base} - B \cdot z) \, dz")
        st.caption("Resolvendo essa integral definida, obtemos a fórmula algébrica usada no software.")
        
        st.markdown("**Centro de Massa:**")
        st.write("Calculado pela razão entre o Momento de 1ª Ordem e a Massa Total:")
        st.latex(r"\bar{z} = \frac{\int z \cdot \rho(z) \, dV}{\int \rho(z) \, dV}")

    with col_code:
        st.markdown("**2. O Algoritmo (Python)**")
        st.write("O código implementa o resultado analítico da integral $\int (A - Bz)dz = Az - \frac{Bz^2}{2}$.")
        
        code_snippet = f"""
# Dados Físicos
Area = {area_base:.2f}
h = {opt_h:.2f}
rho_base = {rho_base}
B = {density_gradient_B:.4f} # Gradiente de densidade

# Cálculo da Massa (Resultado da Integral)
# Termo 1: rho_base * h
# Termo 2: (B * h^2) / 2
massa = Area * (rho_base * h - (density_gradient_B * h**2) / 2)

# Cálculo do Centro de Massa (Momento / Massa)
momento = Area * ((rho_base * h**2)/2 - (density_gradient_B * h**3)/3)
z_cm = momento / massa
"""
        st.code(code_snippet, language="python")

if selected == "Simulação Térmica":
    st.markdown("<h3 class='sub-header'><i class='bi bi-thermometer-high icon-blue'></i> Termodinâmica e EDO</h3>", unsafe_allow_html=True)
    st.markdown("Previsão de temperatura baseada na **Lei de Resfriamento de Newton**.")

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

    t_values = np.linspace(0, time_span, 100)
    temp_values = t_amb + (t_initial - t_amb) * np.exp(-k_const * t_values)
    risk_indices = np.where(temp_values >= t_critical)[0]
    time_to_fail = t_values[risk_indices[0]] if len(risk_indices) > 0 else None

    col_graph, col_educ = st.columns([2, 1])

    with col_graph:
        st.markdown("#### <i class='bi bi-graph-up-arrow icon-gray'></i> Curva de Aquecimento", unsafe_allow_html=True)
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=t_values, y=temp_values, mode='lines', name='Temperatura', line=dict(color='#0d6efd', width=3)))
        fig_temp.add_trace(go.Scatter(x=[0, time_span], y=[t_critical, t_critical], mode='lines', name='Crítico', line=dict(color='red', dash='dash')))
        fig_temp.update_layout(xaxis_title="Tempo (h)", yaxis_title="Temp (°C)", height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode="x unified", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_temp, use_container_width=True)
        
        if time_to_fail:
            st.error(f"🚨 **PERIGO:** Limite atingido em **{time_to_fail:.1f} horas**.")
        else:
            st.success("✅ **SEGURO:** Temperatura estável no período.")

    with col_educ:
        st.markdown("#### <i class='bi bi-journal-text icon-gray'></i> Equações Diferenciais (EDO)", unsafe_allow_html=True)
        st.write("""
        A Lei de Newton afirma que a **velocidade** de mudança da temperatura ($dT/dt$) é proporcional à diferença entre a temperatura atual e a ambiente.
        """)
        st.latex(r"\frac{dT}{dt} \propto (T - T_{amb})")
        
        st.markdown("**Interpretação:**")
        st.write("Quando o produto está muito frio e o dia quente, a diferença é grande, então ele esquenta rápido (inclinação alta no início do gráfico). Conforme ele esquenta, a troca de calor diminui.")
