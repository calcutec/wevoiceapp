import sys
import os
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from forms import LoginForm, SelectionForm, CommentForm, DeleteCommentForm
from django.contrib.auth.models import User
from models import Client, Talent, Vendor, Language, Selection, Comment, Rating, UserProfile
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from .validators import validate_user_is_authorized


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.data['username'], password=form.data['password'])
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    login(request, user)
                    if user.userprofile.client:
                        return HttpResponseRedirect(reverse('index', args=(user.userprofile.client.username,)))
                    elif user.userprofile.vendor:
                        return HttpResponseRedirect('/admin')
                    else:
                        raise Http404("That user not found")

                else:
                    # An inactive account was used - no logging in!
                    return HttpResponse("Sorry, this WeVoice account has been disabled.")
            else:
                # Bad login details were provided. So we can't log the user in.
                print("Invalid login details: {0}, {1}".format(form.data['username'], form.data['password']))
                return HttpResponse("Invalid login details supplied.")

    else:
        if request.user.is_authenticated():
            logout(request)
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def index(request, client_name):
    validate_user_is_authorized(request.user, client_name)
    client = get_client(client_name)
    return render(request, 'index.html', {
        'client': client,
    })


@login_required
def delete_comment(request):
    if request.method == "POST":
        form = DeleteCommentForm(request.POST)
        if form.is_valid():
            client = get_object_or_404(Client, pk=form.cleaned_data['client_id'])
            comment = get_object_or_404(Comment, pk=form.cleaned_data['comment_id'])
            selection = get_object_or_404(Selection, pk=form.cleaned_data['selection_id'])
            comment.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {
                'selection': selection,
                'client': client})
        else:
            raise Http404("That page does not exist")
    else:
        raise Http404("That page does not exist")


@login_required
def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            client = get_object_or_404(Client, pk=form.cleaned_data['client_id'])
            selection = get_object_or_404(Selection, pk=form.cleaned_data['selection_id'])
            if form.cleaned_data['text'] != '':
                author = request.user
                comment_text = form.cleaned_data['text']
                comment = Comment(author=author, text=comment_text, selection=selection)
                comment.save()
            if form.cleaned_data['rating'] != '':
                Rating.objects.update_or_create(
                    rater=request.user,
                    talent=selection.talent,
                    defaults={'rating': form.cleaned_data['rating']}
                )
                selection.talent.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {
                'selection': selection,
                'client': client})
    else:
        return Http404("That page does not exist")


@login_required
def selections(request, client_name, status, pk=None):
    validate_user_is_authorized(request.user, client_name)
    comment_form, delete_comment_form, selection_types = (None, None, None)
    if request.method == 'POST':
        form = SelectionForm(request.POST)
        if form.is_valid():
            client = Client.objects.get(id=form.cleaned_data['client_id'])
            talent = Talent.objects.get(id=form.cleaned_data['talent_id'])
            talent_selection = Selection.objects.filter(client=client).filter(talent=talent)[0]
            if request.POST.get('submit') == 'ACCEPT':
                talent_selection.status = 'APPROVED'
                talent_selection.save()
            elif request.POST.get('submit') == 'REJECT':
                talent_selection.status = 'REJECTED'
                talent_selection.save()
            elif request.POST.get('submit') == 'FOR APPROVAL':
                talent_selection.status = 'PREAPPROVED'
                talent_selection.save()
            else:
                raise Http404()
    else:
        form = SelectionForm

    client = get_client(client_name)
    no_selections, selection_types = get_selections(client, status)

    if pk and int(pk) > 0:
        pk = int(pk)
        selection = get_selection(pk)
        selection.last_modified = datetime.now()
        selection.save()
        comment_form = CommentForm
        delete_comment_form = DeleteCommentForm

    return render(request, 'selections.html', {
        'client': client,
        'form': form,
        'comment_form': comment_form,
        'delete_comment_form': delete_comment_form,
        'pk': pk,
        'status': status,
        'no_selections': no_selections,
        'selection_types': selection_types
    })


def get_selections(client, status):
    no_selections = False
    status_filter_dict = {
        'for_approval': 'PREAPPROVED',
        'accepted': 'APPROVED',
        'rejected': 'REJECTED'
    }
    status_filter = None
    if status in ['for_approval', 'accepted', 'rejected']:
        status_filter = status_filter_dict[status]
    all_selections = client.selection_set.filter(status=status_filter).order_by('talent__language')
    if all_selections.count() == 0:
        no_selections = True
    selection_types = []
    for type_filter in ["PRO", "HR", "TTS"]:
        currentselections = all_selections.filter(talent__type=type_filter)
        if currentselections.exists():
            selection_types.append({
                'selections': currentselections,
                'type': type_filter
            })
    return no_selections, selection_types


def updatedb(request):
    from legacy.models import Talent as OldTalents
    from legacy.models import Client as OldClients
    from legacy.models import Main as OldMainClients
    from legacy.models import Language as OldLanguages
    from legacy.models import Admin as OldAdmin
    from legacy.models import Vendor as OldVendors

    User.objects.create_superuser('william.burton', 'william.burton@welocalize.com', 'L0cal!ze1')

    superclient = Client.objects.create(
        name="Welocalize",
        username="welocalize"
    )

    superclient.password = make_password("Welo!")
    superclient.save()

    welocalize_profile = UserProfile.objects.get_or_create(
        user=User.objects.get(username='william.burton'),
    )

    welocalize_profile[0].client = superclient
    welocalize_profile[0].save()

    for oldadmin in OldAdmin.objects.all():
        new_superuser = User.objects.create_superuser(
            oldadmin.username,
            '',
            oldadmin.password
        )
        new_superuser.save()
        new_userprofile = UserProfile.objects.get_or_create(
            user=new_superuser,
        )
        new_userprofile[0].client = superclient
        new_userprofile[0].save()

    for oldvendor in OldVendors.objects.all():
        create_vendor_objects(oldvendor)

    for oldlanguage in OldLanguages.objects.all():
        Language.objects.create(
            language=oldlanguage.language
        )

    for oldtalent in OldTalents.objects.all():
        vendor, created = Vendor.objects.get_or_create(name=oldtalent.vendor_name)
        language, created = Language.objects.get_or_create(language=oldtalent.language)
        age_range = "26-45"
        if oldtalent.age_range == "16-25":
            age_range = "16-25"
        elif oldtalent.age_range == "26-45":
            age_range = "26-45"
        elif oldtalent.age_range == "46-75":
            age_range = "46-75"

        try:
            newtalent = Talent.objects.create(
                welo_id=oldtalent.welo_id,
                vendor=vendor,
                gender=oldtalent.gender,
                age_range=age_range,
                language=language,
                audio_file=oldtalent.sample_url.split('/')[1],
                comment=oldtalent.comment,
                rate=oldtalent.rate,
            )
            newtalent.save()
        except Exception as e:
            print_error(e)

        try:
            if oldtalent.vendor_name:
                vendor, created = Vendor.objects.get_or_create(name=oldtalent.vendor_name)
                newtalent.vendor = vendor
                newtalent.save()
        except Exception as e:
            print_error(e)

        try:
            if oldtalent.hr == "y":
                newtalent.type = "HR"
            elif oldtalent.tts == 'y':
                newtalent.type = "TTS"
            else:
                newtalent.type = "PRO"
            newtalent.save()
        except Exception as e:
            print_error(e)

    for oldclient in OldClients.objects.all():
        old_main_clients = [
            'demo_client',
            'vmware',
            'nationalinstruments',
            'LS2015',
            'NMHG',
            'BC',
            'ELmind',
            'Workday',
            'rethinkrobotics',
            'uber-voice',
            'workday',
            'UTC',
            'avigilon',
            'resaas'
        ]
        if oldclient.username not in old_main_clients:
            print("Processing Client: " + oldclient.username)
            process_client(oldclient, OldTalents)

    nonbranded = ['Orlando', 'Rethink Robotics', 'E Learning Mind', 'BC', 'National Instruments', 'Workday', 'UTC',
                  'avigilon']
    for oldclientusername in nonbranded:
        print("Processing Client: " + oldclientusername)
        oldclient = OldClients.objects.filter(name=oldclientusername)[0]
        newclient = create_client_objects(oldclient)
        oldmainclienttalents = OldMainClients.objects.filter(client=oldclientusername)
        for talent in oldmainclienttalents:
            try:
                newtalent = Talent.objects.get(welo_id=talent.talent)
                if talent.accepted == 'y':
                    status = "APPROVED"
                else:
                    status = "REJECTED"
                new_selection = Selection.objects.create(talent=newtalent, client=newclient)
                new_selection.status = status
                new_selection.save()
            except Exception as e:
                print_error(e)
        for talent in OldTalents.objects.filter(pre_approved="y").filter(allclients="y"):
            if (talent.welo_id,) not in oldmainclienttalents.values_list("talent"):
                try:
                    newtalent = Talent.objects.get(welo_id=talent.welo_id)
                    new_selection = Selection.objects.create(talent=newtalent, client=newclient)
                    new_selection.status = "PREAPPROVED"
                    new_selection.save()
                except Exception as e:
                    print_error(e)

    return HttpResponse("All done!")


def process_client(oldclient, oldtalents):

    newclient = create_client_objects(oldclient)

    try:
        oldtalents.objects.raw("SELECT * FROM talent WHERE %s='y'" % oldclient.username)[0]
    except Exception as e:
        print_error(e)
        if oldclient:
            print(oldclient.username + ": " + "PREAPPROVED")
    else:
        process_talent_types(
            status="PREAPPROVED",
            oldclient=oldclient,
            newclient=newclient,
            process_function=get_talents_for_approval
        )
    finally:
        try:
            oldtalents.objects.raw("SELECT * FROM %s" % oldclient.username)[0]
        except Exception as e:
            print_error(e)
            if oldclient:
                print(oldclient.username + ": " + "ACCEPTED")
        else:
            process_talent_types(
                status="APPROVED",
                oldclient=oldclient,
                newclient=newclient,
                process_function=get_accepted_talents
            )
        try:
            oldtalents.objects.raw("SELECT * FROM %s" % oldclient.username)[0]
        except Exception as e:
            if IndexError:
                pass
            else:
                print_error(e)
                if oldclient:
                    print(oldclient.username + ": " + "REJECTED")
        else:
            process_talent_types(
                status="REJECTED",
                oldclient=oldclient,
                newclient=newclient,
                process_function=get_rejected_talents
            )


def create_client_objects(oldclient):
    try:
        newclient = Client.objects.create(
            name=oldclient.name,
            username=oldclient.username,
            logo="client_logos/%slogo.png" % oldclient.username
        )
        newuser = User.objects.get_or_create(
            first_name=oldclient.name,
            last_name="Client",
            username=oldclient.username
        )
        newuser[0].password = oldclient.password
        newuser[0].save()
        newprofile = UserProfile.objects.get_or_create(
            user=newuser[0],
        )
        newprofile[0].client = newclient
        newprofile[0].save()

        return newclient
    except Exception as e:
        print(e)


def create_vendor_objects(oldvendor):
    try:
        newvendor = Vendor.objects.create(
            name=oldvendor.name,
            username=oldvendor.username,
        )
        newuser, created = User.objects.get_or_create(
            first_name=oldvendor.name,
            last_name="Vendor",
            username=oldvendor.username
        )
        newuser.password = oldvendor.password
        newuser.is_staff = True
        newuser.save()
        newprofile = UserProfile.objects.get_or_create(
            user=newuser,
        )
        newprofile[0].vendor = newvendor
        newprofile[0].save()
        new_group, created = Group.objects.get_or_create(name='Vendors')
        can_add_talent = Permission.objects.filter(name='Can add talent')[0]
        can_change_talent = Permission.objects.filter(name='Can change talent')[0]
        can_delete_talent = Permission.objects.filter(name='Can delete talent')[0]
        new_group.permissions.add(can_add_talent)
        new_group.permissions.add(can_change_talent)
        new_group.permissions.add(can_delete_talent)
        newuser.groups.add(new_group)

    except Exception as e:
        print(e)


def process_talent_types(status, oldclient, newclient, process_function):
    try:
        protalents, hometalents, ttstalents = process_function(oldclient.username)
    except Exception as e:
        print_error(e)
    else:
        process_type(protalents, newclient, status, "protalents")
        process_type(hometalents, newclient, status, "hometalents")
        process_type(ttstalents, newclient, status, "ttstalents")


def process_type(talent_type, newclient, status, type_of_talent):
    for talent_old in talent_type:
        try:
            talent = None
            if 'talent' in talent_old:
                talent = Talent.objects.get(welo_id=talent_old['talent'])
            elif 'welo_id' in talent_old:
                talent = Talent.objects.get(welo_id=talent_old['welo_id'])
            if newclient:
                new_selection, created = Selection.objects.get_or_create(talent=talent, client=newclient)
                if not created:
                    print("%s: %s: %s: %s" % (newclient.name, type_of_talent, status, talent.welo_id))
                    new_selection.status = status
                    new_selection.save()
                else:
                    new_selection.status = status
                    new_selection.save()
            else:
                print("No newclient found")
        except Exception as e:
            if hasattr(talent_old, 'welo_id'):
                print_error(e)
                print("welo_id: " + talent_old.welo_id + "client: " + newclient.username)
            elif hasattr(talent_old, 'talent'):
                print_error(e)
                print("talent: " + talent_old.talent + "client: " + newclient.username)


