import random
import string

from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.business_name.replace(" ", ""))
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def unique_slug_generator_booking(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify("B")
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=9)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def unique_slug_generator_services(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify("ser")
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=5)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_slug_generator_product(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name.replace(" ", ""))
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=5)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_slug_generator_staff(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.first_name)
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug, company=instance.company).exists()
    if qs_exists:
        new_slug = "{slug}{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=2)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def unique_slug_generator_order(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify("O")
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=9)
        )
        return unique_slug_generator_order(instance, new_slug=new_slug)
    return slug