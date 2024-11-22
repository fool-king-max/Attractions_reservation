# -*- coding:utf-8 -*-
"""

作者：忽悠王的世界
日期：2024年11月22日
"""
from django.contrib.sessions.models import Session
Session.objects.all().delete()
