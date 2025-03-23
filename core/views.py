from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#------------------------------------------------------------
# Accounts
@login_required(login_url="account_login")
def profile(request):
    context = {}
    return render(request, 'home/profile.html', context)

@login_required(login_url="account_login")
def articles(request):
    context = {}
    return render(request, 'home/articles.html', context)

@login_required(login_url="account_login")
def article_manager(request):
    context = {}
    return render(request, 'home/article_manager.html', context)

@login_required(login_url="account_login")
def edit_article(request, post_id):
    context = {
        'post_id': post_id,
    }
    return render(request, 'home/edit-articles.html', context)

#------------------------------------------------------------
# 所有文章
def articles_list(request):
    context = {}
    return render(request, 'home/articles_list.html', context)

#------------------------------------------------------------
# 文章內容
def article(request, slug):
    context = {
        'slug': slug,

    }
    return render(request, 'home/article_content.html', context)



def index(request):
    context = {}
    return render(request, 'home/index.html', context)

def leaderboard(request):
    context = {}
    return render(request, 'home/leaderboard.html', context)


def pages(request, page=None):
    context = {}

    # Set default page to 'index' if page is None
    load_template = 'index' if page is None else page
    return render(request, 'home/' + load_template + '.html', context)
