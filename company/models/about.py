from django.db import models

class About(models.Model):
    company_name = models.CharField(max_length=255)
    official_email = models.EmailField()
    num_employees = models.IntegerField()
    linkedin_url = models.CharField(max_length=100)
    about_content = models.TextField()
    location = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name