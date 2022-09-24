from django.contrib import admin

from .models import Usernew, Ask, Reply, Bad, Solved, Chat, Yes

admin.site.register(Ask)
admin.site.register(Reply)
admin.site.register(Usernew)
admin.site.register(Bad)
admin.site.register(Solved)
admin.site.register(Chat)
admin.site.register(Yes)