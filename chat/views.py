from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Room, Message
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
import google.generativeai as palm
import os
import threading
# Create your views here.
os.environ['API_KEY']= 'AIzaSyB5xBomrmwEg5Eu4ZUxjuv6nwvxDamG5yE'
palm.configure(api_key=os.environ['API_KEY'])
def home(request):
    return render(request, 'home.html')
    

def checkview(request):
    room = request.POST['roomNumber']
    username = request.POST['username']
    if Room.objects.filter(name = room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

# def send(request):
#     message = request.POST['message']
#     username = request.POST['username']
#     room_id = request.POST['room_id']
#     new_message = Message.objects.create(value = message, user = username, room = room_id)
#     new_message.save()

#     prompt = f'''{new_message.value}'''
#     completion = palm.generate_text(
#         model="models/text-bison-001",
#         prompt=prompt,
#         temperature=0,
#         max_output_tokens=800,
#     )
#     botresponse = completion.result
#     username = 'ChatbotAKR'
#     room_id = request.POST['room_id']
#     new_message = Message.objects.create(value = botresponse, user = username, room = room_id)
#     new_message.save()
#     return HttpResponse('Message sent successfully')
    
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()

    prompt = f'{new_message.value}'

    # # Define a function to generate the AI response
    # def generate_ai_response(prompt):
    #     completion = palm.generate_text(
    #         model="models/text-bison-001",
    #         prompt=prompt,
    #         temperature=0,
    #         max_output_tokens=800,
    #     )
    #     return completion.result

    # # Start a new thread to generate the AI response
    # ai_thread = threading.Thread(target=generate_ai_response, args=(prompt,))
    # ai_thread.start()

    # # Wait for the AI thread to finish and get the response
    # ai_thread.join(timeout=120)  # Wait for up to 120 seconds (adjust as needed)

    # # Check if the AI response is available
    # if ai_thread.is_alive():
    #     # If the AI thread is still alive, it means it hasn't finished within the timeout
    #     # Handle the case where the AI response is not available within the timeout
    #     return HttpResponse('AI response not available within the timeout.')
    # else:
    #     # If the AI thread has finished within the timeout, get the response
    #     botresponse = ai_thread.result

    #     username = 'ChatbotAKR'
    #     room_id = request.POST['room_id']
    #     new_message = Message.objects.create(value=botresponse, user=username, room=room_id)
    #     new_message.save()
    #     return HttpResponse('Message sent successfully')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name = room)

    return render(request, 'room.html', {'username': username, 'room': room, 'room_details': room_details})

def getMessages(request, room):
    room_details = Room.objects.get(name = room)
    messages = Message.objects.filter(room = room_details.id)
    return JsonResponse({'messages': list(messages.values())})

# def chatbot(request, room):
#     room_details = Room.objects.get(name = room)
#     message = Message.objects.filter(room = room_details.id)
#     message1 = list(message.values)

#     os.environ['API_KEY']= 'AIzaSyB5xBomrmwEg5Eu4ZUxjuv6nwvxDamG5yE'
#     palm.configure(api_key=os.environ['API_KEY'])

#     prompt = f'''{message1[len(message1)-1]}'''
#     completion = palm.generate_text(
#         model="models/text-bison-001",
#         prompt=prompt,
#         temperature=0,
#         max_output_tokens=800,
#     )
#     botresponse = completion.result
#     username = 'ChatbotAKR'
#     room_id = request.POST['room_id']
#     new_message = Message.objects.create(value = botresponse, user = username, room = room_id)
#     new_message.save()
#     return HttpResponse('Message sent successfully')