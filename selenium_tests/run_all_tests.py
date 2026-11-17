import csv
import glob
import importlib

test_files = sorted(glob.glob("tc*.py"))

all_results = []
for file_name in test_files:
    module = importlib.import_module(file_name[:-3])
    all_results += module.run()

with open("test_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Test Case ID", "Section", "Title", "Test Data", "Actual Result", "Status"])
    writer.writerows(all_results)

passed = sum(1 for r in all_results if r[5] == "Pass")
failed = len(all_results) - passed

print()
print("=" * 70)
print(f"   TOTAL: {len(all_results)} test cases   PASSED: {passed}   FAILED: {failed}")
print("   Results saved in: test_results.csv")
print("=" * 70)
