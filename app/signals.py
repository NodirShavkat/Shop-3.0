from django.db.models.signals import post_save, pre_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from .models import Product, Category

# POST SAVE & PRE SAVE
@receiver(post_save, sender=Product) # dekaratorsiz shunday yozish ham mumkin -> pre_save.connect(post_save_product, sender=Product)
def post_save_product(sender, instance, created, *args, **kwargs):
    if created:
        print("Product added, product id: ", instance.id)
    else:
        print("Product updated, product id: ", instance.id)

@receiver(pre_save, sender=Product)
def pre_save_product(sender, instance, *args, **kwargs):
    print("Product adding, product id: ", instance.id)

# @receiver(post_save, sender=Product)
# def create_category_for_product(sender, instance, created, *args, **kwargs):
#     if created:
#         category = Category.objects.create(user=instance)

@receiver(pre_delete, sender=Product)
def pre_delete_product(sender, instance, *args, **kwargs):
    print("Product deleting, product id", instance.id)

@receiver(post_delete, sender=Product)
def post_delete_product(sender, instance, *args, **kwargs):
    print("Product deleted, product id", instance.id)

# @receiver(m2m_changed, sender=Product.category.through)
# def m2m_changed_book(sender, instance, action, *args, **kwargs):
#     print(action)
#     print(kwargs)

#=============================== Category's Signals
@receiver(post_save, sender=Category) 
def post_save_product(sender, instance, created, *args, **kwargs):
    if created:
        print("Category added, category id: ", instance.id)
    else:
        print("Category updated, category id: ", instance.id)

@receiver(pre_save, sender=Category)
def pre_save_product(sender, instance, *args, **kwargs):
    print("Category adding, category id: ", instance.id)

@receiver(pre_delete, sender=Category)
def pre_delete_product(sender, instance, *args, **kwargs):
    print("Category deleting, category id", instance.id)

@receiver(post_delete, sender=Category)
def post_delete_product(sender, instance, *args, **kwargs):
    print("Category deleted, category id", instance.id)
