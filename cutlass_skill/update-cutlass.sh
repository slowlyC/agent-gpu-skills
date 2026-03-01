#!/bin/bash
# 从 GitHub 获取/更新 CUTLASS 源码（sparse checkout，只拉需要的目录）
# 用法: bash update-cutlass.sh [--full]
#
# 默认使用 sparse checkout，只拉 ~30MB 的关键目录
# --full  拉取完整仓库（depth=1）

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$SCRIPT_DIR/cutlass-repo"
REPO_URL="https://github.com/NVIDIA/cutlass.git"
BRANCH="main"

FULL_MODE=false
if [ "$1" = "--full" ]; then
    FULL_MODE=true
fi

# sparse checkout 的目录列表
SPARSE_DIRS=(
    # CuTeDSL Python DSL
    "python/CuTeDSL"
    "python/pycute"
    "python/cutlass_library"
    # CuTeDSL 和 C++ 示例
    "examples"
    # CuTe 和 CUTLASS 头文件
    "include"
    # 工具
    "tools/library"
    "tools/util"
)

if [ -d "$REPO_DIR/.git" ]; then
    echo "更新 CUTLASS 源码..."
    cd "$REPO_DIR"
    git pull --ff-only origin "$BRANCH" 2>/dev/null || git pull origin "$BRANCH"
    echo "更新完成."
else
    echo "首次 clone CUTLASS 源码..."

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

check "$REPO_DIR/python/CuTeDSL/cutlass" "CuTeDSL source"
check "$REPO_DIR/python/pycute/layout.py" "pycute"
check "$REPO_DIR/examples/python/CuTeDSL" "CuTeDSL examples"
check "$REPO_DIR/examples/cute/tutorial" "CuTe tutorials"
check "$REPO_DIR/examples/49_hopper_gemm_with_collective_builder" "Hopper GEMM example"
check "$REPO_DIR/examples/70_blackwell_gemm" "Blackwell GEMM example"
check "$REPO_DIR/include/cute/layout.hpp" "CuTe headers"
check "$REPO_DIR/include/cutlass/gemm" "CUTLASS GEMM headers"

echo ""
echo "验证: $PASS 通过, $FAIL 失败"

du -sh "$REPO_DIR" 2>/dev/null | awk '{print "仓库大小: "$1}'
