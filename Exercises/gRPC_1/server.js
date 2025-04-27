const grpc = require('@grpc/grpc-js');
const protoLoader = require("@grpc/proto-loader");
const packageDef = protoLoader.loadSync("todo.proto", {});
const grpcObject = grpc.loadPackageDefinition(packageDef);
const todoPackage = grpcObject.todoPackage;

const server = new grpc.Server();

server.addService(todoPackage.Todo.service, 
    {
        "createTodo": createTodo,
        "readTodos": readTodos
    });

server.bindAsync("127.0.0.1:40000", grpc.ServerCredentials.createInsecure(), (err, port) => {
    if (err) {
        console.error(err);
        return;
    }
    server.start();
    console.log(`Server running at 127.0.0.1:${port}`);
});

function createTodo (call, callback) {
    console.log(call);
}

function readTodos (call, callback) {

}
