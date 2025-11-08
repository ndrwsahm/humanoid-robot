import re

def write_cal_data(offset_data):
    # Path to settings file
    settings_path = "firmware/settings.py"

    # Read the file
    with open(settings_path, "r") as f:
        content = f.read()

    # Replace values using regex
    content = re.sub(r"LHR_DEFAULT_ANGLE\s*=\s*.*", f"LHR_DEFAULT_ANGLE = {offset_data[0]}", content)
    content = re.sub(r"LHA_DEFAULT_ANGLE\s*=\s*.*", f"LHA_DEFAULT_ANGLE = {offset_data[1]}", content)
    content = re.sub(r"LHE_DEFAULT_ANGLE\s*=\s*.*", f"LHE_DEFAULT_ANGLE = {offset_data[2]}", content)
    content = re.sub(r"LK_DEFAULT_ANGLE\s*=\s*.*",  f"LK_DEFAULT_ANGLE = {offset_data[3]}", content)
    content = re.sub(r"LAA_DEFAULT_ANGLE\s*=\s*.*", f"LAA_DEFAULT_ANGLE = {offset_data[4]}", content)
    content = re.sub(r"LAE_DEFAULT_ANGLE\s*=\s*.*", f"LAE_DEFAULT_ANGLE = {offset_data[5]}", content)

    content = re.sub(r"RHR_DEFAULT_ANGLE\s*=\s*.*", f"RHR_DEFAULT_ANGLE = {offset_data[6]}", content)
    content = re.sub(r"RHA_DEFAULT_ANGLE\s*=\s*.*", f"RHA_DEFAULT_ANGLE = {offset_data[7]}", content)
    content = re.sub(r"RHE_DEFAULT_ANGLE\s*=\s*.*", f"RHE_DEFAULT_ANGLE = {offset_data[8]}", content)
    content = re.sub(r"RK_DEFAULT_ANGLE\s*=\s*.*",  f"RK_DEFAULT_ANGLE = {offset_data[9]}", content)
    content = re.sub(r"RAA_DEFAULT_ANGLE\s*=\s*.*", f"RAA_DEFAULT_ANGLE = {offset_data[10]}", content)
    content = re.sub(r"RAE_DEFAULT_ANGLE\s*=\s*.*", f"RAE_DEFAULT_ANGLE = {offset_data[11]}", content)

    # Write back
    with open(settings_path, "w") as f:
        f.write(content)

    print("settings.py updated successfully.")
