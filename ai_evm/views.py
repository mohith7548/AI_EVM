from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings 
from django.core.mail import EmailMessage 
from threading import Thread
from mailjet_rest import Client
from .models import Voter, Party, Vote


'''
1. Persons detections
2. Mask detection
3. Face Recognition
4. Vote 
'''

# fetch only firstnames for face recognition phase
names = Voter.objects.values_list('first_name', flat=True)


def init_session(request):
    request.session['phase_1'] = False
    request.session['phase_2'] = False
    request.session['phase_3'] = False
    request.session['phase_4'] = False


def start(request):
    # check for app state is initialized or not
    if 'phase_1' not in request.session:
        init_session(request)

    if request.method == 'POST':
        if not request.session['phase_1']:
            # get # of persons
            from detect_person.camera import PERSON_COUNT 
            request.session['persons'] = PERSON_COUNT
            print('PERSONS:', PERSON_COUNT)

            if PERSON_COUNT == 1:
                messages.success(request, 'Persons Detection Phase completed')
                request.session['phase_1'] = True
                return render(request, 'index.html', {'stream': 'detect_mask'})
            else:
                messages.error(request, 'More than one person not allowed in the Polling Booth!')
                return render(request, 'index.html', {'stream': 'detect_person'})

        elif not request.session['phase_2']:
            # get mask status
            from detect_mask.camera import HAS_MASK
            request.session['has_mask'] = HAS_MASK
            print('HAS_MASK:', HAS_MASK)

            if not HAS_MASK:
                # mark as complete & render phase-3
                messages.success(request, 'Mask Detection Phase completed')
                request.session['phase_2'] = True
                return render(request, 'index.html', {'stream': 'recognize_face'})
            else:
                # revert back to same phase
                messages.warning(request, 'Please remove your mask!')
                return render(request, 'index.html', {'stream': 'detect_mask'})
        
        elif not request.session['phase_3']:
            # get face name
            from recognize_face.camera import FACE_NAME
            request.session['face_name'] = FACE_NAME
            print('FACE_NAME:', FACE_NAME)

            if FACE_NAME in names:
                # mark as complete & move to phase_4 (voting)
                messages.success(request, 'Face Recognition Phase completed')
                request.session['phase_3'] = True
                # if alread voted clear session & send back to main page
                request.method = 'GET'
                return start(request)
            else:
                messages.error(request, 'Your nomination is not in this constituency!')
                return render(request, 'index.html', {'stream': 'recognize_face'})

        elif not request.session['phase_4']:
            voted_to = Party.objects.get(name=request.POST['voted_to'])
            voter = Voter.objects.get(first_name=request.session['face_name'])
            Vote(voter=voter, voted_to=voted_to).save()
            Thread(target= success, args=(voter, voted_to.full_name)).start()
            # return JsonResponse(dict(request.POST))
            messages.success(request, 'Thank for you vote! Your vote has been received!')
            request.session.flush()
            request.method = 'GET'
            return start(request)
        
        else:
            return HttpResponse('No suitable POST condition satisfied!')

    else:
        if not request.session['phase_1']:
            return render(request, 'index.html', context = {'stream': 'detect_person'})
        if not request.session['phase_2']:
            return render(request, 'index.html', context = {'stream': 'detect_mask'})
        if not request.session['phase_3']:
            return render(request, 'index.html', context = {'stream': 'recognize_face'})
        if not request.session['phase_4']:
            if len(Vote.objects.filter(voter__first_name=request.session['face_name'])) > 0:
                messages.error(request, 'Sorry, You have already voted!')
                request.session.flush()
                request.method = 'GET'
                return start(request)
            else:
                return render(request, 'index.html', {'pts': Party.objects.all()})




def dbg(request):
    return JsonResponse(dict(request.session))


def success(voter, voted_to):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "nktchhn1997@gmail.com",
            "Name": "Ankit"
        },
        "To": [
            {
            "Email": voter.email, # In future make sure to query by pk
            "Name": voter.first_name
            }
        ],
        "Subject": "Greetings AI-EVM.",
        "TextPart": "Your vote has been counted",
        "HTMLPart": f"<h3>Dear {voter.first_name}, This mail is to remind you that your vote has been taken into consideration! <br> You have voted to {voted_to} </h3><br />Thank You!",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)