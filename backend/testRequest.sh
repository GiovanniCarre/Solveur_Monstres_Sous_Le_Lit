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
echo "Test de l'API /generateChallenge..."
curl -s http://localhost:3000/generateChallenge

echo -e "\nTest de l'API /testChallenge avec POST..."

# Définition du tableau des monstres à envoyer en JSON
json_data='{"tableauMonstres": [0, 0, 0, 2, 0, 0, 0, 3, 0]}'

# Envoyer la requête POST à l'API /testChallenge
response=$(curl -s -X POST http://localhost:3000/testChallenge \
  -H "Content-Type: application/json" \
  -d "$json_data")

# Afficher la réponse du serveur
echo "Réponse de l'API /testChallenge : $response"

echo "Tests terminés."
