const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;
const cors = require('cors');
const fs = require('fs');
const path = require('path');


app.use(cors());
// Middleware pour gérer les réponses JSON
app.use(express.json());

// Route /generateChallenge : Appel à un script Python pour générer un challenge
app.post('/generateChallenge', (req, res) => {
    let { valeurChambres, valeurMasques } = req.body; // Récupération des données envoyées

    if (!valeurChambres || !valeurMasques) {
        return res.status(400).send("Données manquantes");
    }

    valeurChambres = valeurChambres.map(cube =>
        cube.map(ligne =>
            ligne.map(val => (val === -1 ? 0 : val))
        )
    );

    // Transformer `true` en `0` et `false` en `1` dans `valeurMasques`
    valeurMasques = valeurMasques.map(cube =>
        cube.map(ligne =>
            ligne.map(val => (val === true ? 1 : 0))
        )
    );

    // Chemins des fichiers JSON
    const dispositionVisuellesPath = "map/dispositionVisuelle.json";
    const masquesFixesPath = "map/masquesFixes.json";

    try {
        // Écriture des valeurs dans les fichiers correspondants
        fs.writeFileSync(dispositionVisuellesPath, JSON.stringify(valeurChambres, null, 2));
        fs.writeFileSync(masquesFixesPath, JSON.stringify(valeurMasques, null, 2));

    } catch (error) {
        console.error("Erreur lors de l'enregistrement :", error);
        res.status(500).send("Erreur lors de l'enregistrement des fichiers.");
    }
    const command = '/bin/bash -c "source /home/etud/jupyter_env/bin/activate && python3 scriptPyCSP3/generateChallenge.py"';

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Erreur: ${error.message}`);
            return res.status(500).json({ error: error.message });
        }
        if (stderr) {
            console.error(`Erreur de script: ${stderr}`);
            return res.status(500).json({ error: stderr });
        }
        // Le script Python renvoie un JSON ou un texte que l'on parse
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (e) {
            console.error('Erreur lors du parsing JSON:', stdout);
            res.status(500).json({ error: 'Erreur lors du parsing du JSON' });
        }
    });
});



// Route /testChallenge : Appel à un script Python pour vérifier le défi
app.post('/testChallenge', (req, res) => {

    const tableauMonstresString = JSON.stringify(req.body.tableauMonstres);
    const command = `/bin/bash -c "source /home/etud/jupyter_env/bin/activate && python3 scriptPyCSP3/testChallenge.py '${tableauMonstresString}'"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Erreur: ${error.message}`);
            return res.status(500).json({ error: error.message });
        }
        if (stderr) {
            console.error(`Erreur de script: ${stderr}`);
            return res.status(500).json({ error: stderr });
        }
        try {
            res.json({ result: stdout });
        } catch (e) {
            console.error('Erreur lors du parsing JSON:', stdout);
            res.status(500).json({ error: 'Erreur lors du parsing du JSON' });
        }
    });
});

// Route
app.post('/generateMap', (req, res) => {

    const tableauMonstresString = JSON.stringify(req.body.tableauMonstres);
    const command = `/bin/bash -c "source /home/etud/jupyter_env/bin/activate && python3 scriptPyCSP3/generateMap.py '${tableauMonstresString}'"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Erreur: ${error.message}`);
            return res.status(500).json({ error: error.message });
        }
        if (stderr) {
            console.error(`Erreur de script: ${stderr}`);
            return res.status(500).json({ error: stderr });
        }
        try {

            res.json({ result: stdout });
        } catch (e) {
            console.error('Erreur lors du parsing JSON:', stdout);
            res.status(500).json({ error: 'Erreur lors du parsing du JSON' });
        }
    });
});

app.get('/resetChallenge', async (req, res) => {
    try {
        let sourceFile = 'map/dispositionVisuelleSave.json';
        let destinationFile = 'map/dispositionVisuelle.json';

        // Supprimer et copier le premier fichier
        await new Promise((resolve, reject) => {
            fs.unlink(destinationFile, (err) => {
                if (err && err.code !== 'ENOENT') return reject(err);
                fs.copyFile(sourceFile, destinationFile, (err) => {
                    if (err) return reject(err);
                    resolve();
                });
            });
        });

        sourceFile = 'map/masquesFixesSave.json';
        destinationFile = 'map/masquesFixes.json';

        // Supprimer et copier le deuxième fichier
        await new Promise((resolve, reject) => {
            fs.unlink(destinationFile, (err) => {
                if (err && err.code !== 'ENOENT') return reject(err);
                fs.copyFile(sourceFile, destinationFile, (err) => {
                    if (err) return reject(err);
                    resolve();
                });
            });
        });

        // Envoyer la réponse une seule fois
        res.send("Jeu réinitialisé avec succès !");
    } catch (error) {
        console.error("Erreur :", error);
        res.status(500).send("Erreur lors de la réinitialisation.");
    }
});


// Route pour servir les données JSON
app.get('/dispositionVisuelle', (req, res) => {
    // Lire le fichier JSON
    fs.readFile(path.join(__dirname, 'map/dispositionVisuelle.json'), 'utf-8', (err, data) => {
        if (err) {
            res.status(500).send('Erreur lors de la lecture du fichier');
        } else {
            res.json(JSON.parse(data));  // Envoie les données JSON au client
        }
    });
})

// Route pour servir les données JSON
app.get('/masquesFixes', (req, res) => {
    // Lire le fichier JSON
    fs.readFile(path.join(__dirname, 'map/masquesFixes.json'), 'utf-8', (err, data) => {
        if (err) {
            res.status(500).send('Erreur lors de la lecture du fichier');
        } else {
            res.json(JSON.parse(data));  // Envoie les données JSON au client
        }
    });
})


// Démarrer le serveur
app.listen(port, () => {
    console.info(`Serveur à l'écoute sur http://localhost:${port}`);
});
