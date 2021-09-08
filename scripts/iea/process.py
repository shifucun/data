#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
from datetime import datetime

RAW_XLSX = "Archive_Table_Revised August 2021.xlsx - Old Breakdown.csv"
FUEL_TYPES = {
  "Combustible Fuels": "Monthly_Generation_Electricity_CombustibleFuel",
  "Nuclear": "Monthly_Generation_Electricity_Nuclear",
  "Hydro": "Monthly_Generation_Electricity_HydroelectricPumpedStorage",
  "Geothermal": "Monthly_Generation_Electricity_Geothermal",
  "lectricity Supplied": "Monthly_Generation_Electricity",
}
STAT_VARS = [
  "Monthly_Generation_Electricity_CombustibleFuel",
  "Monthly_Generation_Electricity_Nuclear",
  "Monthly_Generation_Electricity_HydroelectricPumpedStorage",
  "Monthly_Generation_Electricity_Geothermal",
  "Monthly_Generation_Electricity",
]


def load_country_dcid():
  result = {}
  with open("country.csv") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
      result[row[0]] = row[1]
  return result


def process():
  result = {}
  country_dcid = None
  dates = []
  country_row = False
  country_name_to_dcid = load_country_dcid()
  with open(RAW_XLSX) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      # Start of a new country
      if row[0] == "GWh":
        country_row = True
        continue
      elif country_row:
        country_row = False
        country_name = row[0]
        if country_name.capitalize() in country_name_to_dcid:
          country_dcid = country_name_to_dcid[country_name.capitalize()]
          result[country_dcid] = {}
          dates = row[1:]
      else:
        for x in FUEL_TYPES:
          if x in row[0]:
            stat_var = FUEL_TYPES[x]
            result[country_dcid][stat_var] = {}
            for i, cell in enumerate(row[1:]):
              if cell == "#REF!":
                continue
              result[country_dcid][stat_var][dates[i]] = cell.replace(" ", "")
  # Write result to csv file
  with open('iea_electricity.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    header = ["place", "date"]
    header.extend(STAT_VARS)
    writer.writerow(header)
    for country, country_data in result.items():
      dated_data = {}
      for stat_var, data in country_data.items():
        for date_str, val in data.items():
          date_object = datetime.strptime(date_str, "%b-%y")
          date = date_object.strftime("%Y-%m")
          if date not in dated_data:
            dated_data[date] = {}
          dated_data[date][stat_var] = val
      # write row
      for date, sv_data in dated_data.items():
        row = [country, date]
        row.extend([sv_data.get(sv, "") for sv in STAT_VARS])
        writer.writerow(row)


def main():
    """Runs the program."""
    process()


if __name__ == '__main__':
    main()
