import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.serializer import OrganizationSerializer, OrganizationCreateSerializer, DepartmentSerializer, \
    DepartmentCreateSerializer, HoldingCreateSerializer, HoldingSerializer, PropertySerializer
from .fixture import script
from .models import Holding, Organization, Department, MOL, Property, InventoryList


class OrganizationRetrieve(RetrieveAPIView):
    model = Organization
    serializer_class = OrganizationSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def retrieve(self, request, *args, **kwargs):
        queryset = Organization.objects.get(pk=kwargs['pk'])
        return Response({'organizations': [queryset]}, template_name='organization.html')


class OrganizationList(ListAPIView):
    queryset = Organization.objects.filter(is_deleted=False)
    model = Organization
    serializer_class = OrganizationSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        if query_name := request.query_params.get('search'):
            print(self.get_queryset().filter(is_deleted=True))
            queryset = self.get_queryset().filter(name__contains=query_name)  # TODO МБ ПОЛУЧШЕ РЕШЕНИЕ ЕСТЬ
        else:
            queryset = self.get_queryset()
        holding_queryset = Holding.objects.all()  # TODO мб придется переделывать,/
                                                  # TODO потому что 2 кверисета в одной вьюшке такое себе,/
                                                  # TODO либо не все поля возвращать

        return Response({'organizations': queryset, 'holdings': holding_queryset,
                         'success_create': bool(request.query_params.get('success_create'))},  # TODO переделать
                        template_name='organization.html')


@method_decorator(csrf_exempt, name='dispatch')
class OrganizationCreate(CreateAPIView):
    model = Organization
    serializer_class = OrganizationCreateSerializer

    def post(self, request, *args, **kwargs):

        organization = self.create(request, *args, **kwargs)

        if request.META.get('HTTP_REFERER').split('?')[0] == 'http://127.0.0.1:8000/organization/':  # TODO убрать отношение к МЕТА данным
            return redirect("http://127.0.0.1:8000/organization/?success_create=True")
        else:
            return organization


class OrganizationDelete(CreateAPIView):
    model = Organization
    serializer_class = OrganizationSerializer

    def post(self, request, *args, **kwargs):
        # map(lambda i:  setattr(i, 'is_deleted', True), [i for i in Organization.objects.filter(pk__in=request.data.keys())])
        # TODO Сделать через map как строкой выше
        for i in Organization.objects.filter(pk__in=request.data):
            # print(request.data)
            i.is_deleted = True
            i.save()
        # if request.META.get('HTTP_REFERER') is not None and request.META.get('HTTP_REFERER').split('?')[0] == 'http://127.0.0.1:8000/organization/':  # TODO убрать отношение к МЕТА данным
        #     return redirect("http://127.0.0.1:8000/organization/?success_update=True")
        # else:
        #     return Response(request.data)


class OrganizationUpdate(CreateAPIView):
    model = Organization
    serializer_class = OrganizationSerializer

    def post(self, request, *args, **kwargs):
        # print(request.data)
        for organization_row in request.data:
            obj = Organization.objects.get(pk=organization_row['id'])
            obj.name = organization_row['name']
            obj.address = organization_row['address'] # TODO через сериализатор можно или **
            # obj.holding = organization_line['holding']

            obj.save()
        # print(request.data)
        # print(1)
        return Response(request.data)
# class OrganizationDelete(DestroyAPIView):
#     def delete(self, request, *args, **kwargs):
#         if request:
#             self.destroy(request, *args, **kwargs)
#         else:


# class OrganizationDelete(DestroyAPIView):
#     model = Organization
#     serializer_class = OrganizationSerializer
#
#
# class OrganizationUpdate(DestroyAPIView):
#     model = Organization
#     serializer_class = OrganizationSerializer


class DepartmentRetrieve(RetrieveAPIView):
    model = Department
    serializer_class = DepartmentSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def retrieve(self, request, *args, **kwargs):
        queryset = Department.objects.get(pk=kwargs['pk'])
        return Response({'departments': [queryset]}, template_name='department.html')


