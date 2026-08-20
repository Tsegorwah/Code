import os
import sys
import re
import argparse
from collections import defaultdict
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stock_code_extractor
import pdf_stock_scheduler

DOWNLOAD_DIR = pdf_stock_scheduler.DOWNLOAD_DIR
RESULT_DIR = pdf_stock_scheduler.RESULT_DIR

DATE_PREFIX_RE = re.compile(r'^(\d{8})_')


def show_banner():
    print("=" * 70)
    print("  PDF股票代码提取工具 - 按月份汇总统计")
    print("=" * 70)
    print()


def parse_month(month_str):
    """校验并规范化月份输入，返回 YYYYMM 格式"""
    s = month_str.replace('-', '').replace('/', '')
    if len(s) != 6 or not s.isdigit():
        return None
    year, month = int(s[:4]), int(s[4:])
    if year < 1900 or year > 9999 or month < 1 or month > 12:
        return None
    return s


def list_available_months(download_dir):
    """扫描 pdf_files 目录，返回可用的月份集合 (YYYYMM)"""
    months = set()
    if not os.path.exists(download_dir):
        return months
    for fname in os.listdir(download_dir):
        if not fname.lower().endswith('.pdf'):
            continue
        m = DATE_PREFIX_RE.match(fname)
        if m:
            months.add(m.group(1)[:6])
    return months


def get_pdfs_in_month(month_str, download_dir):
    """获取指定月份的所有 PDF，列表元素为 (date_str, filename)"""
    pdfs = []
    if not os.path.exists(download_dir):
        return pdfs
    for fname in os.listdir(download_dir):
        if not fname.lower().endswith('.pdf'):
            continue
        m = DATE_PREFIX_RE.match(fname)
        if not m:
            continue
        date_str = m.group(1)
        if date_str.startswith(month_str):
            pdfs.append((date_str, fname))
    pdfs.sort(key=lambda x: (x[0], x[1]))
    return pdfs


def read_cached_result(date_str, result_dir):
    """尝试从 result_files 读取已缓存的 (filename -> {code:name}) 结果"""
    result = {}
    path = os.path.join(result_dir, f"stock_codes_{date_str}.txt")
    if not os.path.exists(path):
        return result, False

    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_source = None
        current_stocks = {}
        in_section = False

        for line in lines:
            line = line.rstrip('\n')
            if '来源文件:' in line:
                if current_source and current_stocks:
                    result[current_source] = current_stocks.copy()
                idx = line.find('来源文件:')
                current_source = line[idx + len('来源文件:'):].strip()
                current_stocks = {}
                in_section = True
            elif in_section and ('小计:' in line or '汇总统计' in line or
                                 line.strip().startswith('=====')):
                if current_source and current_stocks:
                    result[current_source] = current_stocks.copy()
                current_source = None
                current_stocks = {}
                in_section = False
            elif in_section and line.strip() and \
                    not line.strip().startswith('---') and \
                    not line.strip().startswith('==='):
                parts = line.strip().split(None, 1)
                if len(parts) >= 2:
                    code = parts[0]
                    name = parts[1]
                    if code in stock_code_extractor.CODE_TO_NAME:
                        current_stocks[code] = name

        if current_source and current_stocks:
            result[current_source] = current_stocks.copy()
        return result, True
    except Exception as e:
        print(f"⚠ 读取缓存文件失败 {path}: {e}")
        return {}, False


