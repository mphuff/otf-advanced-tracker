import asyncio
import os
from datetime import datetime

import json
import csv
from otf_api import Otf
from otf_api.models.classes import DoW

USERNAME = os.getenv("OTF_EMAIL")
PASSWORD = os.getenv("OTF_PASSWORD")

async def write_data(data):
    with open('output.csv', 'w', newline='') as file:
    # Create a DictWriter object
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))

        # Write the header row
        writer.writeheader()

        # Write the data rows
        writer.writerows(data)

async def main():
    otf = otf = Otf(USERNAME, PASSWORD)

    #resp = await otf.get_bookings(start_date=datetime.today().date())
    #print(resp.model_dump_json(indent=4))

    #studios = await otf.search_studios_by_geo(40.7831, 73.9712, distance=100)

    #studio_uuids = [studio.studio_uuid for studio in studios.studios]

    # To get upcoming classes you can call the `get_classes` method
    # You can pass a list of studio_uuids or, if you want to get classes from your home studio, leave it empty
    # this also takes a start date, end date, and limit - these are not sent to the API, they are used in the
    # client to filter the results
    #classes = await otf.get_classes(studio_uuids, day_of_week=[DoW.TUESDAY, DoW.THURSDAY, DoW.SATURDAY])

    # print(classes.classes[0].model_dump_json(indent=4))

    # You can also get the classes that you have booked
    # You can pass a start_date, end_date, status, and limit as arguments

    #bookings = await otf.get_bookings()

    # Calories	Splat Points	Average Heart Rate	 Grey Zone	Blue Zone	Green Zone	Orange Zone	Red Zone	Peak Heart Rate	Coach	Location	Steps	Total Tread Distance	Total Tread Minutes	Total Tread Seconds	Total Time in Hours	Avg Speed	Max Speed	Avg Incline	Max Incline	Avg Pace	Max Pace	Elevation

    performance_summaries = await otf.get_performance_summaries(limit=1000)
    #print(performance_summaries.model_dump_json(indent=4))

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

    #print(json.dumps(data, indent=4))
    #asyncio.run(write_data(data))

    with open('output.csv', 'w', newline='') as file:
    # Create a DictWriter object
        writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))

        # Write the header row
        writer.writeheader()

        # Write the data rows
        writer.writerows(data)


    # performance_tracking_id = performance_summaries.summaries[0].id
    # telemetry = await otf.get_telemetry(performance_summary_id=performance_tracking_id, max_data_points=240)
    # print(telemetry.model_dump_json(indent=4))

    #print("Latest Upcoming Class:")
    #print(bookings.bookings[-1].model_dump_json(indent=4))

if __name__ == "__main__":
    asyncio.run(main())
