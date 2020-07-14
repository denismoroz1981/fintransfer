from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .models import Invoice, Entity, Vendor, BKLimit, Business
# Create your views here.



def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_invoices = Invoice.objects.all().count()
    num_vendors = Vendor.objects.all().count()
    # Доступные книги (статус = 'a')
    #num_limits = BKLimit.objects.filter(status__exact='a').count()
    num_limits = BKLimit.objects.count()
    num_entities = Entity.objects.count()  # Метод 'all()' применен по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_invoices': num_invoices, 'num_vendors': num_vendors,
                 'num_limits': num_limits, 'num_entities': num_entities},
    )

from django.views import generic

"""
class InvoiceListView(generic.ListView):
    model = Invoice
    ids = []
    #context_object_name = 'my_invoice_list'  # ваше собственное имя переменной контекста в шаблоне
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и иниуиализируем ее некоторым значением
        #context['ids'] = self.ids
        #context['ids'] = self.ids
        return context

    def get_queryset(self):

      if self.request.GET:
           self.ids.clear()
           get_list = self.request.GET.dict()
           get_list.pop("csrfmiddlewaretoken")
           for key in get_list:
               self.ids.append(key)
           #self.ids = self.ids[:]

           queryset = Invoice.objects.filter(id__in=self.ids)

     #  queryset = Invoice.objects.all()
      else:
           queryset = Invoice.objects.all()

      return queryset
    #template_name = 'templates/invoices/invoice_list.html'  # Определение имени вашего шаблона и его расположения

    #def get_queryset(self):
        #return Invoice.objects.all()
"""

def createuser (request):
    """
    function to create new user
    """
    from django.contrib.auth.models import User

    # Создайте пользователя и сохраните его в базе данных
    user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

    # Обновите поля и сохраните их снова
    user.first_name = 'John'
    user.last_name = 'Citizen'
    user.save()
    return render(
        request,
        'index.html',
        context={'num_invoices': "new user created"},
    )

def send (request):
    sent = False
    if request.POST:
        form = EmailPostForm(request.POST)
        if form.is_valid():
            send_ids = []
            get_list = request.POST.dict()
            get_list.pop("csrfmiddlewaretoken")
            get_list.pop("email")
            for key in get_list:
                send_ids.append(key)

            send_invoices = Invoice.user_invoices.filter(id__in=send_ids)
            #send_invoices = get_object_or_404(queryset)
            cd = form.cleaned_data
            #sending form...

            subject = "Подтверждение КЗ по поставщику..."
            html_message = render_to_string('cabinet/mail_template.html',{'invoice_list':send_invoices})
            plain_message = strip_tags(html_message)
            send_mail(subject,plain_message,'admin@myblog.com',[cd['email']],html_message=html_message)
            sent = True


    invoice_list = Invoice.user_invoices.filter(i_vendor_code=request.user)
    form = EmailPostForm()

    return render(request,"cabinet/invoice_list.html",{'invoice_list': invoice_list, 'form':form,'sent':sent})