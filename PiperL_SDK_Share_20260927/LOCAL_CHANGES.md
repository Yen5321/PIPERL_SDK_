# 本地版本说明

- `piper_sdk 0.6.2`：从本机已有厂家 SDK 源码构建 wheel。SDK 源码在整理过程中未修改；文档完整保留。未在线更新到其他版本。
- `python-can-agx-cando 0.1.0+capture1`：来自本项目实际使用的 wheel，与随包 `source/python_can_agx_cando_capture1/agx_cando` 的 Python 文件和 DLL 逐文件比对一致。它是本地修订版，不应标记为未经修改的厂家发布包。
- 此 AGX 版本的接收帧时间戳使用接收时刻，附带 native 接收辅助 DLL。实现详见源码和 `native/README.md`。
- AGX 后端的 `send(timeout=...)` 在当前源码中不实现写入超时保证，不要把该参数当成已经验证的硬件超时保护。
- 随包新示例显式传入 `one_shot=False`，与本项目当前配置一致；上游/随包原始示例可能使用不同默认值。
- 新增离线安装脚本、导入/解码检查和只接收示例；本次不会运行厂家运动示例或打开真实 CAN 连接。
