import numpy as np

def simulate_cooling(t_amb, t_initial, t_critical, time_span, k_const):
    """
    Resolve a EDO de Newton e verifica falhas.
    """
    t_values = np.linspace(0, time_span, 100)
    # Solução Analítica
    temp_values = t_amb + (t_initial - t_amb) * np.exp(-k_const * t_values)
    
    # Verificação de Risco
    risk_indices = np.where(temp_values >= t_critical)[0]
    time_to_fail = t_values[risk_indices[0]] if len(risk_indices) > 0 else None
    
    return t_values, temp_values, time_to_fail