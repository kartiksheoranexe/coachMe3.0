from main.models import CustomUser, Coach, Client

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError



def create_private_channel(slack_client, coach, cl):
    
    try:
        # Generate channel name using coached, client, and package data
        channel_name = f"{coach.user.username}-{cl.user.username}"
        print(channel_name)

        # List all private channels in the workspace
        response = slack_client.conversations_list(
            types="private_channel"
        )
        print(response)
   
        # Search for a private channel with the desired name
        channel_id = None
        for channel in response["channels"]:
      
            if channel["name"] == channel_name:
         
                channel_id = channel["name"]
                break

        # If the channel does not exist, create it
        if channel_id is None:
          
            response = slack_client.conversations_create(
                name=channel_name,
                is_private=True
            )
      
            channel_id = response["channel"]["name"]

        # Store the channel ID in the client model
        cl.channel_id = channel_id
        cl.save()

        print(f"Private channel created or fetched: {channel_name}")
    except SlackApiError as e:
        print("Error creating or fetching")

def send_message(slack_client, coach, client, message):
    try:
        response = slack_client.chat_postMessage(
            channel=client.channel_id,
            text=f"{coach}: {message}"
        )
        print(response)
    except SlackApiError as e:
        print("Error sending message: {}".format(e))

def send_coach_message(slack_client, coach, cl, message):
    c_user = CustomUser.objects.get(username=coach)
    coached = Coach.objects.get(user=c_user)
    client = cl
    print(client)
    send_message(slack_client, coach, client, message)

def send_client_message(slack_client, client, message):
    cl_user = CustomUser.objects.get(username=client)
    cl = Client.objects.get(user=cl_user)
    print(cl)
    coach = cl.coach
    send_message(slack_client, coach, cl, message)

@csrf_exempt
def communicate(request):
    slack_app_token = os.environ["SLACK_APP_TOKEN_USER"]
    slack_client = WebClient(slack_app_token)

    coach_user = request.POST.get("coach_user")
    client_user = request.POST.get("client_user")
    message = request.POST.get("message") 
    c_user = CustomUser.objects.get(username=coach_user)
    cl_user = CustomUser.objects.get(username=client_user)  
    coach = Coach.objects.get(user=c_user)
    cl = Client.objects.get(user=cl_user)
    create_private_channel(slack_client, coach, cl)
    
    if coach.user == c_user:
        send_coach_message(slack_client, coach, cl, message)
    elif cl.user == cl_user:
        send_client_message(slack_client, cl, message)
    
    return JsonResponse({"success": True})