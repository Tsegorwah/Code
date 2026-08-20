import os
import sys
import argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdf_stock_scheduler
import stock_code_extractor
from collections import defaultdict

def show_banner():
    print("=" * 70)
    print("  PDF股票代码提取工具 - 按日期选择下载")
    print("=" * 70)
    print()

def get_all_dates(pdf_links):
    """获取所有可用的日期及其PDF数量"""
    dates_count = defaultdict(int)
    dates_pdfs = defaultdict(list)

    for pdf in pdf_links:
        date_str = pdf_stock_scheduler.parse_date_to_str(pdf['date'])
        if date_str:
            dates_count[date_str] += 1
            dates_pdfs[date_str].append(pdf)

    return dates_count, dates_pdfs

def display_dates(dates_count):
    """显示所有可用日期"""
    print("\n可用的日期选项：")
    print("-" * 70)

    sorted_dates = sorted(dates_count.keys(), reverse=True)

    for i, date_str in enumerate(sorted_dates, 1):
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        count = dates_count[date_str]
        print(f"  {i:2d}. {formatted_date}  ({count}个PDF文件)")

    print("-" * 70)
    return sorted_dates

def read_existing_results(output_filename):
    """读取已有的结果文件，返回一个字典，key是来源文件名，value是股票代码字典"""
    existing_results = {}
    
    if not os.path.exists(output_filename):
        return existing_results
    
    try:
        with open(output_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_source = None
        current_stocks = {}
        in_stock_section = False
        
        for line in lines:
            line = line.rstrip('\n')
            
            # 检测新的来源文件部分
            if '来源文件:' in line:
                # 保存上一个来源的结果
                if current_source and current_stocks:
                    existing_results[current_source] = current_stocks.copy()
                
                # 提取文件名
                idx = line.find('来源文件:')
                filename_part = line[idx + len('来源文件:'):].strip()
                current_source = filename_part
                current_stocks = {}
                in_stock_section = True
            # 检测小计行或其他分隔符，表示该来源结束
            elif in_stock_section and ('小计:' in line or '--------' in line or 
                                       '=====' in line or '汇总统计' in line):
                if current_source and current_stocks:
                    existing_results[current_source] = current_stocks.copy()
                current_source = None
                current_stocks = {}
                in_stock_section = False
            # 提取股票代码（跳过只包含分隔符的行）
            elif in_stock_section and line.strip() and not line.strip().startswith('---') and not line.strip().startswith('==='):
                parts = line.strip().split(None, 1)
                if len(parts) >= 2:
                    code = parts[0]
                    name = parts[1]
                    # 验证代码是否有效
                    if code in stock_code_extractor.CODE_TO_NAME:
                        current_stocks[code] = name
        
        # 保存最后一个来源的结果
        if current_source and current_stocks:
            existing_results[current_source] = current_stocks.copy()
        
    except Exception as e:
        print(f"⚠ 读取已有结果文件时出错: {e}")
    
    return existing_results

def download_and_process(date_str, pdfs, existing_pdfs):
    """下载指定日期的PDF并提取股票代码"""
    print(f"\n{'='*70}")
    print(f"开始处理 {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} 的PDF文件")
    print(f"{'='*70}")

    # 先处理所有PDF，不管新旧
    test_pdfs = pdfs.copy()

    # 下载并处理PDF
    pdf_stock_scheduler.ensure_directory(pdf_stock_scheduler.DOWNLOAD_DIR)

    new_results = []  # 存储新的 (来源文件, 股票代码字典, 原始日期) 的元组
    processed_files = []

    for i, pdf_info in enumerate(test_pdfs, 1):
        filename = pdf_stock_scheduler.get_pdf_filename_with_date(pdf_info['name'], date_str)
        pdf_info['filename_with_date'] = filename
        save_path = os.path.join(pdf_stock_scheduler.DOWNLOAD_DIR, filename)

        print(f"\n[{i}/{len(test_pdfs)}] {filename}")

        # 如果文件不存在，则下载
        if not os.path.exists(save_path):
            print(f"  ↓ 正在下载...")
            if not pdf_stock_scheduler.download_pdf(pdf_info['url'], save_path):
                print(f"  ✗ 下载失败，跳过")
                continue
        else:
            print(f"  ✓ 文件已存在，跳过下载")

        # 提取股票代码
        print(f"  → 正在提取股票代码...")
        stock_codes, source_filename = stock_code_extractor.extract_stock_codes_with_source(save_path)

        # 保存原始日期信息
        original_date = pdf_info['date']
        
        if stock_codes:
            new_results.append((source_filename, stock_codes, original_date))
            print(f"  ✓ 提取到 {len(stock_codes)} 个股票代码")
        else:
            print(f"  - 未找到股票代码")
            # 即使没找到，也记录下来以保持连续性
            new_results.append((source_filename, {}, original_date))

        processed_files.append(filename)

    return new_results, processed_files

def merge_and_save_results(date_str, new_results):
    """合并新结果与已有的结果，并保存"""
    result_dir = "result_files"
    # 确保结果目录存在
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    output_filename = os.path.join(result_dir, f"stock_codes_{date_str}.txt")
    
    # 先读取已有的结果
    existing_results = read_existing_results(output_filename)
    
    # 合并：新结果覆盖旧结果（按文件名）
    # 把new_results转换为字典格式，并保存日期信息
    new_results_dict = {}
    filename_to_date = {}
    
    for item in new_results:
        if len(item) == 3:
            filename, stock_codes, original_date = item
            new_results_dict[filename] = stock_codes.copy()
            filename_to_date[filename] = original_date
        else:
            # 兼容旧格式
            filename, stock_codes = item
            new_results_dict[filename] = stock_codes.copy()
    
    # 合并
    merged_dict = existing_results.copy()
    merged_dict.update(new_results_dict)  # 新结果覆盖旧结果
    
    # 转换回列表格式，并按网站上的原始日期排序（最新的在前）
    merged_results = []
    for filename, stock_codes in merged_dict.items():
        # 获取日期信息
        original_date = filename_to_date.get(filename, "")
        merged_results.append((filename, stock_codes, original_date))
    
    # 按原始日期排序（最新的在前）
    # 先按日期排序，再按文件名排序
    def get_date_sort_key(item):
        original_date = item[2]
        # 转换日期格式为可排序的格式
        if original_date:
            # 日期格式为 "2026/4/22 14:26:59"
            parts = original_date.split(' ')
            if len(parts) >= 1:
                date_part = parts[0]
                time_part = parts[1] if len(parts) >= 2 else "00:00:00"
                
                # 处理日期部分
                date_parts = date_part.split('/')
                if len(date_parts) == 3:
                    year = date_parts[0]
                    month = date_parts[1].zfill(2)
                    day = date_parts[2].zfill(2)
                    
                    # 处理时间部分
                    time_parts = time_part.split(':')
                    hour = time_parts[0].zfill(2) if len(time_parts) >= 1 else "00"
                    minute = time_parts[1].zfill(2) if len(time_parts) >= 2 else "00"
                    second = time_parts[2].zfill(2) if len(time_parts) >= 3 else "00"
                    
                    # 格式化为 YYYYMMDDHHMMSS
                    return f"{year}{month}{day}{hour}{minute}{second}"
        # 如果没有日期，使用文件名作为备份
        return item[0]
    
    # 反转顺序，让最新的日期在前面
    merged_results.sort(key=get_date_sort_key, reverse=True)
    
    # 转换为 stock_code_extractor 期望的格式
    report_results = [(filename, stock_codes) for filename, stock_codes, original_date in merged_results]
    
    # 生成报告
    report = stock_code_extractor.generate_grouped_report(report_results, date_str)
    
    # 保存
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 计算统计信息
    total_files = len(merged_results)
    all_codes = {}
    for item in merged_results:
        if len(item) == 3:
            source_file, stock_codes, original_date = item
        else:
            source_file, stock_codes = item
        all_codes.update(stock_codes)
    
    return output_filename, total_files, len(all_codes)

def main():
    parser = argparse.ArgumentParser(description='PDF股票代码提取工具')
    parser.add_argument('date', nargs='?', help='日期 (格式: YYYYMMDD，例如: 20260421)')
    parser.add_argument('--list', '-l', action='store_true', help='显示所有可用日期')
    args = parser.parse_args()

    show_banner()

    # 获取PDF列表
    print("正在获取PDF列表...")
    html_content = pdf_stock_scheduler.fetch_pdf_list()

    if not html_content:
        print("❌ 无法获取PDF列表")
        sys.exit(1)

    pdf_links = pdf_stock_scheduler.parse_pdf_links(html_content)
    print(f"✓ 获取到 {len(pdf_links)} 个PDF文件\n")

    # 获取所有日期
    dates_count, dates_pdfs = get_all_dates(pdf_links)

    if not dates_count:
        print("❌ 未找到任何日期信息")
        sys.exit(1)

    sorted_dates = sorted(dates_count.keys(), reverse=True)

    # 如果使用 --list 参数，显示所有日期并退出
    if args.list:
        display_dates(dates_count)
        sys.exit(0)

    # 如果没有提供日期，显示选择菜单
    if not args.date:
        display_dates(dates_count)

        print(f"\n使用方法:")
        print(f"  python {os.path.basename(__file__)} 20260421")
        print(f"  python {os.path.basename(__file__)} --list")
        print(f"\n请提供日期参数（格式: YYYYMMDD）")
        sys.exit(1)

    # 验证日期格式
    selected_date = args.date.replace('-', '').replace('/', '')

    if len(selected_date) != 8 or not selected_date.isdigit():
        print(f"❌ 日期格式错误，请使用 YYYYMMDD 格式，例如: 20260421")
        sys.exit(1)

    if selected_date not in dates_count:
        print(f"⚠ 日期 {selected_date} 没有可用的PDF文件，尝试使用上一天的日期...")
        from datetime import datetime, timedelta
        try:
            current_dt = datetime.strptime(selected_date, "%Y%m%d")
            for days_back in range(1, 30):
                prev_dt = current_dt - timedelta(days=days_back)
                prev_date = prev_dt.strftime("%Y%m%d")
                if prev_date in dates_count:
                    selected_date = prev_date
                    print(f"✓ 使用上一天日期: {selected_date[:4]}-{selected_date[4:6]}-{selected_date[6:8]}")
                    break
            else:
                print(f"❌ 在最近30天内未找到可用的PDF文件")
                print(f"\n可用的日期范围: {sorted_dates[-1][:4]}-{sorted_dates[-1][4:6]}-{sorted_dates[-1][6:8]} 到 {sorted_dates[0][:4]}-{sorted_dates[0][4:6]}-{sorted_dates[0][6:8]}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ 日期处理失败: {e}")
            print(f"\n可用的日期范围: {sorted_dates[-1][:4]}-{sorted_dates[-1][4:6]}-{sorted_dates[-1][6:8]} 到 {sorted_dates[0][:4]}-{sorted_dates[0][4:6]}-{sorted_dates[0][6:8]}")
            sys.exit(1)

    print(f"\n✓ 已选择: {selected_date[:4]}-{selected_date[4:6]}-{selected_date[6:8]}")

    # 获取已下载文件
    existing_pdfs = pdf_stock_scheduler.get_existing_pdfs()

    # 下载并处理
    new_results, processed_files = download_and_process(selected_date, dates_pdfs[selected_date], existing_pdfs)

    if new_results is None:
        print("\n❌ 处理失败")
        sys.exit(1)

    # 合并并保存结果
    output_file, total_files, unique_stocks = merge_and_save_results(selected_date, new_results)

    print(f"\n{'='*70}")
    print(f"✅ 处理完成！")
    print(f"{'='*70}")
    print(f"\n📊 结果汇总：")
    print(f"  • 处理文件数: {total_files}")
    print(f"  • 股票代码总数（去重）: {unique_stocks}")
    print(f"  • 输出文件: {output_file}")

    print(f"\n📋 详细结果已保存到: {output_file}")
    print(f"   文件中包含每个PDF来源及其对应的股票代码，已有数据已保留！")

    print(f"\n{'='*70}")

if __name__ == "__main__":
    main()
