from django.contrib import admin
from .models import login_table, State, City, Area, Vehicle, Booking, Complaint, Feedback, Contactus
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def export_to_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0,0), (-1,0), colors.grey),
       ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
       ('ALIGN', (0,0), (-1,-1), 'CENTER'),
       ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
       ('FONTSIZE', (0,0), (-1,0), 14),
       ('BOTTOMPADDING', (0,0), (-1,0), 12),
       ('BACKGROUND', (0,1), (-1,-1), colors.beige),
       ('GRID', (0,0), (-1,-1), 1, colors.black),
   ])

   # Create the table headers
   headers = ['user', 'vehicle', 'booking_date','booking_amount']

   # Create the table data
   data = []
   for obj in queryset:
       data.append([obj.user.name, obj.vehicle, obj.booking_date,obj.booking_amount])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response

export_to_pdf.short_description = "Export to PDF"


@admin.register(login_table)
class LoginTableAdmin(admin.ModelAdmin):
    list_display = ['name', 'email_id', 'phone_no', 'usertype','photos', 'is_verified']
    list_filter = ['usertype', 'is_verified']
    search_fields = ['name', 'email_id']


    def has_add_permission(self, request):
        return False
    # def has_change_permission(self, request, obj=None):
    #     return False

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']




@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'company', 'model_year', 'base_rent_perday', 'weekend_multiplier', 'location', 'vendor','photos','rc_book']
    list_filter = ['location', 'vendor']
    search_fields = ['model_name', 'company']
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle', 'booking_date', 'is_confirmed', 'booking_from', 'booking_to','booking_amount','payment_mode','payment_status','cancellation_status','owner_cancel']
    # def has_add_permission(self, request):
    #     return False
    # def has_change_permission(self, request, obj=None):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False
    list_filter = ["booking_date"]
    actions = [export_to_pdf]

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle', 'description', 'date']
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle', 'rating', 'comment', 'date']
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Contactus)
class ContactusAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','subject','message']
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

admin.site.site_header="Admin"
admin.site.index_title="Welcome to Admin Panel"