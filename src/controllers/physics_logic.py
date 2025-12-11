import numpy as np
from src.controllers.optimization_logic import calculate_optimal_geometry

def calculate_mass_properties(geo_type, num_sides, vol, c_base, c_lat, rho_base, rho_top):
    """
    Recalcula geometria e integra massa e centro de massa.
    """
    # 1. Recupera geometria ótima (Reuso de lógica)
    opt_dim, opt_h, _, k_area, _ = calculate_optimal_geometry(geo_type, num_sides, vol, c_base, c_lat)
    
    area_base = k_area * opt_dim**2
    density_gradient_B = (rho_base - rho_top) / opt_h

    # 2. Integral da Massa
    total_mass = area_base * (rho_base * opt_h - (density_gradient_B * opt_h**2) / 2)
    
    # 3. Integral do Momento (Centro de Massa)
    moment_xy = area_base * ((rho_base * opt_h**2)/2 - (density_gradient_B * opt_h**3)/3)
    z_cm = moment_xy / total_mass

    return total_mass, z_cm, opt_h, rho_base, density_gradient_B

def generate_density_profile(h, rho_base, B):
    z_vals = np.linspace(0, h, 100)
    rho_vals = rho_base - B * z_vals
    return z_vals, rho_vals