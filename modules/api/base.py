

class BaseInterface:

    def __init__(self, token):
        self.token = token
        self.url = f"http://finance-tracking.ru/api/{token}"

    
    def return_json(self, responce, status_code):

        if responce.status_code == status_code:
            
            if status_code == 204:
                return True
            
            return responce.json()
        else:
            return False