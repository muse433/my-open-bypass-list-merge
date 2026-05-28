#!/usr/bin/env python3
"""
my-open-bypass-list-merge — 代理规则合并工具

从多个源拉取 Shadowrocket/Clash 规则，合并去重后输出一个文件。
每天 UTC 00:00 由 GitHub Action 自动运行。
"""

import re
import os
import urllib.request
import urllib.error

# ====== 配置区域：在此追加新的规则源 ======
URLS = [
    # Reddit
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Reddit/Reddit.list",
    # Twitter/X
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Twitter/Twitter.list",
    # 流媒体代理
    "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyMedia.list",
    # Gemini
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Gemini/Gemini.list",
    # AI 服务
    "https://testingcf.jsdelivr.net/gh/ACL4SSR/ACL4SSR@master/Clash/Ruleset/AI.list",
    # OpenAI / ChatGPT
    "https://testingcf.jsdelivr.net/gh/ACL4SSR/ACL4SSR@master/Clash/Ruleset/OpenAi.list",
]

# ====== 手动追加规则（不在上游源中的域名） ======
EXTRA_RULES = [
    # Jina AI (jina.ai)
    "DOMAIN-SUFFIX,jina.ai",
    # YouMind (youmind.com)
    "DOMAIN-SUFFIX,youmind.com",
]

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "merged.list")


def fetch(url: str) -> str:
    """从 URL 拉取规则内容。失败时抛异常。"""
    req = urllib.request.Request(url, headers={
        "User-Agent": "my-open-bypass-list-merge/1.0 GitHub Action"
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def is_valid_rule(line: str) -> bool:
    """判断一行是否为合法规则（非注释、非空行）。"""
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return False
    # 允许的规则前缀
    valid_prefixes = (
        "DOMAIN,", "DOMAIN-SUFFIX,", "DOMAIN-KEYWORD,", "IP-CIDR,",
        "IP-CIDR6,", "URL-REGEX,", "GEOIP,", "FINAL,", "MATCH,",
        "AND,", "OR,", "NOT,", "RULE-SET,",
        "DOMAIN-SUFFIX,", "DOMAIN-KEYWORD,",
    )
    return stripped.startswith(valid_prefixes)


def parse_rules(text: str) -> list:
    """解析规则文本，返回去注释后的规则列表。"""
    rules = []
    for line in text.splitlines():
        if not is_valid_rule(line):
            continue
        # 去掉行尾注释（# 后面的内容）
        clean = re.sub(r"\s*#.*$", "", line).strip()
        if clean:
            rules.append(clean)
    return rules


def main():
    all_rules = []
    errors = []

    for url in URLS:
        try:
            print(f"Fetching: {url}")
            text = fetch(url)
            rules = parse_rules(text)
            all_rules.extend(rules)
            print(f"  -> {len(rules)} rules parsed")
        except Exception as e:
            error_msg = f"  -> FAILED: {e}"
            print(error_msg)
            errors.append(f"# FAILED: {url} — {e}")

    # 追加手动规则
    all_rules.extend(EXTRA_RULES)

    # 去重（保持首次出现顺序）
    seen = set()
    unique_rules = []
    for rule in all_rules:
        if rule not in seen:
            seen.add(rule)
            unique_rules.append(rule)

    # 写入
    header_lines = [
        "# my-open-bypass-list-merge — 自动合并规则列表",
        "# https://github.com/muse433/my-open-bypass-list-merge",
        f"# 规则源: {len(URLS)} 个",
        f"# 原始规则: {len(all_rules)} 条",
        f"# 去重后: {len(unique_rules)} 条",
        f"# 生成时间: {__import__('datetime').datetime.now().isoformat()}",
        "",
    ]

    if errors:
        header_lines.append("# ⚠️ 下列源获取失败：")
        header_lines.extend(errors)
        header_lines.append("")

    content = "\n".join(header_lines + unique_rules)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✅ Done! {len(unique_rules)} unique rules written to {OUTPUT_FILE}")
    if errors:
        print(f"⚠️  {len(errors)} source(s) had errors (listed in header)")


if __name__ == "__main__":
    main()
