from django.views import View
from django.contrib.auth.models import User
from .models import SignTask, SignLog
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core import serializers
import json


class LoginView(View):

    def get(self, request):
        username = request.GET.get("username", None)
        password = request.GET.get("password", None)
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(data={"message": "登陆成功！"})
            else:
                return JsonResponse(status=404, data={"message": "登陆失败！"})
        else:
            return JsonResponse(status=404, data={"message": "用户名或密码不得为空！"})

    def post(self, request):
        pass


class TaskView(View):

    def get(self, request):
        di = {}
        tasks = serializers.serialize("json", SignTask.objects.all().order_by("-upload_time"))
        # di = json.loads(json.dumps(di))
        return JsonResponse(data={"tasks": tasks})

    def post(self, request):
        message = json.loads(request.body.decode())
        username = message.get("nickName", None)
        openid = message.get("openid", "12138")
        pk = message.get("pk", None)
        sign = SignLog(openid=openid, username=username, sign_task=SignTask.objects.get(pk=pk))
        sign.save()
        return JsonResponse(data={"message": username + "签到成功！"})


class GetTaskManagerView(View):

    def get(self, request):
        pk = request.GET.get("pk", None)
        logs = SignLog.objects.filter(sign_task__id=pk)
        if len(logs) == 1:
            return JsonResponse(data={"logs": str(logs[0])})
        elif len(logs) == 0:
            return JsonResponse(status=400, data={"message": "当前没有签到记录！"})

        return JsonResponse(data={"logs": serializers.serialize("json", logs)})


class GetTaskView(View):
    def get(self, request):
        pk = request.GET.get("pk", None)
        if pk:
            task = SignTask.objects.get(pk=pk)
            return JsonResponse(data={"task": str(task)})


class SignView(View):

    def get(self, request):
        username = request.GET.get("username", None)
        if username:
            tasks = SignTask.objects.filter(uploader__username=username)
            if len(tasks) == 0:
                return JsonResponse(status=400, data={"message": "没有任何签到任务！"})
            elif len(tasks) == 1:
                return JsonResponse(data={"tasks": str(tasks[0])})
            return JsonResponse(data={"tasks": serializers.serialize("json", tasks)})

    def post(self, request):
        message = json.loads(request.body.decode())

        title = message.get("title", None)
        uploader = message.get("username", None)
        uploader = User.objects.get(username=uploader)
        if title and uploader:
            task = SignTask(title=title, uploader=uploader)
            task.save()
            return JsonResponse(data={"message": title + "添加成功！"})
        else:
            return JsonResponse(status=404, data={"message": "信息不能为空！"})


class TaskDetailView(View):

    def get(self, request):
        pk = request.GET.get("pk", None)
        logs = serializers.serialize("json", SignLog.objects.filter(sign_task=SignTask.objects.filter(pk=pk)))
        return JsonResponse(data={"logs": logs})