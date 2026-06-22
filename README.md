# Fanuc R-1000iA Robot PyBullet Simulation

This is a 3D robotics simulation project for the 6-DOF Fanuc R-1000iA industrial robot arm running inside the PyBullet physics engine. I built this to simulate smooth point-to-point path tracking and test basic motion control configurations.

## What it Does
* **Fixes Broken File Paths:** Legacy URDF files use a `package://` string scheme that crashes on macOS. I wrote a path-fixing script (`fix_urdf_paths.py`) that automatically sweeps the URDF and swaps out the strings with local relative paths so the 3D meshes load perfectly on Mac.
* **Trajectory Tracking:** The main script uses PyBullet's numerical Inverse Kinematics (IK) to calculate joint positions and interpolates between set coordinates smoothly so the robot arm moves cleanly without snapping.

## Project Structure
* `fanuc_pybullet.py` - The primary simulation script that handles the setup, environment rendering, and motion control loop.
* `fix_urdf_paths.py` - A utility helper script that opens the URDF configuration and updates the internal mesh folder paths.
* `assets/` - Folder containing the robot's physical links and visual meshes.

## How to Run the Code
1. Make sure you have PyBullet installed in your Python environment:
   ```bash
   pip install pybullet
2. Run the path-fixer script:
    ```bash
    python fix_urdf_paths.py
3. Launch the simulation:
    ```bash
    python fanuc_pybullet.py
## Acknowledgments & Credits
* The URDF configuration and 3D mesh files for the Fanuc R-1000iA robot utilized in this simulation environment were sourced from this public dataset: https://github.com/Daniella1/urdf_files_dataset/tree/main/urdf_files/ros-industrial/xacro_generated/fanuc/fanuc_r1000ia_support