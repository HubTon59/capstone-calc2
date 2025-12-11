import streamlit as st

def load_css(file_path):
    """Carrega o arquivo CSS global."""
    try:
        with open(file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo de estilo não encontrado: {file_path}")

def render_header():
    """Renderiza o cabeçalho padrão das páginas."""
    st.markdown("""
    <h1 class='main-header'>
        <i class="bi bi-buildings-fill icon-blue"></i> Otimização de Tanque Industrial
    </h1>
    <p style='font-size: 1.1rem; opacity: 0.8;'>
        <b>Cálculo 2 Aplicado à Engenharia</b> — Modelagem matemática para maximização de eficiência e análise de fenômenos físicos.
    </p>
    """, unsafe_allow_html=True)
    with st.expander("Entenda o Problema de Engenharia (O Dilema Custo vs. Geometria)", expanded=False):
        st.markdown("""
        **O Desafio:** Projetar um reservatório que armazene um volume fixo $V$, mas que custe o mínimo possível.
        
        **A Tensão:** * Se fizermos o tanque muito **largo e baixo** (parece uma piscina), gastamos muito material na base e tampa (que são caros por serem reforçados).
        * Se fizermos o tanque muito **alto e fino** (parece um tubo), gastamos muito material na parede lateral.
        
        **A Solução via Cálculo:** Existe um "ponto ideal" entre esses dois extremos. Usamos **Derivadas Parciais** e **Multiplicadores de Lagrange** para encontrar exatamente onde a taxa de variação do custo se anula em relação à geometria.
        """)
    