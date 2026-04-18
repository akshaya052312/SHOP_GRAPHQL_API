import graphene
from graphene_django import DjangoObjectType
from .models import Shop, ShopEmail, ShopPhone

# GraphQL Types
class ShopEmailType(DjangoObjectType):
    class Meta:
        model = ShopEmail
        fields = ('id', 'email')

class ShopPhoneType(DjangoObjectType):
    class Meta:
        model = ShopPhone
        fields = ('id', 'phone')

class ShopType(DjangoObjectType):
    emails = graphene.List(ShopEmailType)
    phones = graphene.List(ShopPhoneType)

    class Meta:
        model = Shop
        fields = ('id', 'name', 'address')

    def resolve_emails(self, info):
        return self.emails.all()

    def resolve_phones(self, info):
        return self.phones.all()

# Query
class Query(graphene.ObjectType):
    all_shops = graphene.List(ShopType)
    shop = graphene.Field(ShopType, id=graphene.Int(required=True))

    def resolve_all_shops(self, info):
        return Shop.objects.all()

    def resolve_shop(self, info, id):
        try:
            return Shop.objects.get(pk=id)
        except Shop.DoesNotExist:
            return None

# Mutations
class CreateShop(graphene.Mutation):
    shop = graphene.Field(ShopType)

    class Arguments:
        name = graphene.String(required=True)
        address = graphene.String(required=True)
        emails = graphene.List(graphene.String)
        phones = graphene.List(graphene.String)

    def mutate(self, info, name, address, emails=None, phones=None):
        shop = Shop.objects.create(name=name, address=address)

        if emails:
            for email in emails:
                ShopEmail.objects.create(shop=shop, email=email)

        if phones:
            for phone in phones:
                ShopPhone.objects.create(shop=shop, phone=phone)

        return CreateShop(shop=shop)

class UpdateShop(graphene.Mutation):
    shop = graphene.Field(ShopType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        address = graphene.String()
        emails = graphene.List(graphene.String)
        phones = graphene.List(graphene.String)

    def mutate(self, info, id, name=None, address=None, emails=None, phones=None):
        try:
            shop = Shop.objects.get(pk=id)
        except Shop.DoesNotExist:
            return None

        if name is not None:
            shop.name = name
        if address is not None:
            shop.address = address

        shop.save()

        if emails is not None:
            shop.emails.all().delete()
            for email in emails:
                ShopEmail.objects.create(shop=shop, email=email)

        if phones is not None:
            shop.phones.all().delete()
            for phone in phones:
                ShopPhone.objects.create(shop=shop, phone=phone)

        return UpdateShop(shop=shop)

class DeleteShop(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            shop = Shop.objects.get(pk=id)
            shop.delete()
            return DeleteShop(ok=True)
        except Shop.DoesNotExist:
            return DeleteShop(ok=False)

# Mutation
class Mutation(graphene.ObjectType):
    create_shop = CreateShop.Field()
    update_shop = UpdateShop.Field()
    delete_shop = DeleteShop.Field()
