from django.db import models
import uuid
import json
from django.contrib.auth.models import User


class SignTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), verbose_name='UUID')
    title = models.CharField(max_length=20, verbose_name='任务名')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='上传者')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    stop = models.BooleanField(verbose_name='状态', default=False)

    def __str__(self):
        return json.dumps({
            'id': str(self.id),
            'title': self.title,
            'uploader': self.uploader.username,
            'upload_time': str(self.upload_time),
            'stop': '已结束' if self.stop else '进行中'
        })

    def __repr__(self):
        return json.dumps({
            'id': str(self.id),
            'title': self.title,
            'uploader': self.uploader.username,
            'upload_time': str(self.upload_time),
            'stop': '已结束' if self.stop else '进行中'
        })


class SignLog(models.Model):
    openid = models.CharField(max_length=30, verbose_name='用户ID')
    username = models.CharField(max_length=20, verbose_name='用户名')
    sign_task = models.ForeignKey(SignTask, on_delete=models.CASCADE, verbose_name='签到任务')
    sign_time = models.DateTimeField(verbose_name='签到时间', auto_now_add=True)

    def __str__(self):
        return json.dumps({
            "openid": self.openid,
            "username": self.username,
            "sign_task": self.sign_task.title,
            "sign_time": str(self.sign_time)
        })

    def __repr__(self):
        return self.__str__()
