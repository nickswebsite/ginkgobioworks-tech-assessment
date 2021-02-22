from django import forms
from django.contrib import admin
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template.response import TemplateResponse
from django.urls import path

from protein_search.importer import import_sequences
from protein_search.models import ProteinSearchJob, ProteinDatabaseEntry


class ImportProteinDatabaseEntryForm(forms.Form):
    identifiers = forms.CharField(widget=forms.Textarea)


class ProteinDatabaseEntryModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        return super().get_urls() + [
            path('import-protein-database-entry', self.import_protein_database_entry_view),
        ]

    def import_protein_database_entry_view(self, request):
        if request.method == "GET":
            form = ImportProteinDatabaseEntryForm()
            return TemplateResponse(request, "protein_search/import-protein-database-entry.html", {"form": form})
        elif request.method == "POST":
            form = ImportProteinDatabaseEntryForm(request.POST)
            if form.is_valid():
                identifiers_str = form.cleaned_data["identifiers"]
                identifiers = identifiers_str.split()

                import_sequences(identifiers)

                return HttpResponse(f"Import running for the given identifiers: {identifiers}")
            else:
                return TemplateResponse(request, "protein_search/import-protein-database-entry.html", {"form": form})
        else:
            return HttpResponseNotAllowed(["GET", "POST"])


admin.site.register(ProteinSearchJob)
admin.site.register(ProteinDatabaseEntry, ProteinDatabaseEntryModelAdmin)
