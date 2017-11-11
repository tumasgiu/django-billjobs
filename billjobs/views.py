# -*- coding: utf-8 -*-
import urllib
from django.contrib.auth import authenticate
from django import forms
from django.forms import ModelForm, ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, Paragraph
from io import BytesIO
from .settings import BILLJOBS_DEBUG_PDF, BILLJOBS_BILL_LOGO_PATH, \
    BILLJOBS_BILL_LOGO_WIDTH, BILLJOBS_BILL_LOGO_HEIGHT, \
    BILLJOBS_BILL_PAYMENT_INFO, BILLJOBS_FORCE_SUPERUSER, \
    BILLJOBS_FORCE_USER_GROUP, BILLJOBS_SLACK_TOKEN
from .models import Bill, UserProfile
from textwrap import wrap
from urllib.request import urlopen


class UserSignupForm(ModelForm):
    ''' Form for signup '''

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        if data == "":
            raise ValidationError(_("This field is required."))
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data == "":
            raise ValidationError(_("This field is required."))
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data == "":
            raise ValidationError(_("This field is required."))
        return data


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['billing_address']

    def clean_billing_address(self):
        data = self.cleaned_data['billing_address']
        if data == "":
            raise ValidationError(_('This field is required.'))
        return data


class UserLoginForm(forms.Form):
    ''' Form for login (regular user) '''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        data = self.cleaned_data['username']
        if data == "":
            raise ValidationError(_("This field is required."))
        if not User.objects.filter(username__exact=data).exists():
            raise ValidationError(_("This user does not exists"))
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == "":
            raise ValidationError(_("This field is required."))
        return data


def force_user_properties(user):
    ''' Force user properties to be set when we register them '''
    user.is_staff = True
    if BILLJOBS_FORCE_SUPERUSER is True:
        user.is_superuser = True
    if BILLJOBS_FORCE_USER_GROUP is not None:
        group = Group.objects.get(name=BILLJOBS_FORCE_USER_GROUP)
        user.groups.add(group.id)
    user.save()


def login(request):
    ''' Login view for regular users '''
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                from django.contrib.auth import login
                login(request, user)
                return redirect(request.GET.get('next', 'home'))
            else:
                form.add_error('password', 'Wrong password')
    else:
        form = UserLoginForm()
    return render(
        request,
        'billjobs/login.html',
        {'user_form': form}
    )


@login_required
def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')


def onboarding(request):
    ''' Signup view for new user '''
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        user_form = UserSignupForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            force_user_properties(user)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            send_slack_invite(user_form)
            # TODO: check response ?
            return redirect('billjobs_signup_success')
    else:
        user_form = UserSignupForm()
        profile_form = UserProfileForm()
    return render(
        request,
        'billjobs/onboarding.html',
        {'user_form': user_form, 'profile_form': profile_form}
    )


def send_slack_invite(user_form):
    # generate your token here (this has been tested with a user token) :
    # https://api.slack.com/custom-integrations/legacy-tokens
    if BILLJOBS_SLACK_TOKEN is not None:
        q = dict(token=BILLJOBS_SLACK_TOKEN, email=user_form.cleaned_data['email'],
                 first_name=user_form.cleaned_data['first_name'], last_name=user_form.cleaned_data['last_name'])
        data = urllib.parse.urlencode(q).encode("utf-8")
        urllib.request.urlopen('https://slack.com/api/users.admin.invite', data)


def signup_success(request):
    return render(request, 'billjobs/signup_success.html')


