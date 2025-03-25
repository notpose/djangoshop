from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Wishlist, Cart, CartItem, MonthlyProfit
import json

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'model', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category', 'brand', 'has_smart_tv', 'has_3d', 'has_hdr',
                  'show_technical_specs', 'show_additional_features', 'show_interfaces']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'brand', 'model', 'technical_specs_description',
                    'additional_features_description', 'interfaces_description']
    readonly_fields = ['created', 'updated']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description', 'image', 'price', 'stock', 'available')
        }),
        ('Отображение разделов', {
            'fields': ('show_technical_specs', 'show_additional_features', 'show_interfaces'),
            'classes': ('collapse',)
        }),
        ('Брендинг', {
            'fields': ('brand', 'model', 'country_of_origin', 'warranty_months', 'sale_price')
        }),
        ('Технические характеристики', {
            'fields': (
                ('screen_size', 'resolution'),
                ('color', 'weight'),
                ('dimensions', 'power_consumption'),
                'technical_specs_description'
            ),
            'classes': ('collapse',)
        }),
        ('Дополнительные функции', {
            'fields': (
                ('has_wifi', 'has_bluetooth', 'has_smart_tv'),
                ('has_3d', 'has_hdr'),
                ('has_dolby_vision', 'has_dolby_atmos'),
                'additional_features_description'
            ),
            'classes': ('collapse',)
        }),
        ('Интерфейсы', {
            'fields': (
                ('hdmi_ports', 'usb_ports'),
                ('ethernet_port', 'optical_audio', 'headphone_jack'),
                'interfaces_description'
            ),
            'classes': ('collapse',)
        }),
        ('Заказ', {
            'fields': ('minimum_order_quantity', 'unit')
        }),
        ('Метаданные', {
            'fields': ('created', 'updated')
        }),
    )

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['user__username']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'total_price', 'total_items']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'subtotal']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['cart__user__username', 'product__name']

@admin.register(MonthlyProfit)
class MonthlyProfitAdmin(admin.ModelAdmin):
    list_display = ['month', 'profit', 'created_at', 'updated_at']
    list_filter = ['month']
    search_fields = ['month']
    ordering = ['-month']
    
    def changelist_view(self, request, extra_context=None):
        # Получаем данные для графика
        profits, predictions, future_predictions = MonthlyProfit.get_profit_data()
        
        # Подготавливаем данные для графика
        chart_data = {
            'labels': [p.month.strftime('%B %Y') for p in profits] + 
                     [p['month'].strftime('%B %Y') for p in future_predictions],
            'actual': [float(p.profit) for p in profits] + 
                     [None] * len(future_predictions),
            'predictions': [float(p) if p is not None else None for p in predictions] + 
                         [float(p['prediction']) for p in future_predictions]
        }
        
        # Добавляем данные в контекст
        extra_context = extra_context or {}
        extra_context['chart_data'] = json.dumps(chart_data)
        
        return super().changelist_view(request, extra_context=extra_context)
    
    class Media:
        js = ('https://cdn.jsdelivr.net/npm/chart.js', 'admin/js/chart.js',)
