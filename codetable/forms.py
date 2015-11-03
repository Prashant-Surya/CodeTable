from django import forms
from .models import Code
from django_ace import AceWidget
class CodeForm(forms.Form):
	text = forms.CharField(widget = AceWidget(showprintmargin=True))
	inp = forms.CharField(widget = forms.Textarea(attrs={'id':'input'}),required=False)
	l = [('C', 'C'), ('CPP', 'C++'), ('CPP11', 'C++11'), ('CLOJURE', 'Clojure'), ('CSS', 'CSS'), ('CSHARP', 'C#'), 
	('HTML', 'HTML'), ('GO', 'Go'), ('JAVA', 'Java'), ('JAVASCRIPT', 'Javascript(Rhino)'),
	 ('JAVASCRIPT_NODE', 'Javascript(Node.js)'), ('HASKELL', 'Haskell'), ('PERL', 'Perl'), 
	 ('PHP', 'PHP'), ('PYTHON', 'Python'), ('RUBY', 'Ruby'), ('RUST', 'Rust')]
	langs = forms.ChoiceField(l,initial='C')