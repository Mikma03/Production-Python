# requirements.txt

# certifi==2022.6.15
# cffi==1.15.1
# charset-normalizer==2.1.0
# cryptography==37.0.4
# django-environ==0.9.0
# et-xmlfile==1.1.0
# idna==3.3
# msal==1.18.0
# Office365-REST-Python-Client==2.3.13
# openpyxl==3.0.10
# pycparser==2.21
# PyJWT==2.4.0
# pytz==2022.1
# requests==2.28.1
# urllib3==1.26.10


from urllib import response
import environ
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
import datetime

env = environ.Env()
environ.Env.read_env()

USERNAME = env('sharepoint_email')
PASSWORD = env('sharepoint_password')
SHAREPOINT_SITE = env('sharepoint_url_site')
SHAREPOINT_SITE_NAME = env('sharepoint_site_name')
SHAREPOINT_DOC = env('sharepoint_doc_library')

class SharePoint:
    def _auth(self):
        conn = ClientContext(SHAREPOINT_SITE).with_credentials(
            UserCredential(
                USERNAME,
                PASSWORD
            )
        )
        return conn

    def _get_files_list(self, folder_name):
        conn = self._auth()
        target_folder_url = f'{SHAREPOINT_DOC}/{folder_name}'
        root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Files", "Folders"]).get().execute_query()
        return root_folder.files    
        
    def get_file_properties_from_folder(self, folder_name):
        files_list = self._get_files_list(folder_name)
        properties_list = []
        for file in files_list:
            file_dict = {
                'file_id': file.unique_id,
                'file_name': file.name,
                'major_version': file.major_version,
                'minor_version': file.minor_version,
                'file_size': file.length,
                'time_created': file.time_created,
                'time_last_modified': file.time_last_modified
            }
            properties_list.append(file_dict)
            file_dict = {}
        return properties_list
    
# 1 args = SharePoint Folder name


def get_properties_by_folder(folder):
    files_properties = SharePoint().get_file_properties_from_folder(folder)
    print('File count:', len(files_properties))
    for file in files_properties:
        print(file)
        

get_properties_by_folder("my/path/here")


root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
root_folder.get().execute_query()
root_folder.expand(["Files", "Folders"]).execute_query()
