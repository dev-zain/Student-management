from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Student(models.Model):
    photo = models.ImageField(upload_to='images')
    student_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    dob = models.CharField(max_length=20)
    contact = models.CharField(max_length=20, null=True)
    roll_no = models.CharField(max_length=20)
    department = models.CharField(max_length=30)
    enrollment_year =  models.CharField(max_length=20)
    completion_date = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    medical_conditions = models.TextField()
    qr_code = models.ImageField(upload_to='qrcodes', blank=True)
    card_issue_date =  models.CharField(max_length=20)
    expiry_date =  models.CharField(max_length=20)
    id_card_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.student_name

    def save(self, *args, **kwargs):
        if not self.pk:
            # New student, generate QR code
            qr_image = qrcode.make(self.id_card_number)
            qr_offset = Image.new('RGB', (310, 310), 'white')
            qr_offset.paste(qr_image)
            qr_code_file_name = f'{self.student_name}_qr.png'
            stream = BytesIO()
            qr_offset.save(stream, 'PNG')
            self.qr_code.save(qr_code_file_name, File(stream), save=False)
            qr_offset.close()
        else:
            try:
                old_student = Student.objects.get(pk=self.pk)
                if old_student.id_card_number != self.id_card_number:
                    # Only generate a new QR code if the ID card number has changed
                    qr_image = qrcode.make(self.id_card_number)
                    qr_offset = Image.new('RGB', (310, 310), 'white')
                    qr_offset.paste(qr_image)
                    qr_code_file_name = f'{self.student_name}_qr.png'
                    stream = BytesIO()
                    qr_offset.save(stream, 'PNG')
                    self.qr_code.save(qr_code_file_name, File(stream), save=False)
                    qr_offset.close()
            except Student.DoesNotExist:
                pass  # It's a new student, no need to compare old values

        super(Student, self).save(*args, **kwargs)

@receiver(pre_delete, sender=Student)
def delete_student_images(sender, instance, **kwargs):
    # Delete the associated images
    if instance.photo:
        instance.photo.delete(save=False)
    if instance.qr_code:
        instance.qr_code.delete(save=False)
