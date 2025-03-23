from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # 如果是使用 Google 登入，將 email_verified 設置為 True

        if sociallogin.account.provider == 'google' or user.is_superuser:
            user.emailaddress_set.filter(email=user.email).update(verified=True)
            print(user)
        else:
            user.emailaddress_set.filter(email=user.email).update(verified=False)
        return user