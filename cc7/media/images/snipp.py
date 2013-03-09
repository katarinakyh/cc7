make data get filter etc
data = 
return HttpResponse(json.data(data), content_type='application/json')

def json(self): 
	return {
	'name': self.name
	'post': [post.json() for post in post.pbjects.filter(maker.self).order_by('name')]
	}
	loop over object. with filter. 
	
	restful api. 
	
import simplejson as json

# Parse the JSON
objs = json.loads(request.POST)

# Iterate through the stuff in the list
for o in objs:
    # Do something Djangoey with o's name and message, like
    record = SomeDjangoModel(name = o.name, message = o.message)
    record.save()
