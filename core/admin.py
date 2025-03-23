from django.contrib import admin

from .models import BasicInformation, SocialLink, ContactInformation

# Register your models here.
class BasicInformationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow adding only if there are no BasicInformation instances
        return not BasicInformation.objects.exists()

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0  # Change to 0 to make social links optional

class ContactInformationInline(admin.TabularInline):
    model = ContactInformation
    extra = 0  # Change to 0 to make contact information optional

class BasicInformationAdminWithOptionalSocialLink(admin.ModelAdmin):
    inlines = [SocialLinkInline, ContactInformationInline]

admin.site.register(BasicInformation, BasicInformationAdminWithOptionalSocialLink)