"""Check whether this build exposes GPU-offload support.

This test does not load a model and does not prove that model layers are offloaded.
Run it using the same Python environment as the target application.
"""
import llama_cpp
from llama_cpp import llama_cpp as native

print("llama_cpp version:", llama_cpp.__version__)
print("llama_cpp path:", llama_cpp.__file__)

supports = bool(native.llama_supports_gpu_offload())
print("GPU offload support:", supports)

if not supports:
    raise SystemExit(
        "FAIL: this build does not report GPU-offload support. "
        "Check package selection, build flags, and native DLLs."
    )

print("PASS: backend reports GPU-offload support.")
print("NOTE: use a real model test and verbose logs to verify device detection and layer offload.")
