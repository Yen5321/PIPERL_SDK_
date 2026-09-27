# Piper L SDK 分享包

这是当前项目使用/参考的本地版本整理包，整理日期 2026-09-27，不代表厂家最新版本。不含训练模型、录制数据、机器人日志或原电脑的虚拟环境。

## 包里有什么

| 内容 | 版本 / 用途 |
|---|---|
| Piper SDK 源码及 wheel | 0.6.2，本地厂家源码构建；含 V2 协议、接口、示例和文档 |
| python-can | 4.6.1，Python CAN 通信接口 |
| python-can-agx-cando | 0.1.0+capture1，本项目使用的 Windows AGX 后端修订版 |
| cando.dll / agx_receive.dll | AGX wheel 和源码内含 x64、x32 文件 |
| wrapt / packaging / typing_extensions | Windows Python 3.12 x64 离线依赖 |
| smoke_test.py | 不连接硬件的导入、插件注册和 SDK 解码检查 |
| examples/windows_receive_only.py | Windows AGX 只接收反馈示例，使用 SDK V2 解码器 |

`source/` 包含双方源码、原有许可证和说明。`wheels/` 包含安装包。`SHA256SUMS.txt` 用于核对文件完整性。

## Windows 同学怎么用

1. 先安装 **Python 3.12 64 位**，包含 Python Launcher（`py` 命令）。Python 安装程序未打包。
2. 把整个压缩包解压到一个普通目录，不要在压缩包内直接运行。
3. 双击 `Install_Windows.cmd`。它建立独立 `.venv`，只从随包 wheels 离线安装，不改系统 Python 环境，也不会连接机械臂。
4. 看到 `PASS` 表示软件安装及协议解码测试通过，不表示硬件已连接或抓取已验证。

当前离线依赖针对 Windows x64 / CPython 3.12，其他 Python 版本不要直接套用。AGX wheel 标记为通用 Python 包，但其 DLL 后端仍要求 Windows。

想接收真实反馈时，关闭其他采集/CAN 程序，连接适配器，在解压目录运行：

```powershell
.\.venv\Scripts\python.exe .\examples\windows_receive_only.py --channel 0 --seconds 10
```

这个例子会打开适配器并设置 1 Mbps 波特率，只调用接收，不发送使能、关节、夹爪、回零或查询指令。它没有在同学的设备上验证。USB 适配器需被 Windows 正确识别；独立 USB 系统驱动安装程序未包含，随包 DLL 不等于系统设备驱动。

## SDK 与 Windows 通信包的区别

原版 `C_PiperInterface_V2` 默认连接 Linux SocketCAN / `can0`，包含 Linux 接口检查。**安装 AGX 后端不会自动把这个高层连接入口移植到 Windows。** 此项目在 Windows 端使用 `python-can + agx_cando` 通信，本包只接收示例则进一步使用厂家 SDK 的协议解码器。

若同学要开发 Windows 控制程序，需要按接口文档对接通信层，不能把 Linux 示例的 `can0` 简单改成 `0` 就认为能用。本包没有重新移植或验证整套 Windows 高层运动控制接口。SDK 原有运动示例保留在源码中，须先阅读用途，安装脚本不会运行它们。

## Linux 同学怎么用

使用 `source/piper_sdk_0.6.2` 的厂家源码和文档，或安装对应 wheel；AGX Windows 后端及 Windows wrapt wheel 不适用。已具备 Python/pip 且可联网的环境中：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ./wheels/piper_sdk-0.6.2-py3-none-any.whl
```

pip 将按 Linux 平台获取 `python-can` 等依赖。随后按厂家文档配置 SocketCAN 设备。Linux 安装与硬件连接未在本次打包中测试。

## 文档和来源

- 厂家中文说明：`source/piper_sdk_0.6.2/README(ZH).MD`
- V2 接口文档：`source/piper_sdk_0.6.2/asserts/V2/INTERFACE_V2.MD`
- 厂家 SDK 来源：https://github.com/agilexrobotics/piper_sdk
- AGX 后端上游：https://github.com/agilexrobotics/python-can-agx-cando
- 本地 AGX 版本说明：`LOCAL_CHANGES.md`

保留随源码、wheel 分发的原有许可证和版权声明。此包不包含 D435、LeRobot、PyTorch、CUDA、训练/部署应用，它们不是本次 SDK 通信依赖。
