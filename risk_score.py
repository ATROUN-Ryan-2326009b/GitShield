def calculate_global_score(file_results, total_files):
    if total_files == 0:
        return 0

    if not file_results:
        return 0

    suspicious_files = len(file_results)
    highest_file_score = max(result["score"] for result in file_results)

    ratio_score = int((suspicious_files / total_files) * 40)
    severity_score = int(highest_file_score * 0.6)

    final_score = ratio_score + severity_score

    return min(final_score, 100)


def count_threatening_files(file_results):
    threatening_files = 0

    for result in file_results:
        if result["score"] >= 50:
            threatening_files += 1

    return threatening_files


def get_verdict(score):
    if score >= 75:
        return "High risk"
    elif score >= 45:
        return "Suspicious"
    elif score >= 15:
        return "Low risk"
    else:
        return "No obvious threat detected"