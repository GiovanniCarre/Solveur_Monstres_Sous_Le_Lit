const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;
const cors = require('cors');


app.use(cors());
// Middleware pour gérer les réponses JSON
app.use(express.json());

// Route /generateChallenge : Appel à un script Python pour générer un challenge
app.get('/generateChallenge', (req, res) => {
    // Utilisation de /bin/bash -c pour exécuter les commandes dans un shell interactif
    const command = '/bin/bash -c "source /home/etud/Documents/cours/deep_learning/virtualenv/bin/activate && python3 scriptPyCSP3/generateChallenge.py"';

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
            console.log(stdout)
            res.json(result);
        } catch (e) {
            console.error('Erreur lors du parsing JSON:', stdout);
            res.status(500).json({ error: 'Erreur lors du parsing du JSON' });
        }
    });
});



// Route /verifyGame : Appel à un script Python pour vérifier le jeu
app.get('/verifyGame', (req, res) => {
    exec('python3 path/to/your/verify_game.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Erreur: ${error.message}`);
            return res.status(500).json({ error: error.message });
        }
        if (stderr) {
            console.error(`Erreur de script: ${stderr}`);
            return res.status(500).json({ error: stderr });
        }
        // Supposons que le script retourne un true ou false
        const result = stdout.trim() === 'true'; // On suppose que le script retourne "true" ou "false"
        res.json({ success: result });
    });
});

// Route /generateNewGame : Appel à un script Python pour générer un nouveau jeu
app.get('/generateNewGame', (req, res) => {
    exec('python3 path/to/your/generate_new_game.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Erreur: ${error.message}`);
            return res.status(500).json({ error: error.message });
        }
        if (stderr) {
            console.error(`Erreur de script: ${stderr}`);
            return res.status(500).json({ error: stderr });
        }
        try {
            const result = JSON.parse(stdout);
            console.log(result)
            res.json(result);  // Envoie le résultat au client
        } catch (e) {
            console.error('Erreur lors du parsing JSON:', e);
            res.status(500).json({ error: 'Erreur lors du parsing du JSON' });
        }
    });
});

// Route /solveGame : Appel à un script Python pour résoudre le jeu
app.get('/solveGame', (req, res) => {
    const command = '/bin/bash -c "source /home/etud/Documents/cours/deep_learning/virtualenv/bin/activate && python3 scriptPyCSP3/solveGame.py"';

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

            // Nettoyage : enlever les retours à la ligne et espaces
            let cleanedStdout = stdout.trim();

            // Ajouter les crochets nécessaires si le JSON est incomplet ou mal formé
            if (cleanedStdout.startsWith("[") && cleanedStdout.endsWith("]")) {
                cleanedStdout = cleanedStdout; // Déjà au bon format
            } else {
                console.error('La sortie n\'est pas au format JSON attendu.');
                return res.status(500).json({ error: 'La sortie n\'est pas au format JSON attendu.' });
            }

            const result = JSON.parse(cleanedStdout);

            // Vérification du type de résultat et de son format
            if (result === false) {
                res.json({ result: "False" });
            } else if (Array.isArray(result) && result.every(Array.isArray)) {
                res.json({ result: result });
            } else {
                res.status(500).json({ error: 'Format de réponse invalide' });
            }
        } catch (e) {
            console.error('Erreur lors du parsing JSON:', e);
            res.status(500).json({ error: 'Erreur lors du parsing du JSON' });
        }


    });
});

// Démarrer le serveur
app.listen(port, () => {
    console.log(`Serveur à l'écoute sur http://localhost:${port}`);
});
