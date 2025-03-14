from django.contrib import admin
from .models import App, Screenshot

class ScreenshotAdmin(admin.ModelAdmin):
    """
    Custom admin panel settings for managing user-uploaded screenshots.
    Allows filtering, approving, and rejecting screenshots.
    """

    # Fields to display in the Django Admin list view
    list_display = ('user', 'app', 'status')

    # Sidebar filter to filter screenshots based on status (Pending, Approved, Rejected)
    list_filter = ('status',)

    # Admin actions that allow bulk approval or rejection of screenshots
    actions = ['approve_screenshots', 'reject_screenshots']

    def get_queryset(self, request): # get_queryset is a built-in method of Django's ModelAdmin class.
        """
        Customize the default queryset:
        - Only shows screenshots with 'pending' or 'approved' status.
        - Excludes 'rejected' screenshots from the admin list by default.
        """
        qs = super().get_queryset(request)  # Django provides other built-in functions that you can override in ModelAdmin
        return qs.filter(status__in=["pending", "approved", "rejected"])  # Show only Pending & Approved
        # status__in means: Look at the status field in the Screenshot model.

    def approve_screenshots(self, request, queryset):
        """
        Approve selected screenshots in bulk.
        - Updates the status to 'approved'.
        """
        queryset.update(status="approved")

    def reject_screenshots(self, request, queryset):
        """
        Reject selected screenshots by admin in bulk.
        - Updates the status to 'rejected'.
        - parameter 'queryset' contains the selected screenshots that the admin has chosen in the Django Admin panel.
        """
        queryset.update(status="rejected")

    # Set display names for admin actions
    approve_screenshots.short_description = "Approve selected screenshots"
    reject_screenshots.short_description = "Reject selected screenshots"


# Register the Screenshot model with the customized admin settings
# Django automatically adds a delete action along with any custom actions (like "Approve" and "Reject").
admin.site.register(Screenshot, ScreenshotAdmin) 

admin.site.register(App)

