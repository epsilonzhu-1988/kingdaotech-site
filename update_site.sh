#!/bin/bash
# KINGDAO 官网一键更新（推送到 GitHub Pages）
# 用法: bash update_site.sh "改动说明"
set -e
cd /c/Users/Administrator/kingdaotech_newsite

MSG="${1:-site update $(date +%Y-%m-%d\ %H:%M)}"

echo "▶ 检查改动…"
if [ -z "$(git status --porcelain)" ]; then
  echo "  没有改动，无需推送"
  exit 0
fi

echo "▶ 提交…"
git add -A
git -c user.email="rongtao@kingdaotech.com" -c user.name="KINGDAO" commit -q -m "$MSG"
echo "  $(git log --oneline -1)"

echo "▶ 同步远程（GitHub 会自动加 CNAME 等文件）…"
git -c user.email="rongtao@kingdaotech.com" -c user.name="KINGDAO" pull --rebase origin main 2>&1 | tail -2 || true

echo "▶ 推送…"
git push origin main 2>&1 | tail -3

echo ""
echo "✅ 推送完成。GitHub Pages 约 1 分钟后自动生效："
echo "   https://new.kingdaotech.com"
echo ""
echo "查看构建进度:"
echo "   https://github.com/epsilonzhu-1988/kingdaotech-site/actions"
