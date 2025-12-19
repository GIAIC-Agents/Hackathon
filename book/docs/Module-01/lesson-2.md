---
title: "Lesson 2: Fundamentals of ROS2"
sidebar_label: "Fundamentals of ROS2"
---

# Lesson 2: Fundamentals of ROS2

Robot Operating System 2 (ROS2) is the next-generation framework for developing robot applications. Unlike its predecessor ROS1, ROS2 was built from the ground up to address critical limitations in safety, security, and real-time performance. It is designed to be suitable for production environments and industrial applications, making it an essential tool for humanoid robotics development.

ROS2 provides a comprehensive middleware layer that enables communication between different components of a robotic system. At its core, ROS2 implements a publish-subscribe communication model, where nodes can publish data to topics and subscribe to data from other topics. This decentralized architecture allows for modular development and easy integration of new components. Additionally, ROS2 supports services for request-response communication and action servers for long-running tasks with feedback.

Key concepts in ROS2 include:

- **Nodes**: Individual processes that perform computation. Nodes are the basic building blocks of a ROS2 program.
- **Topics**: Named buses over which nodes exchange messages. Topics implement a publish-subscribe communication pattern.
- **Messages**: Data structures used when publishing and subscribing to topics. Messages are defined in special files ending with the .msg extension.
- **Services**: Provides a request-response pattern for communication. Services are defined in files ending with the .srv extension.
- **Packages**: Organizational units that contain libraries, nodes, and other resources. Packages are fundamental to ROS2's modularity.
- **Parameter Server**: Allows nodes to store and retrieve configuration parameters.
- **Actions**: For long-running tasks that require feedback and goal management.

ROS2 uses Data Distribution Service (DDS) as its underlying middleware for communication. DDS provides quality of service (QoS) policies that allow fine-tuning of communication characteristics, including reliability, durability, and deadline handling. This makes ROS2 suitable for real-time and safety-critical applications.

The ROS2 ecosystem includes several essential tools:

- **ros2 run**: Execute a node from a package.
- **ros2 launch**: Launch multiple nodes using a launch file.
- **ros2 topic**: Command-line tools for inspecting and publishing to topics.
- **ros2 service**: Command-line tools for calling and managing services.
- **rqt**: Graphical tool for visualizing and debugging ROS2 systems.
- **RViz2**: 3D visualization tool for displaying sensor data, robot models, and other information.

ROS2 also features improved security compared to ROS1, with authentication, access control, and message encryption capabilities. Additionally, it supports multiple programming languages including C++, Python, and Rust, enabling broader adoption and integration with existing software ecosystems.

In the context of humanoid robotics, ROS2 serves as the backbone for coordinating complex multi-sensor systems, managing communication between perception and control modules, and providing standardized interfaces for hardware abstraction. The modular architecture of ROS2 enables teams to develop components independently and integrate them seamlessly, which is crucial for complex humanoid robots that require coordination of numerous subsystems.