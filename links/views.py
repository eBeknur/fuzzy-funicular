from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Link
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
import json
from pathlib import Path

class LinksView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'upload_link.html')

    def post(self, request):
        file = request.FILES.get('file')
        url = request.POST.get('url')
        description = request.POST.get('description')
        views = request.POST.get('views', 0)

        if not file :
            messages.error(request, "Fayl va URL kiritilishi shart.")
            return redirect('/')

        Link.objects.create(
            file=file,
            description=description,
            views=views,
            author=request.user
        )

        messages.success(request, "Link muvaffaqiyatli yuklandi.")
        return redirect('/')





class LinkDetailView(View):
    def get(self, request, url):
        link = get_object_or_404(Link, url=url)

        if timezone.now() - link.created_at >= timedelta(hours=24):
            link.delete()
            return render(request, "link_detail.html", {"expired": True})

        ip_address = self.get_client_ip(request)
        user = request.user.username if request.user.is_authenticated else "Anonymous"

        log_data = {
            "user": user,
            "ip_address": ip_address,
            "url": str(link.url),
            "accessed_at": timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Terminalga chiqarish
        print(f"[LOG] {log_data}")

        # JSON faylga yozish
        self.save_log_to_json(log_data)

        remaining_time = (link.created_at + timedelta(hours=24)) - timezone.now()

        return render(request, "link_detail.html", {
            "link": link,
            "expired": False,
            "remaining_time": remaining_time
        })

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def save_log_to_json(self, log_data):
        log_file_path = Path("logs/access_logs.json")
        try:
            with log_file_path.open("r") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []

        logs.append(log_data)

        with log_file_path.open("w") as f:
            json.dump(logs, f, indent=2)




class UserLinksView(LoginRequiredMixin, View):
    def get(self, request):
        links = Link.objects.filter(author=request.user)
        return render(request, 'user_links.html', {'links': links})