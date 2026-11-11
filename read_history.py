import json

total_checks = 0
successful_checks = 0

successful_duration_total = 0

saved_urls = set()
all_results = []

with open("run_history.jsonl", "r") as file:
    for line in file:
        run_results = json.loads(line)
        for result in run_results:
            saved_urls.add(result['url'])
            all_results.append(result)

print("Saved URLs")

url_options = sorted(saved_urls)
for num, url in enumerate(url_options, start=1):
    print(f'{num}. {url}')

try:
    choice = int(input('Input an option number:\n'))
except ValueError:
    raise SystemExit('Enter a whole number.')
if choice not in range(1, len(url_options)+1):
    raise SystemExit(f'Choose a number from 1 to {len(url_options)}.')

target_url = url_options[choice-1]
for result in all_results:
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