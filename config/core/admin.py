from django.contrib import admin
from django.http import HttpRequest
from .models import Signatory, Element, LabelTemplate

#admin.site.register(model here)
admin.site.register(Signatory)

admin.site.register(Element)

@admin.register(LabelTemplate)
class templateAdmin(admin.ModelAdmin):
    list_display = ()

    #adding and editing done through custom page
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    #only allow delete from admin page
    def has_delete_permission(self, request, obj=None):
        return True