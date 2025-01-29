# molcas_IO_test

## Description du test

- Soumission de calculs en job array au cluster pour tester la limite de l'I/O utilisant le /scratch comme tmp pour les fichiers temporaires.

- Type de calculs: Single point CASSCF avec OpenMolcas évaluant les énergies, gradient et coupling nonadiabatique

- Chaque sous-dossier contient N copie du même calcul (1,10,100 et 1000) avec une estimation de 500 MB nécessaire en disque pour chaque calcul individuel. 500 GB nécessaire pour le test à 1000.

## Protocol
- Un script de soumission de calculs sub_molcas_nautilus_Xjob.sh est donné pour chaque set. 

- Le script est configuré pour faire un job array avec X calculs écrivant tous en utilisant le /scratch comme tmp

- Soumettre chaque script individuellement pour tester proprement la vitesse de 1 calcul et une seule I/O sur /scratch vs. X calculs et X écriture sur le /scratch

## Contenu des dossiers

Les dossiers Xjob contiennent X sous-dossiers géometrie par calculs:
```
100job
|--geom_1
|--geom_2
...
|--geom_100
```

Chaque dossier géometrie peut contenir les fichiers suivants:

```
--geom_X
  |--geometry_1.xyz         #fichier xyz avec la géometrie moléculaire
  |--mol_input_1.input      #Input de molcas
  |--start.RasOrb           #Guess pour les orbitales moléculaires
  |
  |--mol_input_1.output     #Output du calculs molcas (contient le walltime)
  |--mol_input_1.status     #fichier contenant le message final du calcul ("Happy landing" si execution sans problème)
```

Le walltime et cputime sont dans les dernières lignes de mol_input_1.output

## Nettoyage du tmp ou scratch

- Tous les calculs font l'I/O du tmp sur /scratch/waves/users/$USER/noRICD/X ou X correspond au nombre de calculs dans le job array. Effacer /scratch/waves/users/$USER/noRICD permet de tout nettoyer.
