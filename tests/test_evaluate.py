from engine.evaluate import calculate_metrics


def _make_logs(n_normal: int, n_attack: int) -> list[dict]:
    logs = [{"label": "normal"} for _ in range(n_normal)]
    logs += [{"label": "attack"} for _ in range(n_attack)]
    return logs


def test_perfect_recall():
    logs = _make_logs(n_normal=5, n_attack=3)
    attack_indices = {5, 6, 7}
    result = calculate_metrics(logs, attack_indices)
    assert result["recall"] == 1.0


def test_zero_recall():
    logs = _make_logs(n_normal=5, n_attack=3)
    result = calculate_metrics(logs, set())
    assert result["recall"] == 0.0


def test_fp_rate_zero():
    logs = _make_logs(n_normal=5, n_attack=3)
    attack_indices = {5, 6, 7}
    result = calculate_metrics(logs, attack_indices)
    assert result["fp_rate"] == 0.0


def test_fp_rate_one():
    logs = _make_logs(n_normal=5, n_attack=0)
    all_normal_indices = set(range(5))
    result = calculate_metrics(logs, all_normal_indices)
    assert result["fp_rate"] == 1.0


def test_mixed_results():
    logs = _make_logs(n_normal=3, n_attack=2)
    # 공격 1건 탐지 (인덱스 3), 정상 1건 오탐 (인덱스 0)
    detections = {0, 3}
    result = calculate_metrics(logs, detections)
    assert result["recall"] == 0.5
    assert abs(result["fp_rate"] - 1 / 3) < 1e-9
