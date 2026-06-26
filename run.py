#!/usr/bin/env python3
"""
AI Affiliate - 一键运行入口

Usage:
  python3 run.py              # 每日内容生成
  python3 run.py status       # 查看系统状态
  python3 run.py publish      # 记录发布（互动式）
  python3 run.py plan         # 生成内容计划
"""

import sys
from engine.pipeline import AffiliatePipeline
from engine.keyword_research import KeywordResearch
from engine.tracker import Tracker


def cmd_daily():
    """Daily content generation."""
    pipeline = AffiliatePipeline()
    pipeline.daily_run()


def cmd_status():
    """System status overview."""
    pipeline = AffiliatePipeline()
    pipeline.check_status()


def cmd_plan():
    """Generate content plan from products."""
    pipeline = AffiliatePipeline()
    products = pipeline.load_products()
    if not products:
        return

    print("=" * 56)
    print("  内容计划")
    print("=" * 56)
    print()

    plans = KeywordResearch.plan_content_batch(products, count_per_product=4)
    print(f"  共 {len(plans)} 个内容任务\n")

    current_product = ""
    for p in plans:
        if p["product"] != current_product:
            current_product = p["product"]
            print(f"\n  [{current_product}]")
        print(f"    - {p['keyword']}")
        print(f"      平台: {', '.join(p['recommended_platforms'])} | 意图: {p['intent']}")

    print()
    print(f"  运行 python3 run.py 开始生成内容")


def cmd_publish():
    """Record a publishing event interactively."""
    tracker = Tracker()
    pipeline = AffiliatePipeline()
    products = pipeline.load_products()

    print("=" * 56)
    print("  记录发布")
    print("=" * 56)
    print()

    # Show recent generated content
    stats = tracker.get_stats()
    print(f"  待发布内容: {stats['total_content'] - stats['total_published']} 篇")
    print(f"  已发布: {stats['total_published']} 篇")
    print()

    # Check if we can read from input (non-interactive mode)
    if not sys.stdin.isatty():
        # Batch mode: read from stdin, each line: product,platform,url
        for line in sys.stdin:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) >= 3:
                tracker.log_publish(0, parts[1], parts[2], notes=parts[0])
                print(f"  [OK] 已记录: {parts[0]} -> {parts[1]}")
        return

    # Interactive mode
    print("  记录发布 (Ctrl+C 退出):")
    try:
        while True:
            product = input("  产品名 > ").strip()
            platform = input("  平台 > ").strip()
            url = input("  URL > ").strip()
            if product and platform:
                tracker.log_publish(0, platform, url, notes=product)
                print(f"  [OK] 已记录\n")
    except (EOFError, KeyboardInterrupt):
        print("\n  [DONE]")


def cmd_menu():
    """Interactive menu mode."""
    while True:
        print()
        print("=" * 48)
        print("  AI Affiliate")
        print("=" * 48)
        print("  1. 每日内容生成")
        print("  2. 查看系统状态")
        print("  3. 生成内容计划")
        print("  4. 记录发布")
        print("  5. 退出")
        print()

        try:
            choice = input("  选一个 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        print()
        if choice == "1":
            cmd_daily()
        elif choice == "2":
            cmd_status()
        elif choice == "3":
            cmd_plan()
        elif choice == "4":
            cmd_publish()
        elif choice in ("5", "q", "quit", "exit"):
            print("  Bye")
            break
        else:
            print("  输入 1-5")

        input("\n  按回车继续...")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "menu"

    commands = {
        "daily": cmd_daily,
        "status": cmd_status,
        "plan": cmd_plan,
        "publish": cmd_publish,
        "menu": cmd_menu,
    }

    action = commands.get(cmd)
    if action:
        action()
    else:
        print("用法:")
        print("  python3 run.py           # 交互菜单")
        print("  python3 run.py daily     # 直接生成")
        print("  python3 run.py status    # 系统状态")
        print("  python3 run.py plan      # 内容计划")
        print("  python3 run.py publish   # 记录发布")


if __name__ == "__main__":
    main()
