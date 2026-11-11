import urllib.request as r
import urllib.error as e
import time as t
from datetime import datetime as d, timezone as tz
import json
import sqlite3 as sql


def check_endpoint(page_url):
    # Check one URL and return a dictionary describing the outcome.
    try:
        response = r.urlopen(page_url, timeout = 5.0)

        # HTTP status codes from 200 through 299 count as successful.
        if response.status in range(200,300):
            return {
                'ok': True,
                'status_code': response.status,
                'message': f'Page is available ({response.status}).'
            }
    except e.HTTPError as error:
        # The server replied with an HTTP error, so we can record its status code.
        return {
            'ok': False,
            'status_code': error.code,
            'message': f"Currently unable to retrieve page ({error.code} {error.reason})."
        }
    except e.URLError as error:
        # urllib can wrap a timeout inside a URLError. Check the underlying reason.
        if isinstance(error.reason, TimeoutError):
            return {
                'ok': False,
                'status_code': None,
                'message': "Request timed out."
            }
        else:
            # Other connection failures include DNS lookup errors.
            return {
                'ok': False,
                'status_code': None,
                'message': f"Connection failed: {error.reason}."
            }
    except TimeoutError:
        # A timeout can also be raised directly.
        return {
            'ok': False,
            'status_code': None,
            'message': "Request timed out."
        }


# These test URLs exercise a successful response, a DNS failure, and a 404.
url_list = ['https://www.python.org', 'https://does-not-exist.invalid', 'https://www.python.org/this-page-should-not-exist-12345/']

success_count = 0
failure_count = 0
results = []

# Capture the batch start time once so all checks in this run share a UTC timestamp.
run_timestamp = d.now(tz.utc).isoformat()

for url in url_list:
    # Measure the full check and convert the elapsed time from seconds to milliseconds.
    request_time = t.perf_counter()
    result = check_endpoint(url)
    get_time = t.perf_counter()
    check_duration = (get_time - request_time) * 1000

    # Attach the URL, duration, and batch timestamp before saving the result.
    result['check_duration'] = check_duration
    result['url'] = url
    result['checked_at'] = run_timestamp
    results.append(result)

    # Count the outcome for the summary and display this check.
    if result["ok"]:
        success_count += 1
    else:
        failure_count += 1
    print(f'\nPage URL: {url}\nStatus: {result['message']}\nCheck duration: {check_duration:.1f}ms\n')

print(f'Summary: {success_count} successful, {failure_count} failed.')

# Replace the latest snapshot with this run's results as readable JSON.
with open("latest_run.json", "w") as file:
    json.dump(results, file, indent=2)

# Append the whole run as one JSON line. The newline separates it from the next run.
with open("run_history.jsonl", "a") as file:
    file.write(json.dumps(results) + '\n')

connection = sql.connect("monitor.db")
create_table_sql = '''CREATE TABLE IF NOT EXISTS checks(id INTEGER PRIMARY KEY, url TEXT, checked_at TEXT, ok INTEGER, status_code INTEGER, check_duration REAL, message TEXT)'''

connection.execute(create_table_sql)
insert_check_sql = '''INSERT INTO checks(url, checked_at, ok, status_code, check_duration, message) VALUES(?, ?, ?, ?, ?, ?)'''

for result in results:
    values = (
        result["url"],
        result["checked_at"],
        result["ok"],
        result["status_code"],
        result["check_duration"],
        result["message"]
    )
    connection.execute(insert_check_sql, values)

connection.commit()
connection.close()