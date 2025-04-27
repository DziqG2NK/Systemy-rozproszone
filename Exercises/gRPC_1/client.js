const grpc = require('@grpc/grpc-js');
const protoLoader = require("@grpc/proto-loader");
const packageDef = protoLoader.loadSync("todo.proto", {});
const grpcObject = grpc.loadPackageDefinition(packageDef);
const todoPackage = grpcObject.todoPackage;

const readline = require("readline");

const client = new todoPackage.Todo("127.0.0.1:40000", grpc.credentials.createInsecure());

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function askInput() {
    rl.question('Wpisz wiadomość (albo "exit" żeby zakończyć): ', (input) => {
        if (input.toLowerCase() === 'exit') {
            rl.close();
            return;
        }

        client.createTodo({ 
            "id": -1, 
            "text": input 
        }, (err, response) => {
            if (err) {
                console.error('Błąd:', err);
            } else {
                console.log('Odpowiedź serwera:', JSON.stringify(response));
            }            
            askInput();
        });
    });
}

askInput();