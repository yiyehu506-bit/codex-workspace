# 视频整理助手（Python 入门项目）

这是一个适合 Python 初学者的第一个实用项目：把文件夹里的视频文件按扩展名整理到不同子文件夹中。

例如，`.mp4` 会进入 `MP4` 文件夹，`.mov` 会进入 `MOV` 文件夹，其他非视频文件会保持不动。程序默认只预览操作，不会真的移动文件；确认预览结果后加上 `--apply` 才会执行移动。

## 项目能做什么

- 支持常见视频格式：MP4、MOV、AVI、MKV、WMV、FLV、WEBM、M4V、MPEG、MPG、3GP、TS。
- 默认处理源文件夹的第一层文件；加上 `--recursive` 可以处理所有子文件夹。
- 按扩展名创建目标子文件夹。
- 默认使用预览模式，避免第一次运行时误移动文件。
- 如果目标文件名已存在，会自动生成 `文件名 (1).mp4`、`文件名 (2).mp4` 等新名称。
- 只使用 Python 标准库，不需要安装第三方包。

## 文件结构

    codex-workspace/
    ├─ main.py             # 可直接运行的入口文件
    ├─ requirements.txt    # 依赖说明（本项目无第三方依赖）
    ├─ .gitignore          # 忽略虚拟环境和缓存文件
    └─ README.md           # 项目说明和验收步骤

## Windows + VS Code：从零运行

### 1. 准备工具

安装以下工具：

1. Python 3.11 或更高版本，安装时勾选 `Add Python to PATH`。
2. Visual Studio Code。
3. VS Code 的 Python 扩展（发布者为 Microsoft）。

在 VS Code 中按 `Ctrl+Shift+P`，选择 `Python: Select Interpreter`，选择已安装的 Python。

### 2. 获取项目

在 VS Code 中按 `Ctrl+Shift+P`，选择 `Git: Clone`，输入：

    https://github.com/yiyehu506-bit/codex-workspace.git

选择本地保存位置，然后点击 `Open` 打开项目文件夹。

也可以在 VS Code 的终端中运行：

    git clone https://github.com/yiyehu506-bit/codex-workspace.git
    cd codex-workspace

### 3. 创建并启用虚拟环境

在 VS Code 菜单选择 `Terminal > New Terminal`，然后运行：

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1

如果 PowerShell 不允许执行激活脚本，可以直接在 VS Code 中选择 `.venv\Scripts\python.exe` 作为解释器，或者使用命令提示符终端运行：

    .venv\Scripts\activate.bat

看到终端前面出现 `(.venv)`，说明虚拟环境已经启用。

### 4. 安装依赖

本项目没有第三方依赖，但仍建议执行这条命令，确保以后扩展项目时习惯一致：

    py -m pip install -r requirements.txt

### 5. 先查看帮助

    py main.py --help

如果能看到参数说明，说明入口文件可以正常运行。

### 6. 建立安全的练习数据

为了避免误操作真实视频，先在项目文件夹中创建两个文件夹：

    demo_input
    demo_output

在 VS Code 左侧资源管理器中，右键 `demo_input`，创建以下几个空文件：

- `lesson.mp4`
- `short_clip.mov`
- `readme.txt`

这些文件只用于练习。也可以复制几段不重要的视频副本到 `demo_input`。

### 7. 预览整理结果

在 VS Code 终端运行：

    py main.py --source demo_input --destination demo_output

程序会列出准备移动的文件，但不会真正移动它们。确认输出中的源路径、目标路径都正确。

处理真实路径时，请使用引号，例如：

    py main.py --source "C:\Users\你的用户名\Videos\待整理" --destination "C:\Users\你的用户名\Videos\已整理"

### 8. 确认后执行移动

确认预览结果后，再运行：

    py main.py --source demo_input --destination demo_output --apply

预期结果：

- `demo_output\MP4\lesson.mp4` 存在。
- `demo_output\MOV\short_clip.mov` 存在。
- `demo_input\readme.txt` 仍然存在，因为它不是视频。

如果还要处理子文件夹中的视频，加上 `--recursive`：

    py main.py --source demo_input --destination demo_output --recursive --apply

## 常用命令

| 目的 | 命令 |
| --- | --- |
| 查看帮助 | `py main.py --help` |
| 预览第一层文件 | `py main.py --source "源文件夹" --destination "目标文件夹"` |
| 执行第一层整理 | `py main.py --source "源文件夹" --destination "目标文件夹" --apply` |
| 预览所有子文件夹 | `py main.py --source "源文件夹" --destination "目标文件夹" --recursive` |
| 执行所有子文件夹整理 | `py main.py --source "源文件夹" --destination "目标文件夹" --recursive --apply` |

`--source` 和 `--destination` 必须填写。目标文件夹不存在时，程序会自动创建。省略 `--apply` 时永远只预览，不移动文件。

## 验收清单

完成下面 6 项，就完成了这个入门项目：

- [ ] `py --version` 能显示 Python 版本。
- [ ] `py main.py --help` 能显示帮助信息。
- [ ] 预览模式能列出待整理的视频，并且没有改变源文件夹。
- [ ] 加上 `--apply` 后，MP4 和 MOV 文件分别进入对应文件夹。
- [ ] 非视频文件没有被移动。
- [ ] 同名文件再次整理时不会被覆盖，会自动增加编号。

## 常见问题

### `py` 不是命令

重新安装 Python，并勾选 `Add Python to PATH`。也可以尝试使用 `python` 替代命令中的 `py`。

### PowerShell 禁止激活脚本

不激活虚拟环境也可以运行本项目。直接使用 VS Code 选择的 Python 解释器运行 `py main.py ...`，或者切换到命令提示符终端。

### 目标文件夹里已经有同名文件

程序不会覆盖已有文件，会自动使用带编号的新文件名。

### 想撤销移动怎么办

本项目只负责移动，不记录历史。练习时请先使用视频副本；如果已经执行移动，可以在目标文件夹中手动把文件移回原位置。

## 下一步练习

可以在这个项目上继续添加：按拍摄日期整理、按年份和月份建立目录、支持复制模式、写入日志文件，或为整理逻辑补充自动化测试。
