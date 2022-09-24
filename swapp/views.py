from django.shortcuts import render, redirect
from django.forms import modelformset_factory
import os
from django.conf import settings
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as l

from .models import Usernew, Ask, Reply, Bad, Solved, Chat, Yes
from .forms import AskForm, ReplyForm, BadForm, SolvedForm, ChatForm, YesForm


def index(request):
    context = {}
    return render(request, 'swapp/index.html', context)


def home(request):
    for r in Reply.objects.all():
        if r.day_past:
            r.yn = True
            r.from_usernew.coins += r.ask.coins
            r.from_usernew.coins_earned += r.ask.coins
            r.from_usernew.asks_resolved += 1
            r.to_usernew.asks_made += 1
    context = {}
    if request.user.is_authenticated:
        if not Usernew.objects.filter(user=request.user).exists():
            new = Usernew.objects.create(user=request.user, coins=10, liv=1, coins_earned=0,
                                         coins_spent=0, asks_resolved=0, asks_made=0, evaluation=5)
            new.save()
        new = Usernew.objects.get(user=request.user)
        context['new'] = new
        context["len"] = len(Reply.objects.all().filter(
            to_user=request.user, yn=False))
    return render(request, 'swapp/home.html', context)


def contactus(request):
    context = {}
    context['chat'] = Chat.objects.all().filter(user=request.user)[::-1]
    return render(request, 'swapp/contactus.html', context)


def chat(request):
    context = {}
    context['chat'] = Chat.objects.all()[::-1]
    return render(request, 'swapp/chat.html', context)


def write(request):
    context = {}
    form = ChatForm(request.POST, request.FILES)
    if form.is_valid():
        c = form.save(commit=False)
        c.user = request.user
        c.usernew = Usernew.objects.get(user=request.user)
        c.title = request.user.username
        c.save()
        return redirect(contactus)
    context['form'] = form
    return render(request, 'swapp/write.html', context)


def adminwrite(request, chat_id):
    context = {}
    context['username'] = ""
    form = ChatForm(request.POST, request.FILES)
    if form.is_valid():
        o = Chat.objects.get(id=chat_id)
        c = form.save(commit=False)
        c.user = o.user
        c.usernew = Usernew.objects.get(user=o.user)
        o.done = True
        c.title = '?Admin_' + request.user.username
        c.save()
        o.save()
        return redirect('/user/'+str(o.usernew.id))
        context['username'] = o.user.username
    context['form'] = form
    return render(request, 'swapp/adminwrite.html', context)


def users(request):
    context = {}
    context['usernews'] = Usernew.objects.all()
    n_ns = {}
    for usernew in Usernew.objects.all():
        n_n = 0
        for chat in Chat.objects.all():
            if chat.usernew == usernew and chat.done == False and not '?' in chat.title:
                n_n += 1
        n_ns[usernew.user.username] = n_n
    ns = {}
    for usernew in Usernew.objects.all():
        n = 0
        for chat in Chat.objects.all():
            if chat.usernew == usernew and not '?' in chat.title:
                n += 1
        ns[usernew.user.username] = n
    context['n_num_msgs'] = n_ns
    context['num_msgs'] = ns
    return render(request, 'swapp/users.html', context)


def user(request, user_id):
    context = {}
    to_user = Usernew.objects.get(id=user_id).user
    context['to_user'] = to_user
    context['chat_id'] = Chat.objects.all().filter(user=to_user).last().id
    context['chat'] = Chat.objects.all().filter(user=to_user)[::-1]
    context['msg'] = Chat.objects.all().filter(user=to_user).last()
    return render(request, 'swapp/user.html', context)


def about(request):
    context = {}
    return render(request, 'swapp/about.html', context)


def ask(request):
    context = {}
    return render(request, 'swapp/ask.html', context)


def refunds(request):
    context = {}
    if request.user.is_authenticated:
        replies = Reply.objects.all().filter(to_user=request.user)
        bads = Bad.objects.filter(text="")
        for reply in replies:
            bads |= Bad.objects.all().filter(reply=reply)
        solveds = Solved.objects.filter(text="")
        for bad in bads:
            solveds |= Solved.objects.all().filter(bad=bad)
        context["solveds"] = solveds[::-1]
    return render(request, 'swapp/refunds.html', context)


