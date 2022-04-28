from django import forms


class JournalEntry(forms.Form):
    entry = forms.CharField(label="Make your diary entry",
                                 widget=forms.Textarea(attrs={"rows": 50, "cols": 60}))
