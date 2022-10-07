from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import django_filters

from statistic.models.models import Statistic
from statistic.serializers import statistic as statistic_serializer
from statistic.models.choices import StatisticQPData


class StatisticQPSwagger(django_filters.FilterSet):
    data = openapi.Parameter(
        name="data",
        in_=openapi.IN_QUERY,
        description=f"What data you need: "
        f"{StatisticQPData.DEFAULT.name}, "  # pylint: disable=E1101
        f"{StatisticQPData.DAILY_STATS.name}, "  # pylint: disable=E1101
        f"{StatisticQPData.CASH_AMOUNT.name}",  # pylint: disable=E1101
        type=openapi.TYPE_STRING,
    )
    operation = openapi.Parameter(
        name="operation",
        in_=openapi.IN_QUERY,
        description=f"What should be done: {StatisticQPData.RESET.name}",  # pylint: disable=E1101
        type=openapi.TYPE_STRING,
    )


@method_decorator(name="list", decorator=swagger_auto_schema(manual_parameters=[StatisticQPSwagger.data]))
@method_decorator(name="create", decorator=swagger_auto_schema(manual_parameters=[StatisticQPSwagger.operation]))
class StatisticViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Statistic.objects.all()
    serializer_class = statistic_serializer.StatisticDefaultSerializer

    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment

    def parse_data_request(self):
        if "data" not in self.request.query_params:
            return StatisticQPData.DEFAULT.name

        if self.request.query_params["data"] not in StatisticQPData.values:  # pylint: disable=E1101:
            return StatisticQPData.DEFAULT.name

        return self.request.query_params["data"]

    def parse_operation_request(self):
        if "operation" not in self.request.query_params:
            return StatisticQPData.DEFAULT.name

        if self.request.query_params["operation"] not in StatisticQPData.values:  # pylint: disable=E1101:
            return StatisticQPData.DEFAULT.name

        return self.request.query_params["operation"]

    def get_queryset(self):
        data_choice = self.parse_data_request()

        if data_choice == StatisticQPData.CASH_AMOUNT.name:
            # TODO: Return object and not array of one object
            return Statistic.objects.get_cash_amount()  # pylint: disable=E1120

        if data_choice == StatisticQPData.DAILY_STATS.name:
            return Statistic.objects.get_daily_stats()

        if data_choice == StatisticQPData.SHOP_STATS.name:
            return Statistic.objects.get_shop_state()

        return super(StatisticViewSet, self).get_queryset()  # default

    def get_serializer_class(self):
        data_choice = self.parse_data_request()
        operation_choice = self.parse_operation_request()

        if data_choice == StatisticQPData.CASH_AMOUNT.name:
            return statistic_serializer.StatisticCashAmountSerializer  # pylint: disable=E1120

        if data_choice == StatisticQPData.DAILY_STATS.name:
            return statistic_serializer.StatisticDailyStatsSerializer  # pylint: disable=E1120

        if operation_choice == StatisticQPData.RESET.name:
            return statistic_serializer.StatisticResetSerializer  # pylint: disable=E1120

        return super(StatisticViewSet, self).get_serializer_class()  # default

    def query_params_data_choice(self, request) -> str:
        if "data" in request.query_params:
            return request.query_params["data"]

    def list(self, request, *args, **kwargs):
        return super(StatisticViewSet, self).list(request)

    def create(self, request: Request, *args, **kwargs):
        operation_choice = self.parse_operation_request()

        if operation_choice == StatisticQPData.RESET.name:
            return super().create(request)

        # Error
        return Response(
            data={"error": f"{StatisticViewSet.create.__qualname__} - Expected operation type: (RESET, ...)"},
            status=status.HTTP_400_BAD_REQUEST,
        )