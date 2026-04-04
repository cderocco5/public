# Log Shipper to Splunk (HEC)

A lightweight Python script that continuously monitors local log files and forwards new log entries to Splunk via the HTTP Event Collector (HEC).

It tracks file offsets to ensure logs are not re-sent and safely persists state on shutdown.

---

## Features

- Monitors multiple log files
- Sends only new log lines using file offsets
- Persists offsets to avoid duplicate ingestion
- Handles log rotation (resets offset if file shrinks)
- Graceful shutdown with offset saving
- Sends logs to Splunk via HEC (raw endpoint)
- Includes hostname (FQDN) in events

---

## Monitored Log Files

The script currently watches:
