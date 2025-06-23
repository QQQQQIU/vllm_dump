import re
import pandas as pd

# python /root/vllm_dump/examples/offline_inference/basic/basic.py > add_all.log 2>&1

def extract_log_blocks(log_file_path):
    """
    从日志文件中提取符合规则的记录块
    """
    blocks = []  # 存储提取的记录块
    current_block = []  # 当前正在收集的记录块
    recording = False  # 是否正在记录块
    
    with open(log_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 移除行首尾空白字符

            # if recording and (not re.search(r'^\[DUMP\]-{40}', line)):
            if recording and (not re.search(r'^\[DUMP\]-{40}', line)) and re.search(r'^\[DUMP', line):
                current_block.append(line)

            elif recording and re.search(r'^\[DUMP\]-{40}', line):
                blocks.append('\n'.join(current_block))  # 将块合并为字符串
                recording = False
            
            elif re.search(r'^\[DUMP', line):
                recording = True
                current_block = [line]  # 开始新的记录块
            

    
    return blocks

def save_to_excel(blocks, output_file):
    """
    将提取的日志块保存到Excel文件
    """
    # 创建DataFrame，每个块作为一行
    df = pd.DataFrame(blocks, columns=['Log Block'])
    
    # 保存到Excel文件
    df.to_excel(output_file, index=False)
    print(f"成功保存 {len(blocks)} 个日志块到 {output_file}")

if __name__ == "__main__":
    input_log = "/root/qinzq_log/add_all.log"    # 输入的日志文件路径
    output_excel = "/root/qinzq_log/add_all.xlsx"  # 输出的Excel文件路径
    
    # 提取日志块并保存到Excel
    log_blocks = extract_log_blocks(input_log)
    save_to_excel(log_blocks, output_excel)