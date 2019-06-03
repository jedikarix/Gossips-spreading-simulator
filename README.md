Wymagania wstępne:

Aby uruchomić symulację, należy mieć na komputerze uruchomiony serwer XMPP. W projekcie wykorzystany został serwer Prosody. Można go pobrać z [a link]https://prosody.im/. By umożliwić działanie symulacji należy go odpowiednio skonfigurować. 

W konfiguracji należy ustawić odpowiedni interfejs i umożliwić rejestrowanie użytkowników.

interfaces = {"127.0.0.1"} 
allow_registration = true

dodatkowo, na końcu pliku z konfiguracją należy umieścić 

VirtualHost "localhost"

Należy także pobrać pliki potrzebne do uruchomienia modelu sieci neuronowej. W tym celu należy uruchomić skrypt code/SemanticAnalysis/setup.py
