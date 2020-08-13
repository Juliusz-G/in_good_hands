
# Django
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    """Defines category model."""
    name = models.CharField(max_length=64, verbose_name='Nazwa kategorii')

    def __str__(self):
        return self.name


INSTITUTION_TYPES = [
    (1, 'Fundacja'),
    (2, 'Organizacja porządkowa'),
    (3, 'Zbiórka lokalna')
]


class Institution(models.Model):
    """Defines institution model."""
    name = models.CharField(max_length=64, verbose_name='Nazwa instytucji')
    description = models.CharField(max_length=128, verbose_name='Opis')
    type = models.IntegerField(choices=INSTITUTION_TYPES, default=1, verbose_name='Typ')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie')

    def __str__(self):
        return self.name

    @property
    def category_names(self):
        """Returns all category names that belong to specify institution."""
        result = []
        for category in self.categories.all():
            result.append(category.name)
        return result

    @property
    def category_ids(self):
        """Returns category id that belong to specify institution."""
        result = []
        for category in self.categories.all():
            result.append(category.id)
        return result

    @property
    def type_names(self):
        """Returns institution type (name) from INSTITUTION_TYPE list."""
        return INSTITUTION_TYPES[self.type - 1][1]


class Donation(models.Model):
    """Defines donation model."""
    quantity = models.PositiveSmallIntegerField(verbose_name='Liczba worków')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='Instytucja')
    address = models.CharField(max_length=128, verbose_name='Adres')
    phone_number = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Numer telefonu')
    city = models.CharField(max_length=128, verbose_name='Miasto')
    zip_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(verbose_name='Data odbioru')
    pick_up_time = models.TimeField(verbose_name='Godzina odbioru')
    pick_up_comment = models.CharField(max_length=254, verbose_name='Komentarz')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Użytkownik')

    def __str__(self):
        return self.address
