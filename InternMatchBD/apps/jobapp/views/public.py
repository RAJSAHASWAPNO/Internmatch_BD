from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.db.models import F
from jobapp.models import Job
from jobapp.selectors import get_listed_jobs, search_jobs
from jobapp.constants import CONTACT_INFO

User = get_user_model()


def home_view(request):
   
    published_jobs = Job.objects.filter(is_published=True, is_deleted=False).order_by('-updated_at')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page', None)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        job_lists = []
        for job_list in page_obj.object_list.values():
            job_lists.append(job_list)
        data = {
            'job_lists': job_lists,
            'current_page_no': page_obj.number,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'no_of_page': paginator.num_pages,
            'prev_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        }
        return JsonResponse(data)

    
    stats = cache.get('home_stats')
    if not stats:
        stats = {
            'total_candidates': User.objects.filter(role='employee').count(),
            'total_companies': User.objects.filter(role='employer').count(),
            'total_jobs': jobs.count(),
            'total_completed_jobs': published_jobs.filter(is_closed=True).count(),
        }
        cache.set('home_stats', stats, 60 * 15)

    context = {
        'total_candidates': stats['total_candidates'],
        'total_companies': stats['total_companies'],
        'total_jobs': stats['total_jobs'],
        'total_completed_jobs': stats['total_completed_jobs'],
        'page_obj': page_obj,
    }
    return render(request, 'jobapp/index.html', context)


def about_view(request):
    
    context = {
        'page_title': 'About InternMatch BD',
    }
    return render(request, 'jobapp/about.html', context)


def contact_view(request):
    
    context = {
        'page_title': 'Contact InternMatch BD',
        'contact_info': CONTACT_INFO,
    }
    return render(request, 'jobapp/contact.html', context)


class JobListView(ListView):
    
    template_name = 'jobapp/job-list.html'
    context_object_name = 'page_obj'
    paginate_by = 12

    def get_queryset(self):
        user_id = self.request.GET.get('user_id')
        if user_id:
            # If viewing own jobs (logged in as the job poster), show all active jobs
            if self.request.user.is_authenticated and str(self.request.user.id) == user_id:
                return Job.objects.prefetch_related('skills').select_related('user').filter(user_id=user_id).order_by('-updated_at')
            # Otherwise, only show published and open jobs
            return get_listed_jobs().filter(user_id=user_id)
        return get_listed_jobs()


class SingleJobView(DetailView):
   
    template_name = 'jobapp/job-single.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        job_id = self.kwargs['id']
        
        # Try to get from cache first
        job = cache.get(job_id)
        if job is None:
            # Check if job exists (active jobs only)
            try:
                job = Job.objects.get(id=job_id)
            except Job.DoesNotExist:
                # If not found in active jobs, check if it exists at all and if user is the owner
                if self.request.user.is_authenticated:
                    try:
                        job = Job.all_objects.get(id=job_id, user=self.request.user)
                    except Job.DoesNotExist:
                        # Job doesn't exist or user is not the owner
                        raise Http404("Job not found")
                else:
                    # Not authenticated, can't view non-published jobs
                    raise Http404("Job not found")
            
            cache.set(job_id, job, 60 * 15)
        
       
        if job.is_deleted and (not self.request.user.is_authenticated or job.user != self.request.user):
            raise Http404("Job not found")
        
        if not job.is_published and (not self.request.user.is_authenticated or job.user != self.request.user):
            raise Http404("Job not found")
        
        Job.objects.filter(id=job_id).update(views_count=F('views_count') + 1)
        job.views_count += 1
        cache.set(job_id, job, 60 * 15)
            
        return job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            related_job_list = self.object.tags.similar_objects()
        except (KeyError, Exception):
            
            tag_ids = self.object.tags.values_list('id', flat=True)
            if tag_ids:
                related_job_list = Job.objects.filter(
                    tags__id__in=tag_ids
                ).exclude(id=self.object.id).distinct().order_by('-updated_at')[:20]
            else:
               
                related_job_list = Job.objects.filter(
                    job_type=self.object.job_type,
                    is_published=True,
                    is_deleted=False
                ).exclude(id=self.object.id).order_by('-updated_at')[:20]
        
        paginator = Paginator(related_job_list, 5)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        context['total'] = len(related_job_list)
        return context


class SearchResultView(ListView):
    
    template_name = 'jobapp/result.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        return search_jobs(
            title_or_company=self.request.GET.get('job_title_or_company_name'),
            location=self.request.GET.get('location'),
            job_type=self.request.GET.get('job_type'),
        )



