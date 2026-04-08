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

    print(f"config_{ID}.ini updated successfully.")
