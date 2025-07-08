from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from core.models.resource_models import Note, VideoResource, Flashcard
from ..forms import NoteForm, VideoResourceForm, FlashcardForm
from .user_views import StaffRequiredMixin


class ResourceListView(StaffRequiredMixin, ListView):
    """List all resources"""
    template_name = 'staff/resources/resource_list.html'
    
    def get_queryset(self):
        return None  # Will be implemented with combined resources


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
