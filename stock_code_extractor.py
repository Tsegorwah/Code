import os
import re
import sys
from datetime import datetime
import PyPDF2

TDX_FILE = "tdx.txt"

def load_stocks_from_tdx(tdx_file_path):
    stocks = {}
    if not os.path.exists(tdx_file_path):
        print(f"警告: {tdx_file_path} 文件不存在")
        return stocks
    with open(tdx_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                code = parts[0].strip()
                name = parts[1].strip()
                if code and name:
                    stocks[code] = name
    print(f"从 {tdx_file_path} 加载了 {len(stocks)} 只股票")
    return stocks

MAIN_BOARD_STOCKS = load_stocks_from_tdx(TDX_FILE)
CODE_TO_NAME = {code: name for code, name in MAIN_BOARD_STOCKS.items()}
NAME_TO_CODES = {}
for code, name in MAIN_BOARD_STOCKS.items():
    if name not in NAME_TO_CODES:
        NAME_TO_CODES[name] = []
    NAME_TO_CODES[name].append(code)

def extract_stock_codes_with_source(pdf_path):
    """从PDF文件中提取股票代码，返回 (股票代码字典, 来源文件名)"""
    stock_codes_found = {}
    source_filename = os.path.basename(pdf_path)

    try:
        print(f"开始解析 PDF 文件: {pdf_path}")
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            print(f"PDF 文件共有 {len(reader.pages)} 页")

            all_text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                all_text += text + "\n"

            # 1. 精确匹配股票代码 (所有A股代码)
            # 上海主板: 600xxx, 601xxx, 603xxx, 605xxx
            # 深圳主板: 000xxx, 001xxx
            # 深圳中小板: 002xxx, 003xxx
            # 深圳创业板: 300xxx, 301xxx
            code_pattern = r'(60[0-59]\d{4}|00[0-39]\d{4}|30[0-19]\d{4})'
            code_matches = re.findall(code_pattern, all_text)
            for code in code_matches:
                if code in CODE_TO_NAME:
                    stock_codes_found[code] = CODE_TO_NAME[code]

            # 2. 通过股票名称匹配（更精确）
            for code, name in CODE_TO_NAME.items():
                if name in all_text and len(name) >= 2:
                    stock_codes_found[code] = name

            # 3. 尝试匹配 "代码: xxxxxx" 等格式
            explicit_pattern = r'(?:股票代码|代码|代码：|股票)\s*[:：]?\s*([6003]\d{5})'
            explicit_matches = re.findall(explicit_pattern, all_text)
            for code in explicit_matches:
                if code in CODE_TO_NAME:
                    stock_codes_found[code] = CODE_TO_NAME[code]

            print(f"从 {source_filename} 找到 {len(stock_codes_found)} 个股票代码")

    except Exception as e:
        print(f"解析PDF失败 {pdf_path}: {e}")
        import traceback
        traceback.print_exc()

    return stock_codes_found, source_filename

def extract_stock_codes(pdf_path):
    """兼容旧接口"""
    stock_codes, _ = extract_stock_codes_with_source(pdf_path)
    return stock_codes

def generate_grouped_report(all_results, date_str):
    """生成按来源文件分组的报告"""
    report = f"股票代码汇总\n"
    report += f"日期: {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}\n"
    report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    # 统计
    total_files = len(all_results)
    total_stocks = 0

    # 按来源文件分组
    report += f"\n{'='*70}\n"
    report += f"按来源文件分组的股票代码\n"
    report += f"{'='*70}\n\n"

    for source_filename, stock_codes in all_results:
        if not stock_codes:
            continue

        report += f"📄 来源文件: {source_filename}\n"
        report += f"{'-'*70}\n"

        sorted_codes = sorted(stock_codes.keys())
        for code, name in sorted(stock_codes.items()):
            report += f"  {code} {name}\n"

        report += f"  小计: {len(stock_codes)} 只\n\n"
        total_stocks += len(stock_codes)

    # 汇总
    report += f"{'='*70}\n"
    report += f"汇总统计\n"
    report += f"{'='*70}\n"
    report += f"处理文件数: {total_files}\n"
    report += f"股票代码总数: {total_stocks}\n\n"

    # 所有股票代码列表（去重）
    all_codes = {}
    for source_filename, stock_codes in all_results:
        all_codes.update(stock_codes)

    if all_codes:
        report += f"{'='*70}\n"
        report += f"全部股票代码（去重）\n"
        report += f"{'='*70}\n"
        sorted_codes = sorted(all_codes.keys())
        for code, name in sorted(all_codes.items()):
            report += f"{code} {name}\n"

        report += f"\n去重后总数: {len(all_codes)}\n"

    return report

def summarize_stock_codes(stock_codes_dict, date_str, source_files=None):
    """兼容旧接口"""
    if not stock_codes_dict:
        return "没有找到股票代码"

    sorted_codes = sorted(stock_codes_dict.keys())
    report = f"股票代码汇总\n"
    report += f"日期: {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}\n"
    report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    if source_files:
        report += f"来源文件: {', '.join(source_files)}\n"
    report += f"总数量: {len(sorted_codes)}\n\n"

    for code, name in sorted(stock_codes_dict.items()):
        report += f"{code} {name}\n"
    return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python stock_code_extractor.py <pdf文件路径>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    stock_codes = extract_stock_codes(pdf_path)

    print(f"\n提取到 {len(stock_codes)} 个股票代码:")
    for code, name in sorted(stock_codes.items()):
        print(f"  {code} {name}")
