"""
Plot movement profiles (supports frames with 12 or 18 values).
Run:
    python plot_movement_profiles.py --movement walk_forward --speed 60 --step_length 1.5 --num_steps 2
"""

import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Ensure project root (parent folder) is on sys.path so `from globals import *` works
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    import movement_profiles
    import kinematics
    from globals import *
except Exception as e:
    print("Import error. Make sure this script is in the project root or PROJECT_ROOT is correct.")
    print("Import error:", e)
    raise

# Descriptive joint names for up to 18 values (legs + arms)
JOINT_NAMES_18 = [
    # left leg (6)
    "L Hip Rotator", "L Hip Abductor", "L Hip Extendor",
    "L Knee Extendor", "L Ankle Abductor", "L Ankle Extendor",
    # left arm (3)
    "L Shoulder Yaw", "L Shoulder Pitch", "L Elbow",
    # right leg (6)
    "R Hip Rotator", "R Hip Abductor", "R Hip Extendor",
    "R Knee Extendor", "R Ankle Abductor", "R Ankle Extendor",
    # right arm (3)
    "R Shoulder Yaw", "R Shoulder Pitch", "R Elbow"
]

JOINT_NAMES_12 = JOINT_NAMES_18[:6] + JOINT_NAMES_18[9:15]  # left leg (6) + right leg (6)

def ensure_array(movement):
    if movement is None:
        return None
    arr = np.array(movement, dtype=float)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    if arr.shape[1] not in (12, 18):
        raise ValueError(f"Expected 12 or 18 angles per frame, got shape {arr.shape}")
    return arr

