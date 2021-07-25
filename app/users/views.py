from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from users.models import User, Invite
from users.serializers import UserSerializer
from .forms import LoginForm, SignUpForm
from .helper import account_activation_token

response_schema_dic = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "200": "200_value_1",
                "200_key2": "200_valu",
            }
        }
    ),
    "205": openapi.Response(
        description="custom 205 description",
        examples={
            "application/json": {
                "205_key1": "205_value_1",
                "205_key2": "205_value_2",
            }
        }
    ),
}


@swagger_auto_schema(operation_description="partial_update description override", responses=response_schema_dic,
                     method='post')
@api_view(['POST'])
def current_user(request):
    current_user = request.user
    return current_user.id


@api_view(['POST'])
def login_view_alt(request):
    return True


@api_view(['POST'])
def password_reset(request):
    return True


@api_view(['POST'])
def new_password(request):
    return True


@api_view(['POST'])
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


@api_view(['POST'])
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('SAVING THE FORM!!!')
            password11 = form.clean_password2()
            User.objects.create_user(email=form.cleaned_data['email'], password=password11)
            # form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                return HttpResponse('User is not authenticated')

            msg = 'Please confirm your email address to complete registration.'
            success = True

            invitation = Invite.objects.filter(receiver=user.email)
            for invite in invitation:
                # add the user to the corresponding Organization
                # registered_user = User.objects.get(email=email)
                user.organizations.add(invite.organization)
                for gr in invite.groups:
                    user.groups.add(gr)

            # whether user has been invited or not, get user to confirm email address
            user.is_active = True  # False
            user.save()

            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(message)
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            # last_ten_feedbacks = Feedback.objects.all().order_by('-id')[:10]
            # last_ten_requests = Request.objects.all().order_by('-id')[:10]
            return render(request, "/email-confirmation.html", {"msg": msg, "success": success})
            # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
            # return render(request, "/register-company.html", {"form": company_form, "msg" : msg, "success" : success})

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


@api_view(['POST'])
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return render(request, "/login.html", {"msg" : "Activation link is invalid!", "success" : False})
        redirect("/login/")
    else:
        return render(request, "email-confirmation.html", {"msg": "Activation link is invalid!", "success": False})
        # return HttpResponse('Activation link is invalid!')


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(ViewSet, APIView):
    serializer_class = AuthTokenSerializer
    permission_classes = []

    def create(self, request):
        return ObtainAuthToken().post(request)


class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
