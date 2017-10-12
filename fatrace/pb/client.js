var grpc = require('grpc');
var messages = require('./core_pb');
var services = require('./core_grpc_pb');

var endpoint = 'localhost:50051';

var func_entries = {
    'echo': echo,
    'ghost_echo': ghost_echo,
    'ingrdb': db_insert
}

function echo() {
    var client = new services.EchoerClient(
        endpoint, grpc.credentials.createInsecure()
    );
    var request = new messages.Foo();
    request.setContent('Yo, I am sent from js.');
    client.echo(request, (err, res) => {
        console.log('client:', res.getContent());
    });
}

function ghost_echo() {
    var client = new services.EchoerClient(
        endpoint, grpc.credentials.createInsecure()
    );
    var request = new messages.Foo();
    client.ghostEcho(request, (err, res) => {
        console.log('client: testing echo service..');
    });
}

function db_insert() {
    var client = new services.IngrDBManagerClient(
        endpoint, grpc.credentials.createInsecure()
    );
    var ingr01 = new messages.Ingr();
    ingr01.setName('chicken');
    var ingr02 = new messages.Ingr();
    ingr02.setName('potato');

    var request = new messages.Dish();
    request.setName('Fried chicken');
    request.setIngrsList([ingr01, ingr02]);

    client.insert(request, (err, res) => {
        console.log('client:', res.getIsUpdated());
    });
}

function main() {
    if (process.argv.length <= 2) {
        console.log('No specified function to be executed.');
        return;
    }
    var entry = process.argv[2];
    if (entry in func_entries) {
        func_entries[entry]();
    }
    else {
        console.log('No given entry: ' + entry);
    }
}

main();
