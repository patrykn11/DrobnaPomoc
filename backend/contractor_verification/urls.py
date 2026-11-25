from django.urls import path

from . import views

urlpatterns = [
    path("questions/", views.QuestionListView.as_view(), name="verification-questions"),
    path(
        "applications/me/", views.MyApplicationsView.as_view(), name="my-applications"
    ),
    path(
        "applications/",
        views.ConsultantApplicationsView.as_view(),
        name="verification-applications",
    ),
    path(
        "applications/<int:pk>/review/",
        views.ReviewApplicationView.as_view(),
        name="review-application",
    ),
]
