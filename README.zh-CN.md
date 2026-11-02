# llama-cpp-python 0.4.5 — Windows AMD HIP 版 Wheel

这是一个由社区构建的、启用 HIP 后端的 Windows x64 版 `llama-cpp-python` 0.4.5 Wheel。当前首先在 AMD Radeon RX 7900 XT（`gfx1100`）上完成验证。

> **项目状态：社区构建，验证范围有限。** 本项目不是 `llama-cpp-python`、`llama.cpp` 或 AMD 官方发布。重新分发 Wheel 前，请先审查 `LICENSES.md`。在完成所有随附二进制文件的许可证和声明义务核查之前，不要假定它们都可以重新分发。

## 已验证的构建产物

| 项目 | 信息 |
|---|---|
| Python 分发包 | `llama-cpp-python` |
| 版本 | `0.4.5` |
| Wheel 文件 | `llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl` |
| Python ABI | CPython 3.12 |
| 平台 | Windows x86-64 |
| 后端 / 目标架构 | HIP / `gfx1100` |
| 构建环境 | Windows、ROCm/HIP SDK 7.2、Ninja、Visual Studio x64 Build Tools |
| 测试显卡 | AMD Radeon RX 7900 XT；报告显存为 20,464 MiB |
| Wheel 大小 | 71,044,690 字节 |
| SHA-256 | `0690b7a6527144f6bb01ec6ca40e4a884392b0ae24324c2962b9305c5cb2f34a` |

该哈希值用于标识本地测试过的构建产物。哈希匹配只能验证文件是否与此记录一致，不能证明文件安全，也不代表获得官方认可。

## 验证结果

以下检查已在一台机器上成功完成：

- 从预期的 Python 包目录成功导入 `llama_cpp`。
- 成功加载 `ggml-base.dll`、`ggml.dll` 和 `llama.dll`，未再出现此前的 `WinError 193`。
- 成功导入 `Llama`、`Qwen35ChatHandler` 和 `GenericMTMDChatHandler`。
- `llama_supports_gpu_offload()` 返回 `True`。
- HIP 成功识别一张 AMD Radeon RX 7900 XT（`gfx1100`）。
- 在独立安装环境中设置下文所述 COMGR 缓存环境变量后，Qwen3.5 4B GGUF 推理测试成功完成。

以上结果不代表该构建产物一定兼容其他显卡、驱动程序、模型、Windows 版本或 Python 环境。

## 下载与校验

从 GitHub 仓库的 **Releases** 页面下载 `.whl` 文件，然后在 PowerShell 中执行：

```powershell
$WHEEL = ".\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl"
Get-FileHash $WHEEL -Algorithm SHA256
```

将输出结果与上方记录的 SHA-256 值进行比较。

## 兼容性说明

- 64 位 Windows。
- CPython 3.12 x64（`cp312` / `win_amd64`）。
- 需要与本构建匹配的 AMD 驱动和 HIP 运行时。
- 初始测试配置：ROCm/HIP SDK 7.2，GPU 架构 `gfx1100`。
- 其他 AMD GPU 目标架构**尚未通过此构建产物验证**。请勿将此 Wheel 宣传为兼容所有 AMD 显卡。

请查阅 AMD 对应版本的 [Windows HIP SDK 系统要求](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html)。

## 建议先在独立环境中安装

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --no-deps .\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl
```

`--no-deps` 表示只安装 Wheel 本身，不会自动安装其 Python 依赖。如果导入时提示缺少依赖，请安装上游 `llama-cpp-python` 0.4.5 所需的依赖。不要混用来自其他 Python 安装环境的包。

运行仓库中附带的测试脚本：

```powershell
python .\tests\test_import.py
python .\tests\test_gpu.py
```

GPU 设备识别以及 `llama_supports_gpu_offload()` 返回值只能说明后端具备相关能力，并不能证明模型的所有层都已卸载到 GPU。请实际运行模型，并检查详细日志，以确认真实的 GPU Offload 和推理情况。

## 测试中观察到的 COMGR 缓存临时解决方法

首次加载真实模型时，测试遇到了以下错误：

```text
LLVM ERROR: Can't get available size
```

在当前 PowerShell 会话中设置以下环境变量后，同一独立环境中的推理测试成功：

```powershell
$env:AMD_COMGR_CACHE = "1"
$env:AMD_COMGR_CACHE_DIR = "C:\llama_build\comgr_cache"
New-Item -ItemType Directory -Force $env:AMD_COMGR_CACHE_DIR | Out-Null
```

请根据自己的机器选择一个具有写入权限的缓存目录。这是在单一环境中观察到的临时解决方法，并非适用于所有环境的通用方案，也不是 AMD 官方修复方案。启动应用程序的进程必须继承这些环境变量；在另一个终端中修改变量，不会自动影响已经运行的进程。

## 已知限制与待完善事项

- 现有记录未保留完整的上游源码 commit 和完整构建命令，因此目前尚不能证明能够逐字节复现该 Wheel。
- 构建过程中使用了 ROCm clang，而 SDK 内置的 LLVM 版本不同；尚未独立排除这一版本差异带来的兼容性风险。
- 目前只测试了一张 GPU 和一条模型推理路径；尚未完成大范围性能、压力、多 GPU 或兼容性矩阵测试。
- Wheel 包含原生 DLL。公开二进制文件前，请审查其再分发条款并附上所需声明，详见 [`LICENSES.md`](LICENSES.md)。
- 除非拥有相应再分发许可，否则不要在项目中附带模型权重。

## 构建与故障排查文档

- [`BUILD.md`](BUILD.md)：构建指南
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)：故障排查
- [`LICENSES.md`](LICENSES.md)：许可证审查说明

## 许可证说明

上游 `llama-cpp-python` 项目声明采用 MIT 许可证，但这并不自动意味着该社区构建 Wheel 中捆绑的所有二进制文件都可以不受限制地重新分发。公开二进制文件前，请先审查 [`LICENSES.md`](LICENSES.md)。
