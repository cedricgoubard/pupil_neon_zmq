import argparse

import cv2
import matplotlib.pyplot as plt
import yaml
from pupil_labs.realtime_api.simple import Device, discover_one_device


if __name__ == "__main__":
    # Parse 
    parser = argparse.ArgumentParser(description="ZMQ interface for Pupil Neon glasses")
    parser.add_argument("--cfg", type=str, required=False, help="Path to the configuration file")
    args = parser.parse_args()

    if not args.cfg:
        print("No configuration file provided")
        print("Looking for the next best device...\n\t", end="")
        print(discover_one_device(max_search_duration_seconds=10.0))
        exit(1)


    # Load yaml file
    with open(args.cfg, "r") as f:
        cfg = yaml.safe_load(f)

    dev = Device(cfg["ip"], cfg["port"])

    print(f"Phone IP address: {dev.phone_ip}")
    print(f"Phone name: {dev.phone_name}")
    print(f"Battery level: {dev.battery_level_percent}%")
    print(f"Free storage: {dev.memory_num_free_bytes / 1024**3:.1f} GB")

    scene_sample, gaze_sample = dev.receive_matched_scene_video_frame_and_gaze()

    print("This sample contains the following data:\n")
    print(f"Gaze x and y coordinates: {gaze_sample.x}, {gaze_sample.y}\n")
    print(f"Pupil diameter in millimeters for the left eye: {gaze_sample.pupil_diameter_left} and the right eye: {gaze_sample.pupil_diameter_right}\n")
    print("Location of left and right eye ball centers in millimeters in relation to the scene camera of the Neon module.")
    print(f"For the left eye x, y, z: {gaze_sample.eyeball_center_left_x}, {gaze_sample.eyeball_center_left_y}, {gaze_sample.eyeball_center_left_z} and for the right eye x, y, z: {gaze_sample.eyeball_center_right_x}, {gaze_sample.eyeball_center_right_y}, {gaze_sample.eyeball_center_right_z}.\n")
    print("Directional vector describing the optical axis of the left and right eye.")
    print(f"For the left eye x, y, z: {gaze_sample.optical_axis_left_x}, {gaze_sample.optical_axis_left_y}, {gaze_sample.optical_axis_left_z} and for the right eye x, y, z: {gaze_sample.optical_axis_right_x}, {gaze_sample.optical_axis_right_y}, {gaze_sample.optical_axis_right_z}.")

    scene_with_gaze = scene_sample.bgr_pixels.copy()
    scene_with_gaze = cv2.circle(scene_with_gaze, (int(gaze_sample.x), int(gaze_sample.y)), 10, (0, 0, 255), -1)
    cv2.imwrite("resources/scene.png", scene_with_gaze)

    dev.close()
    


