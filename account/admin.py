from django.contrib import admin
from .models import CustomUser

class WriterFilter(admin.SimpleListFilter):
    title = "Writer Status"
    parameter_name = "is_writer"

    def lookups(self, request, model_admin):
        return (
            ("writer", "Writers"),
            ("non_writer", "Non-Writers"),
        )

    def queryset(self, request, queryset):
        if self.value() == "writer":
            return queryset.filter(is_writer=True)
        if self.value() == "non_writer":
            return queryset.filter(is_writer=False)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_writer", "is_staff")
    list_filter = (WriterFilter, "is_staff", "is_active")  # 👈 ใช้ filter ที่เราสร้างเอง
    search_fields = ("email", "first_name", "last_name")




