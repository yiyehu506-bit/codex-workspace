from __future__ import annotations

import argparse
import itertools
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


VIDEO_EXTENSIONS = {
    ".3gp",
    ".avi",
    ".flv",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpeg",
    ".mpg",
    ".ts",
    ".webm",
    ".wmv",
}


@dataclass(frozen=True)
class PlannedMove:
    source: Path
    target: Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="按视频扩展名整理文件夹中的视频文件。默认只预览，不移动文件。"
    )
    parser.add_argument(
        "--source",
        required=True,
        type=Path,
        help="待整理的源文件夹。",
    )
    parser.add_argument(
        "--destination",
        required=True,
        type=Path,
        help="整理结果保存到的目标文件夹。不存在时会自动创建。",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="同时扫描源文件夹的所有子文件夹。",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="真正移动文件；省略时只显示预览结果。",
    )
    return parser


def is_inside(path: Path, parent: Path) -> bool:
    """Return True when path is parent itself or a child of parent."""
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def iter_video_files(
    source: Path, destination: Path, recursive: bool
) -> Iterable[Path]:
    candidates = source.rglob("*") if recursive else source.iterdir()
    for path in sorted(candidates):
        if not path.is_file() or path.is_symlink():
            continue
        # If the destination is inside source, do not scan files already moved there.
        if is_inside(path, destination):
            continue
        if path.suffix.lower() in VIDEO_EXTENSIONS:
            yield path


def available_target(
    desired: Path, reserved: set[Path]
) -> Path:
    if not desired.exists() and desired not in reserved:
        return desired

    for number in itertools.count(1):
        candidate = desired.with_name(
            f"{desired.stem} ({number}){desired.suffix}"
        )
        if not candidate.exists() and candidate not in reserved:
            return candidate


def plan_moves(
    source: Path, destination: Path, recursive: bool
) -> list[PlannedMove]:
    reserved: set[Path] = set()
    moves: list[PlannedMove] = []
    for path in iter_video_files(source, destination, recursive):
        category = path.suffix.lstrip(".").upper()
        desired = destination / category / path.name
        target = available_target(desired, reserved)
        reserved.add(target)
        moves.append(PlannedMove(source=path, target=target))
    return moves


def run(args: argparse.Namespace) -> int:
    source = args.source.expanduser().resolve()
    destination = args.destination.expanduser().resolve()

    if not source.exists():
        print(f"错误：源文件夹不存在：{source}", file=sys.stderr)
        return 2
    if not source.is_dir():
        print(f"错误：源路径不是文件夹：{source}", file=sys.stderr)
        return 2
    if source == destination:
        print("错误：源文件夹和目标文件夹不能相同。", file=sys.stderr)
        return 2

    moves = plan_moves(source, destination, args.recursive)
    mode = "执行模式" if args.apply else "预览模式"
    print(f"{mode}：{source} -> {destination}")

    if not moves:
        print("未找到可整理的视频文件。")
        return 0

    print(f"发现 {len(moves)} 个视频文件：")
    for move in moves:
        print(f"  {move.source} -> {move.target}")

    if not args.apply:
        print("预览结束：未移动任何文件。确认无误后加上 --apply 执行。")
        return 0

    success_count = 0
    error_count = 0
    for move in moves:
        try:
            move.target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(move.source), str(move.target))
        except OSError as error:
            error_count += 1
            print(f"  移动失败：{move.source} -> {error}", file=sys.stderr)
        else:
            success_count += 1

    print(f"整理完成：成功 {success_count} 个，失败 {error_count} 个。")
    return 1 if error_count else 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())