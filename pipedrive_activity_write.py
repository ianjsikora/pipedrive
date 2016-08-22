from pipedrive_activity_get import Pipedrive, GoogleSheet


def get_deal_data():

    p_deal = p_object.get_deals
    p_deal_data = p_deal()['data']

    return p_deal_data


def print_deal_id():

    deal_data = get_deal_data()
    google_sheet_get_email_count = gd_object.get_past_email_count

    for deal in range(len(deal_data)):

        deal_list = deal_data[deal]
        deal_id = deal_list['id']
        title = deal_list['title']
        last_activity_date = deal_list['last_activity_date']
        last_incoming_mail_time = deal_list['last_incoming_mail_time']
        email_message_count_temp = deal_list['email_messages_count']
        if email_message_count_temp == None:
            email_message_count = 0
        elif email_message_count_temp > 0:
            email_message_count = email_message_count_temp
        user_id = deal_list['user_id']['id']

        google_sheet_data = google_sheet_get_email_count(str(deal_id))

        if google_sheet_data == 'new':
            params = dict()
            params['user_id'] = user_id
            params['subject'] = str(email_message_count) + ' Emails sent to date'
            params['done'] = '1'
            params['type'] = 'daily_email_count'
            params['deal_id'] = deal_id
        else:
            params = dict()
            params['user_id'] = user_id
            params['subject'] = str(email_message_count - int(google_sheet_data)) + ' Emails sent since ' + str(last_activity_date)
            params['done'] = '1'
            params['type'] = 'daily_email_count'
            params['deal_id'] = deal_id
        print '==========================================='
        print 'Updating ' + title
        print params

        post_activities_request = p_object.post_activities(deal_id, params)
        print post_activities_request

        google_sheet_save = gd_object.save_past_email_data(deal_id, title, last_activity_date, last_incoming_mail_time, email_message_count, user_id)
        print google_sheet_save

p_object = Pipedrive()
gd_object = GoogleSheet()
print print_deal_id()
