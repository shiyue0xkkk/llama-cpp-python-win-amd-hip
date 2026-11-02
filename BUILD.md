# Build notes: Windows x64 + AMD HIP

This document distinguishes observed build facts from a recipe that still needs a clean reproduction.

## Recorded environment

- Windows x64.
- Python 3.12.10, `AMD64`.
- AMD Radeon RX 7900 XT, architecture `gfx1100`.
- ROCm/HIP SDK 7.2; `hipconfig` reported `7.2.60201-38d754472`.
- Visual Studio Build Tools x64 environment at `C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat`.
- ROCm compiler binaries under `C:\Program Files\AMD\ROCm\7.2\bin`.
- Ninja CMake generator.
- Source staging directory was `C:\llama_build\llama-cpp-python-hip-stage`.
- Build completed with HIP enabled and target `gfx1100`.
- Wheel was tested in an isolated target install before being installed into ComfyUI's embedded Python environment.

**Reproducibility gap:** the exact upstream source commit, full CMake command line, compiler executable versions, and complete dependency lockfile were not preserved. The recipe below is a starting point, not a claim of bit-for-bit reproduction.

## Prerequisites

1. Install a compatible AMD driver and HIP SDK; use [AMD's Windows HIP SDK docs](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/).
2. Install Visual Studio Build Tools with C++ build tools.
3. Install Python 3.12 x64, CMake, and Ninja.
4. Obtain `llama-cpp-python` 0.4.5 source, and record an exact upstream tag/commit before building.
5. Review licenses of native libraries that will be bundled in the wheel.

## PowerShell build outline

Adapt all paths. Open an x64 Native Tools shell or otherwise activate the Visual Studio compiler environment in the shell used for the build.

```powershell
$ErrorActionPreference = "Stop"

$ROOT = "C:\llama_build"
$SRC = "$ROOT\llama-cpp-python-hip-stage"
$PY = "C:\Path\To\Python312\python.exe"
$ROCM = "C:\Program Files\AMD\ROCm\7.2"
$WHEELHOUSE = "$ROOT\wheelhouse"
$TMPDIR = "$ROOT\tmp"

New-Item -ItemType Directory -Force $WHEELHOUSE, $TMPDIR | Out-Null
$env:TEMP = $TMPDIR
$env:TMP = $TMPDIR

& "$ROCM\bin\clang.exe" --version
& "$ROCM\bin\clang++.exe" --version
& $PY --version
ninja --version
cmake --version

$env:CMAKE_ARGS = "-DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1100"
$env:CMAKE_C_COMPILER = "$ROCM\bin\clang.exe"
$env:CMAKE_CXX_COMPILER = "$ROCM\bin\clang++.exe"

Push-Location $SRC
try {
    & $PY -m pip install --upgrade pip build scikit-build-core ninja cmake
    & $PY -m pip wheel . --no-deps --no-build-isolation --wheel-dir $WHEELHOUSE
    if ($LASTEXITCODE -ne 0) { throw "Wheel build failed with exit code $LASTEXITCODE" }
}
finally {
    Pop-Location
}
```

### Notes

- The Visual Studio `vcvars64.bat` environment does not automatically modify the parent PowerShell process when run as a child. Use the Visual Studio x64 Native Tools shell or a verified activation method.
- The flags above describe the intended HIP build configuration; confirm them against the exact source revision before using them. The original full build command was not preserved.
- A new build can have a different hash due to source revision, toolchain, build paths, or build metadata.

## Check the wheel

```powershell
Get-ChildItem "$ROOT\wheelhouse\*.whl"
Get-FileHash "$ROOT\wheelhouse\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl" -Algorithm SHA256
```

Locally tested artifact SHA-256:

`0690b7a6527144f6bb01ec6ca40e4a884392b0ae24324c2962b9305c5cb2f34a`

## Test in isolation

```powershell
$TEST = "C:\llama_build\llama_test_install"
New-Item -ItemType Directory -Force $TEST | Out-Null
& $PY -m pip install --no-deps --target $TEST "$ROOT\wheelhouse\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl"

# Make sure the test scripts import from the intended target directory.
$env:PYTHONPATH = $TEST
& $PY "$SRC\tests\test_import.py"
& $PY "$SRC\tests\test_gpu.py"
```

Embedded Python distributions may ignore or override expected `PYTHONPATH` behavior. If needed, explicitly insert the test target into `sys.path` in the test process.

## Release checklist

- [ ] Record exact upstream commit/tag and local patches.
- [ ] Record Python, CMake, Ninja, Visual Studio, ROCm, and clang versions.
- [ ] Save full build log and exact command.
- [ ] Confirm wheel tags.
- [ ] Run import, GPU detection, and real-model inference tests in a clean environment.
- [ ] Inventory bundled DLLs and review their licenses.
- [ ] Include required notices.
- [ ] Publish as a GitHub Release asset only after redistribution review.
- [ ] Publish SHA-256 and state tested configurations and limitations.
