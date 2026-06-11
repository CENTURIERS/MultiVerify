import csv
import os


RESULTS_FILE = "docs/experiment_results.csv"
METRICS_FILE = "docs/metrics_summary.csv"
CHARTS_DIR = "docs/latex/figures"


def to_bool(value):
    return str(value).lower() == "true"


def read_results():
    if not os.path.exists(RESULTS_FILE):
        print(f"Brak pliku {RESULTS_FILE}. Najpierw uruchom scripts/run_experiments.py")
        return []

    with open(RESULTS_FILE, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def compute_for_rows(rows):
    by_variant = {}

    for row in rows:
        variant = row["variant"]
        if variant not in by_variant:
            by_variant[variant] = []
        by_variant[variant].append(row)

    metrics = []

    for variant, items in by_variant.items():
        total = len(items)
        correct = 0
        genuine = 0
        impostor = 0
        false_accepts = 0
        false_rejects = 0

        for row in items:
            accepted = to_bool(row["accepted"])
            expected_match = to_bool(row["expected_match"])

            if accepted == expected_match:
                correct += 1

            if expected_match:
                genuine += 1
                if not accepted:
                    false_rejects += 1
            else:
                impostor += 1
                if accepted:
                    false_accepts += 1

        accuracy = correct / total if total else 0.0
        far = false_accepts / impostor if impostor else 0.0
        frr = false_rejects / genuine if genuine else 0.0

        metrics.append({
            "variant": variant,
            "accuracy": round(accuracy, 4),
            "far": round(far, 4),
            "frr": round(frr, 4),
            "total": total,
            "false_accepts": false_accepts,
            "false_rejects": false_rejects,
        })

    return metrics


def save_metrics(metrics):
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)

    with open(METRICS_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "variant",
            "accuracy",
            "far",
            "frr",
            "total",
            "false_accepts",
            "false_rejects",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metrics)


def draw_empty_chart(path, title):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 4))
    plt.title(title)
    plt.text(0.5, 0.5, "Brak danych eksperymentalnych", ha="center", va="center")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def draw_far_frr_chart(metrics):
    import matplotlib.pyplot as plt

    os.makedirs(CHARTS_DIR, exist_ok=True)
    path = os.path.join(CHARTS_DIR, "far_frr_by_variant.png")

    if len(metrics) == 0:
        draw_empty_chart(path, "FAR i FRR wedlug wariantu")
        return

    variants = [row["variant"] for row in metrics]
    far = [float(row["far"]) for row in metrics]
    frr = [float(row["frr"]) for row in metrics]
    x = list(range(len(variants)))

    plt.figure(figsize=(10, 5))
    plt.bar([i - 0.2 for i in x], far, width=0.4, label="FAR")
    plt.bar([i + 0.2 for i in x], frr, width=0.4, label="FRR")
    plt.xticks(x, variants, rotation=25, ha="right")
    plt.ylim(0, 1)
    plt.ylabel("Wartosc")
    plt.title("FAR i FRR dla wariantow")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def compute_threshold_rows(rows):
    summary = []

    for i in range(5, 10):
        threshold = i / 10
        total = 0
        correct = 0
        genuine = 0
        impostor = 0
        false_accepts = 0
        false_rejects = 0

        for row in rows:
            face_score = float(row["face_score"])
            voice_score = float(row["voice_score"])
            final_score = (face_score * 0.6) + (voice_score * 0.4)
            accepted = final_score >= threshold
            expected_match = to_bool(row["expected_match"])

            total += 1
            if accepted == expected_match:
                correct += 1

            if expected_match:
                genuine += 1
                if not accepted:
                    false_rejects += 1
            else:
                impostor += 1
                if accepted:
                    false_accepts += 1

        accuracy = correct / total if total else 0.0
        far = false_accepts / impostor if impostor else 0.0
        frr = false_rejects / genuine if genuine else 0.0

        summary.append({
            "threshold": threshold,
            "accuracy": accuracy,
            "far": far,
            "frr": frr,
        })

    return summary


def draw_threshold_chart(rows):
    import matplotlib.pyplot as plt

    os.makedirs(CHARTS_DIR, exist_ok=True)
    path = os.path.join(CHARTS_DIR, "threshold_sweep.png")
    fusion_rows = [row for row in rows if row.get("variant") == "fusion_60_40"]

    if len(fusion_rows) == 0:
        draw_empty_chart(path, "Wplyw progu na FAR i FRR")
        return

    summary = compute_threshold_rows(fusion_rows)
    thresholds = [row["threshold"] for row in summary]
    far = [row["far"] for row in summary]
    frr = [row["frr"] for row in summary]

    plt.figure(figsize=(8, 5))
    plt.plot(thresholds, far, marker="o", label="FAR")
    plt.plot(thresholds, frr, marker="o", label="FRR")
    plt.ylim(0, 1)
    plt.xlabel("Prog decyzji")
    plt.ylabel("Wartosc")
    plt.title("Wplyw progu na FAR i FRR (fuzja 60/40)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def main():
    rows = read_results()
    metrics = compute_for_rows(rows)
    save_metrics(metrics)
    draw_far_frr_chart(metrics)
    draw_threshold_chart(rows)

    print(f"Zapisano metryki: {METRICS_FILE}")
    print(f"Zapisano wykresy w: {CHARTS_DIR}")


if __name__ == "__main__":
    main()
