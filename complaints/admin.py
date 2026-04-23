"""
Smart Garbage Complaint System — Admin Configuration

Customizes the Django admin panel for efficient complaint management.
Municipal staff can use the admin panel to:
- View and search all complaints
- Filter by status, priority, and date
- Update complaint status and add admin remarks
- View complaint images
"""

from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    """
    Custom admin view for the Complaint model.

    Provides a powerful interface for municipal staff to manage complaints
    with search, filtering, and bulk actions.
    """

    # ─── List Display ─────────────────────────────────────────────────────
    # Columns shown in the complaint list view
    list_display = [
        'reference_number',
        'reporter_name',
        'location_text',
        'status',
        'priority',
        'created_at',
    ]

    # ─── Filters ──────────────────────────────────────────────────────────
    # Sidebar filters for quick filtering
    list_filter = [
        'status',
        'priority',
        'created_at',
    ]

    # ─── Search ───────────────────────────────────────────────────────────
    # Fields searchable from the admin search bar
    search_fields = [
        'reference_number',
        'reporter_name',
        'reporter_email',
        'location_text',
        'description',
    ]

    # ─── Read-Only Fields ─────────────────────────────────────────────────
    # These fields cannot be edited in admin (auto-generated)
    readonly_fields = [
        'reference_number',
        'created_at',
        'updated_at',
    ]

    # ─── Field Grouping ───────────────────────────────────────────────────
    # Organize the edit form into logical sections
    fieldsets = (
        ('📋 Complaint Reference', {
            'fields': ('reference_number',)
        }),
        ('👤 Reporter Information', {
            'fields': ('user', 'reporter_name', 'reporter_email', 'reporter_phone')
        }),
        ('📍 Location', {
            'fields': ('location_text', 'google_maps_link')
        }),
        ('📝 Complaint Details', {
            'fields': ('description', 'image', 'priority')
        }),
        ('⚙️ Status & Administration', {
            'fields': ('status', 'admin_remarks')
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Collapsible section
        }),
    )

    # ─── List Customization ───────────────────────────────────────────────
    list_per_page = 25  # Complaints per page
    date_hierarchy = 'created_at'  # Date-based drill-down navigation
    ordering = ['-created_at']  # Newest first


# ─── Customize Admin Site Header ──────────────────────────────────────────────
admin.site.site_header = '🗑️ Smart Garbage Complaint System — Admin'
admin.site.site_title = 'Garbage Complaints Admin'
admin.site.index_title = 'Municipal Authority Dashboard'
