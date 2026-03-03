#!/bin/bash
# GPU Skill 安装脚本
# 用法: bash install.sh [--agent cursor|claude|codex|gemini] [--copy]
#
# 默认安装到 Cursor。使用 --agent 选择目标工具。
#
# 安装模式（默认混合模式）:
#   - skill 目录: 真实目录（多数工具不识别软链接目录）
#   - SKILL.md: 复制真实文件
#   - repos、references 等子目录/文件: 软链接到项目目录
#
# --copy  全量复制模式（适用于无法软链接的场景）

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

AGENT="cursor"
COPY_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --agent) AGENT="$2"; shift 2 ;;
        --copy)  COPY_MODE=true; shift ;;
        -h|--help)
            echo "用法: bash install.sh [--agent cursor|claude|codex|gemini] [--copy]"
            echo ""
            echo "首次安装:"
            echo "  bash update-repos.sh    # 获取源码 repo"
            echo "  bash install.sh         # 安装到 Cursor (默认，已验证)"
            echo ""
            echo "安装到其他工具 (未验证，如遇问题让对应 AI 协助排查):"
            echo "  bash install.sh --agent claude   # Claude Code (~/.claude/skills/)"
            echo "  bash install.sh --agent codex    # Codex (~/.agents/skills/)"
            echo "  bash install.sh --agent gemini   # Gemini CLI (~/.gemini/skills/)"
            echo ""
            echo "选项:"
            echo "  --copy  全量复制（适用于无法软链接的场景）"
            exit 0
            ;;
        *) echo "未知参数: $1"; exit 1 ;;
    esac
done

get_skill_dir() {
    case $1 in
        cursor) echo "${HOME}/.cursor/skills" ;;
        claude) echo "${HOME}/.claude/skills" ;;
        codex)  echo "${HOME}/.agents/skills" ;;
        gemini) echo "${HOME}/.gemini/skills" ;;
        *)      echo "Unknown agent: $1" >&2; return 1 ;;
    esac
}

if [ ! -d "$SCRIPT_DIR/cuda_skill" ]; then
    echo "错误: 未找到 cuda_skill/ 目录"
    echo "请在项目根目录下运行此脚本"
    exit 1
fi

declare -A SKILLS
SKILLS[cuda-skill]="cuda_skill"
SKILLS[triton-skill]="triton_skill"
SKILLS[cutlass-skill]="cutlass_skill"
SKILLS[sglang-skill]="sglang_skill"

install_to_agent() {
    local agent=$1
    local SKILL_DIR
    SKILL_DIR=$(get_skill_dir "$agent")

    echo "================================"
    echo "安装到 $agent ($SKILL_DIR)"
    echo "================================"
    echo ""

    mkdir -p "$SKILL_DIR"

    for skill_name in "${!SKILLS[@]}"; do
        src_dir="${SKILLS[$skill_name]}"
        src_path="$SCRIPT_DIR/$src_dir"
        target="$SKILL_DIR/$skill_name"

        echo "--- $skill_name ---"

        # 清理旧安装
        if [ "$skill_name" = "triton-skill" ]; then
            old_target="$SKILL_DIR/triton-gluon-skill"
            if [ -L "$old_target" ] || [ -d "$old_target" ]; then
                echo "  移除旧版: triton-gluon-skill"
                rm -rf "$old_target"
            fi
        fi

        if [ -L "$target" ]; then
            rm "$target"
        elif [ -d "$target" ]; then
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
            cp "$src_path/SKILL.md" "$target/SKILL.md"
            echo "  已复制: SKILL.md"

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
}

install_to_agent "$AGENT"

# 验证
echo "================================"
echo "验证"
echo "================================"
echo ""

verify_agent() {
    local agent=$1
    local SKILL_DIR
    SKILL_DIR=$(get_skill_dir "$agent")
    local PASS=0 FAIL=0

    echo "--- $agent ($SKILL_DIR) ---"

    check() {
        if [ -e "$1" ]; then
            echo "  OK: $2"
            PASS=$((PASS + 1))
        else
            echo "  缺失: $2"
            FAIL=$((FAIL + 1))
        fi
    }

    for skill_name in "${!SKILLS[@]}"; do
        check "$SKILL_DIR/$skill_name/SKILL.md" "$skill_name/SKILL.md"
    done

    REFS="$SCRIPT_DIR/cuda_skill/references"
    check "$REFS/ptx-docs" "CUDA 文档: ptx-docs"
    check "$REFS/cuda-guide" "CUDA 文档: cuda-guide"
    check "$REFS/cuda-runtime-docs" "CUDA 文档: cuda-runtime-docs"
    check "$REFS/cuda-driver-docs" "CUDA 文档: cuda-driver-docs"

    local TRITON_REPO="$SKILL_DIR/triton-skill/repos/triton"
    check "$TRITON_REPO/python/tutorials" "Triton 教程"
    check "$TRITON_REPO/python/tutorials/gluon" "Gluon 教程"

    local CUTLASS_REPO="$SKILL_DIR/cutlass-skill/repos/cutlass"
    check "$CUTLASS_REPO/python/CuTeDSL" "CuTeDSL source"
    check "$CUTLASS_REPO/include/cute" "CuTe headers"

    local SGLANG_REPO="$SKILL_DIR/sglang-skill/repos/sglang"
    check "$SGLANG_REPO/python/sglang/srt" "SGLang SRT core"
    check "$SGLANG_REPO/sgl-kernel/csrc" "sgl-kernel CUDA source"

    echo "  验证: $PASS 通过, $FAIL 失败"
    echo ""

    if [ $FAIL -gt 0 ]; then
        echo "  提示: 缺失路径可能影响 skill 搜索功能."
        echo "    - CUDA 文档: 运行 'uv run scrape_docs.py all --force'"
        echo "    - 源码 repo: 运行 'bash update-repos.sh'"
        echo ""
    fi
}

verify_agent "$AGENT"

echo "安装完成."
