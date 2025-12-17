from django.db import models

class ChecklistUpload(models.Model):
    # fields here
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="checklists/")
    processed = models.BooleanField(default=False)

    class Meta:
        db_table = 'checklist_upload'
