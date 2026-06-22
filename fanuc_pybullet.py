import pybullet as p
import pybullet_data
import time
import os

# Connect to PyBullet GUI
physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.81)

# Set camera
p.resetDebugVisualizerCamera(cameraDistance=3, cameraYaw=50, cameraPitch=-30, cameraTargetPosition=[1.0, 0, 1.0])

# Load plane
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.loadURDF("plane.urdf")

# Load FANUC robot
urdf_path = "assets/fanuc_r1000ia_support/urdf/r1000ia80f.urdf"
robot_id = p.loadURDF(urdf_path, useFixedBase=True)

num_joints = p.getNumJoints(robot_id)
movable_joints = [i for i in range(num_joints) if p.getJointInfo(robot_id, i)[2] in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]]

end_effector_index = num_joints - 1

target_positions = [
    [1.5, 0, 1.0],
    [1.5, 0.5, 1.0],
    [1.2, 0.5, 1.2],
    [1.2, 0, 1.2],
    [1.5, 0, 1.0]
]

# Function to move smoothly
def move_to_xyz(target_pos, steps=120):
    target_angles = p.calculateInverseKinematics(robot_id, end_effector_index, target_pos)
    current_angles = [p.getJointState(robot_id, j)[0] for j in movable_joints]

    for t in range(steps):
        blend = t / steps
        interpolated = [(1 - blend) * c + blend * tg for c, tg in zip(current_angles, target_angles)]
        for i, j in enumerate(movable_joints):
            p.setJointMotorControl2(
                bodyIndex=robot_id,
                jointIndex=j,
                controlMode=p.POSITION_CONTROL,
                targetPosition=interpolated[i],
                force=500,
                maxVelocity=1.5
            )
        p.stepSimulation()
        time.sleep(1./240.)

for pos in target_positions:
    move_to_xyz(pos, steps=240)

try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    p.disconnect()