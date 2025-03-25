from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_list', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.IntegerField(verbose_name='Количество на складе')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    image = models.ImageField(upload_to='products/', blank=True, verbose_name='Изображение')
    
    # Специфичные поля для электроники
    brand = models.CharField(max_length=100, blank=True, verbose_name='Бренд')
    country_of_origin = models.CharField(max_length=100, blank=True, verbose_name='Страна производитель')
    model = models.CharField(max_length=100, blank=True, verbose_name='Модель')
    warranty_months = models.IntegerField(null=True, blank=True, verbose_name='Гарантия (месяцев)')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена по акции')
    minimum_order_quantity = models.IntegerField(default=1, verbose_name='Минимальное количество для заказа')
    unit = models.CharField(max_length=20, default='шт', verbose_name='Единица измерения')
    
    # Включение/выключение разделов
    show_technical_specs = models.BooleanField(default=True, verbose_name='Показывать технические характеристики')
    show_additional_features = models.BooleanField(default=True, verbose_name='Показывать дополнительные функции')
    show_interfaces = models.BooleanField(default=True, verbose_name='Показывать интерфейсы')
    
    # Технические характеристики
    screen_size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Размер экрана (дюймы)')
    resolution = models.CharField(max_length=100, blank=True, verbose_name='Разрешение')
    color = models.CharField(max_length=50, blank=True, verbose_name='Цвет')
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Вес (кг)')
    dimensions = models.CharField(max_length=100, blank=True, verbose_name='Габариты (ШxВxГ)')
    power_consumption = models.CharField(max_length=50, blank=True, verbose_name='Потребляемая мощность')
    technical_specs_description = models.TextField(blank=True, verbose_name='Описание технических характеристик')
    
    # Дополнительные функции
    has_wifi = models.BooleanField(default=False, verbose_name='Наличие Wi-Fi')
    has_bluetooth = models.BooleanField(default=False, verbose_name='Наличие Bluetooth')
    has_smart_tv = models.BooleanField(default=False, verbose_name='Поддержка Smart TV')
    has_3d = models.BooleanField(default=False, verbose_name='Поддержка 3D')
    has_hdr = models.BooleanField(default=False, verbose_name='Поддержка HDR')
    has_dolby_vision = models.BooleanField(default=False, verbose_name='Поддержка Dolby Vision')
    has_dolby_atmos = models.BooleanField(default=False, verbose_name='Поддержка Dolby Atmos')
    additional_features_description = models.TextField(blank=True, verbose_name='Описание дополнительных функций')
    
    # Интерфейсы
    hdmi_ports = models.IntegerField(null=True, blank=True, verbose_name='Количество HDMI портов')
    usb_ports = models.IntegerField(null=True, blank=True, verbose_name='Количество USB портов')
    ethernet_port = models.BooleanField(default=False, verbose_name='Наличие Ethernet порта')
    optical_audio = models.BooleanField(default=False, verbose_name='Наличие оптического аудио выхода')
    headphone_jack = models.BooleanField(default=False, verbose_name='Наличие разъема для наушников')
    interfaces_description = models.TextField(blank=True, verbose_name='Описание интерфейсов')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.price

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField(Product, verbose_name='Товары')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-updated']

    def __str__(self):
        return f'Избранное пользователя {self.user.username}'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def update_total(self):
        """Обновляет общую сумму корзины"""
        self.total_price = sum(item.subtotal for item in self.items.all())
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    @property
    def subtotal(self):
        return self.product.current_price * self.quantity

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock:
            self.quantity = self.product.stock
        super().save(*args, **kwargs)

class MonthlyProfit(models.Model):
    month = models.DateField(unique=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-month']
        verbose_name = 'Прибыль за месяц'
        verbose_name_plural = 'Прибыль по месяцам'

    def __str__(self):
        return f"Прибыль за {self.month.strftime('%B %Y')}"

    def save(self, *args, **kwargs):
        # Устанавливаем день месяца на первое число
        self.month = self.month.replace(day=1)
        super().save(*args, **kwargs)

    @classmethod
    def get_profit_data(cls):
        """Получает данные о прибыли и предсказания"""
        profits = list(cls.objects.all().order_by('month'))
        
        if not profits:
            return [], [], []
            
        # Рассчитываем скользящую среднюю за последние 3 месяца
        predictions = []
        future_predictions = []
        
        # Рассчитываем предсказания для существующих месяцев
        for i in range(len(profits)):
            if i < 2:  # Для первых двух месяцев нет предсказания
                predictions.append(None)
            else:
                # Берем среднее значение за последние 3 месяца
                avg = sum(p.profit for p in profits[i-2:i+1]) / 3
                predictions.append(avg)
        
        # Рассчитываем предсказания на 3 месяца вперед
        if len(profits) >= 3:
            last_3_months = profits[-3:]
            last_avg = sum(p.profit for p in last_3_months) / 3
            
            # Получаем последний месяц из данных
            last_month = profits[-1].month
            
            # Добавляем предсказания на следующие 3 месяца
            for i in range(3):
                next_month = last_month.replace(month=last_month.month + i + 1)
                if next_month.month == 1:  # Если перешли на следующий год
                    next_month = next_month.replace(year=last_month.year + 1)
                
                if i == 0:  # Первый месяц - используем среднее за последние 3 месяца
                    prediction = last_avg
                elif i == 1:  # Второй месяц - используем среднее за последние 2 месяца + первое предсказание
                    prediction = (last_3_months[-2].profit + last_3_months[-1].profit + future_predictions[0]['prediction']) / 3
                else:  # Третий месяц - используем последний месяц + два предыдущих предсказания
                    prediction = (last_3_months[-1].profit + future_predictions[0]['prediction'] + future_predictions[1]['prediction']) / 3
                
                future_predictions.append({
                    'month': next_month,
                    'prediction': prediction
                })
        
        return profits, predictions, future_predictions
