import csv
from django.core.management.base import BaseCommand
from openpyxl import Workbook

from api.models.quiz import Quiz

class Command(BaseCommand):
    help = 'Export Quiz records to CSV or Excel based on user choice'

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

        # Fetch all quiz records from the database
        quizzes = Quiz.objects.all()[:5]

        # Define headers for CSV and Excel
        headers = [
            'ID', 'Title', 'Description', 'Category', 'Level', 
            'Estimated Time', 'Tags', 'Created By', 'Created At', 'Updated At'
        ]

        if export_format == 'excel':
            # Create an Excel workbook and worksheet
            wb = Workbook()
            ws = wb.active
            ws.title = "Quizzes"

            # Add headers to the Excel sheet
            ws.append(headers)
            # Add quiz data to the Excel sheet
            for quiz in quizzes:
                row = [
                    str(quiz.id),
                    quiz.title,
                    quiz.description,
                    quiz.category.name if quiz.category else '',
                    quiz.level,
                    quiz.estimated_time,
                    ', '.join([tag.name for tag in quiz.tags.all()]),
                    quiz.created_by.first_name if quiz.created_by else '',
                    quiz.created_at,
                    quiz.updated_at,
                ]
                ws.append(row)

            return 
            # Save the Excel file
            filename = 'quizzes_export.xlsx'
            wb.save(filename)

            self.stdout.write(self.style.SUCCESS(f'Successfully exported quizzes to {filename}'))

        elif export_format == 'csv':
            # Create a CSV file and write the headers and quiz data
            filename = 'quizzes_export.csv'
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                for quiz in quizzes:
                    row = [
                        str(quiz.id),
                        quiz.title,
                        quiz.description,
                        quiz.category.name if quiz.category else '',
                        quiz.level,
                        quiz.estimated_time,
                        ', '.join([tag.name for tag in quiz.tags.all()]),
                        quiz.created_by.first_name if quiz.created_by else '',
                        quiz.created_at,
                        quiz.updated_at
                    ]
                    writer.writerow(row)

            self.stdout.write(self.style.SUCCESS(f'Successfully exported quizzes to {filename}'))
