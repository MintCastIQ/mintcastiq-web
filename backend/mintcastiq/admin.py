from django.contrib import admin
from django.utils.html import format_html
from .models import DimGrade, ChecklistUpload
from django.conf import settings
from .checklist_service import ingest_checklist


@admin.register(DimGrade)
class DimGradeAdmin(admin.ModelAdmin):
    list_display = ("grading_standard", "numeric_value", "grade_label", "overlay_ref")
    search_fields = ("grading_standard", "grade_label")
    list_filter = ("grading_standard",)

    def overlay_preview(self, obj):
        if obj.overlay_ref:
            return format_html(
                '<img src="{}overlays/{}.png" style="height:40px;" alt="{}"/>',
                settings.STATIC_URL,
                obj.overlay_ref,
                obj.grade_label
            )
        return "—"
    overlay_preview.short_description = "Overlay"

@admin.register(ChecklistUpload)
class ChecklistUploadAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "processed")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.file and not obj.processed:
            ingest_checklist(obj.file.path)
            obj.processed = True
            obj.save()
            self.message_user(request, "Checklist ingested successfully.")