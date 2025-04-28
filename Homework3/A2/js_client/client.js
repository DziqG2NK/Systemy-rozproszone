// const grpc = require('@grpc/grpc-js');
// const protoLoader = require('@grpc/proto-loader');
const readline = require('readline');

// Ładowanie pliku .proto z katalogu wyżej
// const packageDef = protoLoader.loadSync('../communication.proto', {});
// const grpcObject = grpc.loadPackageDefinition(packageDef);
// const communicationProto = grpcObject.communication; // Sprawdź, czy to jest właściwa nazwa pakietu

// Tworzenie klienta
// const client = new communicationProto.EventService('127.0.0.1:50000', grpc.credentials.createInsecure());

const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDefinition = protoLoader.loadSync('../communication.proto', {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const proto = grpc.loadPackageDefinition(packageDefinition);

// UWAGA tutaj! Musisz wziąć communication.EventService
const client = new proto.communication.EventService('localhost:50000', grpc.credentials.createInsecure());

// Tworzenie interfejsu do wczytywania danych z klawiatury
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let activeSubscriptions = {};  // Przechowujemy aktywne subskrypcje

// Funkcja subskrybująca kategorię
function subscribeToCategory(category) {
    if (activeSubscriptions[category]) {
        console.log(`Już subskrybujesz kategorię: ${category}`);
        return;
    }

    const request = { category: category };
    // console.log(request);

    console.log("O TO TU")
    const call = client.Subscribe(request);

    call.on('data', (response) => {
        console.log(`Otrzymano dane: ${response.event}`);
    });

    call.on('error', (error) => {
        console.error('Błąd:', error);
    });

    call.on('end', () => {
        console.log(`Subskrypcja kategorii ${category} zakończona.`);
        delete activeSubscriptions[category];  // Usuwamy subskrypcję, gdy zakończona
    });

    activeSubscriptions[category] = call;
    console.log(`Subskrybujesz kategorię: ${category}`);
}

// Funkcja odsubskrybowująca kategorię
function unsubscribeFromCategory(category) {
    const subscription = activeSubscriptions[category];
    if (subscription) {
        subscription.cancel();  // Zatrzymujemy strumień
        delete activeSubscriptions[category];  // Usuwamy subskrypcję
        console.log(`Odsuubskrybowałeś kategorię: ${category}`);
    } else {
        console.log(`Nie masz aktywnej subskrypcji dla kategorii: ${category}`);
    }
}

function createUpdateMessage(name, old_value, new_value) {
    const change = new_value - old_value;
    const changePercentage = ((change) / old_value) * 100;

    let changeStr;
    if (change > 0) {
        changeStr = `Wzrost notowań o ${changePercentage.toFixed(2)} %`;
    } else {
        changeStr = `Spadek notowań o ${Math.abs(changePercentage).toFixed(2)} %`;
    }

    return `Firma ${name} ma wartość ${new_value}.00 PLN\n${changeStr}`;
}

// Funkcja obsługująca zapytania użytkownika o subskrypcję
function askInput() {
    rl.question('Wybierz kategorię do subskrypcji [GAMING|BANKS|INDUSTRY].\nJeśli chcesz odsubskrybować kategorię wpisz [-GAMING|-BANKS|-INDUSTRY].\nWpisz "exit" aby zakończyć: ', (input) => {
        if (input.toLowerCase() === 'exit') {
            rl.close();
            return;
        }

        const categoryMap = {
            'gaming': 1,
            'banks': 2,
            'industry': 3,
        };
       

        const category = categoryMap[input.toLowerCase()];
        const unsubCategory = categoryMap[input.substring(1).toLowerCase()];

        if (category === undefined && unsubCategory === undefined) {
            console.log('Niepoprawna kategoria. Wybierz GAMING, BANKS, lub INDUSTRY.');
        } else if (category) {
            console.log(`Subskrybujesz kategorię: ${input.toUpperCase()}`);
            subscribeToCategory(category);
        } else if (unsubCategory) {
            console.log(`Odsuubskrybujesz kategorię: ${input.toUpperCase().substring(1)}`);
            unsubscribeFromCategory(unsubCategory);
        }

        askInput();
    });
}

askInput();
