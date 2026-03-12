from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from core.models.resource_models import Note, VideoResource, Flashcard
from ..forms import NoteForm, VideoResourceForm, FlashcardForm
from .user_views import StaffRequiredMixin


class ResourceListView(StaffRequiredMixin, ListView):
    """List all resources"""
    model = Note
    template_name = 'staff/resources/resource_list.html'
    context_object_name = 'resources'
    
    def get_queryset(self):
        return Note.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'note_count': Note.objects.count(),
            'video_count': VideoResource.objects.count(),
            'flashcard_count': Flashcard.objects.count(),
            'recent_notes': Note.objects.select_related('topic__subject').order_by('-created_at')[:5],
            'recent_videos': VideoResource.objects.select_related('topic__subject').order_by('-created_at')[:5],
            'recent_flashcards': Flashcard.objects.select_related('topic__subject').order_by('-created_at')[:5],
        })
        return context


class NoteListView(StaffRequiredMixin, ListView):
    """List all notes"""
    model = Note
    template_name = 'staff/resources/note_list.html'
    context_object_name = 'notes'
    paginate_by = 20


class NoteCreateView(StaffRequiredMixin, CreateView):
    """Create new note"""
    model = Note
    form_class = NoteForm
    template_name = 'staff/resources/note_form.html'
    success_url = reverse_lazy('staff:note_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class NoteEditView(StaffRequiredMixin, UpdateView):
    """Edit existing note"""
    model = Note
    form_class = NoteForm
    template_name = 'staff/resources/note_form.html'
    success_url = reverse_lazy('staff:note_list')


class VideoListView(StaffRequiredMixin, ListView):
    """List all videos"""
    model = VideoResource
    template_name = 'staff/resources/video_list.html'
    context_object_name = 'videos'
    paginate_by = 20


class VideoCreateView(StaffRequiredMixin, CreateView):
    """Create new video"""
    model = VideoResource
    form_class = VideoResourceForm
    template_name = 'staff/resources/video_form.html'
    success_url = reverse_lazy('staff:video_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class VideoEditView(StaffRequiredMixin, UpdateView):
    """Edit existing video"""
    model = VideoResource
    form_class = VideoResourceForm
    template_name = 'staff/resources/video_form.html'
    success_url = reverse_lazy('staff:video_list')


class FlashcardListView(StaffRequiredMixin, ListView):
    """List all flashcards"""
    model = Flashcard
    template_name = 'staff/resources/flashcard_list.html'
    context_object_name = 'flashcards'
    paginate_by = 20


class FlashcardCreateView(StaffRequiredMixin, CreateView):
    """Create new flashcard"""
    model = Flashcard
    form_class = FlashcardForm
    template_name = 'staff/resources/flashcard_form.html'
    success_url = reverse_lazy('staff:flashcard_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FlashcardEditView(StaffRequiredMixin, UpdateView):
    """Edit existing flashcard"""
    model = Flashcard
    form_class = FlashcardForm
    template_name = 'staff/resources/flashcard_form.html'
    success_url = reverse_lazy('staff:flashcard_list')
