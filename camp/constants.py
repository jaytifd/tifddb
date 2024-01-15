from .models import *
# Create your views here.
#t_shirt_price=CampPrices.objects.filter(slug__exact="shirt").values()
#t_shirt_price_decimal=t_shirt_price[0]['price']

try:
    linens_price=CampPrices.objects.filter(slug__exact="linen").values()
    linens_price_decimal=linens_price[0]['price']

    dvd_price=CampPrices.objects.filter(slug__exact="dvd").values()
    dvd_price_decimal=dvd_price[0]['price']

    membership_price=CampPrices.objects.filter(slug__exact="membership").values()
    membership_price_decimal=membership_price[0]['price']

    shipping_price=CampPrices.objects.filter(slug__exact="shipping").values()
    shipping_price_decimal=shipping_price[0]['price']

    linen_price=CampPrices.objects.filter(slug__exact="linen").values()
    linen_price_decimal=linen_price[0]['price']

except:
    pass
