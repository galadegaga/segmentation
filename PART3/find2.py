import numpy as np
from scipy.spatial import cKDTree
import os


def read_data():
    init_path = r"F:\pywork119\pythonProject\PART3\init_xyr.dat"
    prop_path = r"F:\pywork119\pythonProject\PART3\property.dat"

    if not os.path.exists(init_path):
        raise FileNotFoundError(f"找不到文件: {init_path}")
    if not os.path.exists(prop_path):
        raise FileNotFoundError(f"找不到文件: {prop_path}")

    print(f"读取文件: {init_path}")
    init_raw = []
    init_list = []
    try:
        with open(init_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                raw_line = line.rstrip('\n')
                init_raw.append(raw_line)

                line_strip = raw_line.strip()
                if not line_strip:
                    continue
                parts = line_strip.split()
                if len(parts) != 3:
                    raise ValueError(f"第{line_num}行格式错误: {line_strip}")
                x = float(parts[0])
                y = float(parts[1])
                radius = float(parts[2])
                init_list.append([x, y, radius])

        init_data = np.array(init_list)
        print(f"读取完成 - 有效数据行: {init_data.shape[0]}")
    except Exception as e:
        raise ValueError(f"读取 {init_path} 出错: {e}")

    print(f"\n读取文件: {prop_path}")
    prop_data = read_property_file(prop_path)

    return init_data, init_raw, prop_data


def read_property_file(file_path):
    all_lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        all_lines = [line.strip() for line in f if line.strip()]

    if not all_lines:
        raise ValueError(f"文件 {file_path} 无有效数据")

    x_list = []
    y_list = []
    prop_list = []

    for line_num, line in enumerate(all_lines, 1):
        parts = line.split()
        if len(parts) < 3:
            print(f"警告: 第 {line_num} 行列数不足，跳过")
            continue

        try:
            x = float(parts[0])
            y = float(parts[1])
            prop = " ".join(parts[2:])

            x_list.append(x)
            y_list.append(y)
            prop_list.append(prop)

        except ValueError:
            print(f"警告: 第 {line_num} 行坐标非数值，跳过")
            continue

    if not x_list:
        raise ValueError(f"文件 {file_path} 无有效数据")

    prop_coords = np.column_stack([x_list, y_list])
    print(f"成功读取 {len(x_list)} 行数据")

    return {"coords": prop_coords, "props": prop_list}


def find_nearest_property(init_data, prop_data):
    prop_coords = prop_data["coords"]
    prop_list = prop_data["props"]

    if len(prop_coords) == 0:
        raise ValueError("property无有效坐标点")

    print(f"\n匹配 {len(init_data)} 个点的最近属性...")
    prop_tree = cKDTree(prop_coords)
    init_coords = init_data[:, :2]
    dists, indices = prop_tree.query(init_coords, k=1)

    match_props = [prop_list[i] for i in indices]
    return match_props, dists


def save_result(init_raw, match_props):
    output_path = r"F:\pywork119\pythonProject\PART3\property_xyr.dat"
    print(f"\n保存结果到: {output_path}")

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    idx = 0
    with open(output_path, 'w', encoding='utf-8') as f:
        for raw_line in init_raw:
            if not raw_line.strip():
                f.write(raw_line + '\n')
                continue
            prop = match_props[idx] if idx < len(match_props) else "N/A"
            new_line = f"{raw_line}  {prop}"
            f.write(new_line + '\n')
            idx += 1

    print(f"保存完成 - 共写入 {len(init_raw)} 行数据")
    return output_path


def main():
    try:
        print("开始处理数据...\n")
        init_data, init_raw, prop_data = read_data()
        match_props, dists = find_nearest_property(init_data, prop_data)
        output_path = save_result(init_raw, match_props)

        print(f"输出文件: {output_path}")

        if dists is not None and len(dists) > 0:
            print(f"平均匹配距离: {dists.mean():.6f}")

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()