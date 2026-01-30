"""
Admin configuration for Projects app
"""
from django.contrib import admin
from .models import Project, ProjectType, ProjectImage, ProjectFile


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'is_primary']


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1
    fields = ['file', 'name', 'description']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer', 'project_type', 'status', 'total_budget', 'total_revenue', 'profit', 'loss', 'created_at']
    list_filter = ['status', 'project_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'customer__name']
    readonly_fields = ['profit', 'loss', 'created_at', 'updated_at']
    inlines = [ProjectImageInline, ProjectFileInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'project_type', 'customer', 'status', 'is_active')
        }),
        ('Financial Information', {
            'fields': ('total_budget', 'total_revenue', 'total_cost', 'profit', 'loss')
        }),
        ('Links', {
            'fields': ('live_url', 'repository_url')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'deadline')
        }),
        ('Additional', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['project__name', 'caption']


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ['project', 'name', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['project__name', 'name', 'description']
