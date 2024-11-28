import asyncio
import os
from os.path import join, dirname
from datetime import datetime
from dotenv import load_dotenv

import csv
from otf_api import Otf
from otf_api.models.classes import DoW

async def main():
    USERNAME = os.getenv("OTF_EMAIL")
    PASSWORD = os.getenv("OTF_PASSWORD")

    otf = None
    try:
        otf = otf = Otf(USERNAME, PASSWORD)
    except ValueError:
        print("Unable to identity authentication credentials in environment.")
        print("Ensure a .env file exists based on env.sample.")
        exit(1)
    
    performance_summaries = await otf.get_performance_summaries(limit=1000)

    data = []
    for summary in performance_summaries.summaries:
        date_format = '%Y-%m-%dT%H:%M:%S'
        date_obj = datetime.strptime(summary.otf_class.starts_at_local, date_format)

        perf_summary_detail = await otf.get_performance_summary(summary.id)

        one_summary = {
            "Date": date_obj.strftime('%m/%d/%Y'),
            "Calories": summary.details.calories_burned,
            "Splat Points": summary.details.splat_points,
            "Average Heart Rate": perf_summary_detail.details.heart_rate.avg_hr,
            "Grey Zone": summary.details.zone_time_minutes.gray,
            "Blue Zone": summary.details.zone_time_minutes.blue,
            "Green Zone": summary.details.zone_time_minutes.green,
            "Orange Zone": summary.details.zone_time_minutes.orange,
            "Red Zone": summary.details.zone_time_minutes.red,
            "Peak Heart Rate": perf_summary_detail.details.heart_rate.peak_hr,
            "Coach": summary.otf_class.coach.first_name,
            "Location":	summary.otf_class.studio.name,
            "Steps": perf_summary_detail.details.step_count,
            "Total Tread Distance": perf_summary_detail.details.equipment_data.treadmill.total_distance.display_value,
            "Total Tread Minutes": int(perf_summary_detail.details.equipment_data.treadmill.moving_time.metric_value)/60,
            "Total Tread Seconds": perf_summary_detail.details.equipment_data.treadmill.moving_time.metric_value,
            "Total Time in Hours": 0, 
            "Avg Speed": perf_summary_detail.details.equipment_data.treadmill.avg_speed.display_value,
            "Max Speed": perf_summary_detail.details.equipment_data.treadmill.max_speed.display_value, 
            "Avg Incline": perf_summary_detail.details.equipment_data.treadmill.avg_incline.display_value,
            "Max Incline": perf_summary_detail.details.equipment_data.treadmill.max_incline.display_value,
            "Avg Pace": perf_summary_detail.details.equipment_data.treadmill.avg_pace.display_value,
            "Max Pace": perf_summary_detail.details.equipment_data.treadmill.max_pace.display_value,
            "Elevation": perf_summary_detail.details.equipment_data.treadmill.elevation_gained.display_value

        }
        data.append(one_summary)

    print ("Found a total of %s performance summaries" % len(data))

    with open('output.csv', 'w', newline='') as file:
    # Create a DictWriter object
        writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))

        # Write the header row
        writer.writeheader()

        # Write the data rows
        writer.writerows(data)

if __name__ == "__main__":
    # Loads the .env files
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Run and write to output.csv
    asyncio.run(main())
