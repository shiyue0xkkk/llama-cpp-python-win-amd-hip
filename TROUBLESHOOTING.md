# Troubleshooting

These notes record issues observed while building and testing this Windows AMD HIP wheel. Fixes are environment-specific unless stated otherwise.

## 1. `WinError 193` loading `ggml-base.dll`

Windows often reports this for a DLL with an incompatible binary architecture/format, though other invalid or incompatible DLL conditions can also produce it.

```powershell
$PY = "C:\Path\To\python.exe"
& $PY -c "import platform,struct; print(platform.python_version()); print(platform.machine()); print(struct.calcsize('P')*8)"
& $PY -c "import llama_cpp; print(llama_cpp.__version__); print(llama_cpp.__file__)"
```

For this wheel, use Python 3.12 x64 and confirm the package path is the one you expect. Inspect DLL architecture and ensure Python is not importing a different installation.

**Observed resolution:** rebuilt for `cp312-cp312-win_amd64`, installed the wheel, and verified `ggml-base.dll`, `ggml.dll`, and `llama.dll` loaded from the intended package directory. This is not a universal fix for every `WinError 193`.

## 2. GPU not detected

```powershell
& "$env:ProgramFiles\AMD\ROCm\7.2\bin\hipconfig.exe" --full
& $PY -c "from llama_cpp import llama_cpp as c; print(c.llama_supports_gpu_offload())"
```

Check that HIP was enabled in the build, the target architecture matches the GPU (this artifact targets `gfx1100`), the driver/runtime is compatible, and the process uses the intended Python environment.

`llama_supports_gpu_offload() == True` indicates backend support; it does not prove a particular model is running on the GPU.

## 3. `LLVM ERROR: Can't get available size`

The first real Qwen3.5 model-load test failed with an LLVM error. The same isolated inference test succeeded after setting COMGR cache variables in the current PowerShell process:

```powershell
$env:AMD_COMGR_CACHE = "1"
$env:AMD_COMGR_CACHE_DIR = "C:\llama_build\comgr_cache"
New-Item -ItemType Directory -Force $env:AMD_COMGR_CACHE_DIR | Out-Null
```

Then rerun the same model test from that shell. The application must inherit these variables; a ComfyUI process already running elsewhere will not automatically receive them.

This was observed on one machine and is not an official AMD fix. If it persists, capture the full log and record driver, HIP SDK, compiler versions, model, context size, batch size, and GPU architecture. Avoid deleting system DLLs or replacing driver files.

## 4. Import error or missing chat handler

```powershell
& $PY -c "import llama_cpp; print(llama_cpp.__version__); print(llama_cpp.__file__)"
& $PY -c "from llama_cpp.llama_chat_format import Qwen35ChatHandler; from llama_cpp.llama_multimodal import GenericMTMDChatHandler; print('handlers OK')"
```

The tested 0.4.5 build included both handlers. If they are missing, Python may be importing another installation or installed files may not match the artifact.

## 5. Model loads but layers are not offloaded

Use verbose logs and a small test model first. If supported by the selected model/API path, test with `n_gpu_layers=-1`. Look for explicit layer-offload and GPU compute-buffer messages. Device detection alone does not establish successful offload.

## 6. ComfyUI or embedded Python uses another package

```powershell
$PY = "C:\AIvideo\ComfyUI_windows_portable\python_embeded\python.exe"
& $PY -c "import sys,llama_cpp; print(sys.executable); print(llama_cpp.__file__)"
```

Back up the active package before replacing it. Avoid manually deleting DLLs until the actual loaded paths are known.

## Bug report checklist

Include Windows edition/build, GPU model/architecture, AMD driver and HIP SDK versions, Python version/architecture, `llama_cpp.__file__`, wheel filename and SHA-256, full verbose logs, model/settings, failure stage, and whether the COMGR cache workaround changes the result.
