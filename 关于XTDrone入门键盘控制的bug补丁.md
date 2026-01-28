# XTDrone 仿真平台键盘控制修复补丁

**相关文件**: `multirotor_keyboard_control.py` (根目录下)

## 📝 问题背景
在使用 XTDrone 进行多旋翼无人机仿真时，原版脚本存在以下问题，影响调试效率：

1.  **显示误导**：具备指定参数但是不为'vel'时，后续终端UI中显示此时改变量为速度，但实际传递值为加速度。
2.  **手感极差**：默认步长 `0.01` 太小，仿真中几乎无反应。

## 🛠️ 修复细节
本补丁对脚本进行了以下修正：

* **增加默认参数**：不输参数时，默认进入 `accel` 模式，不再崩溃。
* **UI 修正**：根据模式动态打印 `vel` 或 `accel`，消除歧义。
* **手感优化**：将 `LINEAR_STEP_SIZE` 调整为 **0.2**，起飞响应更灵敏。
* **Bug 修复**：修正变量命名错误。

## 🚀 使用方法

下载本仓库的脚本替换原文件。

* **速度模式 (推荐)**: `python3 multirotor_keyboard_control.py iris 1 vel`
* **加速度模式**: `python3 multirotor_keyboard_control.py iris 1`
