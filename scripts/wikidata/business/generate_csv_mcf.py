# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import csv


def main():
    """Runs the script to create csv and template MCF."""

    result = {}
    with open("raw.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)

        # Skip the header file
        next(csvreader)

        for row in csvreader:
            if not row[2]:
                continue
            dcid = row[2]
            if dcid not in result:
                result[dcid] = {
                    'name': '',
                    'date': '',
                    'location': '',
                    'url': '',
                    'cik': '',
                }
            if row[1]:
                name = row[1].split("@")[0].replace('"', '')
                result[dcid]['name'] = name
            if row[4]:
                result[dcid]['date'] = row[4].split('T')[0].replace('"', '')
            result[dcid]['location'] = row[6]
            result[dcid]['url'] = row[7]
            result[dcid]['cik'] = row[8]


    with open('data.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        csvwriter.writerow(['dcid', 'name', 'foundingDate', 'location', 'url', 'cik'])
        for dcid, data in result.items():
            csvwriter.writerow([
                dcid,
                data['name'],
                data['date'],
                data['location'],
                data['url'],
                data['cik']]
            )


if __name__ == "__main__":
    main()