def analyze_month(month_str, download_dir, result_dir, use_cache=True):
    """
    分析指定月份的所有 PDF，返回:
      stock_data: {code: {'name': str, 'count': int,
                  'details': {date_str: [filenames]}}}
      pdfs: [(date_str, filename), ...]
      pdfs_by_date: {date_str: [filenames]}
      cached_dates: set
    """
    pdfs = get_pdfs_in_month(month_str, download_dir)
    pdfs_by_date = defaultdict(list)
    for date_str, fname in pdfs:
        pdfs_by_date[date_str].append(fname)

    stock_data = {}
    cached_dates = set()

    for date_str in sorted(pdfs_by_date.keys()):
        date_stocks = None

        if use_cache:
            cached, ok = read_cached_result(date_str, result_dir)
            if ok:
                date_stocks = cached
                cached_dates.add(date_str)

        if date_stocks is None:
            print(f"  → 解析 {date_str} 的 {len(pdfs_by_date[date_str])} 个 PDF...")
            date_stocks = {}
            for fname in pdfs_by_date[date_str]:
                pdf_path = os.path.join(download_dir, fname)
                codes, _ = stock_code_extractor.extract_stock_codes_with_source(pdf_path)
                if codes:
                    date_stocks[fname] = codes

        # 聚合
        for fname, codes in date_stocks.items():
            for code, name in codes.items():
                if code not in stock_data:
                    stock_data[code] = {
                        'name': name,
                        'count': 0,
                        'details': defaultdict(list)
                    }
                stock_data[code]['count'] += 1
                stock_data[code]['details'][date_str].append(fname)

    return stock_data, pdfs, pdfs_by_date, cached_dates


def format_date(date_str):
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"


def generate_report(stock_data, pdfs, pdfs_by_date, cached_dates, month_str):
    """生成可读报告（也是保存到文件的内容）"""
    total_pdfs = len(pdfs)
    total_dates = len(pdfs_by_date)
    total_stocks = len(stock_data)

    lines = []
    lines.append(f"月份股票代码汇总")
    lines.append(f"月份: {month_str[:4]}-{month_str[4:6]}")
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("=" * 70)
    lines.append("汇总统计")
    lines.append("=" * 70)
    lines.append(f"涉及日期数: {total_dates}")
    lines.append(f"涉及 PDF 文件数: {total_pdfs}")
    lines.append(f"股票代码总数（去重）: {total_stocks}")
    if cached_dates:
        lines.append(f"使用缓存的日期: {len(cached_dates)} 个 "
                     f"({', '.join(sorted(cached_dates))})")
    lines.append("")

    # 按提及次数降序排序
    sorted_stocks = sorted(
        stock_data.items(),
        key=lambda kv: (-kv[1]['count'], kv[0])
    )

    lines.append("=" * 70)
    lines.append(f"股票提及次数排行（共 {total_stocks} 只）")
    lines.append("=" * 70)
    lines.append(f"{'排名':<6}{'代码':<10}{'名称':<14}{'次数':<6}涉及天数")
    lines.append("-" * 70)
    for i, (code, info) in enumerate(sorted_stocks, 1):
        days = len(info['details'])
        lines.append(f"{i:<6}{code:<10}{info['name']:<14}{info['count']:<6}{days}")
    lines.append("")

    lines.append("=" * 70)
    lines.append("每只股票的提及明细（按日期 -> PDF）")
    lines.append("=" * 70)
    for code, info in sorted_stocks:
        lines.append("")
        lines.append(f"📈 {code} {info['name']}  ——  共 {info['count']} 次, "
                     f"涉及 {len(info['details'])} 天")
        for date_str in sorted(info['details'].keys()):
            files = info['details'][date_str]
            lines.append(f"  📅 {format_date(date_str)}  ({len(files)} 篇)")
            for f in files:
                lines.append(f"     - {f}")
    lines.append("")
    return "\n".join(lines)


