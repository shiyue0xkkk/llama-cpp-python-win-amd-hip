# Licensing and redistribution review

**Status: incomplete. Do not treat this document as legal advice or as proof that binary redistribution has been cleared.**

The repository owner must complete this review before publicly redistributing the compiled wheel. A source project's license does not automatically grant permission to redistribute every native dependency bundled in a wheel.

## Components identified

| Component | Current knowledge | Required action before publishing the wheel |
|---|---|---|
| `llama-cpp-python` | Upstream repository declares MIT. | Include the exact license text and attribution for the source version/commit used. |
| `llama.cpp` / `ggml` | Native code is compiled into or shipped alongside the Python package. Exact source revision and full license/notice inventory were not preserved in the available notes. | Identify exact revision; include its license and required notices. |
| AMD HIP / ROCm DLLs | Wheel inspection found HIP/ROCm-related DLLs such as `ggml-hip.dll`, `amdhip64_7.dll`, `hipblas.dll`, and `rocblas.dll`. | Identify each DLL's origin/version/license and redistribution conditions. Do not infer that all SDK components may be bundled simply because the SDK can be downloaded. |
| LLVM / Clang runtime components | ROCm clang was used and native dependencies were bundled; the complete DLL inventory and provenance are not recorded here. | Identify included runtime/compiler components and comply with their licenses and notices. |
| Microsoft runtime components | Native binaries may depend on Microsoft runtime DLLs; the exact dependency closure has not been audited here. | Determine whether any Microsoft redistributable is bundled and follow its redistribution terms. |
| Python dependencies | The wheel was installed/tested with `--no-deps`; a complete dependency lockfile was not preserved. | Document required dependencies and their licenses if publishing install instructions or bundled dependencies. |

## Pre-release checklist

- [ ] Pin exact `llama-cpp-python` source commit/tag and record local patches.
- [ ] Preserve upstream license files for the exact source revisions.
- [ ] Generate a complete inventory of wheel contents and native DLL dependencies.
- [ ] Identify the source/version of each bundled DLL.
- [ ] Review redistribution terms for AMD HIP/ROCm, LLVM/Clang runtimes, and Microsoft runtimes.
- [ ] Include required copyright, license, attribution, and notice files.
- [ ] Confirm the wheel contains no proprietary, confidential, or unrelated local files.
- [ ] Record review date and reviewer.
- [ ] If any component's redistribution terms remain unclear, do not distribute that binary; publish build instructions/source-only materials until clarified.

## References

- `llama-cpp-python`: https://github.com/abetlen/llama-cpp-python
- AMD HIP SDK for Windows: https://rocm.docs.amd.com/projects/install-on-windows/en/latest/
- AMD HIP SDK system requirements: https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html

The upstream `llama-cpp-python` project declares MIT in its project metadata and README. This is limited to the upstream project and is not a conclusion about redistribution rights for every binary in this community-built wheel.
