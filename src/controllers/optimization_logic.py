import numpy as np

def calculate_optimal_geometry(geo_type, num_sides, vol, c_base, c_lat):
    """
    Calcula as dimensões ótimas usando Multiplicadores de Lagrange.
    Retorna: (dimensao_otima, altura_otima, custo_minimo, k_area, nome_dimensao)
    """
    if geo_type == "Cilindro (Padrão)":
        k_area = np.pi
        dim_name = "Raio (r)"
        # Lagrange para Cilindro
        opt_dim = ((vol * c_lat) / (2 * np.pi * c_base))**(1/3)
    else:
        # Lagrange para Prisma
        k_area = num_sides / (4 * np.tan(np.pi / num_sides))
        dim_name = "Lado (L)"
        numerator = num_sides * vol * c_lat
        denominator = 4 * (k_area**2) * c_base
        opt_dim = (numerator / denominator)**(1/3)

    # Altura e Custo são derivados da dimensão ótima
    opt_h = vol / (k_area * opt_dim**2)
    area_base = k_area * opt_dim**2
    
    if geo_type == "Cilindro (Padrão)":
        area_side = 2 * np.pi * opt_dim * opt_h
    else:
        area_side = (num_sides * opt_dim) * opt_h
        
    min_cost = (2 * area_base * c_base) + (area_side * c_lat)

    return opt_dim, opt_h, min_cost, k_area, dim_name

def generate_cost_curve_data(opt_dim, vol, c_base, c_lat, geo_type, num_sides, k_area):
    """Gera dados X e Y para o gráfico de curva de custo."""
    dim_range = np.linspace(opt_dim * 0.5, opt_dim * 1.5, 100)
    
    if geo_type == "Cilindro (Padrão)":
        c_curve = (2 * np.pi * dim_range**2 * c_base) + (2 * vol * c_lat / dim_range)
    else:
        term_area = 2 * k_area * (dim_range**2) * c_base
        term_side = (num_sides * dim_range) * (vol / (k_area * dim_range**2)) * c_lat
        c_curve = term_area + term_side
        
    return dim_range, c_curve