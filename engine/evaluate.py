def calculate_metrics(logs: list[dict], detections: set[int]) -> dict:
    """logs의 label 필드와 detections 인덱스 집합으로 Recall·FP율을 계산한다."""
    attack_indices = {i for i, log in enumerate(logs) if log.get("label") == "attack"}
    normal_indices = {i for i, log in enumerate(logs) if log.get("label") == "normal"}

    tp = len(detections & attack_indices)
    fp = len(detections & normal_indices)

    recall = tp / len(attack_indices) if attack_indices else 0.0
    fp_rate = fp / len(normal_indices) if normal_indices else 0.0

    return {"recall": recall, "fp_rate": fp_rate}
