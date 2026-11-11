import urllib.request as r
import urllib.error as e
import time as t
from datetime import datetime as d, timezone as tz
import json

def check_endpoint(page_url):
    try:
        response = r.urlopen(page_url, timeout = 5.0)

        if response.status in range(200,300):
            return {
                'ok': True,
                'status_code': response.status,
                'message': f'Page is available ({response.status}).'
            }
    except e.HTTPError as error:
        return {
            'ok': False,
            'status_code': error.code,
            'message': f"Currently unable to retrieve page ({error.code} {error.reason})."
        }
    except e.URLError as error:
        if isinstance(error.reason, TimeoutError):
            return {
                'ok': False,
                'status_code': None,
                'message': "Request timed out."
            }
        else:
            return {
                'ok': False,
                'status_code': None,
                'message': f"Connection failed: {error.reason}."
            }
    except TimeoutError:
        return {
            'ok': False,
            'status_code': None,
            'message': "Request timed out."
        }

url_list = ['https://www.python.org', 'https://does-not-exist.invalid', 'https://www.python.org/this-page-should-not-exist-12345/']

success_count = 0
failure_count = 0

results = []

run_timestamp = d.now(tz.utc).isoformat()

for url in url_list:
    request_time = t.perf_counter()
    result = check_endpoint(url)
    get_time = t.perf_counter()
    check_duration = (get_time - request_time) * 1000
    result['check_duration'] = check_duration
    result['url'] = url
    result['checked_at'] = run_timestamp
    results.append(result)
    if result["ok"]:
        success_count += 1
    else:
        failure_count += 1
    print(f'\nPage URL: {url}\nStatus: {result['message']}\nCheck duration: {check_duration:.1f}ms\n')
print(f'Summary: {success_count} successful, {failure_count} failed.')
print(json.dumps(results))

with open("latest_run.json", "w") as file:
    json.dump(results, file, indent=2)

with open("run_history.jsonl", "a") as file:
    file.write(json.dumps(results) + '\n')