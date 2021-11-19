#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 16:29:31 2015

@author: weindel
"""


# ###################################### Import des librairies

import os 
from psychopy import core, visual, event, gui, data, monitors
import psychopy.logging as logging
import pandas as pd

from psychopy.constants import *


# ################################### Initialisation de la tâche,des dossiers de stockages des infos du participant/de l'expe

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

expName = 'Posner Task' 
expInfo = {'participant':'', u'tache':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr() 
expInfo['expName'] = expName

filename = _thisDir + os.sep + u'Data' + os.sep + '%s_tache%s_%s' %(expInfo['participant'],expInfo['tache'], expInfo['date'])

task = expInfo['tache']

# ###################################### Module de psychopy de gestion des sauvegardes, logs, etc.

thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)

# ###################################### Définition de l'écran de présentation, distance, largeur, résolution
mon1 = monitors.Monitor('Default')
mon1.setDistance(50) #cm
mon1.setWidth(30) #cm
mon1.setSizePix([800, 600])     

win = visual.Window(size=[800, 600], monitor=mon1, allowGUI=False, units='deg',fullscr=True)#unité = Degré d'angles visuel

# ###################################### Création d'une classe/objet réponse avec différentes caractéristiques  
class KeyResponse:
    def __init__(self):
        self.keys=[]
        self.corr=0
        self.rt=None
        self.clock=None
        self.num_trial = None
        self.num_block = None

# ###################################### Création des stimuli visuels
fixationLeft = visual.GratingStim(win=win, 
            mask='cross', size=2, 
            pos=[-6,0], sf=0, color='white')#Croix de fixation gauche

fixationRight = visual.GratingStim(win=win, 
            mask='cross', size=2, 
            pos=[6,0], sf=0, color='white')#Croix de fixation droite


stimLeft= visual.TextStim(win, height = 4, pos=[-6,0], name='stimleft', text=u"")#Initialisation des stimuli qui apparaissent à gauche
stimRight= visual.TextStim(win, height = 4, pos=[6,0], name='stimright', text=u"")#Idem à droite

texte_fin=visual.TextStim(win, height = 2, ori=0, name='texte_fin',
    text=u"Fin de la tâche %s"%task)# Texte de fin d'expérience

instructions = visual.TextStim(win, ori=0,height = 1.2, name='instructions', 
        text=u"", wrapWidth=25)
        
# ###################################### Consigne f(tâche demandée)
if task == '1':
    instructions.setText(u"Dans ce bloc expérimental, les essais sont organisés comme suit: Un stimulus de fixation ( +  +) suivi d'un stimulus cible (p.ex. a  A). \n\n  Votre tâche consiste à déterminer si les deux lettres composant le stimulus cible sont striquement identiques ou pas. Par exemple, A et A sont identiques; A et a ne sont pas identiques.  \n \n Répondez en appuyant sur les touches M et D du clavier, le plus rapidement possible tout en essayant de ne pas faire d'erreurs. ")
elif task == '2':
    instructions.setText(u"Dans ce bloc expérimental, les essais sont organisés comme suit: Un stimulus de fixation ( +  +) suivi d'un stimulus cible (p.ex. a  A). \n\n  Votre tâche consiste à déterminer si les deux lettres composant le stimulus cible représentent la même lettre ou pas.  Par exemple, A et a sont la même lettre. \n \n  Répondez en appuyant sur les touches M et D du clavier, le plus rapidement possible tout en essayant de ne pas faire d'erreurs.")
elif task == '3':
    instructions.setText(u"Dans ce bloc expérimental, les essais sont organisés comme suit: Un stimulus de fixation ( +  +) suivi d'un stimulus cible (p.ex. b  A). \n\n  Votre tâche consiste à déterminer si les deux lettres composant le stimulus cible sont du même type (deux voyelles ou deux consonnes) ou bien sont de type différent (une voyelle et une consonne).  Par exemple, A et e sont de même type, alors que B et A sont de type différent. \n\n Répondez en appuyant sur les touches M et D du clavier, le plus rapidement possible tout en essayant de ne pas faire d'erreurs.")
elif task == '0':
    instructions.setText(u"Dans ce bloc expérimental, les essais sont organisés comme suit: Un stimulus de fixation ( +  +) suivi d'un stimulus cible (p.ex. 1  4). \n\n  Votre tâche consiste à déterminer si les deux chiffres composant le stimulus cible sont identiques ou pas. \n \n Répondez en appuyant sur les touches M et D du clavier, le plus rapidement possible tout en essayant de ne pas faire d'erreurs.")
else:
    core.quit()

################################### INSTRUCTIONS
while True:
    instructions.draw()
    win.flip()
    instr_event= event.getKeys()
    if instr_event:
        break
    if event.getKeys(["escape"]): core.quit()

#############################TRIALS


#Gestionnaire des essais
trials=data.TrialHandler(nReps=1, method=u'random', 
    originPath=None, extraInfo=expInfo,
    trialList=data.importConditions('Stimuli' + os.sep + 'stim'+ task + '.csv'))
thisTrial=trials.trialList[0]


#Initialisation des paramètres de l'essai
trialClock = core.Clock()
counter = 0
rep = KeyResponse()
rep.clock = core.Clock()
bloc = 0



#Boucle d'essais
for thisTrial in trials:
    if thisTrial!=None:
        for paramName in thisTrial.keys():#Récupérer les proriétés de l'essai n° x
            exec('{} = thisTrial[paramName]'.format(paramName))
    counter += 1 #incrémenter le numéro de l'essai
    rep.num_trial = counter
#Fixation
    win.flip()# Outil pour rafraîchir l'écran
    core.wait(1.5) #ISI
    fixationLeft.draw()
    fixationRight.draw()
    win.flip()
    core.wait(.5) #Fix - stim


#Definition stim
    stimLeft.setText(Left)
    stimRight.setText(Right)

#boucle
    rep.status = NOT_STARTED
    stimLeft.status = STARTED
    continueRoutine = True
    while continueRoutine:
        if stimLeft.status == STARTED:
            stimLeft.draw()
            stimRight.draw()
            event.clearEvents()
            win.flip()
            #send_trigger(int(trigger))
            stimLeft.status = NOT_STARTED
        if rep.status == NOT_STARTED:
            rep.status = STARTED
            rep.clock.reset() 
        if event.getKeys(["escape"]): core.quit()
        if  rep.status == STARTED:
            theseKeys=[]
            #lecture_port = ctypes.windll.inpout32.Inp32(0x379)
            if event.getKeys("m"): 
                #send_trigger(100)
                theseKeys.append("same")
            elif event.getKeys("d"): 
                #send_trigger(200)
                theseKeys.append("different")
            if len(theseKeys) > 0: #Si longueur > 0 alors il y a eu réponse
                rep.rt = rep.clock.getTime() #récupérer TR
                win.flip() #Ecran noir
                #core.wait(2.5) #confidence report interval
                rep.keys=[]
                rep.keys = theseKeys[0] 
                if rep.keys == Expected: #Correct ou incorrect
                    rep.corr = 1
                else:
                    rep.corr = 0
        #Fin de boucle, enregistrement des données
                thisExp.addData('expected', Expected)
                thisExp.addData('response', theseKeys[0])
                thisExp.addData('precision',rep.corr)
                thisExp.addData('rt',rep.rt)
                thisExp.addData('trial',rep.num_trial)
                thisExp.addData('tache',task)
                thisExp.nextEntry()
                continueRoutine = False

    if event.getKeys(["escape"]): 
        win.close
        core.quit()


#routine fin
finPending = True
continueRoutine=True
while continueRoutine:
    if  finPending:
        core.wait(2.0)
        texte_fin.draw()
        win.flip()
        core.wait(5.0)
        finPending = False
    if not continueRoutine:  
        break
    continueRoutine = False 
    if event.getKeys(["escape"]): 
        core.quit()


win.close()
core.quit()