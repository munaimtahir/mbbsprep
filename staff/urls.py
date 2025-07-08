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
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/bulk-upload/', views.BulkUserUploadView.as_view(), name='bulk_user_upload'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.UserEditView.as_view(), name='user_edit'),
    path('users/export/', views.UserExportView.as_view(), name='user_export'),
    path('users/<int:pk>/export/', views.UserExportView.as_view(), name='user_export_single'),
    
    # Question Management
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('questions/add/', views.QuestionCreateView.as_view(), name='question_add'),  # Alias for templates
    path('questions/<int:pk>/edit/', views.QuestionEditView.as_view(), name='question_edit'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('questions/bulk-upload/', views.BulkQuestionUploadView.as_view(), name='bulk_question_upload'),
    path('questions/bulk-action/', views.QuestionBulkActionView.as_view(), name='question_bulk_action'),
    path('questions/export/', views.QuestionExportView.as_view(), name='question_export'),
    path('questions/toggle-status/', views.QuestionToggleStatusView.as_view(), name='question_toggle_status'),
    path('ajax/get-topics/<int:subject_id>/', views.GetTopicsAjaxView.as_view(), name='get_topics_ajax'),
    
    # Subject and Topic Management
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/create/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/edit/', views.SubjectEditView.as_view(), name='subject_edit'),
    path('subjects/ajax/add/', views.SubjectCreateAjaxView.as_view(), name='subject_ajax_add'),
    path('subjects/ajax/<int:pk>/edit/', views.SubjectEditAjaxView.as_view(), name='subject_ajax_edit'),
    path('subjects/toggle-status/', views.SubjectToggleStatusView.as_view(), name='subject_toggle_status'),
    path('subjects/<int:pk>/topics/', views.GetSubjectTopicsView.as_view(), name='get_subject_topics'),
    path('topics/', views.TopicListEnhancedView.as_view(), name='topic_list'),
    path('topics/create/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/edit/', views.TopicEditView.as_view(), name='topic_edit'),
    path('topics/bulk-upload/', views.TopicBulkUploadView.as_view(), name='topic_bulk_upload'),
    path('topics/bulk-template/', views.TopicBulkUploadTemplateView.as_view(), name='topic_template_download'),
    path('topics/ajax/add/', views.TopicCreateAjaxEnhancedView.as_view(), name='topic_ajax_add'),
    path('topics/ajax/<int:pk>/edit/', views.TopicEditAjaxEnhancedView.as_view(), name='topic_ajax_edit'),
    path('topics/toggle-status/', views.TopicToggleStatusView.as_view(), name='topic_toggle_status'),
    path('topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    
    # Tag Management
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tags/add/', views.TagCreateView.as_view(), name='tag_add'),  # Alias for templates
    path('tags/<int:pk>/edit/', views.TagEditView.as_view(), name='tag_edit'),
    path('tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
    # Tag AJAX endpoints
    path('tags/ajax/<int:pk>/', views.TagGetAjaxView.as_view(), name='tag_get_ajax'),
    path('tags/ajax/create/', views.TagCreateAjaxView.as_view(), name='ajax_tag_create'),
    path('tags/ajax/create/', views.TagCreateAjaxView.as_view(), name='tag_create_ajax'),  # Alias for templates
    path('tags/ajax/<int:pk>/update/', views.TagUpdateAjaxView.as_view(), name='tag_update_ajax'),
    path('tags/ajax/toggle-status/', views.TagToggleStatusView.as_view(), name='tag_toggle_status'),
    path('tags/ajax/bulk-action/', views.TagBulkActionView.as_view(), name='tag_bulk_action'),
    path('tags/<int:pk>/subtags/', views.GetTagSubtagsView.as_view(), name='get_tag_subtags'),
    # Subtag AJAX endpoints
    path('subtags/ajax/add/', views.SubtagCreateAjaxView.as_view(), name='subtag_create_ajax'),
    path('subtags/create/', views.SubtagCreateAjaxView.as_view(), name='subtag_create'),  # Alias for templates
    path('subtags/ajax/<int:pk>/update/', views.SubtagUpdateAjaxView.as_view(), name='subtag_update_ajax'),
    path('subtags/<int:pk>/edit/', views.SubtagUpdateAjaxView.as_view(), name='subtag_edit'),  # Alias for templates
    path('subtags/ajax/toggle-status/', views.SubtagToggleStatusView.as_view(), name='subtag_toggle_status'),
    path('subtags/ajax/delete/', views.SubtagDeleteView.as_view(), name='subtag_delete'),
    
    # Quiz Management
    path('quizzes/', views.QuizAttemptListView.as_view(), name='quiz_list'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    
    # Resource Management
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('notes/', views.NoteListView.as_view(), name='note_list'),
    path('notes/create/', views.NoteCreateView.as_view(), name='note_create'),
    path('notes/<int:pk>/edit/', views.NoteEditView.as_view(), name='note_edit'),
    path('videos/', views.VideoListView.as_view(), name='video_list'),
    path('videos/create/', views.VideoCreateView.as_view(), name='video_create'),
    path('videos/<int:pk>/edit/', views.VideoEditView.as_view(), name='video_edit'),
    path('flashcards/', views.FlashcardListView.as_view(), name='flashcard_list'),
    path('flashcards/create/', views.FlashcardCreateView.as_view(), name='flashcard_create'),
    path('flashcards/<int:pk>/edit/', views.FlashcardEditView.as_view(), name='flashcard_edit'),
    
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
