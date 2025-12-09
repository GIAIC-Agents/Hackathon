---
title: "Lesson 5: URDF and XACRO for Humanoid Robot Modeling"
sidebar_label: "URDF and XACRO for Humanoid Robot Modeling"
---

# Lesson 5: URDF and XACRO for Humanoid Robot Modeling

The Unified Robot Description Format (URDF) is a critical component in humanoid robotics development, serving as the standard way to describe robot models in ROS. URDF is an XML format that defines the physical and visual properties of a robot, including its links, joints, inertial properties, and sensor mounting points. For humanoid robots, which have complex kinematic structures with multiple limbs and degrees of freedom, URDF becomes even more important as it provides the foundation for simulation, visualization, and control.

## Understanding URDF Structure

URDF defines a robot as a collection of rigid bodies (links) connected by joints. The basic structure includes:

- **Links**: Represent rigid bodies with properties like mass, inertia, visual geometry, and collision geometry
- **Joints**: Define the connection between links, specifying the type of motion (revolute, prismatic, fixed, etc.)
- **Materials**: Define visual appearance properties
- **Transmissions**: Define how actuators connect to joints

For humanoid robots, the URDF typically includes multiple kinematic chains for legs, arms, and potentially a spine/torso section. Each chain starts from a root link and branches out to end effectors (hands or feet).

## Key Components for Humanoid Robots

When modeling humanoid robots with URDF, consider including:

### Link Definitions
Each body part (head, torso, upper arm, lower arm, hand, upper leg, lower leg, foot) is defined as a link with:
- Mass properties for dynamics simulation
- Inertial tensor for realistic physics
- Visual geometry for rendering
- Collision geometry for physics simulation
- Origin transforms to position the link correctly

### Joint Definitions
Joints connect the links and define the robot's range of motion:
- **Revolute joints**: Single-axis rotation with position, velocity, and effort limits
- **Continuous joints**: Continuous rotation (like a wheel)
- **Prismatic joints**: Linear motion
- **Fixed joints**: Rigid connections between parts
- **Floating joints**: Six degrees of freedom (rarely used in humanoid robots)
- **Planar joints**: Motion on a plane

For humanoid robots, most joints are revolute with specific limits that reflect human-like ranges of motion.

### Transmission Elements
Define how actuators (motors) connect to joints, specifying the mechanical relationship between motor and joint positions.

## XACRO: Enhancing URDF with Macros

XACRO (XML Macros) is an XML macro language that extends URDF with additional features like:
- Macros for reusing common structures
- Mathematical expressions
- Property definitions
- Conditional inclusion

For humanoid robots with many similar joints (like fingers), XACRO macros can significantly reduce the complexity of the model definition.

## Best Practices for Humanoid Robot URDF

### Proper Inertial Properties
Accurate inertial properties are crucial for realistic simulation and control. These include mass, center of mass, and inertia tensor for each link. Inaccurate inertial values can lead to unstable control and unrealistic behavior in simulation.

### Appropriate Collision Models
Collision geometry should be simplified compared to visual geometry for efficient physics simulation. However, it must still accurately represent the physical extent of the robot to enable proper collision detection.

### Joint Limits and Safety
Define realistic joint limits that reflect the physical constraints of the hardware. This prevents impossible motions during simulation and provides a safety boundary for control algorithms.

### Mass Distribution
Consider the center of gravity and mass distribution of the robot, especially important for humanoid robots that need to maintain balance during locomotion.

### Sensor Placement
Define attachment points for sensors in the URDF, including cameras, IMUs, force/torque sensors, and other perception devices. This allows simulation environments to properly position virtual sensors.

## Example Structure for a Humanoid Robot

A typical humanoid robot URDF might include:
- Root link (usually the pelvis or torso)
- Legs: hip joints → upper legs → knee joints → lower legs → ankle joints → feet
- Torso: connection from pelvis to chest
- Arms: shoulder joints → upper arms → elbow joints → lower arms → wrist joints → hands
- Head: neck joint connecting to the torso

Each joint would have appropriate range of motion limits, and each link would have realistic mass and inertia properties.

## Integration with ROS2 Ecosystem

The URDF model integrates with various ROS2 tools and packages:
- RViz for visualization
- Gazebo for physics simulation
- MoveIt! for motion planning
- Robot state publisher for TF tree generation
- Controllers for joint management

The robot state publisher package uses the URDF to generate the TF tree, which is essential for spatial relationships in ROS2.

Proper URDF and XACRO modeling is foundational for humanoid robot simulation and control. The complexity of humanoid robots requires careful attention to kinematic structure, inertial properties, and physical constraints when creating these models. Well-crafted URDF files enable effective simulation, visualization, and control of humanoid robots across various platforms and tools.