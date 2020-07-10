from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid
from django.contrib.auth.models import User


class UserInvoicesManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().filter(....)
        return super().get_queryset().all()

# Create your models here.

class Invoice(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """
    #managers
    objects = models.Manager() #by default
    user_invoices = UserInvoicesManager() #manager for user's invoices

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique ID")
    ##user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sap_entity_code = models.CharField(max_length=4,help_text="SAP номер предприятия")
    sap_vendor_code = models.CharField(max_length=10,help_text="SAP номер поставщика")
    i_vendor_code = models.CharField(max_length=10, help_text="ЕДРПОУ")
    i_vendor_name = models.CharField(max_length=40, help_text="Наименование поставщика")
    sap_document_code = models.CharField(blank=True, max_length=10, help_text="Номер SAP документа")
    sap_document_year = models.CharField(blank=True, max_length=4, help_text="Год SAP документа")
    vendor_contract_number = models.CharField(max_length=20, help_text="Номер договора поставщика")
    doc_date = models.DateField(null=True, help_text="Дата накладной")
    doc_amount = models.FloatField(null=True,help_text="Сумма накладной в валюте документа")
    doc_currency=models.CharField(max_length=3, help_text="Валюта документа")
    doc_duedate = models.DateField(help_text="Дата оплаты по договору")
    vendor_document_code = models.CharField(max_length=20, help_text="Номер накладной поставщика")
    doc_payment_block = models.CharField(blank=True, max_length=1, help_text="Блокировка платежа")


    # Metadata
    class Meta:
        ordering = ["vendor_contract_number"]

    # Methods
    #def get_absolute_url(self):
     #   """
      #  Returns the url to access a particular instance of MyModelName.
       # """
        #return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return '%s, %s' % (self.sap_vendor_code, self.vendor_document_code)





class Entity(models.Model):

    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    sap_entity_code = models.CharField(primary_key=True, max_length=4, verbose_name="Балансовая единица", help_text="Балансовая единица")
    entity_name = models.CharField(max_length=20,verbose_name="Наименования предприятия", help_text="Наименования предприятия")
    business = models.ForeignKey("Business",on_delete=models.CASCADE)


    # Metadata
    class Meta:
        ordering = ["business","sap_entity_code"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.sap_entity_code)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.entity_name

class Vendor(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    sap_vendor_code = models.CharField(primary_key=True, max_length=10, verbose_name="SAP номер поставщика", help_text="SAP номер поставщика")
    vendor_edrpou = models.CharField(max_length=10, verbose_name="Балансовая единица", help_text="Балансовая единица")
    vendor_name = models.CharField(max_length=30,verbose_name="Наименование поставщика", help_text="Наименование поставщика")
    bank_limit = models.FloatField(verbose_name="Сумма лимита факторинга банка", help_text="Сумма лимита факторинга банка")
    red_zone = models.BooleanField(verbose_name="Красная зона", default=False, help_text="Красная зона")

    # Metadata
    class Meta:
        ordering = ["vendor_edrpou"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.sap_vendor_code)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.vendor_name

class Business(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    business = models.CharField(primary_key=True, max_length=3, verbose_name="Бизнес-блок", help_text="Бизнес-блок")
    business_limit_forward = models.FloatField(verbose_name="Сумма лимита переходящего", help_text="Сумма лимита переходящего")
    business_limit_week1 = models.FloatField(verbose_name="Сумма лимита неделя 1", help_text="Сумма лимита неделя 1")
    business_limit_week2 = models.FloatField(verbose_name="Сумма лимита неделя 2", help_text="Сумма лимита неделя 2")
    business_limit_week3 = models.FloatField(verbose_name="Сумма лимита неделя 3", help_text="Сумма лимита неделя 3")
    business_limit_week4 = models.FloatField(verbose_name="Сумма лимита неделя 4", help_text="Сумма лимита неделя 4")
    business_limit_week5 = models.FloatField(verbose_name="Сумма лимита неделя 5", help_text="Сумма лимита неделя 5")


    # Metadata
    class Meta:
        ordering = ["business"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.business)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.business

class BKLimit(models.Model):
    """
    A typical class defining a model, derived from the Model class.
    """

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    business = models.ForeignKey("Business", on_delete=models.CASCADE)
    sap_vendor_code = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    comment = models.CharField(max_length=30, verbose_name="Комментарий", help_text="Комментарий")
    bk_limit_forward = models.FloatField(verbose_name="Сумма лимита переходящего", help_text="Сумма лимита переходящего")
    bk_limit_week1 = models.FloatField(verbose_name="Сумма лимита неделя 1", help_text="Сумма лимита неделя 1")
    bk_limit_week2 = models.FloatField(verbose_name="Сумма лимита неделя 2", help_text="Сумма лимита неделя 2")
    bk_limit_week3 = models.FloatField(verbose_name="Сумма лимита неделя 3", help_text="Сумма лимита неделя 3")
    bk_limit_week4 = models.FloatField(verbose_name="Сумма лимита неделя 4", help_text="Сумма лимита неделя 4")
    bk_limit_week5 = models.FloatField(verbose_name="Сумма лимита неделя 5", help_text="Сумма лимита неделя 5")


    # Metadata
    class Meta:
        ordering = ["business","sap_vendor_code"]

    # Methods
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return '%s, %s' % (self.business, self.sap_vendor_code)