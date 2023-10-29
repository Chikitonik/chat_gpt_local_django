from .models import QueryLog
from django.shortcuts import render, redirect
import os
from user_auth.models import UserProfile
from django.conf import settings

from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
# from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
# https://stackoverflow.com/questions/76950609/what-is-the-difference-between-openai-and-chatopenai-in-langchain
# answer = index.query(query, llm=OpenAI())
# answer = index.query(query, llm=ChatOpenAI())

# DESTINATION_PATH_FILE_DATA = 'C:/dev/chat_gpt_local_django/chat_gpt_local/chat_gpt/media/data.txt'
RELATIVE_DATA_DIR = 'media\\user_data\\'


def home(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_data_dir = os.path.join(
            settings.BASE_DIR, RELATIVE_DATA_DIR, str(current_user.id))
        os.makedirs(user_data_dir, exist_ok=True)
        user_data_file = os.path.join(user_data_dir, 'data.txt')
        # print('=============user_data_file===========')
        # print(user_data_file)

        context = {
            # 'api_key': api_key,
            # 'DESTINATION_PATH_FILE_DATA': DESTINATION_PATH_FILE_DATA,
            'DESTINATION_PATH_FILE_DATA': user_data_file,
        }
        try:

            user_profile = request.user.userprofile
            api_key = user_profile.api_key
            context = {
                'api_key': api_key,
            }
            # data_path = ''
            answer = ''
            query = ''
            file_name = None

            if request.method == 'POST':
                file_name = request.FILES.get('data')
                query = request.POST.get('query')
                if file_name:
                    try:
                        # with open(DESTINATION_PATH_FILE_DATA, 'w', encoding='utf-8', newline='') as file:
                        with open(user_data_file, 'w', encoding='utf-8', newline='') as file:
                            file.write(f"Filename: {file_name.name}\n")
                            new_data_information = file_name.read().decode('utf-8')
                            file.write(new_data_information)
                    except Exception as e:
                        print(f"Error writing to the file: {str(e)}")
                # try:
                    # os.environ["OPENAI_API_KEY"] = api_key
                    # #loader = TextLoader(
                    # #    user_data_file, encoding='utf-8')
                    # loader = TextLoader(
                    #    user_data_file, encoding='utf-8')
                    # # loader = DirectoryLoader(
                    # # 'C:/dev/chat_gpt_local_django/chat_gpt_local/chat_gpt/media/', glob="*.txt")
                    # index = VectorstoreIndexCreator().from_loaders([loader])
                    # answer = index.query(query)
                # except Exception as e:
                #     answer = f'ERROR: {str(e)}'

            # if answer != '':
                if answer == '':
                    if not file_name:
                        try:
                            # with open(DESTINATION_PATH_FILE_DATA, 'r', encoding='utf-8') as file:
                            with open(user_data_file, 'r', encoding='utf-8') as file:
                                file_name = file.readline()
                                file_name = file_name.replace('Filename: ', '')
                        except FileNotFoundError:
                            file_name = 'not found'
                    log_entry = QueryLog(
                        user=request.user, query=query, answer=answer, file_name=file_name)
                    log_entry.save()
                context = {
                    'answer': answer,
                    # 'data_path': data_path,
                    'data_path': user_data_file,
                    'query': query,
                    # 'DESTINATION_PATH_FILE_DATA': DESTINATION_PATH_FILE_DATA,
                    'DESTINATION_PATH_FILE_DATA': user_data_file,
                }

            return render(request, 'homepage.html', context)
        except UserProfile.DoesNotExist:
            # Handle the case where the user profile doesn't exist
            # This may happen if the user profile hasn't been created yet
            return redirect('profile_creation_view')
    else:
        # Handle the case where the user is not authenticated
        # You can redirect them to a login page or show an error message
        return redirect('login')  # Redirect to the login page


def query_log(request):
    if request.user.is_authenticated:
        user_logs = QueryLog.objects.filter(
            user=request.user).order_by('-timestamp')
        context = {
            'user_logs': user_logs,
        }
        return render(request, 'logs.html', context)

    else:
        return redirect('login')
