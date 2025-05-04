from django import forms
from .models import Review

RATING_CHOICES = [
    (1, '1 Star'),
    (2, '2 Stars'),
    (3, '3 Stars'),
    (4, '4 Stars'),
    (5, '5 Stars'),
]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=RATING_CHOICES),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
