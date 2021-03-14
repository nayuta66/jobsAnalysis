from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)
