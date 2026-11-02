# llama-cpp-python 0.4.5 — Windows AMD HIP 版 Wheel

这是一个由社区构建的、启用 HIP 后端的 Windows x64 版 `llama-cpp-python` 0.4.5 Wheel。当前已在 AMD Radeon RX 7900 XT（`gfx1100`）上完成 GPU 识别及实际模型推理验证。

> **项目状态：社区构建，验证范围有限。** 本项目不是 `llama-cpp-python`、`llama.cpp` 或 AMD 官方发布。使用前请阅读本文的兼容性和运行时依赖说明。重新分发 Wheel 前，必须完成 `LICENSES.md` 中的许可证审查及第三方声明核查。

## 当前候选构建产物

| 项目 | 信息 |
|---|---|
| Python 分发包 | `llama-cpp-python` |
| 版本 | `0.4.5` |
| Wheel 文件 | `llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl` |
| Python ABI | CPython 3.12 |
| 平台 | Windows x86-64 |
| 后端 / 目标架构 | HIP / `gfx1100` |
| 构建环境 | Windows、ROCm/HIP SDK 7.2、Ninja、Visual Studio x64 Build Tools |
| 测试显卡 | AMD Radeon RX 7900 XT |
| Wheel 大小 | 20,111,549 字节（约 20.11 MB） |
| SHA-256 | `DDDA9F92B6D4F631B6541EAF465E83B9DFEEC760D29A64FEFC0D13AEEB04ACE7` |

> 该 SHA-256 用于核对文件是否与本项目记录的候选构建产物一致。哈希匹配不代表文件一定安全，也不代表获得上游或 AMD 官方认可。正式发布时，请确保 Release 中的文件与上述哈希一致。

## 验证结果

以下检查已在一台 Windows 设备上完成：

- 成功从预期的 Python 包目录导入 `llama_cpp`。
- 成功加载 `ggml-base.dll`、`ggml.dll` 和 `llama.dll`，此前遇到的 `WinError 193` 不再出现。
- 成功导入 `Llama`、`Qwen35ChatHandler` 和 `GenericMTMDChatHandler`。
- `llama_supports_gpu_offload()` 返回 `True`。
- HIP 成功识别 AMD Radeon RX 7900 XT（`gfx1100`）。
- 在独立安装环境中设置 COMGR 缓存环境变量后，Qwen3.5 4B GGUF 实际推理测试成功。
- 完成 Wheel ZIP CRC、RECORD 文件哈希和文件大小校验。
- 完成安装、导入、DLL 去重及当前测试机器上的动态库加载路径检查。

以上结果仅代表当前测试环境，不能保证其他 GPU、驱动、Windows 版本、Python 环境或模型均可正常工作。

## 下载与校验

从本项目 GitHub 仓库的 Releases 页面下载 `.whl` 文件。

在 PowerShell 中执行：

```powershell
$WHEEL = ".\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl"
Get-FileHash $WHEEL -Algorithm SHA256
```

将输出的 SHA-256 与本文记录进行比较。若不一致，请不要继续安装，先确认下载文件和 Release 版本。

## 兼容性要求

- 64 位 Windows。
- CPython 3.12 x64（`cp312` / `win_amd64`）。
- 与本构建匹配的 AMD 显卡驱动和 HIP Runtime。
- 当前已验证配置：ROCm/HIP SDK 7.2，GPU 架构 `gfx1100`。
- 其他 AMD GPU 目标架构尚未通过本 Wheel 验证。

请查阅 AMD 对应版本的 [Windows HIP SDK 系统要求](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html)。

**不要将本 Wheel 宣传为兼容所有 AMD 显卡或所有 ROCm 版本。**

## 重要：外部运行时依赖

本 Wheel 不包含所有运行时依赖，目标机器需要具备匹配的运行环境。

### AMD HIP Runtime

本次构建没有将以下 AMD 运行时 DLL 打包进 Wheel：

- `amdhip64_7.dll`
- `hipblas.dll`
- `rocblas.dll`

这些运行库需要通过 AMD 官方渠道安装与本构建相匹配的运行环境。不要从来源不明的网站下载 DLL，也不要随意将其他版本的 DLL 复制到 Python 包目录。

