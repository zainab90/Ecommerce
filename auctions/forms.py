from django import  forms

from auctions.models import Auction, Catogery, Bid, Comment


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Catogery
        fields = [
            'catogery'
        ]


class AuctionForm (forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Date', 'autocomplete': 'off'}),
        required=True,
    )



    class Meta:
        model = Auction
        fields = [
            'title',
            'description',
            'imgurl',
            'date',
            'price',
            'user',
            'catogery',
            'active',
            'start_bid',
            'last_bid'
        ]




class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            'user',
            'auctions',
            'bid'
        ]

class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'user',
            'comments',
            'auctions'
        ]