def get_client(client_name):
    try:
        client = Client.objects.get(username=client_name)
    except Client.DoesNotExist:
        raise Http404("That client does not exist")
    return client


def get_selection(pk):
    try:
        selection = Selection.objects.get(pk=pk)
    except Selection.DoesNotExist:
        raise Http404("That selection does not exist")
    return selection


def print_error(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(e, exc_type, fname, exc_tb.tb_lineno)


def my_custom_sql(query):
    from django.db import connections
    cursor = connections['legacy'].cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_talents_for_approval(client_name):

    proresults, homeresults, ttsresults = None, None, None

    proquery = "SELECT * FROM talent " \
        "WHERE pre_approved='y' AND %s='y' AND hr='n' AND tts='n' " \
        "AND NOT EXISTS (SELECT * FROM %s WHERE talent.welo_id=%s.talent) " \
        "ORDER BY language" % (client_name, client_name, client_name)
    homequery = "SELECT * FROM talent " \
        "WHERE pre_approved='y' AND %s='y' AND hr='y' AND tts='n' " \
        "AND NOT EXISTS (SELECT * FROM %s WHERE talent.welo_id=%s.talent) " \
        "ORDER BY language" % (client_name, client_name, client_name)
    ttsquery = "SELECT * FROM talent " \
        "WHERE pre_approved='y' AND %s='y' AND hr='n' AND tts='y' " \
        "AND NOT EXISTS (SELECT * FROM %s WHERE talent.welo_id=%s.talent) " \
        "ORDER BY language" % (client_name, client_name, client_name)

    try:
        proresults = my_custom_sql(proquery)
    except Exception as e:
        print_error(e)

    try:
        homeresults = my_custom_sql(homequery)
    except Exception as e:
        print_error(e)

    try:
        ttsresults = my_custom_sql(ttsquery)
    except Exception as e:
        print_error(e)
    return proresults, homeresults, ttsresults


def get_accepted_talents(client_name):

    proresults, homeresults, ttsresults = None, None, None

    proquery = "SELECT * FROM %s " \
        "WHERE accepted='y' " \
        "AND EXISTS (SELECT * FROM talent WHERE %s.talent=talent.welo_id AND talent.hr='n' AND talent.tts='n') " \
        "ORDER BY language" % (client_name, client_name)

    homequery = "SELECT * FROM %s " \
        "WHERE accepted='y' " \
        "AND EXISTS (SELECT * FROM talent WHERE %s.talent=talent.welo_id AND talent.hr='y' AND talent.tts='n') " \
        "ORDER BY language" % (client_name, client_name)

    ttsquery = "SELECT * FROM %s " \
        "WHERE accepted='y' " \
        "AND EXISTS (SELECT * FROM talent WHERE %s.talent=talent.welo_id AND talent.hr='n' AND talent.tts='y') " \
        "ORDER BY language" % (client_name, client_name)
    try:
        proresults = my_custom_sql(proquery)
    except Exception as e:
        print_error(e)

    try:
        homeresults = my_custom_sql(homequery)
    except Exception as e:
        print_error(e)

    try:
        ttsresults = my_custom_sql(ttsquery)
    except Exception as e:
        print_error(e)
    return proresults, homeresults, ttsresults


def get_rejected_talents(client_name):

    proresults, homeresults, ttsresults = None, None, None

    proquery = "SELECT * FROM %s " \
        "WHERE accepted='n' " \
        "AND EXISTS (SELECT * FROM talent WHERE %s.talent=talent.welo_id AND talent.hr='n' AND talent.tts='n') " \
        "ORDER BY language" % (client_name, client_name)
    homequery = "SELECT * FROM %s " \
        "WHERE accepted='n' " \
        "AND EXISTS (SELECT * FROM talent WHERE %s.talent=talent.welo_id AND talent.hr='y' AND talent.tts='n') " \
        "ORDER BY language" % (client_name, client_name)
    ttsquery = "SELECT * FROM %s " \
        "WHERE accepted='n' " \
        "AND EXISTS (SELECT * FROM talent WHERE %s.talent=talent.welo_id AND talent.hr='n' AND talent.tts='y') " \
        "ORDER BY language" % (client_name, client_name)
    try:
        proresults = my_custom_sql(proquery)
    except Exception as e:
        print_error(e)

    try:
        homeresults = my_custom_sql(homequery)
    except Exception as e:
        print_error(e)

    try:
        ttsresults = my_custom_sql(ttsquery)
    except Exception as e:
        print_error(e)
    return proresults, homeresults, ttsresults
