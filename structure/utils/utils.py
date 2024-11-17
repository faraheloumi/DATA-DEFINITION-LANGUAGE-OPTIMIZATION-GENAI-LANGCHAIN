def print_results(results, label="Result"):
    print(f"\n=== {label} ===")
    print(results)
    print("="*40)

def export_result_to_file(results, filename):
    with open(filename + ".txt", "w") as f:
        f.write(results)
        f.close()
    print(f"Results exported to {filename}.txt")