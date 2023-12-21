from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=[], coerce=int, initial=1,
                                      required=False)
    update = forms.BooleanField(required=False, initial=False,
                                widget=forms.HiddenInput)

    def __init__(self, max_quantity1, *args, **kwargs):
        print(f"{type(max_quantity1)}")
        super().__init__(*args, **kwargs)
        self.fields['quantity'].choices = [
            (i, str(i)) for i in range(1, min(max_quantity1, 20)+1)]
