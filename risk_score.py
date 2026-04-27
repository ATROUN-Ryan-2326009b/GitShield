def count_threatening_files(file_results):
    return sum(1 for result in file_results if result["score"] >= 70)


def count_medium_files(file_results):
    return sum(1 for result in file_results if 40 <= result["score"] < 70)


def calculate_global_score(file_results, total_files):
    if total_files == 0 or not file_results:
        return 0

    suspicious_files = len(file_results)
    threatening_files = count_threatening_files(file_results)
    medium_files = count_medium_files(file_results)

    suspicious_ratio = suspicious_files / total_files
    threatening_ratio = threatening_files / total_files
    medium_ratio = medium_files / total_files

    average_score = sum(result["score"] for result in file_results) / suspicious_files
    max_score = max(result["score"] for result in file_results)

    ratio_component = int(suspicious_ratio * 20)
    medium_component = int(medium_ratio * 25)
    threat_component = int(threatening_ratio * 45)
    average_component = int(average_score * 0.20)
    max_component = int(max_score * 0.10)

    final_score = (
        ratio_component
        + medium_component
        + threat_component
        + average_component
        + max_component
    )

    return min(final_score, 100)


def get_verdict(score):
    if score >= 75:
        return "High risk"
    elif score >= 45:
        return "Suspicious"
    elif score >= 15:
        return "Low risk"
    else:
        return "No obvious threat detected"


def get_risk_color(score):
    if score >= 75:
        return "red"
    elif score >= 45:
        return "yellow"
    elif score >= 15:
        return "cyan"
    else:
        return "green"