"""from flask import Flask, render_template, request, url_for
import qrcode
import io
import base64
import json
import time
import requests  # Nécessaire pour interagir avec l'API Tavus

app = Flask(__name__)

# Configuration de l'API Tavus
TAVUS_API_KEY = 'YOUR_TAVUS_API_KEY'  # Remplacez par votre clé API Tavus
TAVUS_REPLICA_ID = 'YOUR_REPLICA_ID'  # Remplacez par l'ID de votre replica
TAVUS_API_URL = 'https://tavusapi.com/v2/videos'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_info = request.form.get('productInfo')
        if not product_info:
            return render_template('index.html', error='Veuillez entrer les informations du produit')
        
        # Créer les données pour la page de présentation
        presentation_data = {
            'productInfo': product_info,
            'timestamp': int(time.time())
        }
        data_json = json.dumps(presentation_data)
        data_encoded = base64.urlsafe_b64encode(data_json.encode()).decode()

        # Générer l'URL pour la page de présentation
        presentation_url = url_for('presentation', data=data_encoded, _external=True)
        
        # Générer le QR code
        img = qrcode.make(presentation_url)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return render_template('index.html', qr_code=img_str)
    else:
        return render_template('index.html')

@app.route('/presentation')
def presentation():
    data_encoded = request.args.get('data')
    if not data_encoded:
        return 'Aucune donnée fournie', 400
    try:
        data_json = base64.urlsafe_b64decode(data_encoded.encode()).decode()
        data = json.loads(data_json)
        product_info = data.get('productInfo', '')
    except Exception as e:
        return 'Données invalides', 400

    # Intégration de l'API Tavus pour générer la vidéo
    # Vérifier si une vidéo existe déjà pour ces données (vous pouvez implémenter un cache ici)
    video_url = generate_tavus_video(product_info)
    if not video_url:
        return 'Erreur lors de la génération de la vidéo', 500

    return render_template('presentation.html', product_info=product_info, video_url=video_url)

def generate_tavus_video(script):
    # Créer une vidéo via l'API Tavus
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': TAVUS_API_KEY
    }
    data = {
        'replica_id': TAVUS_REPLICA_ID,
        'script': script,
        'video_name': f'Présentation du produit - {int(time.time())}'
    }

    try:
        response = requests.post(TAVUS_API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            video_id = response_data.get('video_id')
        else:
            print('Erreur lors de la création de la vidéo.')
            print('Code de statut :', response.status_code)
            print('Réponse de l\'API :', response.text)
            return None
    except Exception as e:
        print('Exception lors de la création de la vidéo:', e)
        return None

    # URL pour obtenir les détails de la vidéo
    get_video_url = f'{TAVUS_API_URL}/{video_id}'

    # Vérifier le statut de la vidéo jusqu'à ce qu'elle soit prête
    while True:
        try:
            response = requests.get(get_video_url, headers=headers)
            if response.status_code == 200:
                video_data = response.json()
                status = video_data.get('status')
                if status == 'ready':
                    download_url = video_data.get('download_url')
                    return download_url
                elif status == 'error':
                    print('Une erreur est survenue lors de la génération de la vidéo.')
                    return None
                else:
                    print(f'Statut actuel de la vidéo : {status}. Vérification à nouveau dans 15 secondes...')
                    time.sleep(15)
            else:
                print('Erreur lors de la vérification du statut de la vidéo.')
                print('Code de statut :', response.status_code)
                print('Réponse de l\'API :', response.text)
                return None
        except Exception as e:
            print('Exception lors de la vérification du statut de la vidéo:', e)
            return None

if __name__ == '__main__':
    app.run(debug=True)"""


