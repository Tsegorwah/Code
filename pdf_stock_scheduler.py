import os
import re
import time
import sys
import requests
import schedule
from datetime import datetime
from bs4 import BeautifulSoup
import PyPDF2
from collections import defaultdict
from urllib.parse import quote, urljoin, urlparse

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOWNLOAD_DIR = "pdf_files"
RESULT_DIR = "result_files"
OUTPUT_FILE = "stock_codes_summary.txt"
TDX_FILE = "tdx.txt"
LIST_URL = "http://zc.juecan.com/nc/zhong-cai/cl-zzd_PDF/list2.asp"
BASE_URL = "http://zc.juecan.com/nc/zhong-cai/cl-zzd_PDF/"

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

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def fetch_pdf_list():
    try:
        print(f"获取PDF列表页面: {LIST_URL}")
        response = requests.get(LIST_URL, timeout=60)
        response.encoding = 'gbk'
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"获取PDF列表失败: {e}")
        return None

def fix_pdf_url(url):
    """修复PDF URL的编码问题，尝试多种编码方式"""
    try:
        parsed = urlparse(url)
        
        # 获取路径并尝试不同的编码
        path = parsed.path
        
        # 尝试1: 使用完整的quote编码
        try:
            encoded_path = quote(path, safe='/:')
            test_url = f"{parsed.scheme}://{parsed.netloc}{encoded_path}"
            response = requests.head(test_url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                return test_url
        except:
            pass
        
        # 尝试2: 保留更多特殊字符
        try:
            encoded_path = quote(path, safe='/:@!$&\'()*+,;=')
            test_url = f"{parsed.scheme}://{parsed.netloc}{encoded_path}"
            response = requests.head(test_url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                return test_url
        except:
            pass
        
        # 尝试3: 替换问号为全角句号
        if '?' in path:
            path_fixed = path.replace('?', '\uff0e')
            encoded_path = quote(path_fixed, safe='/:')
            test_url = f"{parsed.scheme}://{parsed.netloc}{encoded_path}"
            response = requests.head(test_url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                return test_url
        
        # 如果都失败，返回原始URL
        return url
        
    except Exception as e:
        print(f"修复URL编码失败: {e}")
        return url

def parse_pdf_links(html_content):
    pdf_links = []
    if not html_content:
        return pdf_links
    soup = BeautifulSoup(html_content, 'html.parser')
    for file_item in soup.find_all('li', class_='file-item'):
        link = file_item.find('a', class_='file-link', href=True)
        if link and '.pdf' in link['href'].lower():
            href = link['href']
            href = href.replace('\u003f', '\u30fb')
            if href.startswith('http'):
                full_url = href
            else:
                encoded_href = quote(href, safe='/')
                full_url = urljoin(BASE_URL, encoded_href)
            name = link.get_text(strip=True) or os.path.basename(href)
            date_text = None
            date_span = file_item.find('span', class_='modify-date')
            if date_span:
                date_text = date_span.get_text(strip=True)
                if date_text.startswith('日期: '):
                    date_text = date_text[4:]
            pdf_links.append({
                'url': full_url,
                'name': name,
                'date': date_text
            })
    return pdf_links

def parse_date_to_str(date_text):
    """将日期文本转换为 'YYYYMMDD' 格式的字符串"""
    if not date_text:
        return None
    date_parts = date_text.split()[0].split('/')
    if len(date_parts) == 3:
        year = date_parts[0]
        month = date_parts[1].zfill(2)
        day = date_parts[2].zfill(2)
        return f"{year}{month}{day}"
    return None

def download_pdf(url, save_path, max_retries=3):
    """下载PDF文件，尝试修复URL编码问题"""
    for attempt in range(max_retries):
        try:
            print(f"开始下载 PDF 文件: {url}")
            
            # 如果不是第一次尝试，尝试修复URL
            if attempt > 0:
                print(f"尝试修复URL编码 (第{attempt}次重试)...")
                url = fix_pdf_url(url)
                print(f"修复后的URL: {url}")
            
            response = requests.get(url, timeout=60, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"PDF 文件下载完成: {save_path}")
            return True
            
        except Exception as e:
            print(f"下载PDF失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                # 尝试修复URL后再试
                fixed_url = fix_pdf_url(url)
                if fixed_url != url:
                    print(f"尝试使用修复后的URL: {fixed_url}")
                    url = fixed_url
                time.sleep(1)  # 等待1秒后重试
            else:
                print(f"下载PDF失败 {url}: {e}")
                return False
    
    return False

def extract_stock_codes(pdf_path):
    stock_codes_found = {}
    try:
        print(f"开始解析 PDF 文件: {pdf_path}")
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            print(f"PDF 文件共有 {len(reader.pages)} 页")
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                code_pattern = r'(60[0-59]\d{4})'
                code_matches = re.findall(code_pattern, text)
                for code in code_matches:
                    if code in CODE_TO_NAME:
                        stock_codes_found[code] = CODE_TO_NAME[code]
                for code, name in CODE_TO_NAME.items():
                    if name in text and len(name) >= 2:
                        stock_codes_found[code] = name
    except Exception as e:
        print(f"解析PDF失败 {pdf_path}: {e}")
        import traceback
        traceback.print_exc()
    return stock_codes_found

def summarize_stock_codes(stock_codes_dict, date_str, source_files=None):
    if not stock_codes_dict:
        return "没有找到股票代码"
    sorted_codes = sorted(stock_codes_dict.keys())
    report = f"股票代码汇总\n"
    report += f"日期: {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}\n"
    report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    if source_files:
        report += f"来源文件: {', '.join(source_files)}\n"
    report += f"总数量: {len(sorted_codes)}\n\n"
    sh_main_board = [(code, stock_codes_dict[code]) for code in sorted_codes if code.startswith('60')]
    if sh_main_board:
        report += "上海主板股票代码:\n"
        for code, name in sh_main_board:
            report += f"{code} {name}\n"
    return report

def get_existing_pdfs():
    existing = set()
    if os.path.exists(DOWNLOAD_DIR):
        for f in os.listdir(DOWNLOAD_DIR):
            if f.endswith('.pdf'):
                existing.add(f)
    return existing

def get_pdf_filename_with_date(pdf_name, date_str):
    """在PDF文件名前面加上日期前缀，并清理非法字符"""
    # 清理Windows不允许的文件名字符
    illegal_chars = '?*:"<>|'
    for char in illegal_chars:
        pdf_name = pdf_name.replace(char, ' ')
    # 清理多个连续空格
    pdf_name = ' '.join(pdf_name.split())
    return f"{date_str}_{pdf_name}" if date_str else pdf_name

def merge_existing_stock_codes(filename, new_stock_codes):
    """读取现有文件并合并新的股票代码，去重"""
    existing_stock_codes = {}
    
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                in_code_section = False
                for line in lines:
                    if line.startswith('上海主板股票代码:'):
                        in_code_section = True
                        continue
                    if in_code_section and line.strip():
                        parts = line.strip().split(' ', 1)
                        if len(parts) == 2:
                            code = parts[0]
                            name = parts[1]
                            existing_stock_codes[code] = name
        except Exception as e:
            print(f"读取现有文件 {filename} 失败: {e}")
    
    merged = existing_stock_codes.copy()
    merged.update(new_stock_codes)
    return merged

def run_task():
    print(f"\n{'='*60}")
    print(f"开始执行任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    try:
        ensure_directory(DOWNLOAD_DIR)
        html_content = fetch_pdf_list()
        if not html_content:
            print("无法获取PDF列表，任务终止")
            return
        pdf_links = parse_pdf_links(html_content)
        if not pdf_links:
            print("未找到任何PDF文件链接")
            return
        print(f"找到 {len(pdf_links)} 个PDF文件")
        existing_pdfs = get_existing_pdfs()
        
        new_pdfs = []
        for p in pdf_links:
            date_str = parse_date_to_str(p['date'])
            filename_with_date = get_pdf_filename_with_date(p['name'], date_str)
            if filename_with_date not in existing_pdfs:
                new_pdfs.append(p)
                p['filename_with_date'] = filename_with_date
        
        print(f"其中 {len(new_pdfs)} 个是新文件")
        if not new_pdfs:
            print("没有新的PDF文件需要下载")
            return
        
        pdfs_by_date = defaultdict(list)
        for pdf_info in new_pdfs:
            date_str = parse_date_to_str(pdf_info['date'])
            if date_str:
                pdfs_by_date[date_str].append(pdf_info)
            else:
                print(f"无法解析日期，跳过: {pdf_info['name']}")
        
        for date_str, date_pdfs in pdfs_by_date.items():
            print(f"\n处理日期: {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}, 共 {len(date_pdfs)} 个PDF文件")
            
            date_stock_codes = {}
            date_downloaded_files = []
            
            for pdf_info in date_pdfs:
                pdf_url = pdf_info['url']
                pdf_name = pdf_info['name']
                filename_with_date = pdf_info['filename_with_date']
                save_path = os.path.join(DOWNLOAD_DIR, filename_with_date)
                
                if download_pdf(pdf_url, save_path):
                    stock_codes = extract_stock_codes(save_path)
                    date_stock_codes.update(stock_codes)
                    date_downloaded_files.append(filename_with_date)
            
            if date_stock_codes:
                    ensure_directory(RESULT_DIR)
                    output_filename = os.path.join(RESULT_DIR, f"stock_codes_{date_str}.txt")
                    merged_stock_codes = merge_existing_stock_codes(output_filename, date_stock_codes)
                    report = summarize_stock_codes(merged_stock_codes, date_str, date_downloaded_files)
                    with open(output_filename, 'w', encoding='utf-8') as f:
                        f.write(report)
                    print(f"日期 {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} 处理完成！")
                    print(f"报告已保存到 {output_filename}")
                    print(f"提取到 {len(date_stock_codes)} 个新股票代码，合并后共 {len(merged_stock_codes)} 个")
            else:
                print(f"日期 {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} 未提取到股票代码")
        
        print(f"\n所有任务处理完成！")
        
    except Exception as e:
        print(f"执行过程中出错: {e}")
        import traceback
        traceback.print_exc()

def main():
    import sys
    if len(sys.argv) > 1:
        interval_minutes = int(sys.argv[1])
        print(f"启动定时任务，每隔 {interval_minutes} 分钟执行一次")
        run_task()
        schedule.every(interval_minutes).minutes.do(run_task)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("执行单次任务（要设置定时任务，请传入间隔分钟数作为参数）")
        run_task()

if __name__ == "__main__":
    main()
