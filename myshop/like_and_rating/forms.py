from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} ⭐') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your review...',
                'rows': 4,
                'class': 'form-control'
            }),
        }
        labels = {
            'rating': 'Rating',
            'comment': 'Comment',
        }
        error_messages = {
            'rating': {
                'required': 'Please select a rating',
                'min_value': 'Rating must be between 1 and 5',
                'max_value': 'Rating must be between 1 and 5',
            },
            'comment': {
                'required': 'Please write a comment',
            },
        }