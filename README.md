# llama-cpp-python 0.4.5 — Windows AMD HIP Wheel

A community-built Windows x64 wheel for `llama-cpp-python` 0.4.5 with the HIP backend enabled. It has been validated for GPU detection and real model inference on an AMD Radeon RX 7900 XT (`gfx1100`).

> **Status: community build / limited validation.** This is not an official release from the `llama-cpp-python`, `llama.cpp`, or AMD teams. Review the compatibility and runtime dependency notes below. Before redistributing the wheel, complete the license review and third-party notice checks described in `LICENSES.md`.

## Current candidate artifact

| Item | Value |
|---|---|
| Distribution | `llama-cpp-python` |
| Version | `0.4.5` |
| Wheel | `llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl` |
| Python ABI | CPython 3.12 |
| Platform | Windows x86-64 |
| Backend / target | HIP / `gfx1100` |
| Build environment | Windows, ROCm/HIP SDK 7.2, Ninja, Visual Studio x64 build tools |
| Tested GPU | AMD Radeon RX 7900 XT |
| Wheel size | 20,111,549 bytes (about 20.11 MB) |
| SHA-256 | `DDDA9F92B6D4F631B6541EAF465E83B9DFEEC760D29A64FEFC0D13AEEB04ACE7` |

The SHA-256 identifies the candidate artifact recorded by this project. A matching hash verifies that the file matches this record; it does not prove that the file is safe or officially endorsed. Before publishing a release, verify that the uploaded file matches the hash above.

## Validation status

The following checks were completed on one Windows machine:

- Imported `llama_cpp` from the intended Python package directory.
- Loaded `ggml-base.dll`, `ggml.dll`, and `llama.dll` without the previous `WinError 193`.
- Imported `Llama`, `Qwen35ChatHandler`, and `GenericMTMDChatHandler`.
- `llama_supports_gpu_offload()` returned `True`.
- HIP detected an AMD Radeon RX 7900 XT (`gfx1100`).
- A Qwen3.5 4B GGUF inference test completed in an isolated installation after setting the COMGR cache variables described below.
- Completed wheel ZIP CRC, RECORD hash/size, installation, import, DLL deduplication, and runtime DLL loading-path checks on the test machine.

These results apply only to the tested environment. They do not guarantee compatibility with other GPUs, drivers, Windows versions, Python environments, or models.

## Download and verify

Download the `.whl` file from the **Releases** page of this GitHub repository.

Run the following in PowerShell:

```powershell
$WHEEL = ".\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl"
Get-FileHash $WHEEL -Algorithm SHA256
```

Compare the resulting SHA-256 with the value recorded above. If it does not match, do not install the file until the artifact and release version have been checked.

## Compatibility

- 64-bit Windows.
- CPython 3.12 x64 (`cp312` / `win_amd64`).
- An AMD driver and HIP runtime compatible with this build.
- Currently tested configuration: ROCm/HIP SDK 7.2 and GPU architecture `gfx1100`.
- Other AMD GPU targets have not yet been validated with this wheel.

Check AMD's version-specific [HIP SDK for Windows system requirements](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html).

**Do not advertise this wheel as compatible with every AMD GPU or every ROCm version.**

## Important: external runtime dependencies

This wheel does not bundle every runtime dependency. The target machine must provide a compatible runtime environment.

### AMD HIP Runtime

The following AMD runtime DLLs are not included in this wheel:

- `amdhip64_7.dll`
- `hipblas.dll`
- `rocblas.dll`

Install the matching runtime through official AMD distribution channels. Do not download DLLs from untrusted websites or copy DLLs from unrelated runtime versions into the Python package directory.

### OpenMP Runtime

Some native DLLs in this wheel depend on an OpenMP runtime.

The test machine was able to load `libomp140.x86_64.dll` from its system environment. This does not mean that another Windows machine will necessarily have a compatible version.

**Do not copy or redistribute an OpenMP DLL from a development-tool directory.** Use a runtime distribution method with appropriate redistribution rights, and validate it on the target machine.

Successful GPU detection does not establish that every external runtime dependency is present.

## Install in an isolated Python environment first

Create a virtual environment before installation. This helps avoid changing an existing ComfyUI or other Python environment.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

python -m pip install --no-deps .\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl
```

`--no-deps` installs the wheel itself without automatically installing its Python dependencies. If imports report missing Python packages, install the dependencies required by upstream `llama-cpp-python` 0.4.5.

Do not mix packages from unrelated Python installations.

Run the included checks:

```powershell
python .\tests\test_import.py
python .\tests\test_gpu.py
```

GPU detection and a `True` result from `llama_supports_gpu_offload()` indicate backend capability; they do not prove that all model layers are offloaded. Run a real model and inspect verbose logs for GPU offload and compute-buffer messages.

## COMGR cache issue and observed workaround

The first real model-load test encountered:

```text
LLVM ERROR: Can't get available size
```

The same inference test succeeded in the isolated environment after setting these variables in the current PowerShell session:

```powershell
$env:AMD_COMGR_CACHE = "1"
$env:AMD_COMGR_CACHE_DIR = "$env:LOCALAPPDATA\llama-cpp-python\comgr_cache"

New-Item -ItemType Directory -Force $env:AMD_COMGR_CACHE_DIR | Out-Null
```

Make sure the current user has write access to the cache directory.

This workaround was observed in one test environment. It is not an official AMD fix and is not guaranteed to work on every system.

The ComfyUI or other application process must inherit these environment variables. Changing them in another PowerShell window does not automatically affect an already-running process.

## Known limitations

- Primary validation was performed on one AMD Radeon RX 7900 XT (`gfx1100`). A broad compatibility matrix for other GPU architectures has not been completed.
- The complete upstream source commit and all build commands were not preserved in a form sufficient to establish bit-for-bit reproducibility. This wheel should not be described as a fully reproducible build.
- A real inference test was completed with the specified model, but this does not mean that every model, multimodal workflow, or ComfyUI node has been fully validated.
- Other feature-related DLLs, including `llama-common.dll` and `mtmd.dll`, were not comprehensively tested in the short-text inference path.
- The wheel does not include AMD HIP Runtime DLLs or an OpenMP Runtime DLL. The target system must satisfy the corresponding runtime requirements.
- Broad performance, stress, multi-GPU, and cross-device compatibility testing has not been completed.
- The wheel contains native DLLs. Review the licenses and third-party notice obligations for every binary before public distribution.
- Do not include model weights unless you have the necessary redistribution permissions.

## Project documentation

- [`BUILD.md`](BUILD.md): build instructions
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md): troubleshooting
- [`LICENSES.md`](LICENSES.md): license review notes
- [`THIRD_PARTY_NOTICES.template.txt`](THIRD_PARTY_NOTICES.template.txt): third-party notice template (review still required)

## License

The upstream `llama-cpp-python` project declares the MIT license. This does not automatically mean that every native DLL, third-party component, or dependency bundled in this community wheel can be redistributed without restrictions.

Before publishing binary files, review `LICENSES.md` and confirm that all applicable license texts, copyright notices, and third-party notice requirements have been satisfied.

This project is provided as-is, without guarantees of compatibility, performance, or suitability for a particular device.
