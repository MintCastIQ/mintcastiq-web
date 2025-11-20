# MintCastIQ Development Guide
## Overview
- MintCastIQ is a contributor‑safe pipeline for trading card capture, grading, and benchmarking.  
- This guide documents the development environment, contributor workflow, and host GPU worker setup.
---
## Contributor Workflow
- **Primary focus**: CPU‑safe development in VMs or local environments.
- **Endpoints**: Contributors interact with the GPU worker via HTTP API.
  - `/benchmark` → runs a matrix multiplication benchmark
  - `/process` → accepts JSON payloads for card processing
- **Fallback logic**: If GPU acceleration is unavailable, code runs in CPU mode with identical results.
Contributors **do not need ROCm or GPU drivers**.  
They only need:
- Python 3.10+
- Flask
- Torch (CPU build is sufficient)
---
## Host GPU Worker (Audit Record)
The homelab host runs the accelerated worker service.  
Documented environment for reproducibility:
- **Hardware**: AMD GPU (RX series)
- **Driver stack**: ROCm 7.1
- **Python environment**: venv at `/opt/gpu_worker/gpuvenv`
- **Key packages**:
  - `torch` (ROCm build)
  - `flask`
- **Systemd service**: `gpu-worker.service`  
  - Runs `/opt/gpu_worker/worker.py` via venv interpreter
  - Exposes API on `http://<host-ip>:9091`
---
## Connectivity
  ```bash
  curl http://<host-ip>:9091/benchmark
  ```
Firewall must allow inbound traffic on chosen port.
## Development Standards
Audit clarity: Every architectural decision logged in this guide.
Environment reproducibility: Record GPU model, ROCm version, and PyTorch build.
Contributor safety: No hardware requirements; CPU fallback always available.
API contract: Endpoints documented and stable.
## Example Test
### PRISM endpoint
CPU processing will be used due to the effort level involved in aligning Ubuntu with an AMD GPU.

To see the health of the endpoint or process images
```bash
curl http://mintcastiq-gpu.tail0cc642.ts.net/benchmark
curl http://mintcastiq-gpu.tail0cc642.ts.net/process (not implemented)
```
### Expected response
{"status":"ok","result_shape":[10000,10000]}
## Notes
- Contributors should not attempt ROCm installation unless they are running their own GPU worker.
- Host environment details are included here for audit reproducibility only.
- Future versions may add reverse proxy routing for multiple workers.
