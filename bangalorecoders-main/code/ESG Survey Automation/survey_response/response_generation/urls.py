from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from .views.views_esgreports import * 
from .views.views_health import * 
from .views.views_questionnaire import * 

urlpatterns = [
    path('esgreports/keepalive/ping', HealthView.as_view(), name='health check'),
    path('esgreports/upload', ESGUploadView.as_view(), name='upload reports'),
    path('questionnaire/generatefirstdraft/pdf', SurveyQuestionnaireUpload.as_view(), name='upload Question PDF'),
    path('questionnaire/generatefirstdraft/generateAnswer', AnswerAPIView.as_view(), name='get answer'),
    path('esgreports/retrieve', ListReportAPIView.as_view(), name='get list of document uploaded'),
    path('questionnaire/generatefirstdraft/pdf/<str:reportYear>/<str:TaskId>/status', ReportStatus.as_view(), name='status of report'),
    path('firstdraftreport/download/result/<str:reportYear>', ReportPDF.as_view(), name='Get report for particular year'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)