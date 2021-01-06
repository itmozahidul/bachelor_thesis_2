# Create your views here.
import json
import os
import re
import sys
from typing import List, Any

from django.conf import settings
from django.shortcuts import render
from scipy import spatial
from sent2vec.vectorizer import Vectorizer
from django.core.files.storage import FileSystemStorage
from tkinter import messagebox

from .Mscripts.get_random_number_unequal import get_random_number_unequal
from .Mscripts.get_similer_sentences import get_similer_sentences
from .Mscripts.get_sentence_from_file import get_sentence_from_file
from .Mscripts.group_similer_vectors import group_similer_vectors
from .Mscripts.save_in_jason import save_in_json, edit_in_json


class fileInfo:
    def __init__(self, url, name):
        self.name = name
        self.url = url


def register(request):
    email = []
    password = []
    if len(request.POST) == 0:
        return render(request, 'register.html', {'mesg': ''})
    else:
        if os.path.isfile('./media/User_Info/UserInfo.json'):
            with open('./media/User_Info/UserInfo.json') as ufr1:
                user_data1 = json.load(ufr1)
                for e in user_data1['email']:
                    email.append(e)
                for p in user_data1['password']:
                    password.append(p)
            ufr1.close()

        email.append(request.POST['email'])
        password.append(request.POST['password'])
        u_n_p = {
            'email': email,
            'password': password
        }
        with open('./media/User_Info/UserInfo.json', 'w') as uf:
            json.dump(u_n_p, uf)
        uf.close()
        return render(request, 'register.html', {'mesg': 'Regristation Successful !'})


def logout(request):
    return render(request, 'login.html', {'mesg': 'logged out, please log in !'})


def login(request):
    email = ""
    u_lock = 0
    p_lock = 0
    if len(request.POST) < 3:
        return render(request, 'login.html', {'mesg': ''})
    else:
        email = request.POST['email']
        password = request.POST['password']
        if os.path.isfile('./media/User_Info/UserInfo.json'):
            with open('./media/User_Info/UserInfo.json') as ufr:
                user_data = json.load(ufr)
                if email in user_data['email']:
                    u_lock = 1
                if password in user_data['password']:
                    p_lock = 1
            ufr.close()
            if u_lock == 1 and p_lock == 1:
                return render(request, 'main.html', {'user': email})
            else:
                return render(request, 'login.html', {'mesg': 'failed. please retry !!'})
        else:
            return render(request, 'login.html', {'mesg': 'failed. please retry !!!'})


def collect(request):
    if request.POST:
        if not request.POST['user'] == "":

            [fleiss_kappa, con] = edit_in_json(request.POST)
            context = {
                'user': request.POST['user'],
                'edited': con,
                'fleiss_kappa': fleiss_kappa

            }
            return render(request, 'main.html', context)
        else:
            return render(request, 'login.html', {'mesg': 'logged out. please log in again!'})
    else:
        return render(request, 'login.html', {'mesg': ''})


def k_mean(request):
    message = ''
    c_l_s = []
    sentence = request.POST['sentences']
    k = request.POST['k']
    sepsent = re.split('\n', sentence)
    print(sepsent)
    vectorizer = Vectorizer()
    vectorizer.bert(sepsent)
    vectors_bert = vectorizer.vectors
    vecTosen_dictionary = {}

    counter = 0
    for v in vectors_bert:
        vecTosen_dictionary[sum(v)] = sepsent[counter]
        counter = counter + 1

    [clusters, x, y] = group_similer_vectors(vectors_bert, k)
    if len(clusters) != 0:
        for cluster in clusters:
            print('################################')
            c = []
            for y in cluster.listelement:
                c.append(vecTosen_dictionary[sum(y)])
            c_l_s.append(c)
    else:
        message += 'wrong cluster no. it should be less then sentence numbers'

    context = {
        'clustered_sentences': c_l_s,
        'k': len(c_l_s),
        'msg': message,
        'x': x,
        'y': y,
    }
    return render(request, 'main.html', context)


def main(request):
    if request.POST:
        if not request.POST['user'] == "":
            user = ""
            saved = 0
            jason_data = {}
            query_n_sentences_list = []
            sepsent = []
            sepsent2 = []
            queries = []
            if request.POST:
                user = request.POST['user']
            if request.FILES:
                HateSpeechFile = request.FILES['hatespeechfname']
                SeceondFile = request.FILES['fname']
                sepsent = get_sentence_from_file(HateSpeechFile)
                sepsent2 = get_sentence_from_file(SeceondFile)
                rand_index_list = get_random_number_unequal(2, (len(sepsent) - 1))
                queries = []
                for n in rand_index_list:
                    queries.append(sepsent[n])
            if len(sepsent) != 0 and len(queries) != 0:
                query_n_sentences_list = get_similer_sentences(sepsent, sepsent2, 4)
                saved = save_in_json(query_n_sentences_list)
            context = {'query_n_sentences_list': query_n_sentences_list,
                       'user': user
                       }

            return render(request, 'main.html', context)
        else:
            return render(request, 'login.html', {'mesg': 'logged out. please log in again!'})
    else:
        return render(request, 'login.html', {'mesg': ''})


