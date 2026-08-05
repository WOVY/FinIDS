import random

from data_gen.attack_injector import generate_attack_logs
from data_gen.log_generator import generate_normal_logs
from engine.rules import ALL_RULES, Rule


def calculate_metrics(logs: list[dict], detections: set[int]) -> dict:
    """logs의 label 필드와 detections 인덱스 집합으로 Recall·FP율을 계산한다."""
    attack_indices = {i for i, log in enumerate(logs) if log.get("label") == "attack"}
    normal_indices = {i for i, log in enumerate(logs) if log.get("label") == "normal"}

    tp = len(detections & attack_indices)
    fp = len(detections & normal_indices)

    recall = tp / len(attack_indices) if attack_indices else 0.0
    fp_rate = fp / len(normal_indices) if normal_indices else 0.0

    return {"recall": recall, "fp_rate": fp_rate}


def run_rules(logs: list[dict], rules: list[Rule]) -> set[int]:
    """룰 5종을 모두 실행해 탐지된 로그 인덱스의 합집합을 반환한다."""
    detections: set[int] = set()
    for rule in rules:
        for alert in rule.detect(logs):
            detections.update(alert.log_indices)
    return detections


def _generate_evaluation_logs(n_normal: int = 9_500, n_attack: int = 500) -> list[dict]:
    normal_logs = generate_normal_logs(n_normal)
    attack_logs: list[dict] = []
    while len(attack_logs) < n_attack:
        attack_logs += generate_attack_logs(n_each=20)
    return normal_logs + attack_logs[:n_attack]


def main() -> None:
    random.seed(42)
    n_normal, n_attack = 9_500, 500
    logs = _generate_evaluation_logs(n_normal, n_attack)
    detections = run_rules(logs, ALL_RULES)
    metrics = calculate_metrics(logs, detections)
    print(f"로그 {len(logs)}건 (정상 {n_normal}, 공격 {n_attack}) 평가 완료")
    print(f"Recall: {metrics['recall']:.2%}")
    print(f"FP rate: {metrics['fp_rate']:.2%}")


if __name__ == "__main__":
    main()
