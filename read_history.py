import json

total_checks = 0
successful_checks = 0

target_url = input('Input a target URL:\n')

successful_duration_total = 0

with open("run_history.jsonl", "r") as file:
    for line in file:
        run_results = json.loads(line)
        for result in run_results:
            if result["url"] == target_url:
                total_checks += 1
                if result["ok"] == True:
                    successful_checks += 1
                    successful_duration_total += result["check_duration"]

if total_checks > 0:
    success_rate = (successful_checks/total_checks)*100
    print(f'Success rate: {success_rate:.1f}% ({successful_checks} of {total_checks} checks succeeded)')
    if successful_checks > 0:
        average_duration = successful_duration_total / successful_checks
        print(f'Average successful check duration: {average_duration:.1f} ms')
    else:
        print('No successful checks to average.')
else:
    print('No saved checks for this URL.')