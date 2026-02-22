from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from core_data.models import POICategory
from ml.personalization.models import UserCategoryPreference
from .serializers import CategoryNodeSerializer, UserCategoryPreferenceSerializer, UserPreferencesRequestSerializer
from rest_framework.permissions import IsAuthenticated







class CategoryLevel1APIView(APIView):
    def get(self, request):
        qs = POICategory.objects.values_list("level1", flat=True).distinct().order_by("level1")
        return Response([{"level1": l1} for l1 in qs if l1])



class CategoryLevel2APIView(APIView):
    def get(self, request):
        level1 = request.query_params.get("level1")
        if not level1:
            return Response({"error": "level1 required"}, status=400)

        qs = (
            POICategory.objects
            .filter(level1=level1)
            .values_list("level2", flat=True)
            .distinct()
            .order_by("level2")
        )

        return Response([{"level2": l2} for l2 in qs if l2])




class CategoryLevel3APIView(APIView):
    def get(self, request):
        level1 = request.query_params.get("level1")
        level2 = request.query_params.get("level2")

        if not level1 or not level2:
            return Response({"error": "level1 & level2 required"}, status=400)

        qs = (
            POICategory.objects
            .filter(level1=level1, level2=level2)
            .order_by("level3")
        )

        data = [
            {
                "category_id": c.category_id,
                "label": c.level3 or c.level2
            }
            for c in qs
        ]

        return Response(data)
    






class CategoryChoicesAPIView(APIView):
    """
    Returns categories that are suitable for user selection.
    Default: only categories that have level2 or level3 (more specific).
    """
    def get(self, request):
        only_specific = request.query_params.get("specific", "1")  # 1 = level2/3 only
        qs = POICategory.objects.all()

        if only_specific == "1":
            qs = qs.exclude(level2__isnull=True, level3__isnull=True)

        qs = qs.order_by("level1", "level2", "level3")
        data = CategoryNodeSerializer(qs, many=True).data
        return Response(data)


class UserPreferencesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        prefs = UserCategoryPreference.objects.filter(
            user=request.user
        ).select_related("category")

        return Response(
            UserCategoryPreferenceSerializer(prefs, many=True).data
        )

    @extend_schema(
        request=UserPreferencesRequestSerializer,
        responses={201: dict},
    )

    def post(self, request):
        items = request.data.get("items", [])

        UserCategoryPreference.objects.filter(
            user=request.user
        ).delete()

        created = 0
        for item in items:
            cid = item.get("category_id")
            w = item.get("weight", 1.0)

            cat = POICategory.objects.filter(category_id=int(cid)).first()
            if not cat:
                continue

            UserCategoryPreference.objects.create(
                user=request.user,
                category=cat,
                weight=float(w),
            )
            created += 1

        return Response(
            {"status": "ok", "created": created},
            status=201,
        )





class CategoryTreeAPIView(APIView):
    """
    Returns a nested tree:
    level1 -> level2 -> level3 nodes (with IDs at leaf)
    """
    def get(self, request):
        qs = POICategory.objects.all().order_by("level1", "level2", "level3")

        tree = {}
        for c in qs:
            l1 = c.level1 or "Other"
            l2 = c.level2 or "General"
            l3 = c.level3 or None

            tree.setdefault(l1, {})
            tree[l1].setdefault(l2, [])

            # نسمح بالاختيار على level2/level3:
            if l3:
                tree[l1][l2].append({"category_id": c.category_id, "label": l3})
            else:
                # لو ما فيه level3 نخلي level2 نفسه اختيار
                tree[l1][l2].append({"category_id": c.category_id, "label": l2})

        result = []
        for l1, l2_dict in tree.items():
            children_l2 = []
            for l2, leaves in l2_dict.items():
                children_l2.append({"level2": l2, "options": leaves})
            result.append({"level1": l1, "children": children_l2})

        return Response(result)

