from django import forms
from .models import Registration
from .models import Courses
from .models import Lesson
from .models import CalendarInstance
from .models import CalendarWeekLabel

STATUS_CHOICES = [
    ('pending', 'Pending Assignment'),
    ('completed', 'Completed'),
    ('rejected', 'Rejected'),
]

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'

    # Override the status field to set default value  
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='pending', required=False)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['code', 'description', 'deleted', 'archived']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description']

class CalendarForm(forms.ModelForm):
    class Meta:
        model = CalendarInstance
        fields = ['name', 'date_start', 'date_end', 'holidays']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'holidays': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 2025-05-01, 2025-08-31'
            }),
        }

class WeekLabelForm(forms.ModelForm):
    class Meta:
        model = CalendarWeekLabel
        fields = ['week_number', 'year', 'label']
        widgets = {
            'label': forms.TextInput(attrs={'placeholder': 'e.g. SCHOOL BREAK'}),
        }

class VideoUploadForm(forms.Form):
    video_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            'accept': 'video/*'
        }),
        help_text='Upload video file (MP4, AVI, MOV, etc.)'
    )
    
    upload_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    
    class_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    
    program = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    
    level = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    
    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            # Check file size (limit to 4GB)
            if video_file.size > 4000 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 500MB.')
            
            # Check file type
            allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
            file_extension = os.path.splitext(video_file.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Only video files are allowed.')
        
        return video_file