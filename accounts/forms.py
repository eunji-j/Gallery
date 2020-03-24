from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)
        # 추가시켜줄 필드 있을 경우에 작성한다.

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model() # User모델반환 (cf. settings.AUTH_USER_MODEL은 문자열반환)
            # User모델의 이름이 바뀌어도 변경하지 않아도 되서 편리하다.
        fields = ('email',)  