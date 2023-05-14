import math


def section_modulus_inv(length, thickness):
    return (6*length) / (pow(length, 4) - pow(length - (thickness * 2), 4))


def side_plate_membrane_stress(pressure, radius, length, thickness):
    return (pressure * (radius + length)) / thickness


def corner_membrane_stress(pressure, radius, length, thickness):
    return (pressure / thickness) * ((math.sqrt(2) * length) + radius)


def side_plate_bending_stress_corner(pressure, radius, length, thickness):
    return (section_modulus_inv(length, thickness) / 2) * ((2 * ma(pressure, radius, length)) + (pressure * pow(length, 2)))


def side_plate_bending_stress_center(pressure, radius, length, thickness):
    return ma(pressure, radius, length) * section_modulus_inv(length, thickness)


def corner_bending_stress(pressure, radius, length, thickness):
    return mr(pressure, radius, length) * section_modulus_inv(length, thickness)


def mr(pressure, radius, length):
    theta = math.radians(45)
    coeff = (radius * (math.cos(theta) - (1 - math.sin(theta)))) + 0.5

    return ma(pressure, radius, length) + (pressure * length * coeff)


def ma(pressure, radius, length):
    return pressure / (k3(radius, length))


def k3(radius, length):
    sig = radius / length

    num = ((12 * pow(sig, 2)) - (3 * math.pi * pow(sig, 2)) + 2 + (1.5 * sig * math.pi))
    den = (12 + (3 * math.pi * sig))

    return -pow(length, 2) * (num / den)


def validate_design():
    print("Please enter the following information:")

    side_length = float(input("Cross sectional length of the sides of the rectangle (in mm): "))
    height = float(input("Height of the rectangular shape (in mm): "))
    radius = float(input("Radius of the corner (in mm):"))
    thickness = float(input("Thickness of the rectangle (in mm): "))
    pressure = float(input("Pressure (MPa)"))
    safety_factor = float(input("Safety factor (dimensionless): "))
    yield_strength = float(input("Yield strength of the material (in MPa): "))

    print(yield_strength / safety_factor)

    allowable = side_plate_membrane_stress(pressure, radius, side_length, thickness) + \
                side_plate_bending_stress_center(pressure, radius, side_length, thickness)

    print("Total side membrane + bending at the center: ", allowable)

    allowable = side_plate_membrane_stress(pressure, radius, side_length, thickness) + \
                side_plate_bending_stress_corner(pressure, radius, side_length, thickness)

    print("Total side membrane + bending at the corner: ", allowable)

    allowable = corner_membrane_stress(pressure, radius, side_length, thickness) + \
                corner_bending_stress(pressure, radius, side_length, thickness)

    print("Total corner membrane + bending: ", allowable)


if __name__ == "__main__":
    validate_design()
