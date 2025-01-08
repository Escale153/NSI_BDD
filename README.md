# NSI_BDD

L'interface respecte donc bien notre cahier des charges, cahier de recettes en suivant la trame des spécifications techniques
La base de données l'accompagnant (membres.db) respecte également les contraintes posées.
Il faut noter quelques fonctionnalités supplémentaires : 
	- Un système de recherche plus poussé qu'initialement (utilisation décrite ci-dessous)
	- Une option permettant d'enregistrer la recherche sous json (utile uniquement dans certains cas spécifiques, oui)
	- Une option permettant d'afficher les dernières modifications apportées à la base de données principales (sorte de commit)
	- Une option permettant de se connecter à une autre base de donnée quelconque (exe : fleurs.db) tout en ayant
		la majeure partie des fonctionnalités disponibles (la recherche par id ou les commits)
	- Un système de modification de la base de données plus avancé 
		(modification de tables et colonnes integrées en plus du cahier des charges)
	- Un début vers le respect total des contraintes 
	
Le système de recherche permet de nombreuses dispositions (pouvant être déduites du code certes) :
	- Soit l'affichage de la table uniquement (seule une table sélectionnée)
	- Soit l'affichage d'une colonne précisement (table et colonne)
	- Soit l'affichage d'une valeur précisement dans une table (table, colonne et valeur)
	- Soit la recherche d'une donnée dans toutes les tables (valeur uniquement)
	- Si la table utilisée est membres.db, entrer uniquement un ID et plusieurs 
		informations sur celui-ci seront affichées (d'où une requête avec le JOIN)
	
Des éventuelles remarques : 
	- Nous avons essayé de faire en sorte que les contraintes de domaine et de redondance
		soient respectées lors de l'ajout de nouvelles données, cependant pour des domaines 
		plus rares, les cas n'ont pas été prévus, cela pourrait donc être un point à développer
		si nécessaire
	
	- Malgré l'abondance de blocks try/except pour limiter les erreurs, il n'est pas impossible 
		(pas de notre expérience) que subsistent des erreurs. Un fait assez plausible en considérant
		la complexité qu'il en est de manier une base de données jusque dans sa structure. Par ailleurs 
		il aurait pu être intéressant avec plus de temps de prévoir plus de messages d'erreurs 
		et éventuellement avec une boite de dialogue.
		
	- Certains systèmes de modifications de données ne sont pas forcément optimisés mais fonctionnels
	
	- Veuillez excuser tkinter d'être une purge, de notre côté nous ne le pouvons plus :) (Merci)
		Certaines implémentations sont criticables et peu optimisées sous certains points de vue,
		mais ne le sont pas selon l'angle de vue où tkinter ne pleure pas. Car certains détour ont été
		nécessaires pour éviter ses caprices.
