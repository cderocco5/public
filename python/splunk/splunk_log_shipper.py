#!/usr/bin/env python3

# this script reads log files and uploads them to splunk over hec
# has file offsets to know which lines of the file have been sent to splunk already
# has shutdown handler to save offset before being shutdown on server reboots or ending the script process

import os
import json
import time
import requests
import signal
import sys
from urllib.parse import urlencode
import socket


SPLUNK_HEC_URL = "https://http-inputs-DOMAIN.splunkcloud.com:443/services/collector/raw"
SPLUNK_HEC_TOKEN = XXXXX
INDEX="app_logging_summary"
BUFFER=10
offsets = {}
FQDN = socket.getfqdn()

LOG_FILES = [
    "/opt/ihub/log/error_userlog.txt",
    "/opt/ihub/log/userlog.txt",
    "/opt/ihub/log/stderr.txt",
    "/opt/ihub/log/portal_stderr.txt",
    "/opt/ihub/log/portal_trace.txt",
    "/opt/ihub/log/portal_userlog.txt",
    "/opt/ihub/log/trace.txt",
    "/opt/ihub/log/ui_stderr.txt",
    "/opt/ihub/log/ui_trace.txt",
    "/opt/ihub/log/ui_userlog.txt",
    "/opt/ihub/log/hub_stderr.txt",
    "/opt/ihub/log/hub_trace.txt",
    "/opt/ihub/log/hub_userlog.txt"
]

OFFSET_FILE = "offsets.json"
POLL_INTERVAL = 2  # seconds
HEADERS = {
    "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
    "Content-Type": "text/plain", # "application/json",
}

 
# ---------------------------------------

def shutdown_handler(signum, frame):
    print("Shutting down, saving offsets...")
    save_offsets(offsets)
    sys.exit(0)


def load_offsets():
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, "r") as f:
            return json.load(f)
    return {}

 
def save_offsets(offsets):
    with open(OFFSET_FILE, "w") as f:
        json.dump(offsets, f)


def send_to_splunk(events, source, sourcetype="ihub:text", index="app_logging_summary"):
    print(f"Sending {len(events)} events to Splunk")
    if not events:
        return True

    payload = "\n".join(events)
    payload = payload.encode("utf-8")

    params = {}
    if sourcetype:
        params["sourcetype"] = sourcetype

    if source:
        params["source"] = source

    if index:
        params["index"] = index  
    if FQDN:
        params["host"] = FQDN  

    resp = requests.post(SPLUNK_HEC_URL, params=params, headers=HEADERS, data=payload, timeout=10)

    if resp.status_code != 200:
        print(f"Splunk HEC error: {resp.status_code} {resp.text}")
        return False

    return True

 
def read_new_lines(filepath, offset):
    
    with open(filepath, "r") as f:
        size = os.path.getsize(filepath)
        if offset > size:
            print(f"offset={offset}, size={size}")
            print("offset > size , {filepath} must have truncated due to rotation, resetting file offset to 0")
            offset = 0

        f.seek(offset)
        lines = f.readlines()
        if not lines:
            print("no new lines")
        new_offset = f.tell()
        print(f"old_offset {offset} new_offset {new_offset}")

    return lines, new_offset


def main():

    global offsets
    offsets = load_offsets()

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    print("Starting log shipper...")

    while True:

        for filepath in LOG_FILES:
            print(filepath)
            if not os.path.exists(filepath):
                continue

            print(f"Processing file: {filepath}")
            last_offset = offsets.get(filepath, 0)
            print("starting read_new_lines from offset:", last_offset)
            lines, new_offset = read_new_lines(filepath, last_offset)
            print(f"Read {len(lines)} new lines from {filepath}")

            if not lines:
                continue

            events = []
            for line in lines:
                line = line.strip()
                events.append(line)
                if not line:
                    continue

            if send_to_splunk(events, source=filepath):
                offsets[filepath] = new_offset
                save_offsets(offsets)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()