# Piper L + D435 本地文件提取包

本包以本机已有文件为准，直接复制本地下载件、SDK 源码、通信 DLL 和 Python wheel；没有为本次分享重新下载或编译 SDK。仅本说明、下载文档、依赖清单和校验清单为新增文件。

## 已经装进包里的内容

| 目录 / 文件 | 来自哪里 | 说明 |
|---|---|---|
| `01_PiperL/piper_sdk-master.zip` | 本机 Download 目录 | 原始 ZIP，内部 setup.py 标记 0.6.2 |
| `01_PiperL/piper_sdk_本地源码/` | 本机解压后的 piper_sdk 目录 | 按原文件复制，包含厂家协议、示例、文档和许可证；排除缓存和构建中间文件 |
| `01_PiperL/piper_ros-humble.zip` | 本机 Download 目录 | 原始 ROS Humble 项目 ZIP，Linux/ROS 用户可选 |
| `01_PiperL/agx_cando_本地源码/` | 本项目已有 AGX 源码 | 本地修订版 0.1.0+capture1，含 x64/x32 cando.dll、agx_receive.dll 及许可证 |
| `02_D435/Viewer_下载目录/RealSense.Viewer.exe` | 本机 Download 目录 | 原始 Viewer 程序，未运行、未改动；未从文件资源确认具体版本 |
| `02_D435/Viewer_2026722目录/Intel.RealSense.Viewer.exe` | 本机 Download/2026722 目录 | 另一个本地 Viewer 副本，保留不同目录以免混淆；未确认具体版本 |
| `02_D435/librealsense-master.zip` | 本机 Download/2026722 目录 | 原始源码 ZIP，rs.h 中版本为 **2.57.7**，不是 Windows 完整安装程序 |
| `03_Python_Wheels/pyrealsense2-2.58.4.10922-cp312-cp312-win_amd64.whl` | 本机 pip 缓存 | 原始 wheel 恢复标准文件名；包内文件与本项目当前安装副本逐文件一致 |
| `03_Python_Wheels/` 中其他 wheel | 本机已有安装包 | python-can、AGX 后端及其依赖 |

每个复制文件的原始路径、大小和 SHA256 见 `本地文件来源清单.json`。`SHA256SUMS.txt` 用于检查整个分享目录的文件内容。

## 先选自己要用的部分

- **只看 D435 画面**：解压后使用 `02_D435` 中的 Viewer；本次没有启动 Viewer 验证其依赖或相机连接。不能运行时看下载文档中的 Windows 完整 SDK 安装程序。
- **Python 读取 D435 / Windows AGX 通信**：使用 `03_Python_Wheels`；这套离线包对应 **Windows x64 + CPython 3.12**。
- **使用厂家 Piper 高层 SDK**：使用 `01_PiperL` 中的源码和厂家说明。原 SDK 连接层默认 Linux SocketCAN / `can0`；Windows 安装 AGX 后端后，并不会自动完成原 SDK 高层连接接口的移植。
- **ROS/Linux 开发**：使用对应源码包；不要安装 Windows 专用 `.whl` 或 DLL。

本地 RealSense 源码是 2.57.7，而当前项目 Python 包是 2.58.4.10922，二者不是同一版本；Viewer 的版本未确认。保留这些原件是为了方便同学取得本机现成文件，不表示它们是一套同版本 C++ 开发环境。

## Windows Python 安装方式

先准备 Python 3.12 64 位（若没有，见下载文档）。在本包根目录打开终端：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --no-index --find-links=03_Python_Wheels -r requirements-windows-local.txt
.\.venv\Scripts\python.exe -c "import pyrealsense2, can, agx_cando; print('导入成功，不连接设备')"
```

此步骤安装 D435 Python 包和 CAN 通信包，不安装厂家 Piper 高层 SDK，不启动相机或机械臂。不需要 PyTorch、CUDA 或训练模型。

厂家 Piper SDK 源码安装（构建依赖未随本次原件包收集，以下步骤可能联网）：

```powershell
.\.venv\Scripts\python.exe -m pip install "./01_PiperL/piper_sdk_本地源码"
```

Linux 按同目录厂家 README 操作。不要把本机整个 `.venv` 拷到同学电脑当安装包。

## 本地没找到的内容

在此次检查的下载目录、项目目录、pip 缓存和常见安装目录中，未找到独立的 RealSense Windows 完整 SDK 安装器、Python 3.12 安装器或 AGX USB-CAN 系统驱动安装器；没有据此断言整台电脑所有目录都不存在。

已另附 **`缺失文件_官方下载说明.md` 和同内容 `.txt`**，说明在哪里下载、应选择什么版本。它们未被自动下载到本包。

不包含训练数据、模型、机器人序列号、采集/部署日志。原始源码 ZIP 和源码中的许可证保持原样。
