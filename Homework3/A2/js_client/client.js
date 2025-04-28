const readline = require('readline');
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

const client = new proto.communication.EventService('localhost:50000', grpc.credentials.createInsecure());

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let activeSubscriptions = {}; 

function subscribeToCategory(category) {
    if (activeSubscriptions[category]) {
        console.log(`Już subskrybujesz kategorię: ${category}`);
        return;
    }

    const request = { category: category };
    // console.log(request);

    // console.log("O TO TU")
    const call = client.Subscribe(request);

    call.on('data', (response) => {
        console.log(`Otrzymano dane: ${response.event}`);
    });

    call.on('error', (error) => {
        console.error('Błąd:', error);
    });

    call.on('end', () => {
        console.log(`Subskrypcja kategorii ${category} zakończona.`);
        delete activeSubscriptions[category]; 
    });

    activeSubscriptions[category] = call;
    console.log(`Subskrybujesz kategorię: ${category}`);
}

function unsubscribeFromCategory(category) {
    const subscription = activeSubscriptions[category];
    if (subscription) {
        subscription.cancel();  
        delete activeSubscriptions[category]; 
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

function askInput() {
    rl.question('Wybierz kategorię do subskrypcji [GAMING|BANKS|INDUSTRY].\nJeśli chcesz odsubskrybować kategorię wpisz [-GAMING|-BANKS|-INDUSTRY].\nWpisz "exit" aby zakończyć:\n\n ', (input) => {
        if (input.toLowerCase() === 'exit') {
            rl.close();
            return;
        }

        const categoryMap = {
            'gaming': 1,
            'banks': 2,
            'industry': 3,
        };
       

        // const category = categoryMap[input.toLowerCase()];
        // const unsubCategory = categoryMap[input.substring(1).toLowerCase()];

        // if (category === undefined && unsubCategory === undefined) {
        //     console.log('Niepoprawna kategoria. Wybierz GAMING, BANKS, lub INDUSTRY.');
        // } else if (category) {
        //     console.log(`Subskrybujesz kategorię: ${input.toUpperCase()}`);
        //     subscribeToCategory(category);
        // } else if (unsubCategory) {
        //     console.log(`Odsuubskrybujesz kategorię: ${input.toUpperCase().substring(1)}`);
        //     unsubscribeFromCategory(unsubCategory);
        // }

        if (input.startsWith('-')) {
            const unsubCategory = input.substring(1).toUpperCase();
            if (categoryMap[unsubCategory.toLowerCase()]) {
                console.log(`Odsuubskrybujesz kategorię: ${unsubCategory}`);
                unsubscribeFromCategory(unsubCategory);
            } else {
                console.log('Niepoprawna kategoria do odsubskrybowania.');
            }
        } else {
            const category = categoryMap[input.toLowerCase()];
            if (category) {
                console.log(`Subskrybujesz kategorię: ${category}`);
                subscribeToCategory(category);
            } else {
                console.log('Niepoprawna kategoria. Wybierz GAMING, BANKS, lub INDUSTRY.');
            }
        }

        askInput();
    });
}

askInput();
