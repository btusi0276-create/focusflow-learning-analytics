import pandas as pd

from src.data_validation import validate_learning_log


def create_valid_log() -> pd.DataFrame:
    """创建一条符合 FocusFlow 数据规则的测试记录。"""
    return pd.DataFrame(
        {
            "date": ["2026-10-01"],
            "sleep_duration_hours": [7.5],
            "sleep_quality": [4],
            "study_hours": [4.0],
            "deep_focus_hours": [2.5],
            "phone_entertainment_hours": [1.5],
            "exercise_hours": [0.5],
            "class_load": ["中"],
            "focus_score": [4],
            "notes": ["测试数据"],
        }
    )


def test_valid_log_has_no_issues():
    """正确的数据不应产生任何质量问题。"""
    issues = validate_learning_log(create_valid_log())

    assert issues == []


def test_missing_required_column_is_reported():
    """缺少必要字段时，验证器应报告错误。"""
    df = create_valid_log().drop(columns=["focus_score"])

    issues = validate_learning_log(df)

    assert any("缺少必要字段" in issue for issue in issues)


def test_sleep_duration_out_of_range_is_reported():
    """睡眠超过合理范围时，验证器应报告错误。"""
    df = create_valid_log()
    df.loc[0, "sleep_duration_hours"] = 15

    issues = validate_learning_log(df)

    assert any("sleep_duration_hours 必须在 0–14 小时之间" in issue for issue in issues)


def test_deep_focus_cannot_exceed_total_study_time():
    """深度学习时长不能超过总学习时长。"""
    df = create_valid_log()
    df.loc[0, "study_hours"] = 2.0
    df.loc[0, "deep_focus_hours"] = 3.0

    issues = validate_learning_log(df)

    assert any(
        "deep_focus_hours 不能大于 study_hours" in issue
        for issue in issues
    )


def test_invalid_focus_score_is_reported():
    """专注评分不是 1–5 时，验证器应报告错误。"""
    df = create_valid_log()
    df.loc[0, "focus_score"] = 6

    issues = validate_learning_log(df)

    assert any("focus_score 只能填写 1–5 分" in issue for issue in issues)


def test_invalid_class_load_is_reported():
    """课程负担不属于低、中、高时，验证器应报告错误。"""
    df = create_valid_log()
    df.loc[0, "class_load"] = "很高"

    issues = validate_learning_log(df)

    assert any("class_load 只能填写“低”“中”或“高”" in issue for issue in issues)