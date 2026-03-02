from django.db import models
from django.utils import timezone
import uuid


class Category(models.Model):
    """Model for dish categories"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nom')
    description = models.TextField(blank=True, verbose_name='Description')
    display_order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Dish(models.Model):
    """Model for dishes/menu items"""
    name = models.CharField(max_length=200, verbose_name='Nom du plat')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Prix (MAD)')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes', verbose_name='Catégorie')
    image = models.ImageField(upload_to='dishes/', blank=True, null=True, verbose_name='Image')
    is_available = models.BooleanField(default=True, verbose_name='Disponible')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Plat'
        verbose_name_plural = 'Plats'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Order(models.Model):
    """Model for customer orders"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('preparing', 'En préparation'),
        ('ready', 'Prêt'),
        ('served', 'Servi'),
        ('paid', 'Payé'),
    ]

    order_id = models.CharField(max_length=20, unique=True, verbose_name='N° de commande')
    table_number = models.IntegerField(verbose_name='Numéro de table')
    items = models.JSONField(verbose_name='Articles')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Total (MAD)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Statut')
    special_instructions = models.TextField(blank=True, verbose_name='Instructions spéciales')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Mis à jour le')

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande #{self.order_id} - Table {self.table_number}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def generate_order_id(self):
        """Generate a unique order ID"""
        today = timezone.now().strftime('%Y%m%d')
        last_order = Order.objects.filter(order_id__startswith=f'MM-{today}').order_by('-order_id').first()
        if last_order:
            last_num = int(last_order.order_id.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1
        return f'MM-{today}-{new_num:04d}'

    def get_status_display_class(self):
        """Return CSS class for status badge"""
        status_classes = {
            'pending': 'badge-warning',
            'preparing': 'badge-info',
            'ready': 'badge-success',
            'served': 'badge-primary',
            'paid': 'badge-secondary',
        }
        return status_classes.get(self.status, 'badge-secondary')