def display_console_summary(stock_data, pdfs_by_date, month_str):
    """在控制台打印简明摘要"""
    total_pdfs = sum(len(v) for v in pdfs_by_date.values())
    total_stocks = len(stock_data)
    print()
    print("=" * 70)
    print(f"📊  {month_str[:4]}-{month_str[4:6]}  月度汇总")
    print("=" * 70)
    print(f"  涉及日期: {len(pdfs_by_date)} 天")
    print(f"  涉及 PDF: {total_pdfs} 个")
    print(f"  股票总数(去重): {total_stocks}")
    print()

    sorted_stocks = sorted(
        stock_data.items(),
        key=lambda kv: (-kv[1]['count'], kv[0])
    )
    top = sorted_stocks[:20]
    print(f"🔥 Top 20 高频提及股票：")
    print("-" * 70)
    print(f"{'排名':<6}{'代码':<10}{'名称':<14}{'次数':<6}涉及天数")
    print("-" * 70)
    for i, (code, info) in enumerate(top, 1):
        days = len(info['details'])
        print(f"{i:<6}{code:<10}{info['name']:<14}{info['count']:<6}{days}")
    if len(sorted_stocks) > 20:
        print(f"  ... 另有 {len(sorted_stocks) - 20} 只股票，详见输出文件")
    print("-" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='按月份汇总统计所有 PDF 中提到的股票代码')
    parser.add_argument('month', nargs='?',
                        help='月份 (格式: YYYYMM 或 YYYY-MM，例如: 202605)')
    parser.add_argument('--list', '-l', action='store_true',
                        help='显示所有可用的月份并退出')
    parser.add_argument('--no-cache', action='store_true',
                        help='不使用 result_files 缓存，重新解析 PDF')
    parser.add_argument('--output', '-o', default=None,
                        help='指定报告输出文件路径')
    args = parser.parse_args()

    show_banner()

    months = list_available_months(DOWNLOAD_DIR)
    if not months:
        print(f"❌ 目录 {DOWNLOAD_DIR} 中没有找到带日期前缀的 PDF 文件")
        sys.exit(1)

    if args.list:
        print("可用的月份：")
        print("-" * 40)
        for m in sorted(months, reverse=True):
            print(f"  {m[:4]}-{m[4:]}")
        print("-" * 40)
        sys.exit(0)

    if not args.month:
        print("可用的月份：")
        print("-" * 40)
        for m in sorted(months, reverse=True):
            print(f"  {m[:4]}-{m[4:]}")
        print("-" * 40)
        print()
        print(f"使用方法:")
        print(f"  python {os.path.basename(__file__)} 202605")
        print(f"  python {os.path.basename(__file__)} --list")
        print(f"  python {os.path.basename(__file__)} 202605 --no-cache")
        print(f"\n请提供月份参数（格式: YYYYMM）")
        sys.exit(1)

    month_str = parse_month(args.month)
    if not month_str:
        print(f"❌ 月份格式错误，请使用 YYYYMM 格式，例如: 202605")
        sys.exit(1)

    if month_str not in months:
        print(f"❌ 月份 {month_str[:4]}-{month_str[4:]} 没有可用的 PDF")
        print(f"   可用月份: {', '.join(sorted(months, reverse=True))}")
        sys.exit(1)

    print(f"📅 选定月份: {month_str[:4]}-{month_str[4:]}")
    if args.no_cache:
        print("🔄 模式: 重新解析 PDF（不使用缓存）")
    else:
        print("⚡ 模式: 优先使用 result_files 缓存")
    print(f"📂 扫描目录: {os.path.abspath(DOWNLOAD_DIR)}")
    print()

    stock_data, pdfs, pdfs_by_date, cached_dates = analyze_month(
        month_str, DOWNLOAD_DIR, RESULT_DIR,
        use_cache=not args.no_cache
    )

    if not stock_data:
        print("⚠ 未提取到任何股票代码")
        sys.exit(0)

    display_console_summary(stock_data, pdfs_by_date, month_str)

    if not args.output:
        if not os.path.exists(RESULT_DIR):
            os.makedirs(RESULT_DIR)
        args.output = os.path.join(RESULT_DIR, f"monthly_summary_{month_str}.txt")
    report = generate_report(
        stock_data, pdfs, pdfs_by_date, cached_dates, month_str
    )
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)

    print()
    print(f"📋 详细报告已保存到: {os.path.abspath(args.output)}")
    print(f"   - 包含每只股票的具体提及日期和来源 PDF")
    print(f"   - 包含按提及次数排序的完整排行榜")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
