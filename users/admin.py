from django import forms
from django.contrib import admin
from django.db.models import Count
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AvatarListFilter(admin.SimpleListFilter):
    title = 'avatar'
    parameter_name = 'avatar'

    def lookups(self, request, model_admin):
        return (
            ('with_avatar', 'with avatar'),
            ('no_avatar', 'no avatar'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'with_avatar':
            return queryset.exclude(avatar__exact='')
        if self.value() == 'no_avatar':
            return queryset.filter(avatar__exact='')


class FriendsCountListFilter(admin.SimpleListFilter):
    title = 'friends'
    parameter_name = 'friends'

    def lookups(self, request, model_admin):
        return (
            ('no_friends', 'no friends'),
            ('1-9', '1-9'),
            ('10-19', '10-19'),
            ('20-50', '20-50'),
            ('51-99', '51-99'),
            ('more_than_100', '>100'),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(count=Count('friends'))
        if self.value() == 0:
            return queryset.filter(count=0)
        if self.value() == '1-9':
            return queryset.filter(count__gt=0, count__lt=10)
        if self.value() == '10-19':
            return queryset.filter(count__gt=9, count__lt=20)
        if self.value() == '20-50':
            return queryset.filter(count__gt=19, count__lt=51)
        if self.value() == '51-99':
            return queryset.filter(count__gt=50, count__lt=100)
        if self.value() == 'more_than_100':
            return queryset.filter(count__gt=99)


class UserAdmin(BaseUserAdmin):

    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2'
            ),
            'classes': ('wide',)
        }),
    )

    list_display = ('email', 'username', 'is_active', 'is_superuser')
    list_filter = (
        'is_active', 'is_superuser', AvatarListFilter, FriendsCountListFilter
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'avatar', 'first_name', 'last_name', 'status', 'username'
        )}),
        ('Permissions', {'fields': ('is_superuser',)}),
        ('Timeline', {'fields': ('birthday', 'last_login', 'date_joined')})
    )
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