class DepartmentList(ListAPIView):
    queryset = Department.objects.all()
    model = Department
    serializer_class = DepartmentSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        queryset = Department.objects.all()
        if query_name := request.query_params.get('search'):
            queryset = Department.objects.filter(name__contains=query_name)  # TODO МБ ПОЛУЧШЕ РЕШЕНИЕ ЕСТЬ
        if query_org_id := request.query_params.get('organization_id'):
            queryset = Department.objects.filter(organization__id=query_org_id)
        # if query_cabinet := request.query_params.get('cabinet'):
        #     queryset = Department.
        organization_queryset = Organization.objects.all()  # TODO мб придется переделывать,/
                                                  #  потому что 2 кверисета в одной вьюшке такое себе,/
                                                  #  либо не все поля возвращать

        return Response({'departments': queryset, 'organizations': organization_queryset,
                         'success_create': bool(request.query_params.get('success_create'))},  # TODO переделать
                        template_name='department.html')


@method_decorator(csrf_exempt, name='dispatch')
class DepartmentCreate(CreateAPIView):
    model = Department
    serializer_class = DepartmentCreateSerializer

    def post(self, request, *args, **kwargs):

        department = self.create(request, *args, **kwargs)

        if request.META.get('HTTP_REFERER').split('?')[0] == 'http://127.0.0.1:8000/department/':  # TODO убрать отношение к МЕТА данным
            return redirect("http://127.0.0.1:8000/department/?success_create=True")
        else:
            return department


class HoldingRetrieve(RetrieveAPIView):
    model = Holding
    serializer_class = HoldingSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def retrieve(self, request, *args, **kwargs):
        queryset = Holding.objects.get(pk=kwargs['pk'])
        return Response({'holdings': [queryset]}, template_name='holding.html')


class HoldingList(ListAPIView):
    queryset = Holding.objects.all()
    model = Holding
    serializer_class = HoldingSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        queryset = Holding.objects.all()
        if query_name := request.query_params.get('search'):
            queryset = Holding.objects.filter(name__contains=query_name)  # TODO МБ ПОЛУЧШЕ РЕШЕНИЕ ЕСТЬ
        # if query_org_id := request.query_params.get('organization_id'):
        #     queryset = Department.objects.filter(organization__id=query_org_id)
        # organization_queryset = Organization.objects.all()  # TODO мб придется переделывать,/
                                                  #  потому что 2 кверисета в одной вьюшке такое себе,/
                                                  #  либо не все поля возвращать

        return Response({'holdings': queryset,
                         # 'organizations': organization_queryset,
                         'success_create': bool(request.query_params.get('success_create'))},  # TODO переделать
                        template_name='holding.html')


@method_decorator(csrf_exempt, name='dispatch')
class HoldingCreate(CreateAPIView):
    model = Holding
    serializer_class = HoldingCreateSerializer

    def post(self, request, *args, **kwargs):

        holding = self.create(request, *args, **kwargs)

        if request.META.get('HTTP_REFERER').split('?')[0] == 'http://127.0.0.1:8000/holding/':  # TODO убрать отношение к МЕТА данным и изменить так, чтобы работало на сервере
            return redirect("http://127.0.0.1:8000/holding/?success_create=True")
        else:
            return holding

    # script()

# class FixtureCreate(CreateAPIView):
#     def post (self, request, *args, **kwargs):
#


class Inner(ListAPIView):
    queryset = Department.objects.all()
    model = Department
    serializer_class = DepartmentSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):

        queryset = InventoryList.objects.all()
        if query_name := request.query_params.get('search'):
            queryset = InventoryList.objects.filter(MOL__department__cabinet__contains=query_name)
          # TODO мб придется переделывать,/
        properties = Property.objects.all().order_by('name')
                                                  #  потому что 2 кверисета в одной вьюшке такое себе,/
                                                  #  либо не все поля возвращать

        return Response({'invent_lists': queryset, 'properties': properties,
                         'success_create': bool(request.query_params.get('success_create'))},  # TODO переделать
                        template_name='handler.html')


class InnerUpdate(CreateAPIView):
    model = InventoryList
    serializer_class = OrganizationSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        for inv_row in request.data:
            print(inv_row)
            obj = InventoryList.objects.get(pk=inv_row['id'])
            obj.MOL.department.cabinet = inv_row['cabinet']
            obj.invent_num = inv_row['inv_num']
            obj.property = Property.objects.get(pk=inv_row['property_id'])

            # prop = Property.objects.get(pk=obj.property.id)
            # prop.name = inv_row['property_name']
            # prop.save()

            obj.amount = inv_row['amount']
            obj.description = inv_row['description']
            obj.save()
            print(obj)

        return Response(request.data)


class PropertyCreate(CreateAPIView):
    queryset = Property.objects.all()
    model = Property
    serializer_class = PropertySerializer
