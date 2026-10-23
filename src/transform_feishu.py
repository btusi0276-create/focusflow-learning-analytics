import argparse
from pathlib import Path

import pandas as pd


COLUMN_MAPPING = {
    "日期": "date",
    "睡眠时长": "sleep_duration_hours",
    "睡眠质量": "sleep_quality",
    "学习时长": "study_hours",
    "深度学习时长": "deep_focus_hours",
    "娱乐手机时长": "phone_entertainment_hours",
    "运动时长": "exercise_hours",
    "课程负担": "class_load",
    "专注评分": "focus_score",
    "备注": "notes",
}


def transform_feishu_csv(input_path: str, output_path: str) -> pd.DataFrame:
    """将飞书导出的中文列名 CSV 转换为 FocusFlow 标准英文列名。"""
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(f"找不到输入文件：{input_file}")

    df = pd.read_csv(input_file, encoding="utf-8-sig")

    missing_columns = [
        chinese_name
        for chinese_name in COLUMN_MAPPING
        if chinese_name not in df.columns
    ]

    if missing_columns:
        missing_text = "、".join(missing_columns)
        raise ValueError(
            f"飞书导出的文件缺少以下列：{missing_text}。"
            "请检查飞书表格的字段名称是否完全一致。"
        )

    transformed_df = df.rename(columns=COLUMN_MAPPING)
    transformed_df = transformed_df[list(COLUMN_MAPPING.values())]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    transformed_df.to_csv(output_file, index=False, encoding="utf-8-sig")

    return transformed_df


def parse_args() -> argparse.Namespace:
    """读取终端中输入的文件路径。"""
    parser = argparse.ArgumentParser(
        description="将飞书导出的学习记录 CSV 转换为 FocusFlow 标准格式。"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="飞书导出的原始 CSV 文件路径。",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="转换后的标准 CSV 输出路径。",
    )
    return parser.parse_args()


def main() -> None:
    """运行转换程序，并在终端显示结果。"""
    args = parse_args()

    try:
        transformed_df = transform_feishu_csv(args.input, args.output)
    except (FileNotFoundError, ValueError, UnicodeDecodeError) as error:
        print(f"❌ 转换失败：{error}")
        raise SystemExit(1)

    print(
        f"✅ 转换完成：共处理 {len(transformed_df)} 条记录。\n"
        f"输出文件：{args.output}"
    )


if __name__ == "__main__":
    main()