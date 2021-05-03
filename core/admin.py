from django.contrib import admin
from .models import Group, Transactions, Notice, Question, Answer

# Register your models here.

admin.site.register(Group)
admin.site.register(Transactions)
admin.site.register(Notice)
admin.site.register(Question)
admin.site.register(Answer)