def add(request):
    if request.FILES:
        uploadedFile = request.FILES['fname']
        sepsent = get_sentence_from_file(uploadedFile)
        print(sepsent)
        i = 1
        Svectors = []  # list of all bert vectors
        centroids = {}  # list of centers of clusters

        # for each cluster we defined separate distance and vector list
        Dist1 = []
        Dist2 = []
        Dist3 = []
        Dist4 = []
        Cluster1 = []
        Cluster2 = []
        Cluster3 = []
        Cluster4 = []

        # showing the progress information on the display
        i = 0

        # we take each sentence from the list and calculate its bert representation in vector
        for x in sepsent:
            progress_percent = round(((i * 100) / len(sepsent)), 2)
            remained_time_h = int(((7 * len(sepsent)) - (i * 7)) / 3600)
            remained_time_m = ((7 * len(sepsent)) - (i * 7)) % 3600
            print(' ----------------  progress :' + str(progress_percent) + '% ---------remaining time(hh:mm): ' + str(
                remained_time_h) + ':' + str(remained_time_m) + ' ------', end='\r')
            i = i + 1

            vectorizer = Vectorizer()
            vectorizer.bert(x)
            vectors_bert = vectorizer.vectors
            Svectors.append(vectors_bert[0])
        # we took 4 random centers for k means algorithm
        if os.path.isfile('center_json_data.json'):
            pfc = open('center_json_data.json')
            jcenter = json.load(pfc)
            pfc.close()
            centroid1 = jcenter['center1']
            centroid2 = jcenter['center2']
            centroid3 = jcenter['center3']
            centroid4 = jcenter['center4']

        else:
            centroid1v = sum(Svectors) / len(Svectors)
            centroid2v = sum(Svectors) / (len(Svectors) / 2)
            centroid3v = sum(Svectors) / (len(Svectors) / 10)
            centroid4v = sum(Svectors) / (len(Svectors) / 28)
            centroid1 = centroid1v.tolist()
            centroid2 = centroid2v.tolist()
            centroid3 = centroid3v.tolist()
            centroid4 = centroid4v.tolist()

        print(centroid1)

        # creating json format for them to save them later

        lock1 = 0
        lock2 = 0
        lock3 = 0
        lock4 = 0

        loop_no = 0

        while True:
            print('---cluster:---')
            print(len(Cluster1))
            print(len(Cluster2))
            print(len(Cluster3))
            print(len(Cluster4))

            print('----------------')

            print('#######################')
            if len(Cluster1) > 0:
                if (centroid1 != (sum(Cluster1) / len(Cluster1))).all():
                    centroidiv1 = sum(Cluster1) / len(Cluster1)
                    centroid1 = centroidiv1.tolist()

                else:
                    lock1 = 1
            else:
                if loop_no > 100:
                    lock1 = 1
            if len(Cluster2) > 0:
                if (centroid2 != (sum(Cluster2) / len(Cluster2))).all():
                    centroidiv2 = sum(Cluster2) / len(Cluster2)
                    centroid2 = centroidiv2.tolist()

                else:
                    lock2 = 1
            else:
                if loop_no > 100:
                    lock2 = 1
            if len(Cluster3) > 0:
                if (centroid3 != (sum(Cluster3) / len(Cluster3))).all():
                    centroidiv3 = sum(Cluster3) / len(Cluster3)
                    centroid3 = centroidiv3.tolist()

                else:
                    lock3 = 1
            else:
                if loop_no > 100:
                    lock3 = 1
            if len(Cluster4) > 0:
                if (centroid4 != (sum(Cluster4) / len(Cluster4))).all():
                    centroidiv4 = sum(Cluster4) / len(Cluster4)
                    centroid4 = centroidiv4.tolist()

                else:
                    lock4 = 1
            else:
                if loop_no > 100:
                    lock4 = 1
            Dist1.clear()
            Cluster1.clear()
            Dist2.clear()
            Cluster2.clear()
            Dist3.clear()
            Cluster3.clear()
            Dist4.clear()
            Cluster4.clear()
            for x in Svectors:

                Tdist1 = spatial.distance.cosine(centroid1, x)
                Tdist2 = spatial.distance.cosine(centroid2, x)
                Tdist3 = spatial.distance.cosine(centroid3, x)
                Tdist4 = spatial.distance.cosine(centroid4, x)

                if Tdist1 == min([Tdist1, Tdist2, Tdist3, Tdist4]):
                    Dist1.append(Tdist1)
                    Cluster1.append(x)
                elif Tdist2 == min([Tdist1, Tdist2, Tdist3, Tdist4]):
                    Dist2.append(Tdist2)
                    Cluster2.append(x)
                elif Tdist3 == min([Tdist1, Tdist2, Tdist3, Tdist4]):
                    Dist3.append(Tdist3)
                    Cluster3.append(x)
                elif Tdist4 == min([Tdist1, Tdist2, Tdist3, Tdist4]):
                    Dist4.append(Tdist4)
                    Cluster4.append(x)
            print('---lock---')
            print(lock1)
            print(lock2)
            print(lock3)
            print(lock4)
            loop_no = loop_no + 1
            if lock1 == 1 and lock2 == 1 and lock3 == 1 and lock4 == 1:
                print('break')
                break

        json_center = {'center1': centroid1,
                       'center2': centroid2,
                       'center3': centroid3,
                       'center4': centroid4,
                       }

        with open('center_json_data.json', 'w') as fc:
            json.dump(json_center, fc)
        fc.close()

        if os.path.isfile('meanDistance_json_data.json'):
            pfd = open('meanDistance_json_data.json')
            jdist = json.load(pfd)
            previous_dist1 = jdist['dist1']
            previous_dist2 = jdist['dist2']
            previous_dist3 = jdist['dist3']
            previous_dist4 = jdist['dist4']
            if previous_dist1 != 0:
                Dist1.append(previous_dist1)
            if previous_dist2 != 0:
                Dist2.append(previous_dist2)
            if previous_dist3 != 0:
                Dist3.append(previous_dist3)
            if previous_dist4 != 0:
                Dist4.append(previous_dist4)

        if len(Dist1) > 0:
            MeanDist1 = sum(Dist1) / len(Dist1)
        else:
            MeanDist1 = 0
        if len(Dist2) > 0:
            MeanDist2 = sum(Dist2) / len(Dist2)
        else:
            MeanDist2 = 0
        if len(Dist3) > 0:
            MeanDist3 = sum(Dist3) / len(Dist3)
        else:
            MeanDist3 = 0
        if len(Dist4) > 0:
            MeanDist4 = sum(Dist4) / len(Dist4)
        else:
            MeanDist4 = 0

        json_MeanDist = {'dist1': MeanDist1,
                         'dist2': MeanDist2,
                         'dist3': MeanDist3,
                         'dist4': MeanDist4,
                         }
        with open('meanDistance_json_data.json', 'w') as fd:
            json.dump(json_MeanDist, fd)
        fd.close()

        context = {
            'center': 'centroi', 'dist': 'MeanDist'
        }
    else:
        context = {
            'filename': '', 'dist': ''}
    return render(request, 'ndex.html', context)


