#!/bin/bash
# 从 GitHub 获取/更新 Triton 源码（sparse checkout，只拉需要的目录）
# 用法: bash update-triton.sh [--full]
#
# 默认使用 sparse checkout，只拉 ~7MB 的关键目录
# --full  拉取完整仓库（depth=1）

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$SCRIPT_DIR/triton-repo"
REPO_URL="https://github.com/triton-lang/triton.git"
BRANCH="main"

FULL_MODE=false
if [ "$1" = "--full" ]; then
    FULL_MODE=true
fi

# sparse checkout 的目录列表
SPARSE_DIRS=(
    # Python: tutorials, kernels, language API
    "python/tutorials"
    "python/triton_kernels"
    "python/triton/language"
    "python/triton/experimental/gluon"
    "python/triton/runtime"
    "python/triton/compiler"
    "python/triton/tools"
    "python/examples"
    # C++: 编译器 IR 定义和 passes
    "include"
    "lib"
)

if [ -d "$REPO_DIR/.git" ]; then
    echo "更新 Triton 源码..."
    cd "$REPO_DIR"
    git pull --ff-only origin "$BRANCH" 2>/dev/null || git pull origin "$BRANCH"
    echo "更新完成."
else
    echo "首次 clone Triton 源码..."

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

check "$REPO_DIR/python/tutorials/01-vector-add.py" "Triton tutorials"
check "$REPO_DIR/python/tutorials/gluon/01-intro.py" "Gluon tutorials"
check "$REPO_DIR/python/triton_kernels/triton_kernels/matmul.py" "Triton kernels"
check "$REPO_DIR/python/triton/language/__init__.py" "Triton language"
check "$REPO_DIR/python/triton/experimental/gluon" "Gluon experimental"
check "$REPO_DIR/python/examples" "Examples"
check "$REPO_DIR/include/triton/Dialect" "C++ Dialect headers"
check "$REPO_DIR/lib/Dialect" "C++ Dialect implementations"

echo ""
echo "验证: $PASS 通过, $FAIL 失败"

du -sh "$REPO_DIR" 2>/dev/null | awk '{print "仓库大小: "$1}'
