from django.urls import path, include
from . import views

app_name = 'staff'

urlpatterns = [
    # Authentication
    path('login/', views.AdminLoginView.as_view(), name='login'),
    path('logout/', views.AdminLogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # User Management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/bulk-upload/', views.BulkUserUploadView.as_view(), name='user_bulk_upload'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.UserEditView.as_view(), name='user_edit'),
    path('users/<int:pk>/export/', views.UserExportView.as_view(), name='user_export'),
    
    # Question Management
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/add/', views.QuestionCreateView.as_view(), name='question_add'),
    path('questions/<int:pk>/edit/', views.QuestionEditView.as_view(), name='question_edit'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('questions/bulk-upload/', views.BulkQuestionUploadView.as_view(), name='question_bulk_upload'),
    path('questions/bulk-action/', views.QuestionBulkActionView.as_view(), name='question_bulk_action'),
    path('questions/export/', views.QuestionExportView.as_view(), name='question_export'),
    path('questions/toggle-status/', views.QuestionToggleStatusView.as_view(), name='question_toggle_status'),
    path('ajax/get-topics/', views.GetTopicsAjaxView.as_view(), name='get_topics_ajax'),
    
    # Subject and Topic Management
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject_add'),
    path('subjects/<int:pk>/edit/', views.SubjectEditView.as_view(), name='subject_edit'),
    path('subjects/ajax/add/', views.SubjectCreateAjaxView.as_view(), name='subject_ajax_add'),
    path('subjects/ajax/<int:pk>/edit/', views.SubjectEditAjaxView.as_view(), name='subject_ajax_edit'),
    path('subjects/toggle-status/', views.SubjectToggleStatusView.as_view(), name='subject_toggle_status'),
    path('subjects/<int:pk>/topics/', views.GetSubjectTopicsView.as_view(), name='get_subject_topics'),
    path('topics/', views.TopicListEnhancedView.as_view(), name='topic_list'),
    path('topics/add/', views.TopicCreateView.as_view(), name='topic_add'),
    path('topics/<int:pk>/edit/', views.TopicEditView.as_view(), name='topic_edit'),
    path('topics/ajax/add/', views.TopicCreateAjaxEnhancedView.as_view(), name='topic_ajax_add'),
    path('topics/ajax/<int:pk>/edit/', views.TopicEditAjaxEnhancedView.as_view(), name='topic_ajax_edit'),
    path('topics/toggle-status/', views.TopicToggleStatusView.as_view(), name='topic_toggle_status'),
    path('topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    
    # Tag Management
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/add/', views.TagCreateView.as_view(), name='tag_add'),
    path('tags/<int:pk>/edit/', views.TagEditView.as_view(), name='tag_edit'),
    path('tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
    
    # Quiz Management
    path('quizzes/', views.QuizAttemptListView.as_view(), name='quiz_list'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    
    # Resource Management
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/notes/add/', views.NoteCreateView.as_view(), name='note_add'),
    path('resources/notes/<int:pk>/edit/', views.NoteEditView.as_view(), name='note_edit'),
    path('resources/videos/add/', views.VideoCreateView.as_view(), name='video_add'),
    path('resources/videos/<int:pk>/edit/', views.VideoEditView.as_view(), name='video_edit'),
    path('resources/flashcards/add/', views.FlashcardCreateView.as_view(), name='flashcard_add'),
    path('resources/flashcards/<int:pk>/edit/', views.FlashcardEditView.as_view(), name='flashcard_edit'),
    
    # Payment Management
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/review/', views.PaymentReviewView.as_view(), name='payment_review'),
    path('payments/history/', views.PaymentHistoryView.as_view(), name='payment_history'),
    
    # Support Management
    path('support/', views.SupportInboxView.as_view(), name='support_inbox'),
    path('support/<int:pk>/', views.SupportMessageView.as_view(), name='support_message'),
    
    # Settings and Logs
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('logs/', views.ActivityLogsView.as_view(), name='logs'),
]
