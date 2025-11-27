# SQLite Data Persistence
import uuid
from typing import Optional

from artificer.artificer import ASCI_BLUE, ASCI_RESET, ASCI_ARROW
from sqlalchemy import create_engine
import sqlite3
import csv
import os
from artisan.artisan import Artisan

systeminfo = Artisan()
# Get the user's home directory
home_directory = os.path.expanduser("~")
# Construct the path to the Documents folder
documents_folder = os.path.join(home_directory, "Documents")
# Define the name of the new directory
rpa_directory_name = "TruliooME"
db_subdirectory_name = "Moneta"
# Construct the full path for the new directory
rpa_directory_path = os.path.join(documents_folder, rpa_directory_name)
rpa_cli_subdirectory_path = os.path.join(rpa_directory_path, 'Mekatron')
rpa_server_subdirectory_path = os.path.join(rpa_directory_path, 'MekaGodzilla')
if systeminfo.platform.__contains__("Windows"):
    db_subdirectory_path = os.path.join(rpa_directory_path, db_subdirectory_name)
else:
    db_subdirectory_path = os.path.join(rpa_directory_path, F'.{db_subdirectory_name}')
rpa_server_downloads_path = os.path.join(db_subdirectory_path, 'Downloads')


class Moneta:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Moneta, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self, heimdall):
        if not hasattr(self, '_initialized'):
            self.datasource = create_engine("sqlite:///./moneta.db")
            self.directory_path = rpa_directory_path
            self.cli_directory_path = rpa_cli_subdirectory_path
            self.server_directory_path = rpa_server_subdirectory_path
            self.db_directory_path = db_subdirectory_path
            self.rpa_downloads_path = rpa_server_downloads_path
            # Create the directories
            try:
                os.makedirs(rpa_directory_path, exist_ok=True)
                os.makedirs(rpa_cli_subdirectory_path, exist_ok=True)
                os.makedirs(rpa_server_subdirectory_path, exist_ok=True)
                os.makedirs(db_subdirectory_path, exist_ok=True)
                os.makedirs(rpa_server_downloads_path, exist_ok=True)
                if systeminfo.platform.__contains__("Windows"):
                    os.system(f'attrib +h "{db_subdirectory_path}"')
            except OSError as e:
                print(f"Moneta encountered error creating TruliooME Data Persistence: {e}")
            self.artisan = Artisan()
            self.heimdall = heimdall
            self._initialized = True
            self.heimdall.info_log(F"Initialized Moneta DB Engine::@{uuid.uuid4()}")
            self.heimdall.info_log(F"Moneta DB Engine::Directory@{self.directory_path}")
            self.heimdall.info_log(F"Moneta DB Engine::Logs@{self.db_directory_path}")
            print(F"{ASCI_BLUE}{ASCI_ARROW} Moneta Initialized{ASCI_RESET}")

    def export_db(self):
        # Connect to the SQLite database
        conn = sqlite3.connect('moneta.db')
        cursor = conn.cursor()
        # Execute the query to fetch all data
        cursor.execute("SELECT * FROM your_table_name")
        data = cursor.fetchall()
        # Extract column headers
        headers = [description[0] for description in cursor.description]
        # Write data to CSV file
        output_file_path = os.path.join(self.db_directory_path, F'moneta_{systeminfo.timestamp}.csv')
        with open(output_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(headers)  # Write headers
            csv_writer.writerows(data)  # Write data rows
        # Close the database connection
        conn.close()
        print(F"Exported Moneta DB: {self.db_directory_path}/{F'moneta_{systeminfo.timestamp}.csv'}")

    @staticmethod
    def get_db_directory():
        return db_subdirectory_path

    @staticmethod
    def get_cli_directory():
        return rpa_cli_subdirectory_path

    @staticmethod
    def get_server_directory():
        return rpa_server_subdirectory_path

    @staticmethod
    def get_server_project_directory(project_name: Optional[str] = F"RPA Objective::{Artisan.get_current_timestamp()}"):
        rpa_server_project_folder = os.path.join(rpa_server_subdirectory_path, project_name)
        try:
            os.makedirs(rpa_server_project_folder, exist_ok=True)
        except OSError as e:
            print(f"Moneta encountered error creating TruliooME Data Persistence: {e}")
        return rpa_server_project_folder

    @staticmethod
    def get_server_project_filepath(rpa_server_project_folder:str, file_name: str):
        return os.path.join(rpa_server_project_folder, F"{file_name}")

    @staticmethod
    def get_server_downloads_directory():
        return rpa_server_downloads_path

