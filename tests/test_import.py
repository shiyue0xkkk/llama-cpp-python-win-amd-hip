"""Basic import/API test for the community Windows AMD HIP wheel."""
import platform
import struct
import sys

print("Python:", sys.version)
print("Executable:", sys.executable)
print("Platform:", platform.platform())
print("Machine:", platform.machine())
print("Process bits:", struct.calcsize("P") * 8)

if struct.calcsize("P") * 8 != 64:
    raise SystemExit("FAIL: expected a 64-bit Python process")

import llama_cpp
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Qwen35ChatHandler
from llama_cpp.llama_multimodal import GenericMTMDChatHandler

print("llama_cpp version:", llama_cpp.__version__)
print("llama_cpp path:", llama_cpp.__file__)
print("Llama:", Llama)
print("Qwen35ChatHandler:", Qwen35ChatHandler)
print("GenericMTMDChatHandler:", GenericMTMDChatHandler)
print("PASS: import/API checks completed")