"""from flask import Flask, render_template, request, url_for
import qrcode
import io
import base64
import json
import time
import requests
import pyshorteners  # Pour raccourcir l'URL

app = Flask(__name__)

# Configuration de l'API Tavus
TAVUS_API_KEY = 'b832bc20afdd48ccbc084721ce9a8428'  # Remplacez par votre clé API Tavus
TAVUS_REPLICA_ID = 'r445a7952e'  # Remplacez par l'ID de votre replica
TAVUS_API_URL = 'https://tavusapi.com/v2/videos'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_info = request.form.get('productInfo')
        if not product_info:
            return render_template('index.html', error='Veuillez entrer les informations du produit')
        
        # Créer les données pour la page de présentation
        presentation_data = {
            'productInfo': product_info,
            'timestamp': int(time.time())
        }
        data_json = json.dumps(presentation_data)
        data_encoded = base64.urlsafe_b64encode(data_json.encode()).decode()

        # Générer l'URL pour la page de présentation
        presentation_url = url_for('presentation', data=data_encoded, _external=True)
        
        # Raccourcir l'URL pour réduire la taille du QR code
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(presentation_url)

        # Générer le QR code sans spécifier la version
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,  # Ajustez ce nombre pour changer la taille du QR code
            border=4,
        )
        qr.add_data(short_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#6e48aa", back_color="white")  # Conserver la couleur originale
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return render_template('index.html', qr_code=img_str)
    else:
        return render_template('index.html')

@app.route('/presentation')
def presentation():
    data_encoded = request.args.get('data')
    if not data_encoded:
        return 'Aucune donnée fournie', 400
    try:
        data_json = base64.urlsafe_b64decode(data_encoded.encode()).decode()
        data = json.loads(data_json)
        product_info = data.get('productInfo', '')
    except Exception as e:
        return 'Données invalides', 400

    # Intégration de l'API Tavus pour générer la vidéo
    video_url = generate_tavus_video(product_info)
    if not video_url:
        return 'Erreur lors de la génération de la vidéo', 500

    return render_template('presentation.html', product_info=product_info, video_url=video_url)

def generate_tavus_video(script):
    # Créer une vidéo via l'API Tavus
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': TAVUS_API_KEY
    }
    data = {
        'replica_id': TAVUS_REPLICA_ID,
        'script': script,
        'video_name': f'Présentation du produit - {int(time.time())}'
    }

    try:
        response = requests.post(TAVUS_API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            video_id = response_data.get('video_id')
        else:
            print('Erreur lors de la création de la vidéo.')
            print('Code de statut :', response.status_code)
            print('Réponse de l\'API :', response.text)
            return None
    except Exception as e:
        print('Exception lors de la création de la vidéo:', e)
        return None

    # URL pour obtenir les détails de la vidéo
    get_video_url = f'{TAVUS_API_URL}/{video_id}'

    # Vérifier le statut de la vidéo jusqu'à ce qu'elle soit prête
    while True:
        try:
            response = requests.get(get_video_url, headers=headers)
            if response.status_code == 200:
                video_data = response.json()
                status = video_data.get('status')
                if status == 'ready':
                    download_url = video_data.get('download_url')
                    return download_url
                elif status == 'error':
                    print('Une erreur est survenue lors de la génération de la vidéo.')
                    return None
                else:
                    print(f'Statut actuel de la vidéo : {status}. Vérification à nouveau dans 15 secondes...')
                    time.sleep(15)
            else:
                print('Erreur lors de la vérification du statut de la vidéo.')
                print('Code de statut :', response.status_code)
                print('Réponse de l\'API :', response.text)
                return None
        except Exception as e:
            print('Exception lors de la vérification du statut de la vidéo:', e)
            return None

if __name__ == '__main__':
    app.run(debug=True)"""


from flask import Flask, render_template, request, url_for
import qrcode
import io
import base64
import json
import time
import requests
import pyshorteners

app = Flask(__name__)

# Configuration de l'API Tavus
TAVUS_API_KEY = ''
TAVUS_REPLICA_ID = 'r445a7952e'
TAVUS_API_URL = 'https://tavusapi.com/v2/videos'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_info = request.form.get('productInfo')
        if not product_info:
            return render_template('index.html', error='Veuillez entrer les informations du produit')
        
        # Créer les données pour la page de présentation
        presentation_data = {
            'productInfo': product_info,
            'timestamp': int(time.time())
        }
        data_json = json.dumps(presentation_data)
        data_encoded = base64.urlsafe_b64encode(data_json.encode()).decode()

        # Générer l'URL pour la page de présentation
        presentation_url = url_for('presentation', data=data_encoded, _external=True)
        
        # Raccourcir l'URL pour réduire la taille du QR code
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(presentation_url)

        # Générer le QR code sans spécifier la version
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(short_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#6e48aa", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return render_template('index.html', qr_code=img_str)
    else:
        return render_template('index.html')

@app.route('/presentation')
def presentation():
    data_encoded = request.args.get('data')
    if not data_encoded:
        return 'Aucune donnée fournie', 400
    try:
        data_json = base64.urlsafe_b64decode(data_encoded.encode()).decode()
        data = json.loads(data_json)
        product_info = data.get('productInfo', '')
    except Exception as e:
        return 'Données invalides', 400

    # Intégration de l'API Tavus pour générer la vidéo
    video_url = create_and_get_tavus_video(product_info)
    if not video_url:
        return 'Erreur lors de la génération de la vidéo', 500

    return render_template('presentation.html', product_info=product_info, video_url=video_url)

def create_and_get_tavus_video(script):
    # Créer une vidéo via l'API Tavus
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': TAVUS_API_KEY
    }
    data = {
        'replica_id': TAVUS_REPLICA_ID,
        'script': script,
        'video_name': f'Présentation du produit - {int(time.time())}'
    }

    try:
        response = requests.post(TAVUS_API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            video_id = response_data.get('video_id')
        else:
            print('Erreur lors de la création de la vidéo.')
            print('Code de statut :', response.status_code)
            print('Réponse de l\'API :', response.text)
            return None
    except Exception as e:
        print('Exception lors de la création de la vidéo:', e)
        return None

    # URL pour obtenir les détails de la vidéo
    get_video_url = f'{TAVUS_API_URL}/{video_id}'

    # Vérifier le statut de la vidéo jusqu'à ce qu'elle soit prête
    while True:
        try:
            response = requests.get(get_video_url, headers=headers)
            if response.status_code == 200:
                video_data = response.json()
                status = video_data.get('status')
                if status == 'ready':
                    download_url = video_data.get('download_url')
                    return download_url
                elif status == 'error':
                    print('Une erreur est survenue lors de la génération de la vidéo.')
                    return None
                else:
                    print(f'Statut actuel de la vidéo : {status}. Vérification à nouveau dans 30 secondes...')
                    time.sleep(30)
            else:
                print('Erreur lors de la vérification du statut de la vidéo.')
                print('Code de statut :', response.status_code)
                print('Réponse de l\'API :', response.text)
                return None
        except Exception as e:
            print('Exception lors de la vérification du statut de la vidéo:', e)
            return None

if __name__ == '__main__':
    app.run(debug=True)