### OpenMP Runtime

本 Wheel 的部分原生 DLL 存在 OpenMP 运行时依赖。

当前测试机器能够从系统环境加载 `libomp140.x86_64.dll`，但这不代表其他 Windows 机器一定具有兼容版本。

**不要直接从开发工具目录复制或重新分发 OpenMP DLL。** 请使用具有合法再分发许可的运行时方案，并在目标机器上实际验证。

设备能够识别 GPU，并不意味着所有外部运行时依赖都已经满足。

## 建议先在独立 Python 环境中安装

建议先建立虚拟环境，避免影响 ComfyUI 或其他 Python 项目。

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

python -m pip install --no-deps .\llama_cpp_python-0.4.5-cp312-cp312-win_amd64.whl
```

`--no-deps` 只安装 Wheel 本身，不会自动安装 Python 依赖。如果导入时提示缺少 Python 包，请根据上游 `llama-cpp-python` 0.4.5 的依赖要求安装。

不要混用来自不同 Python 安装环境的包。

运行仓库中附带的检查脚本：

```powershell
python .\tests\test_import.py
python .\tests\test_gpu.py
```

GPU 识别以及 `llama_supports_gpu_offload()` 返回 `True`，只能说明后端具备相关能力，不能证明模型所有层都已卸载到 GPU。请使用实际模型运行推理，并检查详细日志中的 GPU Offload 和计算缓冲区信息。

## COMGR 缓存问题及临时解决方法

首次加载真实模型时，测试遇到了：

```text
LLVM ERROR: Can't get available size
```

在当前 PowerShell 会话中设置以下环境变量后，同一独立环境中的推理测试成功：

```powershell
$env:AMD_COMGR_CACHE = "1"
$env:AMD_COMGR_CACHE_DIR = "$env:LOCALAPPDATA\llama-cpp-python\comgr_cache"

New-Item -ItemType Directory -Force $env:AMD_COMGR_CACHE_DIR | Out-Null
```

请确保当前用户对缓存目录具有写入权限。

这是在单一测试环境中观察到的临时解决方法，不是 AMD 官方修复方案，也不保证适用于所有设备。

启动 ComfyUI 或其他应用程序的进程必须继承这些环境变量。在另一个 PowerShell 窗口中设置变量，不会自动影响已经运行的进程。

## 已知限制

- 当前只在一张 AMD Radeon RX 7900 XT（`gfx1100`）上完成主要验证，其他 GPU 架构尚未建立完整兼容性矩阵。
- 目前没有完整保留可用于逐字节复现的上游源码 commit 和全部构建命令，因此不能声称该 Wheel 已实现完全可复现构建。
- 本次测试完成了指定模型的实际推理，但不代表所有模型、多模态工作流或 ComfyUI 节点均已全面验证。
- `llama-common.dll`、`mtmd.dll` 等其他功能相关 DLL 未在本次短文本推理路径中完成全面验证。
- Wheel 不包含 AMD HIP Runtime DLL，也不包含 OpenMP Runtime DLL；目标机器需要自行满足相应运行时要求。
- 尚未完成大范围性能测试、压力测试、多 GPU 测试及跨设备兼容性测试。
- Wheel 包含原生 DLL。公开分发前，必须核查所有二进制文件的许可证和第三方声明义务。
- 不要在项目中附带模型权重，除非已获得相应的再分发许可。

## 项目文档

- [`BUILD.md`](BUILD.md)：构建指南
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)：故障排查
- [`LICENSES.md`](LICENSES.md)：许可证审查说明
- [`THIRD_PARTY_NOTICES.template.txt`](THIRD_PARTY_NOTICES.template.txt)：第三方声明模板（尚需完成核查）

## 许可证说明

上游 `llama-cpp-python` 项目声明采用 MIT 许可证，但这并不自动意味着本社区构建 Wheel 中所有捆绑的原生 DLL、第三方组件和依赖文件均可自由重新分发。

公开发布二进制文件前，请逐项审查 `LICENSES.md`，确认许可证文本、版权声明和第三方通知要求均已满足。

本项目按现状提供，不对特定设备上的兼容性、性能或适用性作出保证。
