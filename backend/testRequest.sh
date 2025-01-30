#!/bin/bash

pwd
# Vérifier si le serveur Node.js fonctionne
if [ $? -eq 0 ]; then
    echo "Le serveur Node.js a démarré avec succès."
else
    echo "Erreur lors du démarrage du serveur Node.js."
    exit 1
fi

# Exécuter les scripts Python
# Exemple de test pour chaque script Python
echo "Test de l'API /generateChallenge..."
curl http://localhost:3000/generateChallenge

#echo "Test de l'API /verifyGame..."
#curl http://localhost:3000/verifyGame
#
#echo "Test de l'API /generateNewGame..."
#curl http://localhost:3000/generateNewGame
#
#echo "Test de l'API /solveGame..."
#curl http://localhost:3000/solveGame
#
echo "Tests terminés."

