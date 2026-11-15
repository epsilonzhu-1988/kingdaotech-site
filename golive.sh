#!/bin/bash
# KINGDAO 官网正式上线（切到 www.kingdaotech.com）—— 一次性脚本
# 用法: bash golive.sh          切到 www 上线
#       bash golive.sh rollback 域名回滚到 new.
set -e
cd "$(dirname "$0")"
PROD="www.kingdaotech.com"
OLD="new.kingdaotech.com"

if [ "$1" = "rollback" ]; then
  FROM=$PROD; TO=$OLD
else
  FROM=$OLD; TO=$PROD
fi

echo "▶ 域名: $FROM → $TO"
# 1) GitHub Pages 的 CNAME
echo -n "$TO" > CNAME
# 2) sitemap / robots
sed -i "s#https://$FROM#https://$TO#g" sitemap.xml robots.txt
# 3) 所有页面 canonical
find . -name "*.html" -not -path "./.git/*" -exec sed -i "s#https://$FROM#https://$TO#g" {} +

echo "✔ 已改：CNAME / sitemap.xml / robots.txt / $(find . -name '*.html' -not -path './.git/*' | wc -l) 个页面的 canonical"
grep -o "https://[a-z.]*kingdaotech.com" CNAME sitemap.xml | sort -u
echo
echo "下一步（手动，在 DNSPod 控制台）:"
echo "  www  CNAME → epsilonzhu-1988.github.io"
echo "  @    A     → 185.199.108.153 / 109 / 110 / 111（或 A 记录指向同一目标后再做 301 到 www）"
echo "  ⛔ MX / TXT / SPF / DKIM 一条都不要动"
echo
echo "然后:"
echo "  git add -A && git -c user.name=hermes -c user.email=hermes@local commit -m 'go-live: $TO' && git pull --rebase origin main && git push origin main"
echo
echo "回滚（5 分钟复活旧站）: 把 www 的 CNAME 改回 $FROM，或 bash golive.sh rollback"
