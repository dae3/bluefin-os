#!/usr/bin/env python3

import time
import sys
from pydbus import SystemBus

try:
    bus = SystemBus()

    manager = bus.get("org.freedesktop.GeoClue2", "/org/freedesktop/GeoClue2/Manager")

    client_path = manager.CreateClient()
    client = bus.get("org.freedesktop.GeoClue2", client_path)
    client.DesktopId = "my-script.desktop"
    client.RequestedAccuracyLevel = 1
    client.Start()

    # Wait for location
    for _ in range(15):
        if client.Location:
            break
        time.sleep(0.5)
    else:
        print("error: location unavailable", flush=True, file=sys.stderr)
        exit(1)

    # Wait for GeoClue to populate the Location object fully
    for _ in range(15):
        if bus.get("org.freedesktop.GeoClue2", client.Location).Latitude:
            break
        time.sleep(0.5)
    else:
        print("error: location not initialized properly", flush=True)
        exit(1)

    print(bus.get("org.freedesktop.GeoClue2", client.Location).Latitude)

except Exception as e:
    print(f"error: {e}", flush=True, file=sys.stderr)
    exit(1)
