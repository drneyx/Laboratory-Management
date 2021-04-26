from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse


from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Group
from django.db.models import Count
from .utils import cookieCart, cartData
import json
from slb.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
# Create your views here.
def index(request):

    equipment = Equipments.objects.all()
    total_quantity = sum([item.quantity for item in equipment ])
    total_eq = equipment.count()


    students = Students.objects.all()
    total_students = students.count()
    print(total_eq)

    uncollected_equipments = Equipments.objects.filter(borrowed=True, returned=False)
    quantity_uncollected = sum([item.quantity for item in uncollected_equipments])
    total_uncollected = uncollected_equipments.count()
    
    available_equipments = Equipments.objects.filter(borrowed=False, returned=True)
    quantity_available = sum([item.quantity for item in available_equipments])
    total_available = available_equipments.count()


    reserve= Reserve.objects.filter(approved=False, returned=False)
    reserveItem=  ReserveItem.objects.all().filter(reserve__in=reserve)
    reserved_total = sum([item.quantity for item in reserveItem])

    new_reserve= Reserve.objects.filter(returned=False)
    new_reserveItem=  ReserveItem.objects.all().filter(reserve__in=new_reserve)
    new_reserved_total = sum([item.quantity for item in new_reserveItem])

    new_available = total_quantity - new_reserved_total

    context = {'equipment': total_eq, 
            'total_students':total_students, 
            'total_uncollected':total_uncollected, 
            'total_available':total_available, 
            'reserveItem':reserveItem,
            'total_quantity': total_quantity,
            'quantity_uncollected': quantity_uncollected,
            'quantity_available':quantity_available,
            'new_available': new_available,
            'reserved_equipment': new_reserved_total,
            'reserved_total': reserved_total}
    return render(request, 'slb1/admin/index.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)

        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='students'):
            if user.students.status == True:
                auth_login(request, user)
                return redirect('student_home')
            else:
                messages.warning(
                    request, 'Your application is still pending please wait until it is approved!')
        elif user is not None and user.is_staff:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Username or password is incorrect')
            return redirect('login')
    context = {}
    return render(request, 'slb1/auth/login.html')


def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            idn ='LMS2021-00'+str(user.id) 

            student, created = Students.objects.get_or_create(user=user, idn=idn)
            request.user.students = student

            group, created = Group.objects.get_or_create(name='students')
            user.groups.add(group)
            return redirect('login')
            
    context = {'form': form}
    return render(request, 'slb1/auth/register.html', context)


def equipment(request):
    equipment = Equipments.objects.all()
    total_quantity = sum([item.quantity for item in equipment ])
    # total_eq = equipment.count()

    context={'equipment':equipment, 'total_equipment':total_quantity}
    return render(request, 'slb1/admin/equipment.html', context)


def new_equipment(request):

    form = EquipmentForm()

    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.warning(request, 'Equipment added successfuly')
            return redirect('equipment')
        else:
            messages.warning(request, 'An error has occured')
            return redirect('new_equipment')
    context = {'form':form}
    return render(request, 'slb1/admin/new_equipment.html', context)


def update_equipment(request, pk):
    equipment = Equipments.objects.get(pk=pk)

    form = EquipmentForm(instance=equipment)
 
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)

        if form.is_valid():
            form.save()
            messages.warning(request, 'Equipment Updated successfuly')
            return redirect('equipment')
        else:
            messages.warning(request, 'An error has occured')
            return redirect('new_equipment')
    
    context = {'form':form}
    return render(request, 'slb1/admin/new_equipment.html', context)


def delete_equipment(request, pk):
    equipment = Equipments.objects.get(pk=pk)
    equipment.delete()
    messages.warning(request, 'successfully deletd the equipment')
    return redirect('equipment')


def students(request):
    students = Students.objects.all()

    context = {'students':students}
    return render(request, 'slb1/admin/students.html', context)



def student_home(request):
    equipment = Equipments.objects.all()

    data  = cartData(request)
    cartItems = data['cartItems']


    context = {'equipment': equipment, 'cartItems':cartItems}
    return render(request, 'slb1/student/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def reserve_summary(request):
    data  = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems }
    print(context)
    return render(request, 'slb1/student/reserve_summary.html', context)



def updateItem(request):
    data = json.loads(request.body)
    equipmentId = data['equipmentId']
    action =data['action']
    
    print('houseId:',equipmentId)
    print('action:',action)
    
    student = request.user.students
    
    equipment = Equipments.objects.get(id=equipmentId)
    # equipment.borrowed == True
    reserve, created = Reserve.objects.get_or_create(student=student, returned=False)
    
    reserveItem, created =  ReserveItem.objects.get_or_create(reserve=reserve, equipment=equipment)
    
    if action == 'add':
        if(reserveItem.quantity + 1 <= equipment.quantity):
            reserveItem.quantity = (reserveItem.quantity + 1)
        else:
            messages.warning(request, 'Sorry! There is no more equipment of this type')
    elif action == 'remove':
        reserveItem.quantity = (reserveItem.quantity - 1)
    reserveItem.save()
    
    
    if reserveItem.quantity <= 0:
        reserveItem.delete()
        
    
    return JsonResponse('item was added', safe=False)


def reserved(request):

    student = request.user.students

    reserve= Reserve.objects.filter(student=student)
    
    equipment = Equipments.objects.all().filter(borrowed=True)
    reserveItem=  ReserveItem.objects.all().filter(reserve__in=reserve)

    print(reserveItem)

    context = {'reserveItem': reserveItem}
    return render(request, 'slb1/student/reserved.html', context)


def approve(request, pk):
    reserve = Reserve.objects.get(pk=pk)
    reserve.approved = True
    reserve.save()
    messages.success(request, 'Successfully approved the equipments to students')
    return redirect('index')


def complete_order(request, pk):
    reserve = Reserve.objects.get(pk=pk)
    reserve.collect = True
    reserve.save()
    messages.success(request, 'Successfully reserved! please wait for the approval from the lab technician')
    return redirect('rcart')




def collection(request):
    reserve= Reserve.objects.filter(approved=True)
    reserveItem=  ReserveItem.objects.all().filter(reserve__in=reserve)
    reserved_total = sum([item.quantity for item in reserveItem])

    context = {'reserveItem': reserveItem}
    return render(request, 'slb1/admin/collection.html', context)


def collect(request, pk):
    reserve = Reserve.objects.get(pk=pk)
    reserve.returned = True
    reserve.save()
    messages.success(request, 'Equipment collected successfully!')
    return redirect('collection')


def student_approve(request, pk):
    student = Students.objects.get(pk=pk)
    student.status = True
    student.save()
    subject = 'Account Verification'
    message = 'Congratulation your account has now been activated you can log in using your creditials.'
    recepient = str(student.user.email)
    print(recepient)
    send_mail(subject,
                  message,  DEFAULT_FROM_EMAIL,  [recepient], fail_silently=False)
    messages.success(
            request, 'Successfully approved the student')
    return redirect('students')

    