def plot_joint_angles(arr, movement_name, out_dir="."):
    n_joints = arr.shape[1]
    cols = 3
    rows = int(np.ceil(n_joints / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(14, 4 * rows), sharex=True)
    axes = axes.flatten()
    time = np.arange(arr.shape[0])

    names = JOINT_NAMES_12 if n_joints == 12 else JOINT_NAMES_18

    for i in range(n_joints):
        ax = axes[i]
        ax.plot(time, arr[:, i], linewidth=1.5)
        ax.set_title(f"{i}: {names[i]}")
        ax.grid(True)
        ax.set_ylabel("Angle (deg)")
        if i >= (n_joints - cols):
            ax.set_xlabel("Frame")

    # hide unused axes
    for j in range(n_joints, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle(f"Joint Angles over Time — {movement_name} ({n_joints} joints)", fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    out_path = os.path.join(out_dir, f"{movement_name}_angles_{n_joints}j.png")
    fig.savefig(out_path)
    print(f"Saved joint angles plot to {out_path}")
    return fig, out_path

def compute_foot_positions_from_frames(arr):
    """
    Given arr (frames, N), compute left and right foot positions (x,y,z) per frame
    using kinematics.compute_forward_leg_kinematics.
    Returns:
        left_positions: numpy array shape (frames, 3) columns [x, y, z]
        right_positions: numpy array shape (frames, 3) columns [x, y, z]
    """
    left_positions = []
    right_positions = []
    n_joints = arr.shape[1]

    for frame in arr:
        if n_joints == 12:
            left_angles = frame[0:6]
            right_angles = frame[6:12]
        else:  # 18
            left_angles = frame[0:6]
            right_angles = frame[9:15]

        try:
            lx, ly, lz = kinematics.compute_forward_leg_kinematics(left_angles, "left")
            rx, ry, rz = kinematics.compute_forward_leg_kinematics(right_angles, "right")
        except Exception as e:
            print("Forward kinematics error for frame:", e)
            lx = ly = lz = rx = ry = rz = np.nan

        left_positions.append((lx, ly, lz))
        right_positions.append((rx, ry, rz))

    #print(f"Computed foot positions for {np.array(left_positions)}")
    return np.array(left_positions), np.array(right_positions)


def plot_foot_trajectories(left_pos, right_pos, movement_name, out_dir="."):
    """
    Plots:
      1) X vs Z (vertical trajectory)
      2) X vs Y (plan/overhead view)
      3) Time series of X, Y, Z for left and right foot (two columns of 3 subplots)
    """
    # 1) X vs Z
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(left_pos[:, 0], left_pos[:, 2], '-o', markersize=3, label="Left Foot")
    ax1.plot(right_pos[:, 0], right_pos[:, 2], '-o', markersize=3, label="Right Foot")
    ax1.set_xlabel("X (units)")
    ax1.set_ylabel("Z (units)")
    ax1.set_title(f"Foot Trajectories (X vs Z) — {movement_name}")
    ax1.grid(True)
    ax1.legend()
    out1 = os.path.join(out_dir, f"{movement_name}_foot_XZ.png")
    fig1.savefig(out1)
    print(f"Saved X-Z trajectory to {out1}")

    # 2) X vs Y (plan / overhead)
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.plot(left_pos[:, 0], left_pos[:, 1], '-o', markersize=3, label="Left Foot")
    ax2.plot(right_pos[:, 0], right_pos[:, 1], '-o', markersize=3, label="Right Foot")
    ax2.set_xlabel("X (units)")
    ax2.set_ylabel("Y (units)")
    ax2.set_title(f"Foot Trajectories (X vs Y) — {movement_name}")
    ax2.grid(True)
    ax2.legend()
    out2 = os.path.join(out_dir, f"{movement_name}_foot_XY.png")
    fig2.savefig(out2)
    print(f"Saved X-Y trajectory to {out2}")

    # 3) Time series for X, Y, Z for each foot
    frames = np.arange(left_pos.shape[0])
    fig3, axes = plt.subplots(3, 2, figsize=(12, 9), sharex=True)
    # Left foot columns
    axes[0, 0].plot(frames, left_pos[:, 0], label="Left X")
    axes[0, 0].set_ylabel("X (units)")
    axes[1, 0].plot(frames, left_pos[:, 1], label="Left Y")
    axes[1, 0].set_ylabel("Y (units)")
    axes[2, 0].plot(frames, left_pos[:, 2], label="Left Z")
    axes[2, 0].set_ylabel("Z (units)")
    axes[2, 0].set_xlabel("Frame")
    # Right foot columns
    axes[0, 1].plot(frames, right_pos[:, 0], label="Right X", color="C1")
    axes[0, 1].set_ylabel("X (units)")
    axes[1, 1].plot(frames, right_pos[:, 1], label="Right Y", color="C1")
    axes[1, 1].set_ylabel("Y (units)")
    axes[2, 1].plot(frames, right_pos[:, 2], label="Right Z", color="C1")
    axes[2, 1].set_ylabel("Z (units)")
    axes[2, 1].set_xlabel("Frame")

    # Titles and grid
    axes[0, 0].set_title("Left Foot (X,Y,Z over time)")
    axes[0, 1].set_title("Right Foot (X,Y,Z over time)")
    for ax_row in axes:
        for ax in ax_row:
            ax.grid(True)

    fig3.suptitle(f"Foot Position Components over Time — {movement_name}", fontsize=14)
    fig3.tight_layout(rect=[0, 0.03, 1, 0.95])
    out3 = os.path.join(out_dir, f"{movement_name}_foot_time_series.png")
    fig3.savefig(out3)
    print(f"Saved foot time series to {out3}")

    # Optionally show all three figures
    return (fig1, out1), (fig2, out2), (fig3, out3)


def build_movement_array(movement_name, height=WALKING_HEIGHT, step_length=1.0, num_steps=1, speed=50):
    movement_name = movement_name.lower()
    try:
        if movement_name == "stand":
            arr = movement_profiles.build_stand_still_array(height)
        elif movement_name == "walk_forward":
            arr = movement_profiles.build_walk_array(direction=1, height=height, step_length=step_length, num_steps=num_steps, speed=speed)
        elif movement_name == "walk_backward":
            arr = movement_profiles.build_walk_array(direction=-1, height=height, step_length=step_length, num_steps=num_steps, speed=speed)
        elif movement_name == "turn_right":
            arr = movement_profiles.build_turn_right_array(direction=1, height=height, step_length=step_length, num_steps=num_steps, speed=speed)
        elif movement_name == "turn_left":
            arr = movement_profiles.build_turn_left_array(direction=1, height=height, step_length=step_length, num_steps=num_steps, speed=speed)
        else:
            raise ValueError(f"Unknown movement: {movement_name}")
    except Exception as e:
        print(f"Error building movement '{movement_name}': {e}")
        return None
    return arr

def plot_movement(movement_name, height=WALKING_HEIGHT, step_length=1.0, num_steps=1, speed=50, out_dir="."):
    print(f"Building movement '{movement_name}' with height={height}, step_length={step_length}, num_steps={num_steps}, speed={speed}")
    movement = build_movement_array(movement_name, height=height, step_length=step_length, num_steps=num_steps, speed=speed)
    if movement is None:
        print("No movement data generated.")
        return
    arr = ensure_array(movement)
    print(f"Frames: {arr.shape[0]}, Joints per frame: {arr.shape[1]}")
    plot_joint_angles(arr, movement_name, out_dir=out_dir)
    left_pos, right_pos = compute_foot_positions_from_frames(arr)
    plot_foot_trajectories(left_pos, right_pos, movement_name, out_dir=out_dir)
    plt.show()

def parse_args():
    parser = argparse.ArgumentParser(description="Plot movement profiles from movement_profiles.py")
    parser.add_argument("--movement", type=str, default="stand", help="Movement name")
    parser.add_argument("--speed", type=float, default=50.0, help="Speed (0-100)")
    parser.add_argument("--step_length", type=float, default=1.0, help="Step length")
    parser.add_argument("--num_steps", type=int, default=1, help="Number of steps")
    parser.add_argument("--height", type=float, default=None, help="Walking height (defaults to WALKING_HEIGHT)")
    parser.add_argument("--out_dir", type=str, default=".", help="Directory to save plots")
    return parser.parse_args()

def main():
    args = parse_args()
    height = args.height if args.height is not None else WALKING_HEIGHT

    # Create the requested output directory and a subfolder named "movement graphs"
    base_out = args.out_dir or "."
    graphs_dir = os.path.join(base_out, "movement_graphs")
    os.makedirs(graphs_dir, exist_ok=True)

    plot_movement(
        args.movement,
        height=height,
        step_length=args.step_length,
        num_steps=args.num_steps,
        speed=args.speed,
        out_dir=graphs_dir
    )

if __name__ == "__main__":
    main()
