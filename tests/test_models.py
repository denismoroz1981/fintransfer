from django.test import TestCase

# Create your tests here.

from cabinet.models import Entity

class EntityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Entity.objects.create(sap_entity_code='130013', entity_name='Дельта')

    def test_sap_entity_code_label(self):
        entity=Entity.objects.get(id=1)
        field_label = entity._meta.get_field('sap_entity_code').verbose_name
        self.assertEquals(field_label,'sap_entity_code')

    def test_entity_name_label(self):
        entity=Entity.objects.get(id=1)
        field_label = entity._meta.get_field('entity_code').verbose_name
        self.assertEquals(field_label,'entity_code')


    def test_sap_entity_code_max_length(self):
        entity=Entity.objects.get(id=1)
        max_length = entity._meta.get_field('sap_entity_code').max_length
        self.assertEquals(max_length,4)

    def test_object_name_is_entity_name(self):
        entity=Entity.objects.get(id=1)
        expected_object_name = entity.entity_name
        self.assertEquals(expected_object_name,str(entity))

    def test_get_absolute_url(self):
        entity=Entity.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(entity.get_absolute_url(),'/cabinet/sap_entity_code/1')