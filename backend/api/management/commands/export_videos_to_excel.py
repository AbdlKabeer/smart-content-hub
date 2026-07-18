import csv
from django.core.management.base import BaseCommand
from openpyxl import Workbook
from django.utils.timezone import localtime

from api.models.videos import Video

class Command(BaseCommand):
    help = 'Export Video records to CSV or Excel based on user choice'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            choices=['csv', 'excel'],
            default='excel',  # Default to 'excel' if no format is provided
            help='Specify the file format to export (csv or excel)',
        )

    def handle(self, *args, **kwargs):
        # Get the export format from the command-line argument
        export_format = kwargs['format']

        # Fetch all video records from the database
        videos = Video.objects.all().order_by('-created_at')

        # Define headers for CSV and Excel
        headers = [
            'ID', 'Title', 'Slug', 'Description', 'Category', 
            'Tags', 'Video File', 'Thumbnail', 'Views', 'Created At', 'Updated At',
            "Rating","Likes"
        ]

        if export_format == 'excel':
            # Create an Excel workbook and worksheet
            wb = Workbook()
            ws = wb.active
            ws.title = "Videos"

            # Add headers to the Excel sheet
            ws.append(headers)
            data = []
            # Add video data to the Excel sheet
            for video in videos:
                row = [
                    str(video.id),
                    video.title,
                    video.slug,
                    video.description or '',
                    video.category.name if video.category else '',
                    ', '.join([tag.name for tag in video.tags.all()]),
                    video.video_file.url if video.video_file else '',
                    video.thumbnail.url if video.thumbnail else '',
                    video.views,
                    localtime(video.created_at),  # Convert to local time for better readability
                    localtime(video.updated_at),
                    video.get_average_rating(),
                    video.get_likes_count(),
                ]
                ws.append(row)
                data.append(row)
            print(data)
            return
            # Save the Excel file
            filename = 'videos_export.xlsx'
            wb.save(filename)

            self.stdout.write(self.style.SUCCESS(f'Successfully exported videos to {filename}'))

        elif export_format == 'csv':
            # Create a CSV file and write the headers and video data
            filename = 'videos_export.csv'
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                for video in videos:
                    row = [
                        str(video.id),
                        video.title,
                        video.slug,
                        video.description or '',
                        video.category.name if video.category else '',
                        ', '.join([tag.name for tag in video.tags.all()]),
                        video.video_file.url if video.video_file else '',
                        video.thumbnail.url if video.thumbnail else '',
                        video.views,
                        localtime(video.created_at),  # Convert to local time for better readability
                        localtime(video.updated_at),
                        video.get_average_rating(),
                        video.get_likes_count(),
                    ]
                    writer.writerow(row)

            self.stdout.write(self.style.SUCCESS(f'Successfully exported videos to {filename}'))
