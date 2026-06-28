from math import cos, pi, radians, sin, sqrt, tan


def albers(lon: float, lat: float) -> tuple[float, float]:
    # D3's default geoAlbers parameters for the lower 48 states.
    phi1 = radians(29.5)
    phi2 = radians(45.5)
    phi0 = radians(38.7)
    lambda0 = radians(96 + 0.6)
    scale = 1070
    translate = (480, 250)

    n = 0.5 * (sin(phi1) + sin(phi2))
    c = cos(phi1) ** 2 + 2 * n * sin(phi1)
    rho0 = sqrt(c - 2 * n * sin(phi0)) / n

    lam = radians(lon)
    phi = radians(lat)
    theta = n * (lam + lambda0)
    rho = sqrt(c - 2 * n * sin(phi)) / n
    x = translate[0] + scale * rho * sin(theta)
    y = translate[1] - scale * (rho0 - rho * cos(theta))
    return x, y


for name, lon, lat in [
    ("Texas A&M", -96.35, 30.61),
    ("TX NW", -106.65, 36.5),
    ("TX NE", -93.51, 36.5),
    ("TX SW", -106.65, 25.84),
    ("TX SE", -93.51, 25.84),
]:
    print(name, albers(lon, lat))
