import re
from pathlib import Path

# Default firmware config template
DEFAULT_TEMPLATE = """\
[leg_length]
A1_LENGTH = 12
A2_LENGTH = 9.25

[pins]
LEFT_LEG = 8,9,10,11,12,13
RIGHT_LEG = 0,1,2,3,4,5

[default_angles_left]
LHR_DEFAULT_ANGLE = 90
LHA_DEFAULT_ANGLE = 90
LHE_DEFAULT_ANGLE = 90
LK_DEFAULT_ANGLE = 90
LAA_DEFAULT_ANGLE = 90
LAE_DEFAULT_ANGLE = 90

[default_angles_right]
RHR_DEFAULT_ANGLE = 90
RHA_DEFAULT_ANGLE = 90
RHE_DEFAULT_ANGLE = 90
RK_DEFAULT_ANGLE  = 90
RAA_DEFAULT_ANGLE = 90
RAE_DEFAULT_ANGLE = 90

[soft_start_angles]
left_leg = 90,90.0,55.8,90.9,90.0,146.7
right_leg = 90,90.0,124.1,89.0,90.0,33.2

[angle_limits]
left_leg = 0-180,0-180,0-180,0-180,0-180,0-180
right_leg = 0-180,0-180,0-180,0-180,0-180,0-180

[pulse_width_settings]
LEFT_PULSE_WIDTH_SETTINGS = 500-2500,500-2500,500-2500,500-2500,500-2500,500-2500
RIGHT_PULSE_WIDTH_SETTINGS = 500-2500,500-2500,500-2500,500-2500,500-2500,500-2500
"""

def write_cal_data(offset_data, ID):
    settings_path = Path(f"_firmware/configs/{ID}/settings.ini")

    print(settings_path)

    # Ensure folder exists
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    # If file doesn't exist, create it with default template
    if not settings_path.exists():
        settings_path.write_text(DEFAULT_TEMPLATE)

    # Read file
    content = settings_path.read_text()

    # Apply replacements
    keys = [
        "LHR", "LHA", "LHE", "LK", "LAA", "LAE",
        "RHR", "RHA", "RHE", "RK", "RAA", "RAE"
    ]

    
    for i, key in enumerate(keys):
        pattern = rf"{key}_DEFAULT_ANGLE\s*=\s*.*"
        replacement = f"{key}_DEFAULT_ANGLE = {offset_data[i]}"
        content = re.sub(pattern, replacement, content)

    # Write updated content
    settings_path.write_text(content)

    print(f"config/{ID}/settings.ini updated successfully.")

def write_pwm_calibration_data(pwm_min, pwm_max, enabled, ID):
    settings_path = Path(f"_firmware/configs/{ID}/settings.ini")

    # Ensure folder exists
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    # If file doesn't exist, create it with default template
    if not settings_path.exists():
        settings_path.write_text(DEFAULT_TEMPLATE)

    # Read file
    content = settings_path.read_text()

    # ----------------------------------------------------------
    # Extract existing LEFT and RIGHT values from the file
    # ----------------------------------------------------------
    left_match = re.search(r"LEFT_PULSE_WIDTH_SETTINGS\s*=\s*(.*)", content)
    right_match = re.search(r"RIGHT_PULSE_WIDTH_SETTINGS\s*=\s*(.*)", content)

    left_existing = left_match.group(1).split(",") if left_match else ["500-2500"] * 6
    right_existing = right_match.group(1).split(",") if right_match else ["500-2500"] * 6

    # ----------------------------------------------------------
    # Split new values and enabled flags
    # ----------------------------------------------------------
    left_min  = pwm_min[:6]
    right_min = pwm_min[6:]

    left_max  = pwm_max[:6]
    right_max = pwm_max[6:]

    left_enabled  = enabled[:6]
    right_enabled = enabled[6:]

    # ----------------------------------------------------------
    # Merge LEFT (replace only enabled indices)
    # ----------------------------------------------------------
    left_final = []
    for i in range(6):
        if left_enabled[i]:
            left_final.append(f"{left_min[i]}-{left_max[i]}")
        else:
            left_final.append(left_existing[i])  # keep original

    # ----------------------------------------------------------
    # Merge RIGHT (replace only enabled indices)
    # ----------------------------------------------------------
    right_final = []
    for i in range(6):
        if right_enabled[i]:
            right_final.append(f"{right_min[i]}-{right_max[i]}")
        else:
            right_final.append(right_existing[i])  # keep original

    # Convert back to strings
    left_str = ",".join(left_final)
    right_str = ",".join(right_final)

    # ----------------------------------------------------------
    # Replace in file
    # ----------------------------------------------------------
    content = re.sub(
        r"LEFT_PULSE_WIDTH_SETTINGS\s*=.*",
        f"LEFT_PULSE_WIDTH_SETTINGS = {left_str}",
        content
    )

    content = re.sub(
        r"RIGHT_PULSE_WIDTH_SETTINGS\s*=.*",
        f"RIGHT_PULSE_WIDTH_SETTINGS = {right_str}",
        content
    )

    # Write updated content
    settings_path.write_text(content)

    print("Updated LEFT:", left_str)
    print("Updated RIGHT:", right_str)
    print(f"config/{ID}/settings.ini updated successfully.")
