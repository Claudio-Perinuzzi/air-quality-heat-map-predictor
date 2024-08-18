
def calculate_aqi(concentration, breakpoints):
    for bp_low, bp_high, i_low, i_high in breakpoints:
        if bp_low <= concentration <= bp_high:
            aqi = ((i_high - i_low) / (bp_high - bp_low)) * (concentration - bp_low) + i_low
            return int(round(aqi))

    return None

def calculate_aqi_pm25(concentration):

    # As per EPA guidelines, truncate to 1 decimal place
    concentration = float(f"{concentration:.1f}")

    pm25_breakpoints = [
        (0.0, 9.0, 0, 50),
        (9.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 125.4, 151, 200),
        (125.5, 225.4, 201, 300),
        (225.5, float('inf'), 301, float('inf'))
    ]
    
    return calculate_aqi(concentration, pm25_breakpoints)


def calculate_aqi_no2(concentration):
    
    # As per EPA guidelines, truncate to integer
    concentration = int(concentration)

    no2_breakpoints = [
        (0, 53, 0, 50),
        (54, 100, 51, 100),
        (101, 360, 101, 150),
        (361, 649, 151, 200),
        (650, 1249, 201, 300),
        (1250, float('inf'), 301, float('inf'))    
    ]

    return calculate_aqi(concentration, no2_breakpoints)


# o3 is measured avg 8 hours in NYC
def calculate_aqi_o3(concentration):
    
    # As per EPA guidelines, truncate to 3 decimal places
    concentration = float(f"{concentration:.3f}")

    o3_breakpoints = [
        (0, 54, 0, 50),
        (55, 70, 51, 100),
        (71, 85, 101, 150),
        (86, 105, 151, 200),
        (106, 200, 201, 300),
        (201, float('inf'), 301, float('inf'))    
    ]

    return calculate_aqi(concentration, o3_breakpoints)
