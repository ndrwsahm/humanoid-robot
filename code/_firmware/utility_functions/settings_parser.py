import configparser
from pathlib import Path

def load_robot_settings(robot_id):
    BASE = Path(__file__).resolve().parent.parent  # code/_firmware/
    path = BASE / "configs" / str(robot_id) / "settings.ini"

    config = configparser.ConfigParser()
    config.read(path)
    print("Loading:", path)

    # --- Limb lengths ---
    a1_length = config.getfloat("leg_length", "A1_LENGTH")
    a2_length = config.getfloat("leg_length", "A2_LENGTH")

    # --- Pins ---
    left_pins = [int(x) for x in config["pins"]["LEFT_LEG"].split(",")]
    right_pins = [int(x) for x in config["pins"]["RIGHT_LEG"].split(",")]

    # --- Default angles ---
    left_defaults = [
        config.getfloat("default_angles_left", key)
        for key in (
            "LHR_DEFAULT_ANGLE", "LHA_DEFAULT_ANGLE", "LHE_DEFAULT_ANGLE",
            "LK_DEFAULT_ANGLE", "LAA_DEFAULT_ANGLE", "LAE_DEFAULT_ANGLE"
        )
    ]

    right_defaults = [
        config.getfloat("default_angles_right", key)
        for key in (
            "RHR_DEFAULT_ANGLE", "RHA_DEFAULT_ANGLE", "RHE_DEFAULT_ANGLE",
            "RK_DEFAULT_ANGLE", "RAA_DEFAULT_ANGLE", "RAE_DEFAULT_ANGLE"
        )
    ]

    # --- Angle limits (convert "0-180" → [0, 180]) ---
    left_limits = [
        [int(a), int(b)] for a, b in
        (pair.split("-") for pair in config["angle_limits"]["LEFT_LEG"].split(","))
    ]

    right_limits = [
        [int(a), int(b)] for a, b in
        (pair.split("-") for pair in config["angle_limits"]["RIGHT_LEG"].split(","))
    ]

    # --- Soft start angles ---
    soft_start_angles = (
        [float(x) for x in config["soft_start_angles"]["LEFT_LEG"].split(",")] +
        [float(x) for x in config["soft_start_angles"]["RIGHT_LEG"].split(",")]
    )

    left_pulse_width_settings = [
        [int(a), int(b)] for a, b in
        (pair.split("-") for pair in config["pulse_width_settings"]["LEFT_PULSE_WIDTH_SETTINGS"].split(","))
    ]   

    right_pulse_width_settings = [
        [int(a), int(b)] for a, b in
        (pair.split("-") for pair in config["pulse_width_settings"]["RIGHT_PULSE_WIDTH_SETTINGS"].split(","))
    ]   

    return {
        "A1_LENGTH": a1_length,
        "A2_LENGTH": a2_length,
        "LEFT_LEG_PINS": left_pins,
        "RIGHT_LEG_PINS": right_pins,
        "LEFT_DEFAULTS": left_defaults,
        "RIGHT_DEFAULTS": right_defaults,
        "LEFT_LIMITS": left_limits,
        "RIGHT_LIMITS": right_limits,
        "SOFT_START_ANGLES": soft_start_angles,
        "LEFT_PULSE_WIDTH_SETTINGS": left_pulse_width_settings,
        "RIGHT_PULSE_WIDTH_SETTINGS": right_pulse_width_settings
    }