# -*- coding: utf-8 -*-
"""
月度工作流脚本（可重复使用）

用法:
    python run_monthly_workflow.py            # 默认当前月份
    python run_monthly_workflow.py 202608     # 指定月份 YYYYMM

流程:
    1. 依次对本月所有工作日(周一~周五, 截至今天)执行:
       python interactive_stock_extractor.py YYYYMMDD
    2. 最后执行月度汇总:
       python monthly_stock_analyzer.py YYYYMM
"""
import os
import sys
import argparse
from datetime import date, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXTRACTOR = os.path.join(SCRIPT_DIR, "interactive_stock_extractor.py")
ANALYZER = os.path.join(SCRIPT_DIR, "monthly_stock_analyzer.py")


def parse_month(s):
    s = s.replace('-', '').replace('/', '')
    if len(s) != 6 or not s.isdigit():
        return None
    year, month = int(s[:4]), int(s[4:])
    if month < 1 or month > 12:
        return None
    return year, month


def month_end(year, month):
    if month == 12:
        return date(year, 12, 31)
    return date(year, month + 1, 1) - timedelta(days=1)


def get_workdays(year, month, up_to=None):
    """获取指定月份的工作日(周一~周五)列表，可限制到 up_to 日期(含)"""
    end = month_end(year, month) if up_to is None else min(month_end(year, month), up_to)
    workdays = []
    d = date(year, month, 1)
    while d <= end:
        if d.weekday() < 5:
            workdays.append(d)
        d += timedelta(days=1)
    return workdays


def run(script, arg):
    print(f"\n>>> python {os.path.basename(script)} {arg}")
    print("-" * 70)
    ret = os.system(f'"{sys.executable}" "{script}" {arg}')
    return ret == 0


def main():
    parser = argparse.ArgumentParser(description='月度股票提取工作流')
    parser.add_argument('month', nargs='?', help='月份 (格式: YYYYMM，默认当前月份)')
    args = parser.parse_args()

    today = date.today()
    if args.month:
        parsed = parse_month(args.month)
        if not parsed:
            print("❌ 月份格式错误，请使用 YYYYMM 格式，例如: 202608")
            sys.exit(1)
        year, month = parsed
    else:
        year, month = today.year, today.month
    month_str = f"{year}{month:02d}"

    # 当前月份只跑截至今天的工作日；过去月份跑整月
    up_to = today if (year, month) == (today.year, today.month) else None
    if year > today.year or (year == today.year and month > today.month):
        print(f"❌ 月份 {month_str} 是未来月份，暂无数据")
        sys.exit(1)

    workdays = get_workdays(year, month, up_to=up_to)

    print("=" * 70)
    print(f"  月度工作流: {month_str[:4]}-{month_str[4:6]}")
    print(f"  工作日数量: {len(workdays)}" + (f" (截至 {today})" if up_to else " (整月)"))
    print("=" * 70)

    if not workdays:
        print("⚠ 本月没有可执行的工作日")

    # 第一步: 逐个工作日提取
    failed = []
    for i, d in enumerate(workdays, 1):
        date_str = d.strftime("%Y%m%d")
        print(f"\n########## [{i}/{len(workdays)}] 日期 {date_str} ##########")
        if not run(EXTRACTOR, date_str):
            failed.append(date_str)

    # 第二步: 月度汇总
    print(f"\n########## 月度汇总 {month_str} ##########")
    summary_ok = run(ANALYZER, month_str)

    # 结果
    print("\n" + "=" * 70)
    if failed:
        print(f"⚠ 以下 {len(failed)} 个日期执行失败: {', '.join(failed)}")
    else:
        print("✓ 所有工作日提取完成")
    print("✓ 月度汇总完成" if summary_ok else "⚠ 月度汇总执行失败")
    print("=" * 70)

    if failed or not summary_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
