
class Zendesk:
    @classmethod
    def zendesk_create_api(cls, ticket_obj=None):
        if not ticket_obj:
            return True, None
        try:
            from utils.ExternalApiCall import ExternalApi
            from utils.Constants import ZENDESK_API_URL, ZENDESK_API_TOKEN
            data = {
                "ticket": {
                    "comment": {
                        "body": ticket_obj.description
                    },
                    "priority": ticket_obj.priority,
                    "subject": ticket_obj.subject
                }
            }
            headers = {
                "Authorization": f"Basic {ZENDESK_API_TOKEN}"
            }
            is_successful, response = ExternalApi(url=ZENDESK_API_URL, data=data, headers=headers).post()
            if response.get('ticket'):
                ticket_obj.zendesk_ticket_id = response['ticket'].get('id')
                ticket_obj.save()
            return True, None
        except Exception as e:
            return False, str(e)

    @classmethod
    def get_zendesk_ticket_detail(cls, ticket_id):
        if not ticket_id:
            return True, None
        try:
            from utils.ExternalApiCall import ExternalApi
            from utils.Constants import ZENDESK_API_URL, ZENDESK_API_TOKEN
            headers = {
                "Authorization": f"Basic {ZENDESK_API_TOKEN}"
            }
            url = f'{ZENDESK_API_URL}{ticket_id}.json'
            return ExternalApi(url=url, headers=headers).get()
        except Exception as e:
            return False, str(e)
        return True, None

    @classmethod
    def delete_zendesk_ticket(cls, zendesk_ticket_id):
        try:
            from utils.ExternalApiCall import ExternalApi
            from utils.Constants import ZENDESK_API_URL, ZENDESK_API_TOKEN
            headers = {
                "Authorization": f"Basic {ZENDESK_API_TOKEN}"
            }
            ExternalApi(url=f'{ZENDESK_API_URL}{zendesk_ticket_id}', headers=headers).delete()
        except Exception as e:
            return False, str(e)
        return True, None