def earn(request):
    context = {}
    context["asks"] = Ask.objects.all().order_by("date")[::1]
    return render(request, 'swapp/earn.html', context)


def inbox(request):
    context = {}
    if request.user.is_authenticated:
        context["replies"] = Reply.objects.all().filter(
            to_user=request.user).order_by("date")[::-1]
    return render(request, 'swapp/inbox.html', context)


def thanks(request, reply_id):
    context = {}
    form = YesForm(request.POST)
    if form.is_valid():
        r = Reply.objects.all().get(id=reply_id)
        y = form.save(commit=False)
        y.reply = r
        y.reply.yn = True

        y.reply.from_usernew.coins += y.reply.ask.coins
        y.reply.from_usernew.coins_earned += y.reply.ask.coins

        y.reply.from_usernew.asks_resolved += 1
        y.reply.to_usernew.asks_made += 1

        y.reply.save()
        y.reply.from_usernew.save()
        y.reply.to_usernew.save()
        y.save()
        r.save()
        return redirect(inbox)
    context['form'] = form
    return render(request, 'swapp/thanks.html', context)


def bad(request, reply_id):
    context = {}
    form = BadForm(request.POST, request.FILES)
    if form.is_valid():
        r = Reply.objects.all().get(id=reply_id)
        b = form.save(commit=False)
        b.reply = r
        b.reply.yn = True
        b.from_user = request.user
        b.to_user = r.ask.user
        b.from_usernew = Usernew.objects.get(user=request.user)
        b.to_usernew = Usernew.objects.get(user=r.ask.user)

        b.from_usernew.save()
        b.to_usernew.save()
        b.save()
        r.save()
        return redirect(inbox)
    context['form'] = form
    return render(request, 'swapp/bad.html', context)


def bads(request):
    context = {}
    context['bads'] = Bad.objects.all()
    return render(request, 'swapp/bads.html', context)


def solved(request, bad_id):
    context = {}
    form = SolvedForm(request.POST, request.FILES)
    if form.is_valid():
        s = form.save(commit=False)
        s.bad = Bad.objects.get(id=bad_id)
        s.bad.reply.done = True

        s.bad.reply.from_usernew.coins += s.coins_reply
        s.bad.reply.to_usernew.coins += s.coins_ask

        s.bad.reply.from_usernew.coins_earned += s.coins_reply
        s.bad.reply.to_usernew.coins_spent -= s.coins_ask

        if not s.coins_reply == 0:
            s.bad.reply.from_usernew.asks_resolved += 1

        s.save()
        s.bad.reply.save()
        s.bad.reply.from_usernew.save()
        s.bad.reply.to_usernew.save()
        return redirect(bads)
    context['form'] = form
    return render(request, 'swapp/solved.html', context)


def ask(request):
    context = {}
    form = AskForm(request.POST)
    if form.is_valid():
        usernew = Usernew.objects.get(user=request.user)
        coins = form.cleaned_data['coins']
        if coins > usernew.coins or coins < 1:
            return redirect(ask)

        a = form.save(commit=False)
        a.user = request.user
        a.usernew = Usernew.objects.get(user=request.user)

        a.usernew.coins -= a.coins
        a.usernew.coins_spent += a.coins

        a.save()
        a.usernew.save()
        return redirect(earn)
    context['form'] = form
    return render(request, "swapp/ask.html", context)


def reply(request, ask_id):
    context = {}
    form = ReplyForm(request.POST, request.FILES)
    if form.is_valid():
        a = Ask.objects.all().get(id=ask_id)
        if not a.done:
            r = form.save(commit=False)
            a.done = True
            r.ask = a

            r.from_user = request.user
            r.to_user = a.user
            r.from_usernew = Usernew.objects.get(user=request.user)
            r.to_usernew = Usernew.objects.get(user=a.user)

            r.from_usernew.save()
            r.to_usernew.save()
            r.save()
            a.save()
            return redirect(home)
    context['form'] = form
    return render(request, "swapp/reply.html", context)
