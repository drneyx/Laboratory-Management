import json
from .models import *



def cookieCart(request):
	try:
		rcart = json.loads(request.COOKIES['rcart'])
	except:
		rcart = { }

	print('rcart:',rcart)
	items = []
	order = {'get_reserved_total':0, 'get_reserved_items':0}
	cartItems = order['get_reserved_items']


	for i in rcart:
		try:
			cartItems += rcart[i]['quantity']

			equipment = Equipments.objects.get(id =i)
			total = rcart[i]['quantity']

			order['get_reserved_total'] += total
			order['get_reserved_items'] += rcart[i]['quantity']

			item = {
			   'equipment':{
			       'id':equipment.id,
			       'name':equipment.name,
			       'quantity':equipment.quantity,
			       'imageURL':equipment.imageURL
			   },

			   'quantity': rcart[i]['quantity'],
			   'get_total':total,
			}

			items.append(item)
		except:
			pass 
	return {'cartItems':cartItems, 'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		student = request.user.students
		reserve, created = Reserve.objects.get_or_create(student=student, returned=False)
		items =   reserve.reserveitem_set.all()
		cartItems = reserve.get_reserved_items
	else:
		return
	return {'cartItems':cartItems, 'order':reserve, 'items':items}






