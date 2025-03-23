from core.models import BasicInformation, SocialLink, ContactInformation

def get_basic_info(request):
    '''
        取得網站基本資訊

        Args:
            request: Django request object

        Returns:
            dict: 網站基本資訊
    '''
    basic_info = BasicInformation.objects.first()
    if basic_info is None:
        basic_info = BasicInformation.objects.create(title='NFU')
    social_links = SocialLink.objects.filter(basic=basic_info)
    contact_info = ContactInformation.objects.filter(basic=basic_info).first()
    return {
        'basic_info': basic_info,
        'social_links': social_links,
        'contact_info': contact_info,
    }

def get_profile(request):
    '''
        取得使用者資訊

        Args:
            request: Django request object

        Returns:
            dict: 使用者資訊
    '''
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except:
            profile = None
    else:
        profile = None
    return {
        'profile': profile,
    }