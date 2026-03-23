# AI Network Defender

## Overview
**AI Network Defender** is an AI-powered cybersecurity tool that analyzes firewall logs using **Retrieval-Augmented Generation (RAG)** and the MITRE ATT&CK framework.

It acts like a virtual SOC analyst by:
- Ingesting Palo Alto firewall logs  
- Retrieving similar historical events  
- Enriching analysis with threat intelligence  
- Generating AI-driven threat assessments  

---

## Features

- Analyze Palo Alto firewall logs  
- RAG-based contextual reasoning  
- MITRE ATT&CK mapping for threats  
- Threat classification (low / medium / high)  
- Human-readable explanations and response recommendations  

---

## Installation

### 1. Install dependencies
```bash
pip install openai pandas numpy faiss-cpu
```

### 2. Set your OpenAI API key
```bash
export OPENAI_API_KEY="your_api_key_here"
```

---

## Project Structure

```
AI-Network-Defender/
├── main.py
├── palo_alto_logs.csv
└── README.md
```

---

## How to Run

```bash
python main.py
```

---

## How It Works

### 1. Load Logs
`main.py` reads firewall logs from a CSV file:

```python
df = pd.read_csv("palo_alto_logs.csv")
```

Each row is converted into a natural language description:

```
Traffic from 192.168.1.5:51515 to 10.0.0.2:22 using ssh action=allow bytes=1200
```

---

### 2. Add Threat Intelligence
The app includes MITRE ATT&CK techniques such as:

- T1110 – Brute Force  
- T1021 – Remote Services  
- T1046 – Network Scanning  
- T1071 – Application Layer C2  
- T1041 – Data Exfiltration  

---

### 3. Create Embeddings
Both logs and MITRE data are converted into vectors using OpenAI embeddings.

---

### 4. Store in Vector Database
FAISS is used for fast similarity search:

```python
index = faiss.IndexFlatL2(dimension)
```

---

### 5. Retrieve Context (RAG)
When analyzing a new event:
- Finds similar past logs  
- Pulls relevant MITRE techniques  
- Combines them as context  

---

### 6. AI Analysis
The OpenAI model produces a structured response:

```
- Is it malicious?
- Threat level
- MITRE technique
- Explanation
- Recommended response
```

---

## Example Output

```
Event:
Traffic from 192.168.1.100:4444 to 10.0.0.5:3389

AI Analysis:
- Malicious: Yes
- Threat Level: High
- MITRE Technique: T1021 (Remote Services)
- Explanation: Possible lateral movement via RDP
- Recommended Action: Block IP and investigate endpoint
```

---

## Use Cases

- SOC analyst automation  
- Threat detection research  
- Cybersecurity portfolio project  
- AI + security experimentation  

---

## Limitations

- Uses static/simulated log data  
- No real-time ingestion  
- No true anomaly detection model  
- Requires OpenAI API access  

---

## Future Improvements

- Streamlit dashboard for visualization  
- Real-time log streaming  
- Automated response actions (block IPs)  
- ML anomaly detection  
- External threat intelligence feeds  

---

## Inspiration

This project is conceptually similar to systems from:
- Palo Alto Networks  
- CrowdStrike  
- Splunk  

---

## License
MIT License  

---

## Notes
**AI Network Defender** demonstrates how AI + RAG can augment cybersecurity workflows, turning raw firewall logs into actionable intelligence. This makes it a strong portfolio project and a learning tool for AI in cybersecurity.

