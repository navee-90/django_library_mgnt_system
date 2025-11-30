from django.contrib import admin
from .models import Author, Category, Book, Member, Borrow


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'category', 'available_copies')
    search_fields = ('title', 'isbn')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Member)
admin.site.register(Borrow)