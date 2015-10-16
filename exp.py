***************************************fonction de création d une compagne de test ******************************
@login_required
def add(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.owner = User.objects.get(username=request.user)
            c = form.save(commit=False)
            c.owner = request.user.get_username()
            c.save()
            return HttpResponseRedirect("/campaigns/all")
        else:
            return render_to_response('campaign/add.html', {'form': form}, context_instance=RequestContext(request))
    else:
        con = {'form': CampaignForm}
        return render_to_response('campaign/add.html', con, context_instance=RequestContext(request))

************************************* fonction de modification d una compagne de test *********************

@login_required
def edit(request, id):
    csrfContext = RequestContext(request)
    campaign = Campaign.objects.get(pk=id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/campaigns/all")
        else:
            return render_to_response('campaign/edit.html', {'error': True, 'form': form})
    else:
        form = CampaignForm(instance=campaign)
        return render_to_response('campaign/edit.html', {'form': form})

***************fonction de création d un test sous format xml ***************************************

def generatexmlFile(request):
    json_data = json.loads(request.body)
    test = Element('test')
    test.set('name', json_data['nameTest'])
    test.set('description', json_data['descriptionTest'])
    test.set('severity', json_data['severityTest'])
    indent(test)
    tree = ElementTree(test)
    for json_one_data in json_data['data']:
        testStep = Element('testStep')
        testStep.set('name', json_one_data['name'])
        testStep.set('description', json_one_data['description'])
        testStep.set('priority',json_one_data['priority'])
        test.append(testStep)
        if str(json_one_data['assertexist']) == 'True':
            Assert=Element('assert')
            Extractions=Element('Extractions')
            Verifications=Element('Verifications')
            Actions=Element('Actions')
            for ass in json_one_data['assert']:
                for extra in ass['Extractions']:

                    extract = Element('Extract')
                    extract.set('function', extra['function'])
                    for pi in extra['values']:
                        extract.set(pi['name'],pi['value'])
                    Extractions.append(extract)
                Assert.append(Extractions)
                for verif in ass['Verifications']:

                    if str(verif[0]['type'])== 'Check':
                        verifica=Element(verif[0]['type'])
                        verifica.set('first_operand',verif[0]['verifications'][0]['checks'][0]['first_operand'])
                        verifica.set('operator',verif[0]['verifications'][0]['checks'][0]['operator'])
                        verifica.set('second_operand',verif[0]['verifications'][0]['checks'][0]['second_operand'])
                        Verifications.append(verifica)
                    else:
                        verificat=Element(verif[0]['type'])
                        verifica=Element('Check')
                        verifica.set('first_operand',verif[0]['verifications'][0]['checks'][0]['first_operand'])
                        verifica.set('operator',verif[0]['verifications'][0]['checks'][0]['operator'])
                        verifica.set('second_operand',verif[0]['verifications'][0]['checks'][0]['second_operand'])
                        verificat.append(verifica)
                        verifica=Element('Check')
                        verifica.set('first_operand',verif[0]['verifications'][0]['checks'][1]['first_operand1'])
                        verifica.set('operator',verif[0]['verifications'][0]['checks'][1]['operator1'])
                        verifica.set('second_operand',verif[0]['verifications'][0]['checks'][1]['second_operand1'])
                        verificat.append(verifica)
                        Verifications.append(verificat)

                Assert.append(Verifications)

                action1=Element('False')
                action2=Element('True')
                for act in ass['Actions']:
                    if str(act['action'])=='False':
                        actionFalse=Element(act['function'])
                        for val in act['values']:
                            actionFalse.set(val['name'], val['value'])
                        action1.append(actionFalse)

                    else:
                        actionTrue=Element(act['function'])
                        for val1 in act['values']:
                            actionTrue.set(val1['name'],val1['value'])
                        action2.append(actionTrue)

                Actions.append(action1)
                Actions.append(action2)
            Assert.append(Actions)
            testStep.append(Assert)

        for l in json_one_data['sessions']:
            session = Element('session')
            session.set('name',l['name'])
            testStep.append(session)
            if str(l['assertexist']) == 'True':
                Assert=Element('assert')
                Extractions=Element('Extractions')
                Verifications=Element('Verifications')
                Actions=Element('Actions')
                for ass in l['assert']:
                    for extra in ass['Extractions']:
                        extract = Element('Extract')
                        extract.set('function', extra['function'])
                        for pi in extra['values']:
                            extract.set(pi['name'],pi['value'])
                        Extractions.append(extract)
                    Assert.append(Extractions)
                    for verif in ass['Verifications']:

                        if str(verif[0]['type'])== 'Check':
                            verifica=Element(verif[0]['type'])
                            verifica.set('first_operand',verif[0]['verifications'][0]['checks'][0]['first_operand'])
                            verifica.set('operator',verif[0]['verifications'][0]['checks'][0]['operator'])
                            verifica.set('second_operand',verif[0]['verifications'][0]['checks'][0]['second_operand'])
                            Verifications.append(verifica)
                        else:
                            verificat=Element(verif[0]['type'])
                            verifica=Element('Check')
                            verifica.set('first_operand',verif[0]['verifications'][0]['checks'][0]['first_operand'])
                            verifica.set('operator',verif[0]['verifications'][0]['checks'][0]['operator'])
                            verifica.set('second_operand',verif[0]['verifications'][0]['checks'][0]['second_operand'])
                            verificat.append(verifica)
                            verifica=Element('Check')
                            verifica.set('first_operand',verif[0]['verifications'][0]['checks'][1]['first_operand1'])
                            verifica.set('operator',verif[0]['verifications'][0]['checks'][1]['operator1'])
                            verifica.set('second_operand',verif[0]['verifications'][0]['checks'][1]['second_operand1'])
                            verificat.append(verifica)
                            Verifications.append(verificat)

                    Assert.append(Verifications)

                    action1=Element('False')
                    action2=Element('True')
                    for act in ass['Actions']:
                        if str(act['action'])=='False':
                            actionFalse=Element(act['function'])
                            for val in act['values']:
                                actionFalse.set(val['name'], val['value'])
                            action1.append(actionFalse)

                        else:
                            actionTrue=Element(act['function'])
                            for val1 in act['values']:
                                actionTrue.set(val1['name'],val1['value'])
                            action2.append(actionTrue)

                    Actions.append(action1)
                    Actions.append(action2)
                Assert.append(Actions)
                session.append(Assert)
            for n in l['procedures']:
                print n['name']
                if n['type'] == 'procedure':
                    procedure = Element('procedure')
                    procedure.set('name', n['name'])
                    for prc in n['variables']:
                        procedure.set(prc['name'], str(prc['value']));
                    session.append(procedure)
                else:
                    command = Element('Command')
                    command.set('name', n['name'])
                    session.append(command)

                if str(n['assertexist']) == 'True':
                    Assert=Element('assert')
                    Extractions=Element('Extractions')
                    Verifications=Element('Verifications')
                    Actions=Element('Actions')
                    for ass in n['assert']:
                        for extra in ass['Extractions']:
                            extract = Element('Extract')
                            extract.set('function', extra['function'])
                            for pi in extra['values']:
                                extract.set(pi['name'],pi['value'])
                            Extractions.append(extract)
                        Assert.append(Extractions)
                        for verif in ass['Verifications']:

                            if str(verif[0]['type'])== 'Check':
                                verifica=Element(verif[0]['type'])
                                verifica.set('first_operand',verif[0]['verifications'][0]['checks'][0]['first_operand'])
                                verifica.set('operator',verif[0]['verifications'][0]['checks'][0]['operator'])
                                verifica.set('second_operand',verif[0]['verifications'][0]['checks'][0]['second_operand'])
                                Verifications.append(verifica)
                            else:
                                verificat=Element(verif[0]['type'])
                                verifica=Element('Check')
                                verifica.set('first_operand',verif[0]['verifications'][0]['checks'][0]['first_operand'])
                                verifica.set('operator',verif[0]['verifications'][0]['checks'][0]['operator'])
                                verifica.set('second_operand',verif[0]['verifications'][0]['checks'][0]['second_operand'])
                                verificat.append(verifica)
                                verifica=Element('Check')
                                verifica.set('first_operand',verif[0]['verifications'][0]['checks'][1]['first_operand1'])
                                verifica.set('operator',verif[0]['verifications'][0]['checks'][1]['operator1'])
                                verifica.set('second_operand',verif[0]['verifications'][0]['checks'][1]['second_operand1'])
                                verificat.append(verifica)
                                Verifications.append(verificat)

                        Assert.append(Verifications)

                        action1=Element('False')
                        action2=Element('True')
                        for act in ass['Actions']:
                            if str(act['action'])=='False':
                                actionFalse=Element(act['function'])
                                for val in act['values']:
                                    actionFalse.set(val['name'], val['value'])
                                action1.append(actionFalse)

                            else:
                                actionTrue=Element(act['function'])
                                for val1 in act['values']:
                                    actionTrue.set(val1['name'],val1['value'])
                                action2.append(actionTrue)

                        Actions.append(action1)
                        Actions.append(action2)
                    Assert.append(Actions)
                    command.append(Assert)
            #session.set('name',l['name'])
    namefile=json_data['nameTest']+'.xml'
    print prettify(test)
    tree.write(open('TestiMaWeb/static/test/'+namefile, 'a+'), xml_declaration=True, encoding='utf-8', method="xml")
    #open('./static/'+namefile).read()
    return HttpResponse(open('TestiMaWeb/static/test/'+namefile).read(),content_type='text/xml')
