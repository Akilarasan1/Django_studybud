from django.contrib import admin

# Register your models here.
from .models import Room, Topic, CustomMessage#, MessagesUser

admin.site.register(Room)
admin.site.register(CustomMessage)
admin.site.register(Topic)


#admin.site.register(MessagerUser)
