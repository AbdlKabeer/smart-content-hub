import csv
from django.core.management.base import BaseCommand
from openpyxl import Workbook
from django.utils.timezone import localtime

from account.models import Article



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
        articles = Article.objects.all().order_by('-created_at')[:2]

        # Define headers for CSV and Excel
        headers = [
            'ID', 'Title', 'summary', 'Description', 'keywords', 
            'Created At',"Likes"
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
            for article in articles:
                row = [
                    str(article.id),
                    article.title,
                    article.summary or '',
                    article.meta_description or '',
                    article.keywords,
                    localtime(article.created_at),
                    article.get_likes_count(),
                ]
                ws.append(row)
                data.append(row)
            print(data)
            return
            # Save the Excel file
            filename = 'articles_export.xlsx'
            wb.save(filename)

            self.stdout.write(self.style.SUCCESS(f'Successfully exported videos to {filename}'))

        elif export_format == 'csv':
            # Create a CSV file and write the headers and video data
            filename = 'articles_export.csv'
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                for article in articles:
                    row = [
                        str(article.id),
                        article.title,
                        article.summary or '',
                        article.meta_description or '',
                        article.keywords,
                        localtime(article.created_at),
                        article.get_likes_count(),
                    ]
                    writer.writerow(row)

            self.stdout.write(self.style.SUCCESS(f'Successfully exported videos to {filename}'))
