from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#0057A3', help_text="Hex color code")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Resource type application flags
    apply_to_all_resources = models.BooleanField(default=True)
    apply_to_mcq = models.BooleanField(default=False)
    apply_to_videos = models.BooleanField(default=False)
    apply_to_notes = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    @property
    def full_path(self):
        """Returns the full hierarchical path of the tag"""
        return self.name

    def get_resource_count(self):
        """Returns the count of resources associated with this tag"""
        # This is a placeholder - implement based on actual relationships
        # For example, if there's a Question model with a many-to-many field for tags:
        # return self.question_set.count()
        return 0


class Subtag(models.Model):
    tag = models.ForeignKey(Tag, related_name='subtags', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, blank=True, help_text="If blank, inherits from parent tag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Subtag'
        verbose_name_plural = 'Subtags'
        unique_together = ['tag', 'name']
        
    def __str__(self):
        return f"{self.tag.name} > {self.name}"
        
    @property
    def full_path(self):
        """Returns the full hierarchical path of the subtag"""
        return f"{self.tag.name} > {self.name}"
    
    @property
    def display_color(self):
        """Returns the subtag's color or inherits from parent if not specified"""
        if self.color:
            return self.color
        return self.tag.color
    
    def get_resource_count(self):
        """Returns the count of resources associated with this subtag"""
        # This is a placeholder - implement based on actual relationships
        return 0
