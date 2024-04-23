from dataclasses import dataclass
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore
import ast  

@dataclass
class Customer:
    """
    Data class for storing customer information.
    Attributes:
        ip_address (str): The IP address of the customer.
        name (str, optional): The name of the customer.
        phone_number (str, optional): The phone number of the customer.
        email (str, optional): The email address of the customer.
    """
    ip_address: str
    name: str = None
    phone_number: str = None
    email: str = None

class DataManager:
    """
    Manages data parsing and storage using Firebase and OpenAI.
    """
    def __init__(self, api_key: str, firebase_id: str = None):
        """
        Initializes the DataManager with necessary API key and optional Firebase project ID.
        Args:
            api_key (str): The API key for accessing OpenAI's services.
            firebase_id (str, optional): The Firebase project ID for initializing Firebase admin.
        """
        self.customers = {}
        self.cache = {}
        self.client = OpenAI(api_key=api_key)
        self.firebase_id = firebase_id
        self.firestoreClient = self._initialize_firebase()

    def _initialize_firebase(self):
        """
        Initializes the Firebase application and returns the Firestore client.
        If Firebase app is already initialized, it reuses the existing app.
        Returns:
            Firestore client for interacting with the database.
        """
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase.json")
            firebase_admin.initialize_app(cred, {'projectId': self.firebase_id})
        return firestore.client()

    async def parse_and_store_data(self, ip_address: str, prompt: str):
        """
        Parses the prompt using OpenAI and stores the extracted data in Firestore.
        Args:
            ip_address (str): The IP address of the user sending the prompt.
            prompt (str): The text prompt to process.
        """
        if prompt == "Hello Samm, I need help with my renovation project." or prompt in self.cache:
            return

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "Extract names, phone numbers, and emails from the text. Return 'FALSE' if none or format as ['name': 'name?', 'email': 'email?', 'phone': 'phone?']."},
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.choices[0].message.content

            if content == "FALSE":
                self._update_prompt_list(ip_address, prompt)
                return
            else:
                content = content.replace("[", "{").replace("]", "}")
                content_dict = ast.literal_eval(content)

            name = content_dict.get('name', None)
            phone_number = content_dict.get('phone', None)
            email = content_dict.get('email', None)
            self._update_prompt_list(ip_address, prompt)

        except Exception as e:
            print(f"Error while calling GPT-3 API: {e}")

        self.store_customer_data(ip_address, name, phone_number, email)

    def _update_prompt_list(self, ip_address, prompt: str):
        """
        Updates the list of prompts for a specific IP address in Firestore.
        Args:
            ip_address (str): The IP address of the user.
            prompt (str): The prompt to add to the list.
        """
        db = firestore.client()
        doc_ref = db.collection('chatlogs').document(ip_address)
        doc_ref.set({
            'prompt_list': firestore.ArrayUnion([prompt])
        }, merge=True)

    def store_customer_data(self, ip_address, name=None, phone_number=None, email=None):
        """
        Stores customer data in Firestore.
        Args:
            ip_address (str): The IP address of the user.
            name (str, optional): The customer's name.
            phone_number (str, optional): The customer's phone number.
            email (str, optional): The customer's email address.
        """
        db = firestore.client()
        doc_ref = db.collection('chatlogs').document(ip_address)
        data = {k: v for k, v in {'name': name, 'phone_number': phone_number, 'email': email}.items() if v}
        doc_ref.set(data, merge=True)
