from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import FriendRequest, Message
from django.db.models import Q
from django.db.utils import IntegrityError

@api_view(["GET"])
def dashboard(request):
    return render(request, "dashboard.html")


@api_view(["GET", "POST"])
def find_people(request):
    if request.method == "GET":
        data_obj = User.objects.filter().exclude(id=request.user.id)
        status_obj = FriendRequest.objects.filter(from_user=request.user)
        sent_requests = {
            friend_request.to_user.id: True for friend_request in status_obj
        }
        return render(
            request,
            "master/find_people.html",
            {"data_obj": data_obj, "sent_requests": sent_requests},
        )
    else:
        return render(request, "dashboard.html")


@api_view(["GET", "POST"])
def incoming_requests(request):
    if request.method == "GET":
        friend_requests = FriendRequest.objects.filter(
            to_user=request.user, status="pending"
        )
        print("friend_requests",friend_requests)
        return render(
            request,
            "master/incoming_requests.html",
            {"friend_requests": friend_requests},
        )
    elif request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        try:
            friend_request = FriendRequest.objects.get(
                id=request_id, to_user=request.user
            )
            if action == "accept":
                friend_request.status = "accepted"
            elif action == "reject":
                friend_request.status = "rejected"
            friend_request.save()
            return JsonResponse({"status": "success"})
        except FriendRequest.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Request not found"}, status=404
            )


@api_view(["GET", "POST"])
def request_user(request):
    if request.method == "POST":
        is_ajax = request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        if is_ajax:
            user_id = request.POST["user_id"]
            print(user_id)
            user_instance = User.objects.get(id=user_id)
            try:
                status_obj = FriendRequest.objects.get(
                    from_user=request.user, to_user=user_instance
                ) # noqa
                status = "Request already sent"
            except FriendRequest.DoesNotExist:
                status_obj = FriendRequest.objects.create(                # noqa
                    from_user=request.user, to_user=user_instance
                )
                status = "Request sent successfully"

            return JsonResponse({"status": status}, status=200)
    return JsonResponse({"status": "Invalid request"}, status=400)


@api_view(["GET"])
def friends_list(request):
    friends = User.objects.filter(
        id__in=FriendRequest.objects.filter(
            from_user=request.user, status="accepted"
        ).values_list("to_user_id", flat=True)
    ) | User.objects.filter(
        id__in=FriendRequest.objects.filter(
            to_user=request.user, status="accepted"
        ).values_list("from_user_id", flat=True)
    )
    return render(request, "master/friends_list.html", {"friends": friends})


@api_view(["GET", "POST"])
def chat(request, user_id=None):
    if user_id:
        friend_requests = FriendRequest.objects.filter(
            Q(from_user=request.user, to_user_id=user_id, status="accepted")
            | Q(from_user_id=user_id, to_user=request.user, status="accepted")
        )
        if not friend_requests.exists():
            return redirect("friends_list")

    if request.method == "GET":
        messages = []
        if user_id:
            messages = Message.objects.filter(
                (Q(sender=request.user) & Q(receiver_id=user_id))
                | (Q(sender_id=user_id) & Q(receiver=request.user))
            ).order_by("timestamp")
        return render(
            request, "master/chat.html", {
                "messages": messages,
                "user_id": user_id
                }
        )

    elif request.method == "POST":
        message_text = request.POST.get("message")
        receiver_id = request.POST.get("receiver_id")
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(
            sender=request.user, receiver=receiver, message=message_text
        )
        return JsonResponse(
            {
                "status": "success",
                "message": message.message,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


@api_view(["GET"])
def get_messages(request, user_id):
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver_id=user_id))
        | (Q(sender_id=user_id) & Q(receiver=request.user))
    ).order_by("timestamp")
    return JsonResponse(
        {
            "messages": [
                {
                    "sender": msg.sender.username,
                    "message": msg.message,
                    "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for msg in messages
            ]
        }
    )


@api_view(["GET", "POST"])
def signup(request):
    if request.method == "GET":
        return render(request, "master/signup.html")
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            # Check if the user already exists by email
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User already exists."})

            # Create the user with hashed password
            user = User.objects.create_user(             # noqa
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )

            # return JsonResponse({"success": "User created successfully."})
            return HttpResponseRedirect("/")

        except IntegrityError as e:
            print(str(e))
            return JsonResponse({"error": "Username already exists."})

        except Exception as e:
            # General exception handling
            return JsonResponse({"error": str(e)})
