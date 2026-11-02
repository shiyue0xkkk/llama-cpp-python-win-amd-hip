# llama-cpp-python 0.4.5 — Windows AMD HIP Wheel

Community-built Windows x64 wheel for `llama-cpp-python` 0.4.5 with HIP enabled, initially validated on AMD Radeon RX 7900 XT (`gfx1100`).

> **Status: community build / limited validation.** This is not an official release from the `llama-cpp-python`, `llama.cpp`, or AMD teams. Review `LICENSES.md` before redistributing the wheel. Do not assume every bundled binary can be redistributed until its license and notice requirements have been checked.

## Validated artifact

| Item | Value |
|---|---|
| Distribution | `llama-cpp-python` |
| Version | `0.4.5` |
| Wheel | `llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl` |
| Python ABI | CPython 3.12 |
| Platform | Windows x86-64 |
| Backend / target | HIP / `gfx1100` |
| Build environment | Windows, ROCm/HIP SDK 7.2, Ninja, Visual Studio x64 build tools |
| Tested GPU | AMD Radeon RX 7900 XT; 20,464 MiB reported VRAM |
| Wheel size | 71,044,690 bytes |
| SHA-256 | `0690b7a6527144f6bb01ec6ca40e4a884392b0ae24324c2962b9305c5cb2f34a` |

The hash identifies the locally tested artifact. A matching hash verifies file integrity against this record; it does not prove safety or official endorsement.

## Validation status

The following checks succeeded on one machine:

- Imported `llama_cpp` from the intended package directory.
- Loaded `ggml-base.dll`, `ggml.dll`, and `llama.dll` without the previous `WinError 193`.
- Imported `Llama`, `Qwen35ChatHandler`, and `GenericMTMDChatHandler`.
- `llama_supports_gpu_offload()` returned `True`.
- HIP detected one AMD Radeon RX 7900 XT (`gfx1100`).
- A Qwen3.5 4B GGUF inference test completed in an isolated install after setting the COMGR cache variables described below.

These results do not guarantee compatibility with other GPUs, drivers, models, Windows versions, or Python environments.

## Download and verify

Download the `.whl` from the GitHub **Releases** page, then run in PowerShell:

```powershell
$WHEEL = ".\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl"
Get-FileHash $WHEEL -Algorithm SHA256
```

Compare the result with the SHA-256 above.

## Compatibility

- 64-bit Windows.
- CPython 3.12 x64 (`cp312` / `win_amd64`).
- Compatible AMD driver/HIP runtime for this build.
- Initial tested configuration: ROCm/HIP SDK 7.2 and `gfx1100`.
- Other AMD GPU targets are **not verified by this artifact**. Do not advertise this wheel as universally compatible with AMD GPUs.

Check AMD's version-specific [HIP SDK for Windows system requirements](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html).

## Install in an isolated environment first

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --no-deps .\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl
```

`--no-deps` installs the wheel only, not its Python dependencies. If imports report missing packages, install the dependencies required by upstream version 0.4.5. Do not mix packages from unrelated Python installations.

Run the included tests:

```powershell
python .\tests\test_import.py
python .\tests\test_gpu.py
```

GPU detection and `llama_supports_gpu_offload()` are backend checks, not proof that every model layer is offloaded. Run a real model and inspect verbose logs to verify actual offload and inference.

## COMGR cache workaround observed during testing

The first real model load failed with `LLVM ERROR: Can't get available size`. The same isolated inference test succeeded after setting these variables in the current PowerShell session:

```powershell
$env:AMD_COMGR_CACHE = "1"
$env:AMD_COMGR_CACHE_DIR = "C:\llama_build\comgr_cache"
New-Item -ItemType Directory -Force $env:AMD_COMGR_CACHE_DIR | Out-Null
```

Choose a writable cache path on your own machine. This is a workaround observed in one environment, not a universal or official AMD fix. The application must inherit these variables; a running process will not automatically receive changes made in another terminal.

## Known limitations

- The exact upstream source commit and complete build command were not preserved in the available notes; bit-for-bit reproducibility is not established.
- ROCm clang was used, while the embedded SDK contained a different LLVM version. This mismatch was not independently ruled out as a compatibility risk.
- One GPU and one model inference path were tested; no broad performance, stress, multi-GPU, or compatibility matrix was completed.
- The wheel bundles native DLLs. Review redistribution terms and include required notices before publishing; see [`LICENSES.md`](LICENSES.md).
- Do not include model weights unless you have permission to redistribute them.

## Build and troubleshooting

- [`BUILD.md`](BUILD.md)
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)
- [`LICENSES.md`](LICENSES.md)

## License

The upstream `llama-cpp-python` project declares MIT, but this does not automatically settle redistribution rights for every binary bundled in this community wheel. Review `LICENSES.md` before publishing binaries.