@login_required
def generate_pdf(request, bill_id):
    bill = Bill.objects.get(id=bill_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '{} "{}"'.format(
            'attachment; filename=', bill.number)

    # Create a buffer
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    # define new 0,0 bottom left with cm as margin
    pdf.translate(cm, cm)
    # define document width and height with cm as margin
    width, height = A4
    width = width - 2*cm
    height = height - 2*cm

    # if debug draw lines for document limit
    if BILLJOBS_DEBUG_PDF is True:
        pdf.setStrokeColorRGB(1, 0, 0)
        pdf.line(0, 0, width, 0)
        pdf.line(0, 0, 0, height)
        pdf.line(0, height, width, height)
        pdf.line(width, height, width, 0)

    # Put logo on top of pdf original image size is 570px/250px
    pdf.drawImage(
            BILLJOBS_BILL_LOGO_PATH,
            0,
            height-BILLJOBS_BILL_LOGO_HEIGHT,
            width=BILLJOBS_BILL_LOGO_WIDTH,
            height=BILLJOBS_BILL_LOGO_HEIGHT
            )
    # billing information
    lh = 15  # define a line height
    pdf.setFillColorRGB(0.3, 0.3, 0.3)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawRightString(width, height-lh, 'Facture')
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawRightString(width, height-2*lh, u'Numéro : %s' % bill.number)
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(
            width,
            height-3*lh,
            u'Date facturation : {}'.format(
                bill.billing_date.strftime('%d/%m/%Y'))
            )

    # define new height
    nh = height - 90

    # seller
    pdf.setFillColorRGB(0.95, 0.95, 0.95)
    pdf.setStrokeColorRGB(1, 1, 1)
    # rect(x,y,width,height)
    pdf.rect(0, nh-8*lh, width/2-40, 6.4*lh, fill=1)
    # reset fill for text color
    pdf.setFillColorRGB(0.3, 0.3, 0.3)
    pdf.drawString(10, nh-lh, 'Émetteur')
    issuer = Paragraph(bill.issuer_address, getSampleStyleSheet()['Normal'])
    issuer.wrapOn(pdf, width*0.25, 6*lh)
    issuer.drawOn(pdf, 20, nh-6*lh)

    # customer
    pdf.drawString(width/2, nh-lh, 'Adressé à')
    customer = pdf.beginText()
    customer.setTextOrigin(width/2+20, nh-3*lh)
    # create text with \n and remove \r
    text = '{} {}\n{}'.format(
            bill.user.first_name,
            bill.user.last_name,
            bill.billing_address.replace('\r', '')
            )
    # get each line
    for line in text.split('\n'):
        customer.textOut(line)
        customer.moveCursor(0, lh)
    pdf.drawText(customer)
    pdf.setStrokeColorRGB(0, 0, 0)
    # rect(x,y,width,height)
    pdf.rect(width/2, nh-8*lh, width/2, 6.4*lh, fill=0)

    # define new height
    nh = nh - 10*lh

    data = [['Désignation', 'Prix unit. HT', 'Quantité', 'Total HT']]

    for line in bill.billline_set.all():
        description = '{} - {}\n{}'.format(
                line.service.reference,
                line.service.name,
                '\n'.join(wrap(line.service.description, 62)))

        if line.note:
            description = '{}\n{}'.format(
                    description,
                    '\n'.join(wrap(line.note, 62)))

        line = (description, line.service.price, line.quantity, line.total)
        data.append(line)

    data.append((
        'TVA non applicable art-293B du CGI',
        '',
        'Total HT',
        '{} €'.format(bill.amount)
        ))
    data.append(('', '', 'TVA 0%', '0'))
    data.append(('', '', 'Total TTC', '{} €.'.format(bill.amount)))

    # widths in percent of pdf width
    colWidths = (width*0.55, width*0.15, width*0.15, width*0.15)
    style = [
            ('GRID', (0, 0), (-1, 0), 1, colors.black),
            ('GRID', (-2, -3), (-1, -1), 1, colors.black),
            ('BOX', (0, 1), (0, -4), 1, colors.black),
            ('BOX', (1, 1), (1, -4), 1, colors.black),
            ('BOX', (2, 1), (2, -4), 1, colors.black),
            ('BOX', (-1, 1), (-1, -4), 1, colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, -3), (0, -3), 'Helvetica-Bold'),
            ]
    table = Table(data, colWidths=colWidths, style=style)
    # create table and get width and height
    t_width, t_height = table.wrap(0, 0)
    table.drawOn(pdf, 0, nh-t_height)

    p = Paragraph(BILLJOBS_BILL_PAYMENT_INFO, getSampleStyleSheet()['Normal'])
    p.wrapOn(pdf, width*0.6, 100)
    p.drawOn(pdf, 0, 3*lh)

    pdf.line(0, 2*lh, width, 2*lh)
    pdf.setFontSize(8)
    pdf.drawCentredString(width/2.0, lh, 'Association Loi 1901')

    pdf.showPage()
    pdf.save()
    # get pdf from buffer and return it to response
    genpdf = buffer.getvalue()
    buffer.close()
    response.write(genpdf)
    return response
