import json

# These totals are for the URL the user selects.
total_checks = 0
successful_checks = 0
successful_duration_total = 0

# The set keeps each URL once for the menu. The list keeps every check for the report.
saved_urls = set()
all_results = []

try:
    with open("run_history.jsonl", "r") as file:
        for line in file:
            # Each JSON line contains the list of results from one run.
            run_results = json.loads(line)
            for result in run_results:
                saved_urls.add(result['url'])
                all_results.append(result)
except FileNotFoundError:
    raise SystemExit('No saved history yet. Run check_endpoint.py first.')

if not saved_urls:
    raise SystemExit('No saved checks yet. Run check_endpoint.py first.')

# Use the same sorted list to display the menu and look up the selected URL.
print("Saved URLs")

url_options = sorted(saved_urls)
for num, url in enumerate(url_options, start=1):
    print(f'{num}. {url}')

# Convert the input to an integer and exit with a message if conversion fails.
try:
    choice = int(input('Input an option number:\n'))
except ValueError:
    raise SystemExit('Enter a whole number.')

# range excludes its stop value, so add one to include the last menu option.
if choice not in range(1, len(url_options)+1):
    raise SystemExit(f'Choose a number from 1 to {len(url_options)}.')

# Menu numbers start at 1. List indexes start at 0.
target_url = url_options[choice-1]

# Count every check for this URL. Add durations only for successful checks.
for result in all_results:
    if result["url"] == target_url:
        total_checks += 1
        if result["ok"] == True:
            successful_checks += 1
            successful_duration_total += result["check_duration"]

# Check each denominator before dividing.
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