from local_settings import api_token, json_keyfile, google_sheets_file
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import requests


class Pipedrive(object):

    def __init__(self):
        self.api_token = api_token

    def get_deal(self, deal_id):
        endpoint = 'https://api.pipedrive.com/v1/deals/' + str(deal_id) + '?api_token=' + self.api_token
        r = requests.get(endpoint)
        data = r.json()

        return data

    def get_deals(self):

        endpoint = 'https://api.pipedrive.com/v1/deals?api_token=' + self.api_token
        r = requests.get(endpoint)
        data = r.json()

        return data

    def get_activities(self, deal_id):
        endpoint = 'https://api.pipedrive.com/v1/deals/' + str(deal_id) + '/activities?start=0&api_token=' + self.api_token
        r = requests.get(endpoint)
        data = r.json()

        return data

    def post_activities(self, deal_id, params):
        endpoint = 'https://api.pipedrive.com/v1/activities?api_token=' + self.api_token
        r = requests.post(endpoint, json=params)
        data = r.json()

        return data


class GoogleSheet(object):

    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, self.scope)
        self.authorize = gspread.authorize(self.credentials)
        self.past_data_file = self.authorize.open_by_url(google_sheets_file)
        self.past_data_sheet = self.past_data_file.get_worksheet(0)
        self.deal_row = ''

    def get_past_email_count(self, deal_id):

        past_data_sheet = self.past_data_file.get_worksheet(0)
        past_data_ids_list = past_data_sheet.col_values(1)
        if deal_id in past_data_ids_list:
            for i in range(len(past_data_ids_list)):
                if past_data_ids_list[i] == deal_id:
                    self.deal_row = i + 1
                    return past_data_sheet.cell(i + 1, 5).value
                else:
                    pass
        else:
            self.deal_row = 0
            return 'new'

    def save_past_email_data(self, deal_id, title, last_activity_date, last_incoming_mail_time, email_message_count, user_id):

        if self.deal_row == 0:
            row_content = list()
            row_content.append(deal_id)
            row_content.append(title)
            row_content.append(last_activity_date)
            row_content.append(last_incoming_mail_time)
            row_content.append(email_message_count)
            row_content.append(user_id)
            self.past_data_sheet.append_row(row_content)
            print 'Added to Google Sheets'
        elif self.deal_row > 0:
            row_reference = self.past_data_sheet
            row_reference.update_cell(self.deal_row, 1, deal_id)
            row_reference.update_cell(self.deal_row, 2, title)
            row_reference.update_cell(self.deal_row, 3, last_activity_date)
            row_reference.update_cell(self.deal_row, 4, last_incoming_mail_time)
            row_reference.update_cell(self.deal_row, 5, email_message_count)
            row_reference.update_cell(self.deal_row, 6, user_id)
            print 'Updated in Google Sheets'
