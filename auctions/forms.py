from django import  forms

from auctions.models import Auction, Catogery, Bid, Comment


class CategoryForm(forms.ModelForm):
    catogery = forms.CharField(label='Enter name of Category')
    class Meta:
        model = Catogery
        fields = [
            'catogery'
        ]


class AuctionForm (forms.ModelForm):
    date = forms.DateTimeField( label='Select date',
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Date', 'autocomplete': 'off'}),
        required=True,
    )
    title=forms.CharField(label='Enter Title of Listing')
    description = forms.CharField(label='Enter description of Listing')
    imgurl = forms.CharField(label='Enter Image URL of Listing')
    price = forms.CharField(label='Enter price of Listing')


    class Meta:
        model = Auction
        fields = [
            'title',
            'description',
            'imgurl',
            'date',
            'price',

            'catogery',

        ]




class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            'bid'
        ]

class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comments',
        ]