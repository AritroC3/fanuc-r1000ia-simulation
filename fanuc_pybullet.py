import pybullet as p
import pybullet_data
import time

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
end_effector_index = num_joints - 1 

movable_joints = []
for j in range(num_joints):
    if p.getJointInfo(robot_id, j)[2] != p.JOINT_FIXED:
        movable_joints.append(j)

for _ in range(100):
    p.stepSimulation()

# Function to move smoothly
def move_to_xyz(target_pos, steps=240):
    current_ee_state = p.getLinkState(robot_id, end_effector_index)
    start_pos = current_ee_state[0]  
    target_orn = current_ee_state[1]

    for t in range(steps):
        b = t / steps
        
        smooth_blend = 10 * (b**3) - 15 * (b**4) + 6 * (b**5)
        
        interp_x = (1 - smooth_blend) * start_pos[0] + smooth_blend * target_pos[0]
        interp_y = (1 - smooth_blend) * start_pos[1] + smooth_blend * target_pos[1]
        interp_z = (1 - smooth_blend) * start_pos[2] + smooth_blend * target_pos[2]
        current_target = [interp_x, interp_y, interp_z]
        
        target_angles = p.calculateInverseKinematics(
            robot_id, 
            end_effector_index, 
            current_target, 
            targetOrientation=target_orn,
            maxNumIterations=100,
            residualThreshold=1e-5
        )
        
        for i, joint_idx in enumerate(movable_joints):
            p.setJointMotorControl2(
                bodyIndex=robot_id,
                jointIndex=joint_idx,
                controlMode=p.POSITION_CONTROL,
                targetPosition=target_angles[i],
                force=500,
                maxVelocity=1.5
            )
            
        p.stepSimulation()
        time.sleep(1./240.)

target_positions = [
    [1.5, 0.0, 1.0],
    [1.5, 0.5, 1.0],
    [1.2, 0.5, 1.2],
    [1.2, 0.0, 1.2],
    [1.5, 0.0, 1.0]
]

# Execute trajectory
for pos in target_positions:
    print(f"Executing smooth trajectory to: {pos}")
    move_to_xyz(pos, steps=240)

# Keep simulation alive
try:
    print("Sequence complete. Holding position.")
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    p.disconnect()