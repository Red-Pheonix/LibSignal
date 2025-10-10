import json
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Convert and filter traffic network JSON files.")
    parser.add_argument("--og-file", required=True, help="Path to the original network JSON file.")
    parser.add_argument("--cvt-file", required=True, help="Path to the converted network JSON file.")
    parser.add_argument("--flow-file", required=True, help="Path to the flow JSON file.")
    parser.add_argument("--out-network", default="converted_network.json", help="Output path for the converted network JSON.")
    parser.add_argument("--out-flow", default="converted_flow.json", help="Output path for the converted flow JSON.")
    args = parser.parse_args()

    # Load original network
    with open(args.og_file, "r") as f:
        full_data = json.load(f)

    # Load converted network
    with open(args.cvt_file, "r") as f:
        converted_data = json.load(f)

    full_intersections = {inter["id"]: inter for inter in full_data["intersections"]}
    converted_intersections = {inter["id"]: inter for inter in converted_data["intersections"]}

    new_intersections = []
    all_roads = []

    for inter_id in converted_intersections.keys():
        full_inter = full_intersections[inter_id]
        converted_inter = converted_intersections[inter_id]

        new_inter = {
            "id": full_inter["id"],
            "point": converted_inter["point"],
            "width": full_inter["width"],
            "roads": converted_inter["roads"],
            "virtual": full_intersections[inter_id]['virtual'],
        }

        all_roads.extend(converted_inter["roads"])

        road_links_index = [
            (
                link["startRoad"] in converted_inter["roads"]
                and link["endRoad"] in converted_inter["roads"]
            )
            for link in full_inter["roadLinks"]
        ]

        index_map = {}
        counter = 0
        for idx, link_valid in enumerate(road_links_index):
            if link_valid:
                index_map[idx] = counter
                counter += 1
            else:
                index_map[idx] = None

        new_inter["roadLinks"] = [
            link
            for link in full_inter["roadLinks"]
            if link["startRoad"] in converted_inter["roads"]
            and link["endRoad"] in converted_inter["roads"]
        ]

        traffic_light = full_inter["trafficLight"]
        road_link_indices = [
            index_map[i]
            for i in traffic_light["roadLinkIndices"]
            if index_map[i] is not None
        ]

        lightphases = []
        for phase in traffic_light["lightphases"]:
            new_phase = {
                "time": phase["time"],
                "availableRoadLinks": [
                    index_map[i]
                    for i in phase["availableRoadLinks"]
                    if index_map[i] is not None
                ],
            }
            lightphases.append(new_phase)

        new_inter["trafficLight"] = {
            "roadLinkIndices": road_link_indices,
            "lightphases": lightphases,
        }

        new_intersections.append(new_inter)

    converted_data["intersections"] = new_intersections

    # Save converted network
    with open(args.out_network, "w") as f:
        json.dump(converted_data, f, indent=4)

    # Filter and save flow file
    with open(args.flow_file, "r") as f:
        flow_data = json.load(f)

    all_roads = set(all_roads)
    new_flows = [flow for flow in flow_data if all(r in all_roads for r in flow["route"])]

    with open(args.out_flow, "w") as f:
        json.dump(new_flows, f, indent=4)

    print(f"DONE ✅\nSaved network → {os.path.abspath(args.out_network)}\nSaved flow → {os.path.abspath(args.out_flow)}")

if __name__ == "__main__":
    main()