def evaluate(request):
    fc = open('center_json_data.json')
    jcenter = json.load(fc)
    center1 = jcenter['center1']
    center2 = jcenter['center2']
    center3 = jcenter['center3']
    center4 = jcenter['center4']
    fd = open('meanDistance_json_data.json')
    jdist = json.load(fd)
    dist1 = jdist['dist1']
    dist2 = jdist['dist2']
    dist3 = jdist['dist3']
    dist4 = jdist['dist4']
    text = request.GET['text']
    vectorizer = Vectorizer()
    vectorizer.bert(text)
    vectors_bert = vectorizer.vectors
    Tdist1 = spatial.distance.cosine(center1, vectors_bert[0].tolist())
    Tdist2 = spatial.distance.cosine(center2, vectors_bert[0].tolist())
    Tdist3 = spatial.distance.cosine(center3, vectors_bert[0].tolist())
    Tdist4 = spatial.distance.cosine(center4, vectors_bert[0].tolist())
    print(Tdist1)
    print(Tdist2)
    print(Tdist3)
    print(Tdist4)
    result = ''
    if Tdist1 < dist1:
        result = 'hatespeech'
    elif Tdist2 < dist2:
        result = 'hatespeech'
    elif Tdist3 < dist3:
        result = 'hatespeech'
    elif Tdist4 < dist4:
        result = 'hatespeech'
    else:
        result = 'not hatespeech'
    context = {
        'title': 'evaluating', 'result': result
    }
    return render(request, 'evaluate.html', context)
