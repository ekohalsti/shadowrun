from django.contrib import admin

# Register your models here.
from .models import Skill, Attribute, Skill_cost, Skill_specialization, Quality

admin.site.register(Skill)
admin.site.register(Attribute)
admin.site.register(Skill_cost)
admin.site.register(Skill_specialization)
admin.site.register(Quality)
