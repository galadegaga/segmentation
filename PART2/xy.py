import pandas as pd
import os

def pix2phy(in_f, out_f, phy_w=30000.0, phy_h=30000.0, skip_head=False):
    try:
        with open(in_f, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"读取文件失败：{e}")
        return None

    coords = []
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        if skip_head and line_num == 1:
            print(f"跳过表头：第1行 -> {line}")
            continue
        parts = line.split()
        if len(parts) < 2:
            print(f"警告：第{line_num}行数据不足，跳过 -> {line}")
            continue
        try:
            x = int(parts[0])
            y = int(parts[1])
            coords.append((x, y))
        except ValueError:
            print(f"警告：第{line_num}行非数字，跳过 -> {line}")
            continue

    if not coords:
        print("错误：无有效坐标数据")
        return None

    x_vals = [c[0] for c in coords]
    y_vals = [c[1] for c in coords]
    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)
    pix_w = max_x - min_x + 1
    pix_h = max_y - min_y + 1
    pix_phy_w = phy_w / pix_w
    pix_phy_h = phy_h / pix_h

    res = []
    for x, y in coords:
        phy_x = (x + 0.5) * pix_phy_w
        phy_y = (pix_h - 1 - y + 0.5) * pix_phy_h
        res.append({
            'pix_x': x,
            'pix_y': y,
            'x_m': round(phy_x, 6),
            'y_m': round(phy_y, 6)
        })

    df = pd.DataFrame(res)
    df = df.sort_values(['pix_y', 'pix_x']).reset_index(drop=True)
    try:
        df.to_csv(out_f, index=False, encoding='utf-8')
    except Exception as e:
        print(f"保存文件失败：{e}")
        return None

    stats = {
        'count': len(coords),
        'out_f': out_f
    }
    return stats

def main():
    in_f = r"F:\pywork119\pythonProject\segmentation\PART2\xy.txt"
    out_f = r"F:\pywork119\pythonProject\segmentation\PART2\xy_mapping.csv"

    out_dir = os.path.dirname(out_f)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        print(f"创建目录：{out_dir}")

    if not os.path.exists(in_f):
        print(f"错误：文件不存在 -> {in_f}")
        return

    stats = pix2phy(in_f, out_f, 30000.0, 30000.0, True)

    if stats:
        print(f"有效坐标点数量：{stats['count']} 个")
        print(f"输出文件路径：{stats['out_f']}")

if __name__ == "__main__":
    main()