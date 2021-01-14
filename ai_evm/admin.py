from django.contrib import admin
from .models import Voter, Party, Vote


# Register with admin app
admin.site.register(Voter)
admin.site.register(Party)
admin.site.register(Vote)