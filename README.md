 Base de données Topographiques des gouffres du Plateau de la Réchasse et des dalles de l'Arcelin (Pralognan la Vanoise, Savoie 73, France)
===============================================================================================

Overview
--------

Ce dépôt contient les données topographiques et les dessins associés des cavités du Plateau de la Réchasse et des dalles de l'Arcelin (Pralognan la Vanoise, Savoie 73, France). 
Elles ont été produites par les spéléologues de l'association de spéléologie _Continent 8_.

Ce dépôt est mis à jour à chaque fois qu'une nouvelle topographie est rajoutée au système décrit dans cette base de données.

Description
-----------

Ce dépôt sauvegarde les données topographiques et de dessin. Ces fichiers sont pour le logiciel Therion (data + dessins).

Uniquement les fichiers sources sont sauvegardés pour des raisons de taille, bien que certians pdf puissent être présents à des fin de travail.
	
	* .thc, .th, .th2 et .thconfig pour le logiciel Therion
    * .zip pour les exports des séances topo de l'appli Topodroid
	
Pour obtenir les topographies en plan, coupe et/ou 3D, il faut compiler les fichiers Therion.

Il est possible de produire un export à l'échelle du massif ou bien de chaque cavité.


Travail sous Therion
-----------

Une convention a été mise en place pour la gestion des points d'interrogation, et donc des différents départs possibles, avec la définition de différents champs.
S'utilise de la façon suivante dans Therion, pour le point "Continuation" : 
    
-attr Code "" -attr cavite "Arcel1" -attr Reseau "" -attr CA "" -text ""

Le champ "code" décrit le type de terminus. Il peut prendre les valeurs suivantes :
    A : il suffit d'y aller et de continuer, pas d'obstacles
    D1 : Désobstruction de petite ampleur
    D2 : Désobstruction de moyenne ampleur
    E1 : Escalade de petite ampleur
    E2 : Escalade de moyenne ampleur
    P : Puits non descendu
    Q : non renseigné sur la topographie, c'est à voir/vérifier
    S : Siphon à plonger

le champ "cavite" donne le nom de la cavité en question,

le champ "reseau" indique la partie de la cavité où se situe le point d'interrogation (pour pouvoir le retrouver plus rapidement sur les topographies),

le champ "ca" est rempli si présence de courant d'air, avec éventuellement des remarques/commentaires,

le champ "text" permet de rajouter une remarque, un commentaire. Il est facultatif

Licence
-------

L'ensemble de ces données est publié sous la licence libre Creative Commons Attribution-ShareAlike-NonCommercial (Attribution, partage à l'identique et non commerciale) :
	http://creativecommons.org/licenses/by-nc-sa/4.0/

Auteurs de la base de donnée 
-------

L'élaboration et la mise à jour de cette synthèse topographique sous Therion est le fruit d'un travail de : 

_Martin Kern ;Théophile Cailhol ; Benoît Urruty_ (2026)


Contact
-------

Contacter l'auteur du dépot Git ou l'association Continent 8








