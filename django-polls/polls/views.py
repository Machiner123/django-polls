from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone

#notice the somewhat complicated list comp, where we say q.question_text for q in... quite clever to use q this way
#render takes only the request, the name of the template(here its file) and the dictionary 
#so that the html and python know what each others variables are called.
#dont need HttpResponse with render, it creates an HttpResponse object

#index() first defines latest_question_list then puts it into context, which the template later uses
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


	
def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		#a request.post object is like a dictionary that maps keys to submitted data
		#choice being the key here, and if we remember from the template, choice = choice.id.
		#pay careful attention to how objects are stored in variables, in this case in selected_choice
		#the reason there is a KeyError, is in because choice=id, the choic is the key, and it returns
		#an error if there is no data for this ket in the POST data
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#redisplay the question voting form if the user hits submit without choosing a choice
		#since this would create a request.POST object with an id not listed in question.choice_set
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice",
		})
	#the else clause executes code as if it was in the try block, but it avoids raising additional exceptions 
	#since it is after the except clause. think of it as additional try code.
	#the request.POST object, stored in selected_choice, has IntegerField attribute called .vote, and this else
	#clause performs += on it then saves the value
	else:
		selected_choice.votes+= 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button
		# this is alled Redirect because it does not send data back to the same view it came from, instead
		# it sends it to url named 'results' in app_name polls, in regards to questin object with id of choice.question.id
		# notice also, that this is one big function with a HttpResoinseRedirect object as a return value, which 
		# redictect the submitter to a new url - in otherwrds the new polls:vote url's return valye is polls:results
		return HttpResponseRedirect(reverse('polls: results', args=(question.id)))
# Create your views here.
