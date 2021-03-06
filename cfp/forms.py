from django import forms

from .models import Proposal


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = [
            "session_type",
            "title",
            "subtitle",
            "copresenter_names",
            "description",
            "description_private",
            "outline",
            "equipment",
            "aimed_at_new_programmers",
            "aimed_at_teachers",
            "aimed_at_data_scientists",
            "would_like_mentor",
            "would_like_longer_slot",
            "coc_conformity",
            "ticket",
        ]

        labels = {
            "session_type": "What are you proposing?",
            "copresenter_names": "Are you presenting with anybody else?",
            "description": "What is your session about?",
            "description_private": "Is there anything else we should know about your proposal?",
            "outline": "Can you give us an outline of your proposed session?",
            "equipment": "What are your equipment and other requirements?",
            "aimed_at_new_programmers": "new programmers?",
            "aimed_at_teachers": "teachers?",
            "aimed_at_data_scientists": "data scientists?",
            "would_like_mentor": "like a mentor",
            "would_like_longer_slot": "I would like to be considered for a longer talk slot",
        }

        help_texts = {
            "title": "Limit: 60 characters. Required.",
            "subtitle": "Limit: 120 characters. Optional.",
            "copresenter_names": "If you are presenting with anybody else, please list their names here.",
            "description": "If your session is selected, this is the basis of what will be published in the programme. Limit: 300 words. Required.",
            "description_private": "Your answer here is for the benefit of the programme committee, and will not be published. Limit: 300 words.",
            "outline": "An outline of your session is optional, but helps the programme committee. A proposal with an outline is more likely to be selected than one without. More detail, including timings, is better. The outline will not be published.",
            "equipment": "We’ll provide: a projector for talks and workshops; a large board for posters; a room full of Raspberry Pis and micro:bits for Education Summit sessions. Is there anything else you will need us to provide? Optional.",
        }

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": False}),
            "subtitle": forms.TextInput(attrs={"placeholder": False}),
            "copresenter_names": forms.Textarea(
                attrs={"cols": 40, "rows": 3, "placeholder": False}
            ),
            "description": forms.Textarea(attrs={"placeholder": False}),
            "description_private": forms.Textarea(attrs={"placeholder": False}),
            "outline": forms.Textarea(attrs={"placeholder": False}),
            "equipment": forms.Textarea(attrs={"placeholder": False}),
        }

    # Model form does not allow required=True on booleans unless explicitly defined
    coc_conformity = forms.BooleanField(required=True)
    coc_conformity.label = "Does your proposal conform to our Code of Conduct?"
    coc_conformity.help_text = 'I confirm that my proposed session conforms to the requirements of the <a href="https://2018.pyconuk.org/code-conduct/" target="_blank">Code of Conduct</a>'

    ticket = forms.BooleanField(required=True)
    ticket.label = (
        "I understand that I will need to register for a ticket for the event"
    )
    ticket.help_text = "All attendees <strong>including speakers</strong> at PyCon UK need to register for a ticket. I understand that I will either need to buy a ticket for the event <strong>or</strong> request a free ticket through the financial assistance process."
