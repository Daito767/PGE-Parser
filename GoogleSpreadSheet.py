import os.path
from ColoredText import *
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime


class SpreadSheetAPI:
	def __init__(self):
		self.equivalent_pge_column_names = {'Latitude': 'GPSLATITUDE', 'Longitude': 'GPSLONGITUDE', 'Survey Date': 'Visitdate', 'JP Number-SEQ': 'JPNUMBER', 'ADRESS': 'LOCDESC1', 'Manufacture Year': 'INSTALLATIONDATE', 'Species': 'SPECIES', 'Class': 'CLASS', 'Height': 'HEIGHT', 'OriginalCircumference': 'Currentcirc', 'EffectiveCircumference': 'Effectcirc', 'CalculationResult': 'Woodstrength'}
		self.pge_inspection_column_names = {'Survey Date', 'OriginalCircumference', 'EffectiveCircumference', 'CalculationResult'}
		self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
		self.creds = None
		self.service = None
		self.sheet = None

	def try_to_authorize(self) -> bool:
		print_yellow('[INFO]')
		print(' Trying authorization to google api')

		if os.path.exists('token.json'):
			self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
		else:
			println_red('[ERROR]')
			print(' Google token was not found')
			return False

		if self.creds:
			if not self.creds.valid and self.creds.expired and self.creds.refresh_token:
				self.creds.refresh(Request())
		else:
			print_red('[WARNING]')
			print(' Credentials not found')
			return False

		try:
			self.service = build('sheets', 'v4', credentials=self.creds)
			self.sheet = self.service.spreadsheets()

			print_green('[INFO]')
			print(' Successful authorized')
			return True

		except Exception as e:
			println_red('[ERROR]')
			print(f' Authorization failed. {e}')

		return False

	def identify_necessary_data(self, sheet_id: str, sap_ids_range: str = 'B2:B', searched_info_range: str = 'C1:Z1') -> list[list[str], list[str]]:
		sap_ids = self.sheet.values().get(spreadsheetId=sheet_id, range=sap_ids_range, majorDimension='COLUMNS').execute()['values'][0]
		searched_info = self.sheet.values().get(spreadsheetId=sheet_id, range=searched_info_range, majorDimension='ROWS').execute()['values'][0]

		print_yellow('[INFO]')
		print(' The searched parameters of the poles:', searched_info)

		print_yellow('[INFO]')
		print(' The sap id of the identified poles:', sap_ids)

		return [searched_info, sap_ids]

	def populate_poles(self, sheet_id: str, range_values: str, searched_data: list, poles_data: list):
		print_yellow('[INFO]')
		print(' The collected data is analyzed')

		sheet_values = []

		for pole_sap_id in poles_data:
			pole_sheet_values = []
			column_names = searched_data[0]

			if not pole_sap_id.isnumeric():
				for col_name in column_names:
					pole_sheet_values.append('')

				sheet_values.append(pole_sheet_values)
				continue

			general_data = poles_data[pole_sap_id][0]
			inspection_data = poles_data[pole_sap_id][1]

			for col_name in column_names:
				if col_name not in self.equivalent_pge_column_names.keys():
					pole_sheet_values.append('')
					continue

				value = None

				if col_name in self.pge_inspection_column_names:
					if len(inspection_data) > 0:
						value = inspection_data[0][self.equivalent_pge_column_names[col_name]]

						if col_name == 'CalculationResult' and value == 0:
							value = 100
						elif col_name == 'Survey Date' and value is not None:
							value = str(value)
							value = value.replace('/Date(', '').replace(')/', '')
							time = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(int(value) / 1000))
							value = f'{time.month}/{time.day}/{time.year}'

				else:
					value = general_data[self.equivalent_pge_column_names[col_name]]
					if col_name == 'Species':
						if value == 'WC':
							value = 'WCP'
						elif value == 'DF' or value is None:
							value = 'DFP'

					elif col_name == 'JP Number-SEQ' and general_data["JPSEQUENCE"] is not None:
						value += f'-{general_data["JPSEQUENCE"]}'
					elif col_name == 'Manufacture Year' and value is not None:
						time = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(value/1000))
						value = time.year

				if value is None:
					value = ''

				pole_sheet_values.append(value)

			sheet_values.append(pole_sheet_values)

		data = [{'range': range_values, 'values': sheet_values}]

		budy = {'valueInputOption': 'USER_ENTERED', 'data': data}

		print_green('[INFO]')
		print(' The data were analyzed without errors')

		result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body=budy).execute()

		print_green('[INFO]')
		print(' The data was published successfully')

	def populate_pole(self, sheet_id: str, values_range: str, general_data: dict, inspection_data: dict, column_names: list):
		values = []

		for col_name in column_names:
			if col_name not in self.equivalent_pge_column_names.keys():
				values.append(None)
				continue

			value = None

			if col_name in self.pge_inspection_column_names:
				if len(inspection_data) > 0:
					value = inspection_data[0][self.equivalent_pge_column_names[col_name]]

					if col_name == 'CalculationResult' and value == 0:
						value = 100
					elif col_name == 'Survey Date' and value is not None:
						value = str(value)
						value = value.replace('/Date(', '').replace(')/', '')
						time = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(int(value) / 1000))
						value = f'{time.month}/{time.day}/{time.year}'

			else:
				value = general_data[self.equivalent_pge_column_names[col_name]]
				if col_name == 'Species':
					if value == 'WC':
						value = 'WCP'
					elif value == 'DF' or value is None:
						value = 'DFP'

				elif col_name == 'JP Number-SEQ' and general_data["JPSEQUENCE"] is not None:
					value += f'-{general_data["JPSEQUENCE"]}'
				elif col_name == 'Manufacture Year' and value is not None:
					time = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(value/1000))
					value = time.year

			if value is None:
				value = ''

			values.append(value)

		data = [{'range': values_range, 'values': [values]}]

		budy = {'valueInputOption': 'USER_ENTERED', 'data': data}

		result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body=budy).execute()
