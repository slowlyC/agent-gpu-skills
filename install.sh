#!/bin/bash
# Cursor GPU Skill 安装脚本
# 用法: bash install.sh [--copy]
#
# 默认使用混合模式: 真实目录 + 复制 SKILL.md + 软链接其余文件
# Cursor 不识别软链接目录和软链接的 SKILL.md，因此:
#   - skill 目录必须是真实目录
#   - SKILL.md 必须是真实文件
#   - repos、references 等子目录/文件可以用软链接
#
# 源码 repo 维护在各 skill 目录的 repos/ 下
# 首次使用需先运行: bash update-repos.sh
#
# --copy  全量复制模式（适用于无法软链接的场景）

set -e

SKILL_DIR="${HOME}/.cursor/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 解析参数
COPY_MODE=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --copy)    COPY_MODE=true; shift ;;
        -h|--help)
            echo "用法: bash install.sh [--copy]"
            echo ""
            echo "首次安装:"
            echo "  bash update-repos.sh    # 获取源码 repo"
            echo "  bash install.sh         # 安装 skill"
            echo ""
            echo "选项:"
            echo "  --copy  全量复制（适用于无法软链接的场景）"
            exit 0
            ;;
        *) echo "未知参数: $1"; exit 1 ;;
    esac
done

echo "================================"
echo "Cursor GPU Skill 安装"
echo "================================"
echo ""

# 检查源目录
if [ ! -d "$SCRIPT_DIR/cuda_skill" ]; then
    echo "错误: 未找到 cuda_skill/ 目录"
    echo "请在 cursor-gpu-skills 项目根目录下运行此脚本"
    exit 1
fi

# 定义 skill 列表: [安装名]=源目录名
declare -A SKILLS
SKILLS[cuda-skill]="cuda_skill"
SKILLS[triton-skill]="triton_skill"
SKILLS[cutlass-skill]="cutlass_skill"
SKILLS[sglang-skill]="sglang_skill"

mkdir -p "$SKILL_DIR"

for skill_name in "${!SKILLS[@]}"; do
    src_dir="${SKILLS[$skill_name]}"
    src_path="$SCRIPT_DIR/$src_dir"
    target="$SKILL_DIR/$skill_name"

    echo "--- $skill_name ---"

    # 清理旧安装（包括旧名称 triton-gluon-skill）
    if [ "$skill_name" = "triton-skill" ]; then
        old_target="$SKILL_DIR/triton-gluon-skill"
        if [ -L "$old_target" ] || [ -d "$old_target" ]; then
            echo "  移除旧版: triton-gluon-skill"
            rm -rf "$old_target"
        fi
    fi

    if [ -L "$target" ]; then
        echo "  移除旧软链接: $target"
        rm "$target"
    elif [ -d "$target" ]; then
        echo "  移除旧目录: $target"
        rm -rf "$target"
    fi

    if [ ! -d "$src_path" ]; then
        echo "  跳过: $src_dir/ 不存在"
        continue
    fi

    if [ "$COPY_MODE" = true ]; then
        cp -r "$src_path" "$target"
        echo "  已复制: $src_path -> $target"
    else
        mkdir -p "$target"

        # 复制 SKILL.md（Cursor 不识别软链接的 SKILL.md）
        cp "$src_path/SKILL.md" "$target/SKILL.md"
        echo "  已复制: SKILL.md"

        # 其余文件/目录用软链接
        for item in "$src_path"/*; do
            basename="$(basename "$item")"
            [ "$basename" = "SKILL.md" ] && continue
            [[ "$basename" == update-*.sh ]] && continue
            ln -sf "$item" "$target/$basename"
            echo "  已链接: $basename"
        done
    fi
done

echo ""
echo "================================"
echo "安装结果"
echo "================================"
echo ""
ls -la "$SKILL_DIR/" 2>/dev/null | grep -E "cuda-skill|triton-skill|cutlass-skill|sglang-skill" || echo "  (无 skill 安装)"
echo ""

# 验证
echo "--- 验证 ---"
PASS=0
FAIL=0

check() {
    if [ -e "$1" ]; then
        echo "  OK: $2"
        PASS=$((PASS + 1))
    else
        echo "  缺失: $2"
        FAIL=$((FAIL + 1))
    fi
}

check "$SKILL_DIR/cuda-skill/SKILL.md" "cuda-skill/SKILL.md"
check "$SKILL_DIR/triton-skill/SKILL.md" "triton-skill/SKILL.md"
check "$SKILL_DIR/cutlass-skill/SKILL.md" "cutlass-skill/SKILL.md"
check "$SKILL_DIR/sglang-skill/SKILL.md" "sglang-skill/SKILL.md"

# CUDA 文档
REFS="$SCRIPT_DIR/cuda_skill/references"
check "$REFS/ptx-docs" "CUDA 文档: ptx-docs"
check "$REFS/cuda-guide" "CUDA 文档: cuda-guide"
check "$REFS/cuda-runtime-docs" "CUDA 文档: cuda-runtime-docs"
check "$REFS/cuda-driver-docs" "CUDA 文档: cuda-driver-docs"
check "$REFS/ptx-simple" "CUDA 文档: ptx-simple"

# Triton
TRITON_REPO="$SKILL_DIR/triton-skill/repos/triton"
check "$TRITON_REPO/python/tutorials" "Triton 教程"
check "$TRITON_REPO/python/tutorials/gluon" "Gluon 教程"
check "$TRITON_REPO/python/triton_kernels" "Triton Kernels"

# CUTLASS
CUTLASS_REPO="$SKILL_DIR/cutlass-skill/repos/cutlass"
check "$CUTLASS_REPO/python/CuTeDSL" "CuTeDSL source"
check "$CUTLASS_REPO/examples/python/CuTeDSL" "CuTeDSL examples"
check "$CUTLASS_REPO/include/cute" "CuTe headers"
check "$CUTLASS_REPO/include/cutlass/gemm" "CUTLASS GEMM headers"

# SGLang
SGLANG_REPO="$SKILL_DIR/sglang-skill/repos/sglang"
check "$SGLANG_REPO/python/sglang/srt" "SGLang SRT core"
check "$SGLANG_REPO/python/sglang/jit_kernel" "SGLang JIT kernels"
check "$SGLANG_REPO/sgl-kernel/csrc" "sgl-kernel CUDA source"

echo ""
echo "验证: $PASS 通过, $FAIL 失败"

if [ $FAIL -gt 0 ]; then
    echo ""
    echo "提示: 缺失的路径可能影响 skill 的搜索功能."
    echo "  - CUDA 文档: 运行 'uv run scrape_cuda_docs.py all --force'"
    echo "  - 源码 repo: 运行 'bash update-repos.sh'"
fi

echo ""
echo "安装完成. 在 Cursor 中按 Ctrl+Shift+P 执行 'Developer: Reload Window' 即可生效."
echo "手动引用: @cuda-skill, @triton-skill, @cutlass-skill, @sglang-skill"
