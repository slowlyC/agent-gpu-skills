#!/bin/bash
# 从 GitHub 获取/更新 SGLang 源码（sparse checkout，只拉需要的目录）
# 用法: bash update-sglang.sh [--full]
#
# 默认使用 sparse checkout
# --full  拉取完整仓库（depth=1）

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$SCRIPT_DIR/sglang-repo"
REPO_URL="https://github.com/sgl-project/sglang.git"
BRANCH="main"

FULL_MODE=false
if [ "$1" = "--full" ]; then
    FULL_MODE=true
fi

# sparse checkout 的目录列表
SPARSE_DIRS=(
    # Python 核心
    "python/sglang/srt"
    "python/sglang/jit_kernel"
    "python/sglang/lang"
    # CUDA/C++ kernels
    "sgl-kernel/csrc"
    "sgl-kernel/include"
    "sgl-kernel/python"
    "sgl-kernel/tests"
    "sgl-kernel/benchmark"
    # 示例和文档
    "examples"
    "benchmark"
    "docs"
    "test"
)

if [ -d "$REPO_DIR/.git" ]; then
    echo "更新 SGLang 源码..."
    cd "$REPO_DIR"
    git pull --ff-only origin "$BRANCH" 2>/dev/null || git pull origin "$BRANCH"
    echo "更新完成."
else
    echo "首次 clone SGLang 源码..."

    if [ "$FULL_MODE" = true ]; then
        echo "模式: 完整 clone（depth=1）"
        git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$REPO_DIR"
    else
        echo "模式: sparse checkout（只拉关键目录）"
        git clone --filter=blob:none --no-checkout --depth 1 --branch "$BRANCH" "$REPO_URL" "$REPO_DIR"
        cd "$REPO_DIR"
        git sparse-checkout init --cone
        git sparse-checkout set "${SPARSE_DIRS[@]}"
        git checkout "$BRANCH"
    fi

    echo "Clone 完成."
fi

# 验证
echo ""
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

check "$REPO_DIR/python/sglang/srt/layers/attention" "SRT attention layers"
check "$REPO_DIR/python/sglang/srt/models" "SRT models"
check "$REPO_DIR/python/sglang/srt/managers" "SRT managers"
check "$REPO_DIR/python/sglang/srt/mem_cache" "SRT mem_cache"
check "$REPO_DIR/python/sglang/jit_kernel" "JIT kernels"
check "$REPO_DIR/sgl-kernel/csrc" "sgl-kernel CUDA source"
check "$REPO_DIR/examples" "Examples"
check "$REPO_DIR/docs" "Documentation"

echo ""
echo "验证: $PASS 通过, $FAIL 失败"

du -sh "$REPO_DIR" 2>/dev/null | awk '{print "仓库大小: "$1}'
