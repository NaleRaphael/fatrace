var grpc = require('grpc');
var messages = require('./core_pb');
var services = require('./core_grpc_pb');

var endpoint = 'localhost:50051';

var SERVICES_DICT = {
    'echo': echo,
    'ghost_echo': ghost_echo,
    'ingrdb': db_insert,
    'test_ingr': test_ingr,
    'test_dish': test_dish
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
    var ingr01 = new messages.Ingredient();
    ingr01.setName('chicken');
    var ingr02 = new messages.Ingredient();
    ingr02.setName('potato');

    var request = new messages.Dish();
    request.setName('Fried chicken');
    request.setIngrsList([ingr01, ingr02]);

    client.insert(request, (err, res) => {
        console.log('client:', res.getIsUpdated());
    });
}

function test_ingr() {
    var client = new services.TesterClient(
        endpoint, grpc.credentials.createInsecure()
    );
    var request = new messages.Ingredient();
    request.setName('chicken');
    request.setWeight(1.2);

    client.testIngr(request, (err, res) => {
        console.log('client: test successfully');
        console.log(res);
    });
}

function test_dish() {
    var client = new services.TesterClient(
        endpoint, grpc.credentials.createInsecure()
    );
    var ingrs = [
        createIngr('corn', 3.2), 
        createIngr('butter', 1.8), 
        createIngr('ham', 1.2)
    ];

    var request = new messages.Dish();
    request.setName('corn soup');
    for (i=0; i<ingrs.length; i++) {
        request.addIngrs(ingrs[i]);
    }

    client.testDish(request, (err, res) => {
        console.log('client: ' + res);
    });
}

function createIngr(name, weight) {
    var obj = new messages.Ingredient();
    obj.setName(name);
    obj.setWeight(weight);
    return obj;
}

function main() {
    if (process.argv.length <= 2) {
        console.log('No specified function to be executed.');
        return;
    }
    var entry = process.argv[2];
    if (entry in SERVICES_DICT) {
        SERVICES_DICT[entry]();
    }
    else {
        console.log('No given entry: ' + entry);
    }
}

main();
